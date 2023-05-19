package com.meca.did.service.impl;

import com.meca.did.constant.DIDConstant;
import com.meca.did.constant.ErrorCode;
import com.meca.did.constant.ResolveEventLogStatus;
import com.meca.did.contract.DIDContract;
import com.meca.did.exception.DIDBaseException;
import com.meca.did.exception.ResolveAttributeException;
import com.meca.did.protocol.base.*;
import com.meca.did.protocol.response.ResolveEventLogResult;
import com.meca.did.protocol.response.ResponseData;
import com.meca.did.protocol.response.TransactionInfo;
import com.meca.did.service.DIDServiceEngine;
import com.meca.did.util.DIDUtils;
import com.meca.did.util.DataToolUtils;
import com.meca.did.util.DateUtils;
import org.apache.commons.collections4.CollectionUtils;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.web3j.abi.EventEncoder;
import org.web3j.protocol.Web3j;
import org.web3j.protocol.core.DefaultBlockParameter;
import org.web3j.protocol.core.methods.response.EthBlock;
import org.web3j.protocol.core.methods.response.Log;
import org.web3j.protocol.core.methods.response.TransactionReceipt;

import java.io.IOException;
import java.math.BigInteger;
import java.util.*;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeoutException;
import java.util.zip.DataFormatException;

@Service
public class DIDServiceEngineImpl implements DIDServiceEngine {

    private static final Logger logger = LoggerFactory.getLogger(DIDServiceEngineImpl.class);

    private final Web3j web3j;
    private final DIDContract contract;

    //  The topic map.
    private final HashMap<String, String> topicMap;

    //  Block number for stopping parsing.
    private static final int STOP_RESOLVE_BLOCK_NUMBER = 0;

    @Autowired
    public DIDServiceEngineImpl(Web3j web3j, DIDContract contract) {
        this.web3j = web3j;
        this.contract = contract;
        this.topicMap = new HashMap<String, String>();

        this.topicMap.put(
                EventEncoder.encode(DIDContract.DIDATTRIBUTECHANGED_EVENT),
                DIDConstant.DID_EVENT_ATTRIBUTE_CHANGE
        );
    }

    @Override
    public ResponseData<Boolean> createDID(String DIDAddress, String publicKey) {
        logger.info("Create did service engine");
        String auth = new StringBuffer()
                .append(publicKey)
                .append(DIDConstant.SEPARATOR)
                .append(DIDAddress)
                .toString();
        logger.info("auth: " + auth);
        String created = DateUtils.getNoMillisecondTimeStampString();
        TransactionReceipt receipt;
        try {
            logger.info("auth: {}", auth);
            logger.info("created: {}", created);

            receipt = contract.createDID(
                    DIDAddress,
                    DataToolUtils.stringToByteArray(auth),
                    DataToolUtils.stringToByteArray(created),
                    BigInteger.valueOf(DateUtils.getNoMillisecondTimeStamp())
            ).send();

            TransactionInfo info = new TransactionInfo(receipt);
            List<DIDContract.DIDAttributeChangedEventResponse> response =
                    contract.getDIDAttributeChangedEvents(receipt);
            if (CollectionUtils.isEmpty(response)) {
                logger.error(
                        "Error when trying to create a DID"
                );
                return new ResponseData<>(false, ErrorCode.TRANSACTION_EXECUTE_ERROR, info);
            }
            return new ResponseData<>(true, ErrorCode.SUCCESS, info);
        } catch (Exception e) {
            logger.error("[createDID] create DID has error, Error Message：{}", e.toString());
            return new ResponseData<>(false, ErrorCode.UNKNOW_ERROR);
        }
    }

    @Override
    public ResponseData<Boolean> setAttribute(
            String DIDAddress,
            String attributeKey,
            String value) {
        logger.info("Inside setAttribute");
        try {
            byte[] attrValue = value.getBytes();
            BigInteger updated = BigInteger.valueOf(DateUtils.getNoMillisecondTimeStamp());
            TransactionReceipt transactionReceipt = null;

            transactionReceipt =
                    contract.setAttribute(
                            DIDAddress,
                            DataToolUtils.stringToByte32Array(attributeKey),
                            attrValue,
                            updated
                    ).send();

            TransactionInfo info = new TransactionInfo(transactionReceipt);
            List<DIDContract.DIDAttributeChangedEventResponse> response =
                    contract.getDIDAttributeChangedEvents(transactionReceipt);
            if (CollectionUtils.isNotEmpty(response)) {
                return new ResponseData<>(true, ErrorCode.SUCCESS, info);
            } else {
                return new ResponseData<>(false, ErrorCode.DID_PRIVATEKEY_DOES_NOT_MATCH,
                        info);
            }
        } catch (Exception e) {
            logger.error("[setAttribute] set Attribute has error, Error Message：{}", e);
            return new ResponseData<>(false, ErrorCode.UNKNOW_ERROR);
        }
    }

