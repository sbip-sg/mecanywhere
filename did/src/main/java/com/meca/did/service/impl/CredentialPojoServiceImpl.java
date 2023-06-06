package com.meca.did.service.impl;

import com.meca.did.constant.CredentialConstant;
import com.meca.did.constant.ErrorCode;
import com.meca.did.constant.ParamKeyConstant;
import com.meca.did.protocol.base.Cpt;
import com.meca.did.protocol.base.CredentialPojo;
import com.meca.did.protocol.base.DIDDocument;
import com.meca.did.protocol.base.PresentationPojo;
import com.meca.did.protocol.base.Proof;
import com.meca.did.protocol.response.ResponseData;
import com.meca.did.protocol.request.CreateCredentialPojoArgs;
import com.meca.did.service.CptService;
import com.meca.did.service.CredentialPojoService;
import com.meca.did.service.DIDService;
import com.meca.did.util.CredentialPojoUtils;
import com.meca.did.util.CredentialUtils;
import com.meca.did.util.DataToolUtils;
import com.meca.did.util.DateUtils;
import com.github.fge.jsonschema.core.report.ProcessingReport;
import lombok.AllArgsConstructor;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.math.BigInteger;
import java.util.*;

@AllArgsConstructor
@Service
public class CredentialPojoServiceImpl implements CredentialPojoService {

    private static final Logger logger = LoggerFactory.getLogger(CredentialPojoServiceImpl.class);

    private final DIDService didService;
    private final CptService cptService;

    @Override
    public ResponseData<CredentialPojo> createCredential(CreateCredentialPojoArgs args) {
        try {
            ErrorCode innerResponseData =
                    CredentialPojoUtils.isCreateCredentialPojoArgsValid(args);
            if (ErrorCode.SUCCESS.getCode() != innerResponseData.getCode()) {
                logger.error("Create Credential Args illegal: {}",
                        innerResponseData.getCodeDesc());
                return new ResponseData<>(null, innerResponseData);
            }

            ResponseData<Boolean> dIDExists = didService.dIDExists(args.getIssuer());
            if (!dIDExists.getResult()) {
                return new ResponseData<>(null, ErrorCode.CREDENTIAL_ISSUER_NOT_EXISTS);
            }

            CredentialPojo result = new CredentialPojo();
            String context = CredentialUtils.getDefaultCredentialContext();
            result.setContext(context);
            if (StringUtils.isBlank(args.getId())) {
                result.setId(UUID.randomUUID().toString());
            } else {
                result.setId(args.getId());
            }
            result.setCptId(args.getCptId());
            Long issuanceDate = args.getIssuanceDate();
            if (issuanceDate == null) {
                result.setIssuanceDate(DateUtils.getNoMillisecondTimeStamp());
            } else {
                Long newIssuanceDate =
                        DateUtils.convertToNoMillisecondTimeStamp(args.getIssuanceDate());
                if (newIssuanceDate == null) {
                    logger.error("Create Credential Args illegal.");
                    return new ResponseData<>(null, ErrorCode.CREDENTIAL_ISSUANCE_DATE_ILLEGAL);
                } else {
                    result.setIssuanceDate(newIssuanceDate);
                }
            }
            // Comment these lines out since we now support multi-public-keys in WeID document
            // if (!WeIdUtils.validatePrivateKeyWeIdMatches(
            //     args.getWeIdAuthentication().getWeIdPrivateKey(),
            //     args.getIssuer())) {
            //     logger.error("Create Credential, private key does not match the current weid.");
            //     return new ResponseData<>(null, ErrorCode.WEID_PRIVATEKEY_DOES_NOT_MATCH);
            // }
            result.setIssuer(args.getIssuer());
            Long newExpirationDate =
                    DateUtils.convertToNoMillisecondTimeStamp(args.getExpirationDate());
            if (newExpirationDate == null) {
                logger.error("Create Credential Args illegal.");
                return new ResponseData<>(null, ErrorCode.CREDENTIAL_EXPIRE_DATE_ILLEGAL);
            } else {
                result.setExpirationDate(newExpirationDate);
            }
            result.addType(CredentialConstant.DEFAULT_CREDENTIAL_TYPE);
            result.addType(args.getType().getName());

            Object claimObject = args.getClaim();
            String claimStr = null;
            if (!(claimObject instanceof String)) {
                claimStr = DataToolUtils.serialize(claimObject);
            } else {
                claimStr = (String) claimObject;
            }

            HashMap<String, Object> claimMap = (HashMap<String, Object>) DataToolUtils.deserialize(claimStr, HashMap.class);
            result.setClaim(claimMap);

            String privateKey = args.getDIDAuthentication().getDIDPrivateKey().getPrivateKey().trim();
//            if (StringUtils.equals(args.getType().getName(), CredentialType.LITE1.getName())) {
//                return createLiteCredential(result, privateKey);
//            }

            Map<String, Object> saltMap = DataToolUtils.clone(claimMap);
            generateSalt(saltMap, null);
            String rawData = CredentialPojoUtils
                    .getCredentialThumbprintWithoutSig(result, saltMap, null);

            String signature = DataToolUtils.secp256k1Sign(rawData, new BigInteger(privateKey));

            result.putProofValue(ParamKeyConstant.PROOF_CREATED, result.getIssuanceDate());

            String DIDPublicKeyId = args.getDIDAuthentication().getDIDPublicKeyId();
            result.putProofValue(ParamKeyConstant.PROOF_CREATOR, DIDPublicKeyId);

            String proofType = CredentialConstant.CredentialProofType.ECDSA.getTypeName();
            result.putProofValue(ParamKeyConstant.PROOF_TYPE, proofType);
            result.putProofValue(ParamKeyConstant.PROOF_SIGNATURE, signature);
            result.setSalt(saltMap);
            ResponseData<CredentialPojo> responseData = new ResponseData<>(
                    result,
                    ErrorCode.SUCCESS
            );

            return responseData;
        } catch (Exception e) {
            logger.error("Generate Credential failed due to system error. ", e);
            return new ResponseData<>(null, ErrorCode.CREDENTIAL_ERROR);
        }
    }

