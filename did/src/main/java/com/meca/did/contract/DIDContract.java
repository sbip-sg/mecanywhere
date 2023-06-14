package com.meca.did.contract;


import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.web3j.abi.TypeReference;
import org.web3j.abi.datatypes.*;
import org.web3j.abi.datatypes.generated.Bytes32;
import org.web3j.abi.datatypes.generated.Int256;
import org.web3j.abi.datatypes.generated.Uint256;
import org.web3j.crypto.Credentials;
import org.web3j.protocol.Web3j;
import org.web3j.protocol.core.RemoteCall;
import org.web3j.protocol.core.methods.response.Log;
import org.web3j.protocol.core.methods.response.TransactionReceipt;
import org.web3j.tx.Contract;
import org.web3j.tx.gas.ContractGasProvider;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

@Component
public class DIDContract extends Contract {
    private static final Logger logger = LoggerFactory.getLogger(DIDContract.class);

    @Autowired
    public DIDContract(ContractConfig contractConfig, Web3j web3j, Credentials credentials, ContractGasProvider contractGasProvider) {
        super(contractConfig.getDIDContractBinary(),
                contractConfig.getDIDContractAddress(),
                web3j,
                credentials,
                contractGasProvider);
    }

    public static final String FUNC_IDENTITYEXISTS = "identityExists";

    public static final String FUNC_GETFIRSTBLOCKNUM = "getFirstBlockNum";

    public static final String FUNC_SETATTRIBUTE = "setAttribute";

    public static final String FUNC_GETLATESTRELATEDBLOCK = "getLatestRelatedBlock";

    public static final String FUNC_GETDIDCOUNT = "getDIDCount";

    public static final String FUNC_CREATEDID = "createDID";

    public static final String FUNC_GETLATESTBLOCKNUM = "getLatestBlockNum";

    public static final String FUNC_GETNEXTBLOCKNUMBYBLOCKNUM = "getNextBlockNumByBlockNum";

    public static final Event DIDATTRIBUTECHANGED_EVENT = new Event("DIDAttributeChanged",
            Arrays.<TypeReference<?>>asList(new TypeReference<Address>(true) {}, new TypeReference<Bytes32>() {}, new TypeReference<DynamicBytes>() {}, new TypeReference<Uint256>() {}, new TypeReference<Int256>() {}));
    ;

    public static final Event DIDHISTORYEVENT_EVENT = new Event("DIDHistoryEvent",
            Arrays.<TypeReference<?>>asList(new TypeReference<Address>(true) {}, new TypeReference<Uint256>() {}, new TypeReference<Int256>() {}));
    ;

//    public static String getBinary() {
//        return BINARY;
//    }

    public RemoteCall<Boolean> isIdentityExist(String identity) {
        final Function function = new Function(FUNC_IDENTITYEXISTS,
                Arrays.<Type>asList(new org.web3j.abi.datatypes.Address(identity)),
                Arrays.<TypeReference<?>>asList(new TypeReference<Bool>() {}));
        return executeRemoteCallSingleValueReturn(function, Boolean.class);
    }

    public RemoteCall<BigInteger> getFirstBlockNum() {
        final Function function = new Function(FUNC_GETFIRSTBLOCKNUM,
                Arrays.<Type>asList(),
                Arrays.<TypeReference<?>>asList(new TypeReference<Uint256>() {}));
        return executeRemoteCallSingleValueReturn(function, BigInteger.class);
    }

    public RemoteCall<TransactionReceipt> setAttribute(String identity, byte[] key, byte[] value, BigInteger updated) {
        final Function function = new Function(
                FUNC_SETATTRIBUTE,
                Arrays.<Type>asList(new org.web3j.abi.datatypes.Address(identity),
                        new org.web3j.abi.datatypes.generated.Bytes32(key),
                        new org.web3j.abi.datatypes.DynamicBytes(value),
                        new org.web3j.abi.datatypes.generated.Int256(updated)),
                Collections.<TypeReference<?>>emptyList());
        return executeRemoteCallTransaction(function);
    }

    public RemoteCall<BigInteger> getLatestRelatedBlock(String identity) {
        final Function function = new Function(FUNC_GETLATESTRELATEDBLOCK,
                Arrays.<Type>asList(new org.web3j.abi.datatypes.Address(identity)),
                Arrays.<TypeReference<?>>asList(new TypeReference<Uint256>() {}));
        return executeRemoteCallSingleValueReturn(function, BigInteger.class);
    }

