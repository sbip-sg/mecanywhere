package com.meca.did.util;

import com.meca.did.constant.CredentialConstant;
import com.meca.did.constant.ErrorCode;
import com.meca.did.constant.ParamKeyConstant;
import com.meca.did.protocol.base.CredentialPojo;
import com.meca.did.protocol.base.DIDAuthentication;
import com.meca.did.protocol.request.CreateCredentialPojoArgs;
import org.apache.commons.collections4.CollectionUtils;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;

public class CredentialPojoUtils {

    private static final Logger logger = LoggerFactory.getLogger(CredentialPojoUtils.class);

    /**
     * Concat all fields of Credential info, without Signature, in Json format. This should be
     * invoked when calculating Credential Signature. Return null if credential format is illegal.
     * Note that: 1. Keys should be dict-ordered; 2. Claim should use standard getClaimHash() to
     * support selective disclosure; 3. Use compact output to avoid Json format confusion.
     *
     * @param credential target Credential object
     * @param salt Salt Map
     * @param disclosures Disclosure Map
     * @return Hash value in String.
     */
    public static String getCredentialThumbprintWithoutSig(
            CredentialPojo credential,
            Map<String, Object> salt,
            Map<String, Object> disclosures) {
        try {
            Map<String, Object> credMap = DataToolUtils.objToMap(credential);
            // Preserve the same behavior as in CredentialUtils - will merge later
            credMap.remove(ParamKeyConstant.PROOF);
            credMap.put(ParamKeyConstant.CLAIM, getClaimHash(credential, salt, disclosures));
            return DataToolUtils.mapToCompactJson(credMap);
        } catch (Exception e) {
            logger.error("get Credential Thumbprint WithoutSig error.", e);
            return StringUtils.EMPTY;
        }
    }

    /**
     * Check the given CredentialPojo validity based on its input params.
     *
     * @param args CredentialPojo
     * @return true if yes, false otherwise
     */
    public static ErrorCode isCredentialPojoValid(CredentialPojo args) {
        if (args == null) {
            return ErrorCode.ILLEGAL_INPUT;
        }
        if (!DIDUtils.isDIDValid(args.getIssuer())) {
            return ErrorCode.CREDENTIAL_ISSUER_INVALID;
        }
        if (args.getClaim() == null) {
            return ErrorCode.CREDENTIAL_CLAIM_NOT_EXISTS;
        }
        if (args.getIssuanceDate() == null) {
            return ErrorCode.CREDENTIAL_ISSUANCE_DATE_ILLEGAL;
        }
        ErrorCode errorCode = validDateExpired(args.getIssuanceDate(), args.getExpirationDate());
        if (errorCode.getCode() != ErrorCode.SUCCESS.getCode()) {
            return errorCode;
        }
        ErrorCode contentResponseData = isCredentialContentValid(args);
        if (ErrorCode.SUCCESS.getCode() != contentResponseData.getCode()) {
            return contentResponseData;
        }
        return ErrorCode.SUCCESS;
    }

    private static ErrorCode validDateExpired(Long issuanceDate, Long expirationDate) {
        if (issuanceDate != null && issuanceDate <= 0) {
            return ErrorCode.CREDENTIAL_ISSUANCE_DATE_ILLEGAL;
        }
        if (expirationDate == null
                || expirationDate.longValue() < 0
                || expirationDate.longValue() == 0) {
            return ErrorCode.CREDENTIAL_EXPIRE_DATE_ILLEGAL;
        }
        if (!DateUtils.isAfterCurrentTime(expirationDate)) {
            return ErrorCode.CREDENTIAL_EXPIRED;
        }
        if (issuanceDate != null && expirationDate < issuanceDate) {
            return ErrorCode.CREDENTIAL_ISSUANCE_DATE_ILLEGAL;
        }
        return ErrorCode.SUCCESS;
    }

    /**
     * Check the given CredentialPojo content fields validity excluding metadata, based on its
     * input.
     *
     * @param args CredentialPojo
     * @return true if yes, false otherwise
     */
    private static ErrorCode isCredentialContentValid(CredentialPojo args) {
        String credentialId = args.getId();
        if (StringUtils.isEmpty(credentialId) || !CredentialUtils.isValidUuid(credentialId)) {
            return ErrorCode.CREDENTIAL_ID_NOT_EXISTS;
        }
        String context = args.getContext();
        if (StringUtils.isEmpty(context)) {
            return ErrorCode.CREDENTIAL_CONTEXT_NOT_EXISTS;
        }
        if (CollectionUtils.isEmpty(args.getType())) {
            return ErrorCode.CREDENTIAL_TYPE_IS_NULL;
        }
        Map<String, Object> proof = args.getProof();
        return isCredentialProofValid(proof);
    }