    @Override
    public ResponseData<Boolean> DIDExists(String DID) {
        try {

            boolean isExist = contract
                    .isIdentityExist(DIDUtils.convertDIDToAddress(DID)).send();

            return new ResponseData<>(isExist, ErrorCode.SUCCESS);
        } catch (Exception e) {
            logger.error("[didExists] execute failed. Error message :{}", e);
            return new ResponseData<>(false, ErrorCode.UNKNOW_ERROR);
        }
    }

    @Override
    public ResponseData<DIDDocument> getDIDDocument(String DID) {
        Map<Integer, List<DIDContract.DIDAttributeChangedEventResponse>> blockEventMap = new HashMap<>();
        List<Integer> blockList = new ArrayList<>();
        DIDDocument result = new DIDDocument();
        result.setId(DID);
        int latestBlockNumber = 0;
        try {
            String identityAddr = DIDUtils.convertDIDToAddress(DID);
            latestBlockNumber = contract
                    .getLatestRelatedBlock(identityAddr).send().intValue();
            if (0 == latestBlockNumber) {
                return new ResponseData<>(null, ErrorCode.DID_DOES_NOT_EXIST);
            }

            // Step 1: fetch all blocks in this event link in REVERSE order from chain
            resolveEventHistory(DID, latestBlockNumber, blockList, blockEventMap);

            // Step 2: reverse this the block list (so it is ascending order now)
            Collections.reverse(blockList);

            // Step 3: construct DID Document in NORMAL order off-chain
            constructDIDDocument(blockList, blockEventMap, result);

            return new ResponseData<>(result, ErrorCode.SUCCESS);
        } catch (InterruptedException | ExecutionException e) {
            logger.error("Set DID service failed. Error message :{}", e);
            return new ResponseData<>(null, ErrorCode.TRANSACTION_EXECUTE_ERROR);
        } catch (TimeoutException e) {
            logger.error("Set DID service timeout. Error message :{}", e);
            return new ResponseData<>(null, ErrorCode.TRANSACTION_TIMEOUT);
        } catch (ResolveAttributeException e) {
            logger.error("[getDIDDocument]: resolveTransaction failed. "
                            + "DID: {}, errorCode:{}",
                    DID,
                    e.getErrorCode(),
                    e);
            return new ResponseData<DIDDocument>(result,
                    ErrorCode.getTypeByErrorCode(e.getErrorCode()));
        } catch (Exception e) {
            logger.error("[getDIDDocument]: exception.", e);
            return new ResponseData<>(null, ErrorCode.UNKNOW_ERROR);
        }
    }

    /**
     * Resolve the event history given did as key, reversely from on-chain linked blocks.
     *
     * @param did           DID as key
     * @param blockNumber   the current latest block number
     * @param blockList     stored block height list
     * @param blockEventMap stored block event map
     */
    private void resolveEventHistory(
            String did,
            int blockNumber,
            List<Integer> blockList,
            Map<Integer, List<DIDContract.DIDAttributeChangedEventResponse>> blockEventMap
    ) {
        int previousBlock = blockNumber;
        while (previousBlock != STOP_RESOLVE_BLOCK_NUMBER) {
            int currentBlockNumber = previousBlock;
            // Fill-in blockList
            blockList.add(currentBlockNumber);
            previousBlock = 0;
            try {
                List<TransactionReceipt> receipts = getTransactionReceipts(currentBlockNumber);
                for (TransactionReceipt receipt : receipts) {
                    List<Log> logs = receipt.getLogs();
                    for (Log log : logs) {
                        ResolveEventLogResult returnValue =
                                resolveSingleEventLog(did, log, receipt, currentBlockNumber,
                                        blockEventMap);
                        if (returnValue.getResultStatus().equals(
                                ResolveEventLogStatus.STATUS_SUCCESS)) {
                            if (returnValue.getPreviousBlock() == currentBlockNumber) {
                                continue;
                            }
                            previousBlock = returnValue.getPreviousBlock();
                        }
                    }
                }
            } catch (IOException | DataFormatException | DIDBaseException e) {
                logger.error(
                        "[resolveEventHistory]: get TransactionReceipt by did :{} failed.", did, e);
//                throw new ResolveAttributeException(
//                        ErrorCode.TRANSACTION_EXECUTE_ERROR.getCode(),
//                        ErrorCode.TRANSACTION_EXECUTE_ERROR.getCodeDesc(),
//                        e);
            }
        }
    }