    public RemoteCall<BigInteger> getDIDCount() {
        final Function function = new Function(FUNC_GETDIDCOUNT,
                Arrays.<Type>asList(),
                Arrays.<TypeReference<?>>asList(new TypeReference<Uint256>() {}));
        return executeRemoteCallSingleValueReturn(function, BigInteger.class);
    }

    public RemoteCall<TransactionReceipt> createDID(String identity, byte[] auth, byte[] created, BigInteger updated) {
        logger.info("in DIDContract creating DID");
        logger.info("identity {}", identity);
        logger.info("updated {}", updated);
        final Function function = new Function(
                FUNC_CREATEDID,
                Arrays.<Type>asList(new org.web3j.abi.datatypes.Address(identity),
                        new org.web3j.abi.datatypes.DynamicBytes(auth),
                        new org.web3j.abi.datatypes.DynamicBytes(created),
                        new org.web3j.abi.datatypes.generated.Int256(updated)),
                Collections.<TypeReference<?>>emptyList());
        return executeRemoteCallTransaction(function);
    }

    public RemoteCall<BigInteger> getLatestBlockNum() {
        final Function function = new Function(FUNC_GETLATESTBLOCKNUM,
                Arrays.<Type>asList(),
                Arrays.<TypeReference<?>>asList(new TypeReference<Uint256>() {}));
        return executeRemoteCallSingleValueReturn(function, BigInteger.class);
    }

    public RemoteCall<BigInteger> getNextBlockNumByBlockNum(BigInteger currentBlockNum) {
        final Function function = new Function(FUNC_GETNEXTBLOCKNUMBYBLOCKNUM,
                Arrays.<Type>asList(new org.web3j.abi.datatypes.generated.Uint256(currentBlockNum)),
                Arrays.<TypeReference<?>>asList(new TypeReference<Uint256>() {}));
        return executeRemoteCallSingleValueReturn(function, BigInteger.class);
    }

    public List<DIDAttributeChangedEventResponse> getDIDAttributeChangedEvents(TransactionReceipt transactionReceipt) {
        List<Contract.EventValuesWithLog> valueList = extractEventParametersWithLog(DIDATTRIBUTECHANGED_EVENT, transactionReceipt);
        ArrayList<DIDAttributeChangedEventResponse> responses = new ArrayList<DIDAttributeChangedEventResponse>(valueList.size());
        for (Contract.EventValuesWithLog eventValues : valueList) {
            DIDAttributeChangedEventResponse typedResponse = new DIDAttributeChangedEventResponse();
            typedResponse.log = eventValues.getLog();
            typedResponse.identity = (String) eventValues.getIndexedValues().get(0).getValue();
            typedResponse.key = (byte[]) eventValues.getNonIndexedValues().get(0).getValue();
            typedResponse.value = (byte[]) eventValues.getNonIndexedValues().get(1).getValue();
            typedResponse.previousBlock = (BigInteger) eventValues.getNonIndexedValues().get(2).getValue();
            typedResponse.updated = (BigInteger) eventValues.getNonIndexedValues().get(3).getValue();
            responses.add(typedResponse);
        }
        return responses;
    }

    public List<DIDHistoryEventEventResponse> getDIDHistoryEventEvents(TransactionReceipt transactionReceipt) {
        List<Contract.EventValuesWithLog> valueList = extractEventParametersWithLog(DIDHISTORYEVENT_EVENT, transactionReceipt);
        ArrayList<DIDHistoryEventEventResponse> responses = new ArrayList<DIDHistoryEventEventResponse>(valueList.size());
        for (Contract.EventValuesWithLog eventValues : valueList) {
            DIDHistoryEventEventResponse typedResponse = new DIDHistoryEventEventResponse();
            typedResponse.log = eventValues.getLog();
            typedResponse.identity = (String) eventValues.getIndexedValues().get(0).getValue();
            typedResponse.previousBlock = (BigInteger) eventValues.getNonIndexedValues().get(0).getValue();
            typedResponse.created = (BigInteger) eventValues.getNonIndexedValues().get(1).getValue();
            responses.add(typedResponse);
        }
        return responses;
    }

    public static class DIDAttributeChangedEventResponse {
        public Log log;

        public String identity;

        public byte[] key;

        public byte[] value;

        public BigInteger previousBlock;

        public BigInteger updated;
    }

    public static class DIDHistoryEventEventResponse {
        public Log log;

        public String identity;

        public BigInteger previousBlock;

        public BigInteger created;
    }
}