    private static ErrorCode isCredentialProofValid(Map<String, Object> proof) {
        if (proof == null) {
            return ErrorCode.ILLEGAL_INPUT;
        }

        String type = null;
        if (proof.get(ParamKeyConstant.PROOF_TYPE) == null) {
            return ErrorCode.CREDENTIAL_SIGNATURE_TYPE_ILLEGAL;
        } else {
            type = String.valueOf(proof.get(ParamKeyConstant.PROOF_TYPE));
            if (!isCredentialProofTypeValid(type)) {
                return ErrorCode.CREDENTIAL_SIGNATURE_TYPE_ILLEGAL;
            }
        }
        // Created is not obligatory
        if (proof.get(ParamKeyConstant.PROOF_CREATED) == null) {
            return ErrorCode.CREDENTIAL_ISSUANCE_DATE_ILLEGAL;
        } else {
            Long created = Long.valueOf(String.valueOf(proof.get(ParamKeyConstant.PROOF_CREATED)));
            if (created.longValue() <= 0) {
                return ErrorCode.CREDENTIAL_ISSUANCE_DATE_ILLEGAL;
            }
        }
        // Creator is not obligatory either
        if (proof.get(ParamKeyConstant.PROOF_CREATOR) == null) {
            return ErrorCode.CREDENTIAL_ISSUER_INVALID;
        } else {
            String creator = String.valueOf(proof.get(ParamKeyConstant.PROOF_CREATOR));
            //if (!StringUtils.isEmpty(creator) && !WeIdUtils.isWeIdValid(creator)) {
            if (StringUtils.isEmpty(creator)) {
                return ErrorCode.CREDENTIAL_ISSUER_INVALID;
            }
        }
        // If the Proof type is ECDSA or other signature based scheme, check signature
        if (type.equalsIgnoreCase(CredentialConstant.CredentialProofType.ECDSA.getTypeName())) {
            if (proof.get(ParamKeyConstant.PROOF_SIGNATURE) == null) {
                return ErrorCode.CREDENTIAL_SIGNATURE_BROKEN;
            } else {
                String signature = String.valueOf(proof.get(ParamKeyConstant.PROOF_SIGNATURE));
                if (StringUtils.isEmpty(signature)
                        || !DataToolUtils.isValidBase64String(signature)) {
                    return ErrorCode.CREDENTIAL_SIGNATURE_BROKEN;
                }
            }
        }
        return ErrorCode.SUCCESS;
    }

    private static boolean isCredentialProofTypeValid(String type) {
        // Proof type must be one of the pre-defined types.
        if (!StringUtils.isEmpty(type)) {
            for (CredentialConstant.CredentialProofType proofType : CredentialConstant.CredentialProofType.values()) {
                if (StringUtils.equalsIgnoreCase(type, proofType.getTypeName())) {
                    return true;
                }
            }
        }
        return false;
    }

    /**
     * valid claim and salt.
     *
     * @param claim claimMap
     * @param salt saltMap
     * @return boolean
     */
    public static boolean validClaimAndSaltForMap(
            Map<String, Object> claim,
            Map<String, Object> salt) {
        //检查是否为空
        if (claim == null || salt == null) {
            return false;
        }
        //检查每个map里的key个数是否相同
        Set<String> claimKeys = claim.keySet();
        Set<String> saltKeys = salt.keySet();
        if (claimKeys.size() != saltKeys.size()) {
            return false;
        }
        //检查key值是否一致
        for (Map.Entry<String, Object> entry : claim.entrySet()) {
            String k = entry.getKey();
            Object claimV = entry.getValue();
            Object saltV = salt.get(k);
            if (!salt.containsKey(k)) {
                return false;
            }
            if (claimV instanceof Map) {
                //递归检查
                if (!validClaimAndSaltForMap((HashMap) claimV, (HashMap) saltV)) {
                    return false;
                }
            } else if (claimV instanceof List) {
                ArrayList<Object> claimValue = (ArrayList<Object>) claimV;
                if (saltV instanceof ArrayList) {
                    ArrayList<Object> saltValue = (ArrayList<Object>) saltV;
                    if (!validClaimAndSaltForList(claimValue, saltValue)) {
                        return false;
                    }
                } else {
                    continue;
                }
            }
        }
        return true;
    }