    /**
     * Salt generator. Automatically fillin the map structure in a recursive manner.
     *
     * @param map   the passed map (claim, salt or alike)
     * @param fixed fixed value if required to use
     */
    public static void generateSalt(Map<String, Object> map, Object fixed) {
        for (Map.Entry<String, Object> entry : map.entrySet()) {
            Object value = entry.getValue();
            if (value instanceof Map) {
                generateSalt((HashMap<String, Object>) value, fixed);
            } else if (value instanceof List) {
                boolean isMapOrList = generateSaltFromList((ArrayList<Object>) value, fixed);
                if (!isMapOrList) {
                    if (fixed == null) {
                        addSalt(entry);
                    } else {
                        entry.setValue(fixed);
                    }
                }
            } else {
                if (fixed == null) {
                    addSalt(entry);
                } else {
                    entry.setValue(fixed);
                }
            }
        }
    }

    private static void addSalt(Map.Entry<String, Object> entry) {
        String salt = DataToolUtils.getRandomSalt();
        entry.setValue(salt);
    }

    private static boolean generateSaltFromList(List<Object> objList, Object fixed) {
        List<Object> list = objList;
        for (Object obj : list) {
            if (obj instanceof Map) {
                generateSalt((HashMap) obj, fixed);
            } else if (obj instanceof List) {
                boolean result = generateSaltFromList((ArrayList<Object>) obj, fixed);
                if (!result) {
                    return result;
                }
            } else {
                return false;
            }
        }
        return true;
    }

