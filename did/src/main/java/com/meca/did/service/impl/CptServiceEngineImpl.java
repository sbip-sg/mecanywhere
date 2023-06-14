package com.meca.did.service.impl;

import com.meca.did.constant.DIDConstant;
import com.meca.did.constant.ErrorCode;
import com.meca.did.contract.CptContract;
import com.meca.did.contract.CptContract.RegisterCptRetLogEventResponse;
import com.meca.did.protocol.base.Cpt;
import com.meca.did.protocol.base.CptBaseInfo;
import com.meca.did.protocol.response.ResponseData;
import com.meca.did.protocol.response.RsvSignature;
import com.meca.did.protocol.response.TransactionInfo;
import com.meca.did.service.CptServiceEngine;
import com.meca.did.util.DIDUtils;
import com.meca.did.util.DataToolUtils;
import org.apache.commons.collections4.CollectionUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.web3j.crypto.Sign;
import org.web3j.protocol.core.methods.response.TransactionReceipt;
import org.web3j.tuples.generated.Tuple7;

import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;

@Service
public class CptServiceEngineImpl implements CptServiceEngine {

    private static final Logger logger = LoggerFactory.getLogger(CptServiceEngineImpl.class);

    private final CptContract contract;

    @Autowired
    public CptServiceEngineImpl(CptContract contract) {
        this.contract = contract;
    }

    @Override
    public ResponseData<CptBaseInfo> registerCpt(String address, String cptJsonSchemaNew, RsvSignature rsvSignature, String privateKey, int dataStorageIndex) {

        List<byte[]> byteArray = new ArrayList<>();
        TransactionReceipt transactionReceipt;
        try {
            transactionReceipt = contract.registerCpt(
                    address,
                    DataToolUtils.listToListBigInteger(
                            DataToolUtils.getParamCreatedList(DIDConstant.CPT_LONG_ARRAY_LENGTH),
                            DIDConstant.CPT_LONG_ARRAY_LENGTH
                    ),
                    DataToolUtils.bytesArrayListToBytes32ArrayList(
                            byteArray,
                            DIDConstant.CPT_STRING_ARRAY_LENGTH
                    ),
                    DataToolUtils.stringToByte32ArrayList(
                            cptJsonSchemaNew, DIDConstant.JSON_SCHEMA_ARRAY_LENGTH),
                    rsvSignature.getV().getValue(),
                    rsvSignature.getR().getValue(),
                    rsvSignature.getS().getValue()).send();

            ResponseData<CptBaseInfo> response = processRegisterEventLog(transactionReceipt);
            if (response.getErrorCode().intValue() != ErrorCode.SUCCESS.getCode()) {
                return response;
            }
            Integer cptId = response.getResult().getCptId();
            ErrorCode errorCode = processTemplate(cptId, cptJsonSchemaNew);
            int code = errorCode.getCode();
            if (code != ErrorCode.SUCCESS.getCode()) {
                logger.error("[registerCpt]register cpt failed, error code is {}", code);
                return new ResponseData<CptBaseInfo>(null, ErrorCode.getTypeByErrorCode(code));
            }
            return response;
        } catch (Exception e) {
            logger.error("[registerCpt] register cpt failed. exception message: ", e);
            return new ResponseData<CptBaseInfo>(null, ErrorCode.UNKNOW_ERROR);
        }
    }

    @Override
    public ResponseData<Cpt> queryCpt(int cptId, int dataStorageIndex) {

        try {
            Tuple7<String, List<BigInteger>, List<byte[]>, List<byte[]>,
                                BigInteger, byte[], byte[]> valueList;
            valueList = contract
                    .queryCpt(new BigInteger(String.valueOf(cptId)))
                    .sendAsync()
                    .get(DIDConstant.TRANSACTION_RECEIPT_TIMEOUT, TimeUnit.SECONDS);


            if (valueList == null) {
                logger.error("Query cpt id : {} does not exist, result is null.", cptId);
                return new ResponseData<>(null, ErrorCode.CPT_NOT_EXISTS);
            }

            if (DIDConstant.EMPTY_ADDRESS.equals(valueList.component1())) {
                logger.error("Query cpt id : {} does not exist.", cptId);
                return new ResponseData<>(null, ErrorCode.CPT_NOT_EXISTS);
            }
            Cpt cpt = new Cpt();
            cpt.setCptId(cptId);
            cpt.setCptPublisher(
                    DIDUtils.convertAddressToDID(valueList.component1())
            );

            List<BigInteger> longArray = valueList.component2();

            cpt.setCptVersion(longArray.get(0).intValue());
            cpt.setCreated(longArray.get(1).longValue());
            cpt.setUpdated(longArray.get(2).longValue());

            List<byte[]> jsonSchemaArray = valueList.component4();

            String jsonSchema = DataToolUtils.byte32ListToString(
                    jsonSchemaArray, DIDConstant.JSON_SCHEMA_ARRAY_LENGTH);

            Map<String, Object> jsonSchemaMap = (HashMap<String, Object>) DataToolUtils
                    .deserialize(jsonSchema.trim(), HashMap.class);
            cpt.setCptJsonSchema(jsonSchemaMap);

            int v = valueList.component5().intValue();
            byte[] r = valueList.component6();
            byte[] s = valueList.component7();
            Sign.SignatureData signatureData = DataToolUtils
                    .rawSignatureDeserialization(v, r, s);
            String cptSignature =
                    new String(
                            DataToolUtils.base64Encode(
                                    DataToolUtils.simpleSignatureSerialization(signatureData)),
                            StandardCharsets.UTF_8
                    );
            cpt.setCptSignature(cptSignature);

            ResponseData<Cpt> responseData = new ResponseData<Cpt>(cpt, ErrorCode.SUCCESS);
            return responseData;
        } catch (Exception e) {
            logger.error("[queryCpt] query Cpt failed. exception message: ", e);
            return new ResponseData<Cpt>(null, ErrorCode.TRANSACTION_EXECUTE_ERROR);
        }
    }