    private static boolean validClaimAndSaltForList(
            List<Object> claimList,
            List<Object> saltList) {
        //检查是否为空
        if (claimList == null || saltList == null) {
            return false;
        }
        for (int i = 0; i < claimList.size(); i++) {
            Object claimObj = claimList.get(i);
            Object saltObj = saltList.get(i);
            if (claimObj instanceof Map) {
                if (!(saltObj instanceof Map)) {
                    return false;
                }
                if (!validClaimAndSaltForMap((HashMap) claimObj, (HashMap) saltObj)) {
                    return false;
                }
            } else if (claimObj instanceof List) {
                if (!(saltObj instanceof List)) {
                    return false;
                }
                ArrayList<Object> claimObjV = (ArrayList<Object>) claimObj;
                ArrayList<Object> saltObjV = (ArrayList<Object>) saltObj;
                if (!validClaimAndSaltForList(claimObjV, saltObjV)) {
                    return false;
                }
            }
        }
        return true;
    }

    /**
     * Create a full lite CredentialPojo Hash for a Credential based on all its fields.
     *
     * @param credentialPojo target Credential object
     * @return Hash value in String.
     */
    public static String getLiteCredentialPojoHash(CredentialPojo credentialPojo) {

        try {
            Map<String, Object> credMap = DataToolUtils.objToMap(credentialPojo);
            credMap.remove(ParamKeyConstant.CONTEXT);
            credMap.put(ParamKeyConstant.PROOF_TYPE, "lite1");
            credMap.remove(ParamKeyConstant.PROOF);
            String signature = credentialPojo.getSignature();
            credMap.put(ParamKeyConstant.PROOF, signature);
            credMap.put(ParamKeyConstant.CLAIM, getLiteClaimHash(credentialPojo));
            String rawData = DataToolUtils.mapToCompactJson(credMap);
            //System.out.println("LiteCredential's Pre-Hash for evidence: " + rawData);
            return DataToolUtils.sha3(rawData);
        } catch (Exception e) {
            logger.error("get Credential Thumbprint error.", e);
            return StringUtils.EMPTY;
        }
    }

    /**
     * Get the lite credential claim hash.
     *
     * @param credential Credential
     * @return the claimMap value
     */
    public static Map<String, Object> getLiteClaimHash(
            CredentialPojo credential) {

        Map<String, Object> claim = credential.getClaim();
        return DataToolUtils.clone((HashMap) claim);
    }

    /**
     * Create a full CredentialPojo Hash for a Credential based on all its fields, which is
     * resistant to selective disclosure.
     *
     * @param credentialPojo target Credential object
     * @param disclosures Disclosure Map
     * @return Hash value in String.
     */
    public static String getCredentialPojoHash(CredentialPojo credentialPojo,
                                               Map<String, Object> disclosures) {
        String rawData = getCredentialPojoRawDataWithProofWithoutSalt(
                credentialPojo,
                credentialPojo.getSalt(),
                disclosures);
        if (StringUtils.isEmpty(rawData)) {
            return StringUtils.EMPTY;
        }
        // System.out.println(rawData);
        return DataToolUtils.sha3(rawData);
    }

    /**
     * Concat all fields of Credential info, with signature. This should be invoked when calculating
     * Credential Evidence. Return null if credential format is illegal.
     *
     * @param credential target Credential object
     * @param salt Salt Map
     * @param disclosures Disclosure Map
     * @return Hash value in String.
     */
    private static String getCredentialPojoRawDataWithProofWithoutSalt(
            CredentialPojo credential,
            Map<String, Object> salt,
            Map<String, Object> disclosures
    ) {
        try {
            Map<String, Object> credMap = DataToolUtils.objToMap(credential);
            // Replace the Claim value object with claim hash value to preserve immutability
            credMap.put(ParamKeyConstant.CLAIM, getClaimHash(credential, salt, disclosures));
            // Remove the whole Salt field to preserve immutability
            Map<String, Object> proof = (Map<String, Object>) credMap.get(ParamKeyConstant.PROOF);
            proof.remove(ParamKeyConstant.PROOF_SALT);
            proof.put(ParamKeyConstant.PROOF_SALT, null);
            credMap.remove(ParamKeyConstant.PROOF);
            credMap.put(ParamKeyConstant.PROOF, proof);
            return DataToolUtils.mapToCompactJson(credMap);
        } catch (Exception e) {
            logger.error("get Credential Thumbprint error.", e);
            return StringUtils.EMPTY;
        }
    }

    /**
     * Get the claim hash. This is irrelevant to selective disclosure.
     *
     * @param credential Credential
     * @param salt Salt Map
     * @param disclosures Disclosure Map
     * @return the claimMap value
     */
    public static Map<String, Object> getClaimHash(
            CredentialPojo credential,
            Map<String, Object> salt,
            Map<String, Object> disclosures
    ) {

        Map<String, Object> claim = credential.getClaim();
        Map<String, Object> newClaim = DataToolUtils.clone((HashMap) claim);
        addSaltAndGetHash(newClaim, salt, disclosures);
        return newClaim;
    }

