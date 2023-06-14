package com.meca.did.contract;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.web3j.abi.TypeReference;
import org.web3j.abi.Utils;
import org.web3j.abi.datatypes.*;
import org.web3j.abi.datatypes.generated.Bytes32;
import org.web3j.abi.datatypes.generated.Int256;
import org.web3j.abi.datatypes.generated.Uint256;
import org.web3j.abi.datatypes.generated.Uint8;
import org.web3j.crypto.Credentials;
import org.web3j.protocol.Web3j;
import org.web3j.protocol.core.RemoteCall;
import org.web3j.protocol.core.methods.response.Log;
import org.web3j.protocol.core.methods.response.TransactionReceipt;
import org.web3j.tuples.generated.Tuple7;
import org.web3j.tx.Contract;
import org.web3j.tx.gas.ContractGasProvider;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.Callable;

@Component
public class CptContract extends Contract {
    private static final Logger logger = LoggerFactory.getLogger(CptContract.class);

    @Autowired
    public CptContract(ContractConfig contractConfig, Web3j web3j, Credentials credentials, ContractGasProvider contractGasProvider) {
        super(contractConfig.getCptContractBinary(),
                contractConfig.getCptContractAddress(),
                web3j,
                credentials,
                contractGasProvider);
    }

    public static final String FUNC_GETCPTIDLIST = "getCptIdList";

    public static final String FUNC_GETTOTALCPTID = "getTotalCptId";

    public static final String FUNC_GETCREDENTIALTEMPLATEBLOCK = "getCredentialTemplateBlock";

    public static final String FUNC_PUTCLAIMPOLICIESINTOPRESENTATIONMAP = "putClaimPoliciesIntoPresentationMap";

    public static final String FUNC_UPDATEPOLICY = "updatePolicy";

    public static final String FUNC_GETCLAIMPOLICIESFROMPRESENTATIONMAP = "getClaimPoliciesFromPresentationMap";

    public static final String FUNC_REGISTERPOLICY = "registerPolicy";

    public static final String FUNC_UPDATECPT = "updateCpt";

    public static final String FUNC_QUERYCPT = "queryCpt";

    public static final String FUNC_GETCPTDYNAMICJSONSCHEMAARRAY = "getCptDynamicJsonSchemaArray";

    public static final String FUNC_GETPOLICYIDLIST = "getPolicyIdList";

    public static final String FUNC_QUERYPOLICY = "queryPolicy";

    public static final String FUNC_REGISTERCPT = "registerCpt";

    public static final String FUNC_SETROLECONTROLLER = "setRoleController";

    public static final String FUNC_GETTOTALPOLICYID = "getTotalPolicyId";

    public static final String FUNC_PUTCLAIMPOLICIESINTOCPTMAP = "putClaimPoliciesIntoCptMap";

    public static final String FUNC_GETCLAIMPOLICIESFROMCPTMAP = "getClaimPoliciesFromCptMap";

    public static final String FUNC_GETCPTDYNAMICBYTES32ARRAY = "getCptDynamicBytes32Array";

    public static final String FUNC_SETPOLICYDATA = "setPolicyData";

    public static final String FUNC_GETCPTDYNAMICINTARRAY = "getCptDynamicIntArray";

    public static final String FUNC_PUTCREDENTIALTEMPLATE = "putCredentialTemplate";

    public static final Event REGISTERCPTRETLOG_EVENT = new Event("RegisterCptRetLog",
            Arrays.<TypeReference<?>>asList(new TypeReference<Uint256>() {}, new TypeReference<Uint256>() {}, new TypeReference<Int256>() {}));
    ;

    public static final Event UPDATECPTRETLOG_EVENT = new Event("UpdateCptRetLog",
            Arrays.<TypeReference<?>>asList(new TypeReference<Uint256>() {}, new TypeReference<Uint256>() {}, new TypeReference<Int256>() {}));
    ;

    public static final Event CREDENTIALTEMPLATE_EVENT = new Event("CredentialTemplate",
            Arrays.<TypeReference<?>>asList(new TypeReference<Uint256>() {}, new TypeReference<DynamicBytes>() {}, new TypeReference<DynamicBytes>() {}));
    ;