    /**
     * process RegisterEventLog.
     *
     * @param transactionReceipt transactionReceipt
     * @return result
     */
    private ResponseData<CptBaseInfo> processRegisterEventLog(TransactionReceipt transactionReceipt) {
        List<RegisterCptRetLogEventResponse> event = contract.getRegisterCptRetLogEvents(
                transactionReceipt
        );
        if (CollectionUtils.isEmpty(event)) {
            return new ResponseData<>(null, ErrorCode.CPT_EVENT_LOG_NULL);
        }

        return getResultByResolveEvent(
                event.get(0).retCode,
                event.get(0).cptId,
                event.get(0).cptVersion,
                transactionReceipt
        );
    }

    private ErrorCode processTemplate(Integer cptId, String cptJsonSchemaNew) {
        //if the cpt is not zkp type, no need to make template.
        return ErrorCode.SUCCESS;
    }

    /**
     * Resolve CPT Event.
     *
     * @param retCode the retCode
     * @param cptId the CptId
     * @param cptVersion the CptVersion
     * @param receipt receipt
     * @return the result
     */
    private ResponseData<CptBaseInfo> getResultByResolveEvent(
            BigInteger retCode,
            BigInteger cptId,
            BigInteger cptVersion,
            TransactionReceipt receipt) {

        TransactionInfo info = new TransactionInfo(receipt);
        // register
        if (retCode.intValue()
                == ErrorCode.CPT_ID_AUTHORITY_ISSUER_EXCEED_MAX.getCode()) {
            logger.error("[getResultByResolveEvent] cptId limited max value. cptId:{}",
                    retCode.intValue());
            return new ResponseData<>(null, ErrorCode.CPT_ID_AUTHORITY_ISSUER_EXCEED_MAX, info);
        }

        if (retCode.intValue() == ErrorCode.CPT_ALREADY_EXIST.getCode()) {
            logger.error("[getResultByResolveEvent] cpt already exists on chain. cptId:{}",
                    cptId.intValue());
            return new ResponseData<>(null, ErrorCode.CPT_ALREADY_EXIST, info);
        }

        if (retCode.intValue() == ErrorCode.CPT_NO_PERMISSION.getCode()) {
            logger.error("[getResultByResolveEvent] no permission. cptId:{}",
                    cptId.intValue());
            return new ResponseData<>(null, ErrorCode.CPT_NO_PERMISSION, info);
        }

        // register and update
        if (retCode.intValue() == ErrorCode.CPT_PUBLISHER_NOT_EXIST.getCode()) {
            logger.error("[getResultByResolveEvent] publisher does not exist. cptId:{}",
                    cptId.intValue());
            return new ResponseData<>(null, ErrorCode.CPT_PUBLISHER_NOT_EXIST, info);
        }

        // update
        if (retCode.intValue() == ErrorCode.CPT_NOT_EXISTS.getCode()) {
            logger.error("[getResultByResolveEvent] cpt id : {} does not exist.",
                    cptId.intValue());
            return new ResponseData<>(null, ErrorCode.CPT_NOT_EXISTS, info);
        }

        CptBaseInfo result = new CptBaseInfo();
        result.setCptId(cptId.intValue());
        result.setCptVersion(cptVersion.intValue());

        ResponseData<CptBaseInfo> responseData = new ResponseData<>(result, ErrorCode.SUCCESS,
                info);
        return responseData;
    }

}