    @Override
    public ResponseData<Boolean> verifyCredential(String issuerDID, CredentialPojo credential) {
        if (credential == null) {
            logger.error("[verify] The input credential is invalid.");
            return new ResponseData<Boolean>(false, ErrorCode.ILLEGAL_INPUT);
        }

        String issuerId = credential.getIssuer();
        if (!StringUtils.equals(issuerDID, issuerId)) {
            logger.error("[verify] The input issuer DID does not match the credential's DID.");
            return new ResponseData<Boolean>(false, ErrorCode.CREDENTIAL_ISSUER_MISMATCH);
        }
//        if (CredentialPojoUtils.isLiteCredential(credential)) {
//            return verifyLiteCredential(credential, null, null);
//        }
        ErrorCode errorCode = verifyCredentialContent(credential, null, null);
        if (errorCode.getCode() != ErrorCode.SUCCESS.getCode()) {
            logger.error("[verify] credential verify failed. error message :{}", errorCode);
            return new ResponseData<Boolean>(false, errorCode);
        }
        return new ResponseData<Boolean>(true, ErrorCode.SUCCESS);
    }

    private ErrorCode verifyCredentialContent(
            CredentialPojo credential,
            String publicKey,
            String DIDPublicKeyId
    ) {
        ErrorCode checkResp = CredentialPojoUtils.isCredentialPojoValid(credential);
        if (ErrorCode.SUCCESS.getCode() != checkResp.getCode()) {
            return checkResp;
        }
        return verifySingleSignedCredential(credential, publicKey, DIDPublicKeyId);
    }

    private ErrorCode verifySingleSignedCredential(
            CredentialPojo credential,
            String publicKey,
            String DIDPublicKeyId
    ) {
        ErrorCode errorCode = verifyCptFormat(
                credential.getCptId(),
                credential.getClaim(),
                false,
                false
        );
        if (ErrorCode.SUCCESS.getCode() != errorCode.getCode()) {
            return errorCode;
        }
        Map<String, Object> salt = credential.getSalt();
        String thumbprint = CredentialPojoUtils.getCredentialThumbprintWithoutSig(credential, salt, null);
        String signature = credential.getSignature();
        String dIdIssuer = credential.getIssuer();
        if (StringUtils.isEmpty(publicKey)) {
            return verifyProofWithDID(DIDPublicKeyId, dIdIssuer, thumbprint, signature);
        }
        return verifyProofWithPublicKey(DIDPublicKeyId, thumbprint, signature);
    }

    private ErrorCode verifyProofWithDID(String DIDPublicKeyId, String proverDID, String thumbprint, String signature) {
        // Fetch public key from chain
        ResponseData<DIDDocument> innerResponseData =
                didService.getDIDDocument(proverDID);
        if (innerResponseData.getErrorCode() != ErrorCode.SUCCESS.getCode()) {
            logger.error(
                    "Error occurred when fetching DID document for: {}, msg: {}",
                    proverDID, innerResponseData.getErrorMessage());
            if (innerResponseData.getErrorCode() == ErrorCode.DID_DOES_NOT_EXIST.getCode()) {
                return ErrorCode.CREDENTIAL_ISSUER_NOT_EXISTS;
            }
            return ErrorCode.getTypeByErrorCode(innerResponseData.getErrorCode());
        }

        DIDDocument DIDDocument = innerResponseData.getResult();
        return DataToolUtils.verifySecp256k1SignatureFromDID(
                thumbprint, signature, DIDDocument, DIDPublicKeyId);
    }
    
    private ErrorCode verifyProofWithPublicKey(String publicKey, String thumbprint, String signature) {
        boolean result;
        try {
            result = DataToolUtils.verifySecp256k1Signature(thumbprint,
                    signature, new BigInteger(publicKey));

        } catch (Exception e) {
            logger.error("[verifyContent] verify signature fail.", e);
            return ErrorCode.CREDENTIAL_SIGNATURE_BROKEN;
        }
        if (!result) {
            return ErrorCode.CREDENTIAL_VERIFY_FAIL;
        }
        return ErrorCode.SUCCESS;
    }