    private List<TransactionReceipt> getTransactionReceipts(Integer blockNumber)
            throws IOException, DataFormatException, DIDBaseException {
        TransactionReceipt blockTransactionReceipt = null;
        List<TransactionReceipt> blockTransactionReceipts = new LinkedList<>();
        EthBlock ethGetBlockByNumber = null;
        //TODO maybe fix this code
        try {
            List<EthBlock.TransactionResult> txs = web3j.ethGetBlockByNumber(DefaultBlockParameter.valueOf(BigInteger.valueOf(blockNumber)), true).send().getBlock().getTransactions();

            for (EthBlock.TransactionResult tx : txs) {
                EthBlock.TransactionObject transaction = (EthBlock.TransactionObject) tx.get();
                blockTransactionReceipt = web3j.ethGetTransactionReceipt(transaction.getHash()).send().getTransactionReceipt().get();
                logger.info(String.valueOf(blockTransactionReceipt));
                blockTransactionReceipts.add(blockTransactionReceipt);
            }

        } catch (Exception e) {
            logger.error("[getTransactionReceipts] get block {} err: {}", blockNumber, e);
        }
        if (blockTransactionReceipts == null) {
            logger.info("[getTransactionReceipts] get block {} err: is null", blockNumber);
            throw new DIDBaseException("the transactionReceipts is null.");
        }
        return blockTransactionReceipts;

//                .getBlockTransactionReceipts().getTransactionReceipts();
    }

    private ResolveEventLogResult resolveSingleEventLog(
            String DID,
            Log log,
            TransactionReceipt receipt,
            int currentBlockNumber,
            Map<Integer, List<DIDContract.DIDAttributeChangedEventResponse>> blockEventMap
    ) {
        String topic = log.getTopics().get(0);
        String event = topicMap.get(topic);

        if (StringUtils.isNotBlank(event)) {
            return extractEventsFromBlock(DID, receipt, currentBlockNumber, blockEventMap);
        }
        ResolveEventLogResult response = new ResolveEventLogResult();
        response.setResolveEventLogStatus(ResolveEventLogStatus.STATUS_EVENT_NULL);
        return response;
    }

    private ResolveEventLogResult extractEventsFromBlock(
            String DID,
            TransactionReceipt receipt,
            int currentBlockNumber,
            Map<Integer, List<DIDContract.DIDAttributeChangedEventResponse>> blockEventMap
    ) {

        List<DIDContract.DIDAttributeChangedEventResponse> eventlog =
                contract.getDIDAttributeChangedEvents(receipt);
        ResolveEventLogResult response = new ResolveEventLogResult();

        if (CollectionUtils.isEmpty(eventlog)) {
            response.setResolveEventLogStatus(ResolveEventLogStatus.STATUS_EVENTLOG_NULL);
            return response;
        }

        int previousBlock = 0;
        for (DIDContract.DIDAttributeChangedEventResponse res : eventlog) {
            if (res.identity == null || res.updated == null || res.previousBlock == null) {
                response.setResolveEventLogStatus(ResolveEventLogStatus.STATUS_RES_NULL);
                return response;
            }

            String identity = res.identity.toString();
            String weAddress = DIDUtils.convertDIDToAddress(DID);
            if (!StringUtils.equals(weAddress, identity)) {
                response.setResolveEventLogStatus(ResolveEventLogStatus.STATUS_KEY_NOT_MATCH);
                return response;
            }

            // Fill-in blockEventMap
            List<DIDContract.DIDAttributeChangedEventResponse> events = blockEventMap.get(currentBlockNumber);
            if (CollectionUtils.isEmpty(events)) {
                List<DIDContract.DIDAttributeChangedEventResponse> newEvents = new ArrayList<>();
                newEvents.add(res);
                blockEventMap.put(currentBlockNumber, newEvents);
            } else {
                events.add(res);
            }

            //String key = new String(res.key);
            //String value = new String(res.value);
            previousBlock = res.previousBlock.intValue();
        }

        response.setPreviousBlock(previousBlock);
        response.setResolveEventLogStatus(ResolveEventLogStatus.STATUS_SUCCESS);
        return response;
    }