    public RemoteCall<TransactionReceipt> registerCpt(String publisher, List<BigInteger> intArray, List<byte[]> bytes32Array, List<byte[]> jsonSchemaArray, BigInteger v, byte[] r, byte[] s) {
        logger.info(publisher);
        logger.info(intArray.toString());
        logger.info(String.valueOf(bytes32Array));
        logger.info(v.toString());
        logger.info(Arrays.toString(r));
        logger.info(Arrays.toString(s));

        final Function function = new Function(
                FUNC_REGISTERCPT,
                Arrays.<Type>asList(new org.web3j.abi.datatypes.Address(publisher),
                        new org.web3j.abi.datatypes.generated.StaticArray8<org.web3j.abi.datatypes.generated.Int256>(
                                org.web3j.abi.Utils.typeMap(intArray, org.web3j.abi.datatypes.generated.Int256.class)),
                        new org.web3j.abi.datatypes.generated.StaticArray8<org.web3j.abi.datatypes.generated.Bytes32>(
                                org.web3j.abi.Utils.typeMap(bytes32Array, org.web3j.abi.datatypes.generated.Bytes32.class)),
                        new org.web3j.abi.datatypes.generated.StaticArray32<>(
                                Utils.typeMap(jsonSchemaArray, Bytes32.class)),
                        new org.web3j.abi.datatypes.generated.Uint8(v),
                        new org.web3j.abi.datatypes.generated.Bytes32(r),
                        new org.web3j.abi.datatypes.generated.Bytes32(s)),
                Collections.<TypeReference<?>>emptyList());
        logger.info(function.toString());
        return executeRemoteCallTransaction(function);
    }

    public List<RegisterCptRetLogEventResponse> getRegisterCptRetLogEvents(TransactionReceipt transactionReceipt) {
        List<Contract.EventValuesWithLog> valueList = extractEventParametersWithLog(REGISTERCPTRETLOG_EVENT, transactionReceipt);
        ArrayList<RegisterCptRetLogEventResponse> responses = new ArrayList<RegisterCptRetLogEventResponse>(valueList.size());
        for (Contract.EventValuesWithLog eventValues : valueList) {
            RegisterCptRetLogEventResponse typedResponse = new RegisterCptRetLogEventResponse();
            typedResponse.log = eventValues.getLog();
            typedResponse.retCode = (BigInteger) eventValues.getNonIndexedValues().get(0).getValue();
            typedResponse.cptId = (BigInteger) eventValues.getNonIndexedValues().get(1).getValue();
            typedResponse.cptVersion = (BigInteger) eventValues.getNonIndexedValues().get(2).getValue();
            responses.add(typedResponse);
        }
        return responses;
    }

    public RemoteCall<Tuple7<String, List<BigInteger>, List<byte[]>, List<byte[]>, BigInteger, byte[], byte[]>> queryCpt(BigInteger cptId) {
        final Function function = new Function(FUNC_QUERYCPT,
                Arrays.<Type>asList(new org.web3j.abi.datatypes.generated.Uint256(cptId)),
                Arrays.<TypeReference<?>>asList(new TypeReference<Address>() {}, new TypeReference<DynamicArray<Int256>>() {}, new TypeReference<DynamicArray<Bytes32>>() {}, new TypeReference<DynamicArray<Bytes32>>() {}, new TypeReference<Uint8>() {}, new TypeReference<Bytes32>() {}, new TypeReference<Bytes32>() {}));
        return new RemoteCall<Tuple7<String, List<BigInteger>, List<byte[]>, List<byte[]>, BigInteger, byte[], byte[]>>(
                new Callable<Tuple7<String, List<BigInteger>, List<byte[]>, List<byte[]>, BigInteger, byte[], byte[]>>() {
                    @Override
                    public Tuple7<String, List<BigInteger>, List<byte[]>, List<byte[]>, BigInteger, byte[], byte[]> call() throws Exception {
                        List<Type> results = executeCallMultipleValueReturn(function);
                        return new Tuple7<String, List<BigInteger>, List<byte[]>, List<byte[]>, BigInteger, byte[], byte[]>(
                                (String) results.get(0).getValue(),
                                convertToNative((List<Int256>) results.get(1).getValue()),
                                convertToNative((List<Bytes32>) results.get(2).getValue()),
                                convertToNative((List<Bytes32>) results.get(3).getValue()),
                                (BigInteger) results.get(4).getValue(),
                                (byte[]) results.get(5).getValue(),
                                (byte[]) results.get(6).getValue());
                    }
                });
    }

    public static class RegisterCptRetLogEventResponse {
        public Log log;

        public BigInteger retCode;

        public BigInteger cptId;

        public BigInteger cptVersion;
    }

    public static class UpdateCptRetLogEventResponse {
        public Log log;

        public BigInteger retCode;

        public BigInteger cptId;

        public BigInteger cptVersion;
    }

    public static class CredentialTemplateEventResponse {
        public Log log;

        public BigInteger cptId;

        public byte[] credentialPublicKey;

        public byte[] credentialProof;
    }
}