    private static void addSaltAndGetHash(
            Map<String, Object> claim,
            Map<String, Object> salt,
            Map<String, Object> disclosures
    ) {
        for (Map.Entry<String, Object> entry : salt.entrySet()) {
            String key = entry.getKey();
            Object disclosureObj = null;
            if (disclosures != null) {
                disclosureObj = disclosures.get(key);
            }
            Object saltObj = salt.get(key);
            Object newClaimObj = claim.get(key);

            if (saltObj instanceof Map) {
                addSaltAndGetHash(
                        (HashMap) newClaimObj,
                        (HashMap) saltObj,
                        (HashMap) disclosureObj
                );
            } else if (saltObj instanceof List) {
                ArrayList<Object> disclosureObjList = null;
                if (disclosureObj != null) {
                    disclosureObjList = (ArrayList<Object>) disclosureObj;
                }
                addSaltAndGetHashForList(
                        (ArrayList<Object>) newClaimObj,
                        (ArrayList<Object>) saltObj,
                        disclosureObjList
                );
            }
        }
    }

    private static void addSaltAndGetHashForList(
            List<Object> claim,
            List<Object> salt,
            List<Object> disclosures
    ) {
        for (int i = 0; claim != null && i < claim.size(); i++) {
            Object obj = claim.get(i);
            Object saltObj = salt.get(i);
            if (obj instanceof Map) {
                Object disclosureObj = null;
                if (disclosures != null) {
                    disclosureObj = disclosures.get(0);
                }
                addSaltAndGetHash((HashMap) obj, (HashMap) saltObj, (HashMap) disclosureObj);
            } else if (obj instanceof List) {
                ArrayList<Object> disclosureObjList = null;
                if (disclosures != null) {
                    Object disclosureObj = disclosures.get(i);
                    if (disclosureObj != null) {
                        disclosureObjList = (ArrayList<Object>) disclosureObj;
                    }
                }
                addSaltAndGetHashForList(
                        (ArrayList<Object>) obj,
                        (ArrayList<Object>) saltObj,
                        disclosureObjList
                );
            }
        }
    }

    /**
     * Get per-field salted hash value.
     *
     * @param field the field value
     * @param salt the salt value
     * @return the hash value
     */
    public static String getFieldSaltHash(String field, String salt) {
        return DataToolUtils.sha3(String.valueOf(field) + String.valueOf(salt));
    }

    /**
     * Check the given CreateCredentialPojoArgs validity based on its input params.
     *
     * @param args CreateCredentialPojoArgs
     * @return true if yes, false otherwise
     */
    public static ErrorCode isCreateCredentialPojoArgsValid(
            CreateCredentialPojoArgs args) {
        if (args == null) {
            return ErrorCode.ILLEGAL_INPUT;
        }
        if (!DIDUtils.isDIDValid(args.getIssuer())) {
            return ErrorCode.CREDENTIAL_ISSUER_INVALID;
        }

        if (args.getClaim() == null) {
            return ErrorCode.CREDENTIAL_CLAIM_NOT_EXISTS;
        }
        ErrorCode errorCode = validDateExpired(args.getIssuanceDate(), args.getExpirationDate());
        if (errorCode.getCode() != ErrorCode.SUCCESS.getCode()) {
            return errorCode;
        }
        if (args.getDIDAuthentication() != null
                && !StringUtils.isEmpty(args.getDIDAuthentication().getDID())
                && !args.getDIDAuthentication().getDID().equalsIgnoreCase(args.getIssuer())) {
            return ErrorCode.CREDENTIAL_ISSUER_INVALID;
        }
        return isDIDAuthenticationValid(args.getDIDAuthentication());
    }

    /**
     * Check DIDAuthentication validity.
     *
     * @param callerAuth DIDAuthentication
     * @return true if yes, false otherwise
     */
    public static ErrorCode isDIDAuthenticationValid(DIDAuthentication callerAuth) {
        if (callerAuth == null
                || callerAuth.getDIDPrivateKey() == null
                || StringUtils.isBlank(callerAuth.getDIDPrivateKey().getPrivateKey())
                || StringUtils.isBlank(callerAuth.getDIDPublicKeyId())) {
            return ErrorCode.ILLEGAL_INPUT;
        }
        if (!DIDUtils.isDIDValid(callerAuth.getDID())) {
            return ErrorCode.DID_INVALID;
        }
        return ErrorCode.SUCCESS;
    }
}