    private void constructDIDDocument(
            List<Integer> blockList,
            Map<Integer, List<DIDContract.DIDAttributeChangedEventResponse>> blockEventMap,
            DIDDocument didDocument) {
        String DID = didDocument.getId();
        // Iterate thru the blocklist (now ascending)
        for (int block : blockList) {
            List<DIDContract.DIDAttributeChangedEventResponse> eventList = blockEventMap.get(block);
            for (DIDContract.DIDAttributeChangedEventResponse event : eventList) {
                String key = new String(event.key);
                String value = new String(event.value);
                constructDIDAttribute(key, value, DID, didDocument);
            }
        }
    }

    /**
     * Identify the event and construct DID Document.
     *
     * @param key    the key
     * @param value  the value (mainly pubkeys including tag)
     * @param DID    the DID
     * @param result the updating Document
     */
    private void constructDIDAttribute(
            String key, String value, String DID, DIDDocument result) {
        if (StringUtils.startsWith(key, DIDConstant.DID_DOC_PUBLICKEY_PREFIX)) {
            constructDIDPublicKeys(key, value, DID, result);
        } else if (StringUtils.startsWith(key, DIDConstant.DID_DOC_AUTHENTICATE_PREFIX)) {
            if (!value.contains(DIDConstant.REMOVED_PUBKEY_TAG)) {
                constructDIDPublicKeys(null, value, DID, result);
            }
            constructDIDAuthentication(value, DID, result);
        } else if (StringUtils.startsWith(key, DIDConstant.DID_DOC_SERVICE_PREFIX)) {
            constructDIDService(key, value, DID, result);
        } else {
            constructDefaultDIDAttribute(key, value, DID, result);
        }
    }

    private void constructDIDPublicKeys(String key, String value, String DID,
                                        DIDDocument result) {

        logger.info("method constructDIDPublicKeys() parameter::value:{}, DID:{}, "
                + "result:{}", value, DID, result);
        List<PublicKeyProperty> pubKeyList = result.getPublicKey();

        String type = DIDConstant.PublicKeyType.SECP256K1.getTypeName();
        // Identify explicit type from key
        if (!StringUtils.isEmpty(key)) {
            String[] keyArray = StringUtils.splitByWholeSeparator(key, "/");
            if (keyArray.length > 2) {
                type = keyArray[2];
            }
        }

        // In ascending order approach, we use the new obtained value as overriding attribute.
        // We 1st: UDPATE STATUS, by going thru the existing pubkeys list. If it already contains
        // this pubkey, simply override the tag and return.
        Boolean isRevoked = value.contains(DIDConstant.REMOVED_PUBKEY_TAG);
        String trimmedPubKey = StringUtils
                .splitByWholeSeparator(value.replace(DIDConstant.REMOVED_PUBKEY_TAG, ""),
                        DIDConstant.SEPARATOR)[0];
        for (PublicKeyProperty pr : pubKeyList) {
            if (pr.getPublicKey().contains(trimmedPubKey)) {
                // update status: revocation
                if (!pr.getRevoked().equals(isRevoked)) {
                    pr.setRevoked(isRevoked);
                }
                // update owner
                String[] publicKeyData = StringUtils
                        .splitByWholeSeparator(value, DIDConstant.SEPARATOR);
                String address = publicKeyData[1];
                String owner = DIDUtils.convertAddressToDID(address);
                pr.setOwner(owner);
                return;
            }
        }

        // 由于目前不允许对一个不存在的key直接remove，因此下面这小段不会被执行到。未来修改时需要留意。
        if (isRevoked) {
            logger.error("Failed to revoke a non-existent pubkey {} from current Document {}",
                    value, result);
            return;
        }

        // We 2nd: not an UPDATE case, now CREATE a new pubkey property and allocate a new ID.
        PublicKeyProperty pubKey = new PublicKeyProperty();
        pubKey.setId(
                new StringBuffer()
                        .append(DID)
                        .append("#keys-")
                        .append(result.getPublicKey().size())
                        .toString()
        );
        String[] publicKeyData = StringUtils.splitByWholeSeparator(value, DIDConstant.SEPARATOR);
        if (publicKeyData != null && publicKeyData.length == 2) {
            pubKey.setPublicKey(publicKeyData[0]);
            String weAddress = publicKeyData[1];
            String owner = DIDUtils.convertAddressToDID(weAddress);
            pubKey.setOwner(owner);
        }
        pubKey.setType(type);
        result.getPublicKey().add(pubKey);
    }