    private ErrorCode verifyCptFormat(
            Integer cptId, Map<String, Object> claim,
            boolean isSelectivelyDisclosed,
            boolean offline
    ) {
        if (cptId == CredentialConstant.CREDENTIALPOJO_EMBEDDED_SIGNATURE_CPT.intValue()) {
            if (!claim.containsKey("credentialList")) {
                return ErrorCode.CREDENTIAL_CLAIM_DATA_ILLEGAL;
            } else {
                return ErrorCode.SUCCESS;
            }
        }
        if (cptId == CredentialConstant.EMBEDDED_TIMESTAMP_CPT.intValue()) {
            if (claim.containsKey("credentialList") && claim.containsKey("claimHash")
                    && claim.containsKey("timestampAuthority") && claim.containsKey("timestamp")
                    && claim.containsKey("authoritySignature")) {
                return ErrorCode.SUCCESS;
            } else {
                return ErrorCode.CREDENTIAL_CLAIM_DATA_ILLEGAL;
            }
        }
        try {
            if (offline) {
                return ErrorCode.SUCCESS;
            }
            String claimStr = DataToolUtils.serialize(claim);
            Cpt cpt = cptService.queryCpt(cptId).getResult();
            if (cpt == null) {
                logger.error(ErrorCode.CREDENTIAL_CPT_NOT_EXISTS.getCodeDesc());
                return ErrorCode.CREDENTIAL_CPT_NOT_EXISTS;
            }
            //String cptJsonSchema = JsonUtil.objToJsonStr(cpt.getCptJsonSchema());
            String cptJsonSchema = DataToolUtils.serialize(cpt.getCptJsonSchema());

            if (!DataToolUtils.isCptJsonSchemaValid(cptJsonSchema)) {
                logger.error(ErrorCode.CPT_JSON_SCHEMA_INVALID.getCodeDesc());
                return ErrorCode.CPT_JSON_SCHEMA_INVALID;
            }
            if (!isSelectivelyDisclosed) {
                ProcessingReport checkRes = DataToolUtils.checkJsonVersusSchema(
                        claimStr, cptJsonSchema);
                if (!checkRes.isSuccess()) {
                    logger.error(ErrorCode.CREDENTIAL_CLAIM_DATA_ILLEGAL.getCodeDesc());
                    return ErrorCode.CREDENTIAL_CLAIM_DATA_ILLEGAL;
                }
            }
            return ErrorCode.SUCCESS;
        } catch (Exception e) {
            logger.error(
                    "Generic error occurred during verify cpt format when verifyCredential: ", e);
            return ErrorCode.CREDENTIAL_ERROR;
        }
    }

    @Override
    public ResponseData<Boolean> verifyPresentation(PresentationPojo presentation) {
        if (presentation == null) {
            logger.error("[verifyPresentation] The input presentation is invalid.");
            return new ResponseData<Boolean>(false, ErrorCode.ILLEGAL_INPUT);
        }
        
        String thumbprint;
        try {
            Map<String, Object> map = DataToolUtils.objToMap(presentation);
            map.remove("proof");
            thumbprint = DataToolUtils.mapToCompactJson(map);
        } catch (Exception e) {
            logger.error("[verifyPresentation] The thumbprint is invalid.");
            return new ResponseData<Boolean>(false, ErrorCode.ILLEGAL_INPUT);
        }
        
        String signature = presentation.getProof().getSignatureValue();
        ErrorCode errorCode = verifyProofWithDID(null, presentation.getHolder(), thumbprint, signature);
        if (errorCode.getCode() != ErrorCode.SUCCESS.getCode()) {
            logger.error("[verifyPresentation] presentation verify failed. error message :{}", errorCode);
            return new ResponseData<Boolean>(false, errorCode);
        }
        
        CredentialPojo credential = presentation.getVc();
        return verifyCredential(credential.getIssuer(), credential);
    }

}
