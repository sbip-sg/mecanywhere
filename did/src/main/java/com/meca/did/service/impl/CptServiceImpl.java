package com.meca.did.service.impl;

import com.meca.did.constant.DIDConstant;
import com.meca.did.constant.ErrorCode;
import com.meca.did.protocol.base.Cpt;
import com.meca.did.protocol.base.CptBaseInfo;
import com.meca.did.protocol.base.DIDAuthentication;
import com.meca.did.protocol.base.DIDPrivateKey;
import com.meca.did.protocol.request.CptMapArgs;
import com.meca.did.protocol.request.CptStringArgs;
import com.meca.did.protocol.response.ResponseData;
import com.meca.did.protocol.response.RsvSignature;
import com.meca.did.service.CptService;
import com.meca.did.service.CptServiceEngine;
import com.meca.did.util.DIDUtils;
import com.meca.did.util.DataToolUtils;
import lombok.AllArgsConstructor;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.web3j.crypto.Sign.SignatureData;

import java.math.BigInteger;
import java.util.Map;

@AllArgsConstructor
@Service
public class CptServiceImpl implements CptService {

    private static final Logger logger = LoggerFactory.getLogger(CptServiceImpl.class);

    private final CptServiceEngine cptServiceEngine;

    @Override
    public ResponseData<CptBaseInfo> registerCpt(CptMapArgs args) {
        try {
            if (args == null) {
                logger.error("[registerCpt]input CptMapArgs is null");
                return new ResponseData<>(null, ErrorCode.ILLEGAL_INPUT);
            }
            ErrorCode validateResult =
                    this.validateCptArgs(
                            args.getDIDAuthentication(),
                            args.getCptJsonSchema()
                    );

            if (validateResult.getCode() != ErrorCode.SUCCESS.getCode()) {
                return new ResponseData<>(null, validateResult);
            }

            String dID = args.getDIDAuthentication().getDID();
            DIDPrivateKey dIDPrivateKey = args.getDIDAuthentication().getDIDPrivateKey();
            String cptJsonSchemaNew = DataToolUtils.cptSchemaToString(args);
            RsvSignature rsvSignature = sign(
                    dID,
                    cptJsonSchemaNew,
                    dIDPrivateKey);
            String address = DIDUtils.convertDIDToAddress(dID);
            return cptServiceEngine.registerCpt(address, cptJsonSchemaNew, rsvSignature,
                    dIDPrivateKey.getPrivateKey(), DIDConstant.CPT_DATA_INDEX);
        } catch (Exception e) {
            logger.error("[registerCpt] register cpt failed due to unknown error. ", e);
            return new ResponseData<>(null, ErrorCode.UNKNOW_ERROR);
        }
    }

    @Override
    public ResponseData<CptBaseInfo> registerCpt(CptMapArgs args, Integer cptId) {
        return null;
    }

    @Override
    public ResponseData<CptBaseInfo> registerCpt(CptStringArgs args) {
        return null;
    }

    @Override
    public ResponseData<CptBaseInfo> registerCpt(CptStringArgs args, Integer cptId) {
        return null;
    }

    @Override
    public ResponseData<Cpt> queryCpt(Integer cptId) {
        try {
            if (cptId == null || cptId < 0) {
                return new ResponseData<>(null, ErrorCode.CPT_ID_ILLEGAL);
            }
            ResponseData<Cpt> result;
            result = cptServiceEngine.queryCpt(cptId, DIDConstant.CPT_DATA_INDEX);
            return result;
        } catch (Exception e) {
            logger.error("[updateCpt] query cpt failed due to unknown error. ", e);
            return new ResponseData<>(null, ErrorCode.UNKNOW_ERROR);
        }
    }


    private RsvSignature sign(
            String cptPublisher,
            String jsonSchema,
            DIDPrivateKey cptPublisherPrivateKey) {

        StringBuilder sb = new StringBuilder();
        sb.append(cptPublisher);
        sb.append(DIDConstant.PIPELINE);
        sb.append(jsonSchema);
        SignatureData signatureData = DataToolUtils.secp256k1SignToSignature(
                sb.toString(), new BigInteger(cptPublisherPrivateKey.getPrivateKey().trim()));
        return DataToolUtils.convertSignatureDataToRsv(signatureData);
    }

    private ErrorCode validateCptArgs(
            DIDAuthentication dIDAuthentication,
            Map<String, Object> cptJsonSchemaMap) throws Exception {

        if (dIDAuthentication == null) {
            logger.error("Input cpt dIDAuthentication is invalid.");
            return ErrorCode.DID_AUTHORITY_INVALID;
        }

        String dID = dIDAuthentication.getDID();
        if (!DIDUtils.isDIDValid(dID)) {
            logger.error("Input cpt publisher : {} is invalid.", dID);
            return ErrorCode.DID_INVALID;
        }

        ErrorCode errorCode = validateCptJsonSchemaMap(cptJsonSchemaMap);
        if (errorCode.getCode() != ErrorCode.SUCCESS.getCode()) {
            return errorCode;
        }
        String cptJsonSchema = DataToolUtils.serialize(cptJsonSchemaMap);
        if (!DataToolUtils.isCptJsonSchemaValid(cptJsonSchema)) {
            logger.error("Input cpt json schema : {} is invalid.", cptJsonSchemaMap);
            return ErrorCode.CPT_JSON_SCHEMA_INVALID;
        }
        DIDPrivateKey dIDPrivateKey = dIDAuthentication.getDIDPrivateKey();
        if (dIDPrivateKey == null
                || StringUtils.isEmpty(dIDPrivateKey.getPrivateKey())) {
            logger.error(
                    "Input cpt publisher private key : {} is in valid.",
                    dIDPrivateKey
            );
            return ErrorCode.DID_PRIVATEKEY_INVALID;
        }

        logger.info(dIDPrivateKey.toString());
        logger.info(dID);
        if (!DIDUtils.validatePrivateKeyDIDMatches(dIDPrivateKey, dID)) {
            return ErrorCode.DID_PRIVATEKEY_DOES_NOT_MATCH;
        }
        return ErrorCode.SUCCESS;
    }

    private ErrorCode validateCptJsonSchemaMap(
            Map<String, Object> cptJsonSchemaMap) throws Exception {
        if (cptJsonSchemaMap == null || cptJsonSchemaMap.isEmpty()) {
            logger.error("Input cpt json schema is invalid.");
            return ErrorCode.CPT_JSON_SCHEMA_INVALID;
        }
        //String cptJsonSchema = JsonUtil.objToJsonStr(cptJsonSchemaMap);
        String cptJsonSchema = DataToolUtils.serialize(cptJsonSchemaMap);
        if (!DataToolUtils.isCptJsonSchemaValid(cptJsonSchema)) {
            logger.error("Input cpt json schema : {} is invalid.", cptJsonSchemaMap);
            return ErrorCode.CPT_JSON_SCHEMA_INVALID;
        }
        return ErrorCode.SUCCESS;
    }
}