    private void constructDIDAuthentication(
            String value,
            String DID,
            DIDDocument result
    ) {
        logger.info("method constructDIDAuthentication() parameter::value:{}, DID:{}, "
                + "result:{}", value, DID, result);
        List<PublicKeyProperty> keyList = result.getPublicKey();
        List<AuthenticationProperty> authList = result.getAuthentication();

        // In ascending order approach, we use the similar approach as in pubkey - always override.

        // We 1st: UDPATE STATUS, by going thru the existing auths list. If it already contains
        // this auth, simply override the tag and return.
        // Complexity here is: 1. the ID must follow public key. 2. enable tag case.
        Boolean isRevoked = value.contains(DIDConstant.REMOVED_AUTHENTICATION_TAG);
        for (AuthenticationProperty ap : authList) {
            String pubKeyId = ap.getPublicKey();
            logger.info("ap {}", ap);
            for (PublicKeyProperty pkp : keyList) {
                logger.info("pkp id {}\n pkp publicKey {}", pkp.getId(), pkp.getPublicKey());
                if (pubKeyId.equalsIgnoreCase(pkp.getId()) && value.contains(pkp.getPublicKey())) {
                    logger.info("Found matching authentication and key");
                    // Found matching, now do tag resetting
                    // NOTE: 如果isRevoked为false，请注意由于pubKey此时一定已经是false（见母方法），
                    //  故无需做特别处理。但，未来如果实现分离了，就需要做特殊处理，还请留意。
                    if (!ap.getRevoked().equals(isRevoked)) {
                        ap.setRevoked(isRevoked);
                    }
                    return;
                }
            }
        }

        // 由于目前不允许对一个不存在的key直接remove，因此下面这小段不会被执行到。未来修改时需要留意。
        if (isRevoked) {
            logger.error("Failed to revoke a non-existent auth {} from current Document {}",
                    value, result);
            return;
        }

        // We 2nd: create new one when no matching record is found
        AuthenticationProperty auth = new AuthenticationProperty();
        for (PublicKeyProperty r : keyList) {
            if (value.contains(r.getPublicKey())) {
                for (AuthenticationProperty ar : authList) {
                    if (StringUtils.equals(ar.getPublicKey(), r.getId())) {
                        return;
                    }
                }
                auth.setPublicKey(r.getId());
                result.getAuthentication().add(auth);
            }
        }
    }

    private void constructDIDService(String key, String value, String DID,
                                     DIDDocument result) {

        logger.info("method constructDIDService() parameter::key{}, value:{}, DID:{}, "
                + "result:{}", key, value, DID, result);
        String service = StringUtils.splitByWholeSeparator(key, "/")[2];
        List<ServiceProperty> serviceList = result.getService();

        // Always override when new value is obtained
        for (ServiceProperty sr : serviceList) {
            if (service.equals(sr.getType())) {
                sr.setServiceEndpoint(value);
                return;
            }
        }
        ServiceProperty serviceResult = new ServiceProperty();
        serviceResult.setType(service);
        serviceResult.setServiceEndpoint(value);
        result.getService().add(serviceResult);
    }

    private void constructDefaultDIDAttribute(
            String key, String value, String DID, DIDDocument result) {

        logger.info("method constructDefaultDIDAttribute() parameter::key{}, value:{}, DID:{}, "
                + "result:{}", key, value, DID, result);
        switch (key.trim()) {
            case DIDConstant.DID_DOC_CREATED:
                result.setCreated(Long.valueOf(value));
                break;
            default:
                break;
        }
    }

    @Override
    public ResponseData<List<DIDPojo>> getDIDList(Integer blockNumber, Integer pageSize, Integer indexInBlock, boolean direction) throws Exception {
        return null;
    }

    @Override
    public ResponseData<Integer> getDIDCount() {
        try {
            Integer total = contract.getDIDCount().send().intValue();
            return new ResponseData<>(total, ErrorCode.SUCCESS);
        } catch (Exception e) {
            logger.error("[getDIDCount]: get DID total has unknow error. ", e);
            return new ResponseData<>(0, ErrorCode.UNKNOW_ERROR);
        }
    }

    /**
     * get the first blockNumber for the contract.
     *
     * @return the blockNumber
     * @throws Exception unknown exception
     */
    private Integer getFirstBlockNum() throws Exception {
        return contract.getFirstBlockNum().send().intValue();
    }

    /**
     * get the last blockNumber for the contract.
     *
     * @return the blockNumber
     * @throws Exception unknown exception
     */
    private Integer getLatestBlockNum() throws Exception {
        return contract.getLatestBlockNum().send().intValue();
    }

    /**
     * get the next blockNumber by the currentBlockNumber.
     *
     * @param blockNumber the currentBlockNumber
     * @return the blockNumber
     * @throws Exception unknown exception
     */
    private Integer getNextBlockNum(Integer blockNumber) throws Exception {
        return contract.getNextBlockNumByBlockNum(
                new BigInteger(String.valueOf(blockNumber))
        ).send().intValue();
    }

}
