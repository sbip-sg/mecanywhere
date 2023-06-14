package com.meca.did.service.impl;

import com.meca.did.constant.DIDConstant;
import com.meca.did.constant.ErrorCode;
import com.meca.did.protocol.base.DIDDocument;
import com.meca.did.protocol.base.DIDPrivateKey;
import com.meca.did.protocol.base.DIDPublicKey;
import com.meca.did.protocol.base.PublicKeyProperty;
import com.meca.did.protocol.request.AuthenticationArgs;
import com.meca.did.protocol.request.CreateDIDArgs;
import com.meca.did.protocol.request.PublicKeyArgs;
import com.meca.did.protocol.response.CreateDIDDataResult;
import com.meca.did.protocol.response.ResponseData;
import com.meca.did.service.DIDService;
import com.meca.did.service.DIDServiceEngine;
import com.meca.did.util.DIDUtils;
import com.meca.did.util.DataToolUtils;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.AllArgsConstructor;
import org.apache.commons.lang3.StringUtils;
import org.apache.commons.lang3.math.NumberUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.web3j.crypto.ECKeyPair;
import org.web3j.crypto.Keys;

import java.util.List;

@AllArgsConstructor
@Service
public class DIDServiceImpl implements DIDService {
    /**
     * log4j object, for recording log.
     */
    private static final Logger logger = LoggerFactory.getLogger(DIDServiceImpl.class);

    private final DIDServiceEngine dIDServiceEngine;

    @Override
    public ResponseData<CreateDIDDataResult> createDID() {
        CreateDIDDataResult result = new CreateDIDDataResult();
        ECKeyPair keyPair;
        try {
            keyPair = Keys.createEcKeyPair();
        } catch (Exception e) {
            logger.error("Create DID failed.");
            return new ResponseData<>(null, ErrorCode.DID_KEYPAIR_CREATE_FAILED);
        }

        logger.info("Generated public key {}\n, private key {}", keyPair.getPublicKey(), keyPair.getPrivateKey());

        String publicKey = String.valueOf(keyPair.getPublicKey());
        String privateKey = String.valueOf(keyPair.getPrivateKey());
        DIDPublicKey userDIDPublicKey = new DIDPublicKey();
        userDIDPublicKey.setPublicKey(publicKey);
        result.setDIDPublicKey(userDIDPublicKey);
        DIDPrivateKey userDIDPrivateKey = new DIDPrivateKey();
        userDIDPrivateKey.setPrivateKey(privateKey);
        result.setDIDPrivateKey(userDIDPrivateKey);
        String DID = DIDUtils.convertPublicKeyToDID(publicKey);
        result.setDID(DID);

        logger.info("Generated DID {}", DID);

        ResponseData<Boolean> innerResp = processCreateDID(DID, publicKey);
        if (innerResp.getErrorCode() != ErrorCode.SUCCESS.getCode()) {
            logger.error(
                    "[createDID] Create DID failed. error message is :{}",
                    innerResp.getErrorMessage()
            );
            return new ResponseData<>(null,
                    ErrorCode.getTypeByErrorCode(innerResp.getErrorCode()),
                    innerResp.getTransactionInfo());
        }
        return new ResponseData<>(result, ErrorCode.getTypeByErrorCode(innerResp.getErrorCode()),
                innerResp.getTransactionInfo());
    }

    /**
     * Create a DID.
     *
     * @param createDIDArgs the creation DID args
     * @return the response data
     */
    @Override
    public ResponseData<CreateDIDDataResult> createDID(CreateDIDArgs createDIDArgs) {
        CreateDIDDataResult result = new CreateDIDDataResult();

        if (createDIDArgs == null) {
            logger.error("[createDID]: input parameter createDIDArgs is null.");
            return new ResponseData<>(null, ErrorCode.ILLEGAL_INPUT);
        }

        String publicKey = createDIDArgs.getDIDPublicKey().getPublicKey();
        result.setDIDPublicKey(createDIDArgs.getDIDPublicKey());
        if (StringUtils.isNotBlank(publicKey)) {
            String DID = DIDUtils.convertPublicKeyToDID(publicKey);
            result.setDID(DID);
            ResponseData<Boolean> DIDExistsResp = this.dIDExists(DID);
            logger.info(DID);
            if (DIDExistsResp.getResult() == null || DIDExistsResp.getResult()) {
                logger
                        .error("[createDID]: create DID failed, the DID :{} already exists", DID);
                return new ResponseData<>(null, ErrorCode.DID_ALREADY_EXIST);
            }
            ResponseData<Boolean> innerResp = processCreateDID(DID, publicKey);
            if (innerResp.getErrorCode() != ErrorCode.SUCCESS.getCode()) {
                logger.error(
                        "[createDID]: create DID failed. error message is :{}, public key is {}",
                        innerResp.getErrorMessage(),
                        publicKey
                );
                return new ResponseData<>(
                        null,
                        ErrorCode.getTypeByErrorCode(innerResp.getErrorCode()),
                        innerResp.getTransactionInfo());
            }
            return new ResponseData<>(
                    result,
                    ErrorCode.getTypeByErrorCode(innerResp.getErrorCode()),
                    innerResp.getTransactionInfo());
        } else {
            return new ResponseData<>(null, ErrorCode.DID_PUBLICKEY_INVALID);
        }
    }

    private ResponseData<Boolean> processCreateDID(
            String dID,
            String publicKey) {

        String address = DIDUtils.convertDIDToAddress(dID);
        return dIDServiceEngine.createDID(address, publicKey);
    }

    @Override
    public ResponseData<Boolean> setAuthentication(
            String dID,
            AuthenticationArgs authenticationArgs) {
        if (!verifyAuthenticationArgs(authenticationArgs)) {
            logger.error("[setAuthentication]: input parameter setAuthenticationArgs is illegal.");
            return new ResponseData<>(false, ErrorCode.ILLEGAL_INPUT);
        }
//        if (!DIDUtils.isPrivateKeyValid(privateKey)) {
//            return new ResponseData<>(false, ErrorCode.DID_PRIVATEKEY_INVALID);
//        }
        return processSetAuthentication(
                authenticationArgs.getOwner(),
                authenticationArgs.getPublicKey(),
                dID);
    }

    private ResponseData<Boolean> processSetAuthentication(
            String owner,
            String publicKey,
            String dID) {
        if (DIDUtils.isDIDValid(dID)) {
            ResponseData<Boolean> DIDExistsResp = this.dIDExists(dID);
            if (DIDExistsResp.getResult() == null || !DIDExistsResp.getResult()) {
                logger.error("[setAuthentication]: failed, the DID :{} does not exist",
                        dID);
                return new ResponseData<>(false, ErrorCode.DID_DOES_NOT_EXIST);
            }

            // TODO check this DID document that this pubkey MUST exist first

            String DIDAddress = DIDUtils.convertDIDToAddress(dID);
            if (StringUtils.isEmpty(owner)) {
                owner = DIDAddress;
            } else {
                if (DIDUtils.isDIDValid(owner)) {
                    owner = DIDUtils.convertDIDToAddress(owner);
                } else {
                    logger.error("[setAuthentication]: owner : {} is invalid.", owner);
                    return new ResponseData<>(false, ErrorCode.DID_INVALID);
                }
            }
            try {
                String attrValue = new StringBuffer()
                        .append(publicKey)
                        .append(DIDConstant.SEPARATOR)
                        .append(owner)
                        .toString();
                logger.info("Calling engine to setAttribute\n Prefix {}, attrValue {}", DIDConstant.DID_DOC_AUTHENTICATE_PREFIX, attrValue);
                return dIDServiceEngine
                        .setAttribute(DIDAddress,
                                DIDConstant.DID_DOC_AUTHENTICATE_PREFIX,
                                attrValue);
            } catch (Exception e) {
                logger.error("Set authenticate failed. Error message :{}", e.toString());
                return new ResponseData<>(false, ErrorCode.UNKNOW_ERROR);
            }
        } else {
            logger.error("Set authenticate failed. DID : {} is invalid.", dID);
            return new ResponseData<>(false, ErrorCode.DID_INVALID);
        }
    }

    private boolean verifyPublicKeyArgs(PublicKeyArgs publicKeyArgs) {

        return !(publicKeyArgs == null
                || publicKeyArgs.getType() == null
                || StringUtils.isEmpty(publicKeyArgs.getType().getTypeName())
                || StringUtils.isEmpty(publicKeyArgs.getPublicKey())
                || !(isPublicKeyStringValid(publicKeyArgs.getPublicKey())));
    }

    private boolean verifyAuthenticationArgs(AuthenticationArgs authenticationArgs) {

        return !(authenticationArgs == null
                || StringUtils.isEmpty(authenticationArgs.getPublicKey())
                || !(isPublicKeyStringValid(authenticationArgs.getPublicKey())));
    }

    private boolean isPublicKeyStringValid(String pubKey) {
        // Allow base64, rsa (alphaNum) and bigInt
        return (DataToolUtils.isValidBase64String(pubKey)
                || StringUtils.isAlphanumeric(pubKey)
                || NumberUtils.isDigits(pubKey));
    }

    /**
     * Check if DID exists on Chain.
     *
     * @param dID the DID
     * @return true if exists, false otherwise
     */
    @Override
    public ResponseData<Boolean> dIDExists(String dID) {
        if (!DIDUtils.isDIDValid(dID)) {
            logger.error("[didExists] check DID failed. DID : {} is invalid.", dID);
            return new ResponseData<>(false, ErrorCode.DID_INVALID);
        }
        return dIDServiceEngine.DIDExists(dID);
    }

    @Override
    public ResponseData<DIDDocument> getDIDDocument(String dID) {
        if (!DIDUtils.isDIDValid(dID)) {
            logger.error("Input DID : {} is invalid.", dID);
            return new ResponseData<>(null, ErrorCode.DID_INVALID);
        }
        return dIDServiceEngine.getDIDDocument(dID);
    }

    /**
     * Get a DID Document Json.
     *
     * @param dID the DID
     * @return the DID document json
     */
    @Override
    public ResponseData<String> getDIDDocumentJson(String dID) {

        ResponseData<DIDDocument> responseData = this.getDIDDocument(dID);
        DIDDocument result = responseData.getResult();

        if (result == null) {
            return new ResponseData<>(
                    StringUtils.EMPTY,
                    ErrorCode.getTypeByErrorCode(responseData.getErrorCode())
            );
        }
        ObjectMapper mapper = new ObjectMapper();
        String dIDDocument;
        try {
            dIDDocument = mapper.writerWithDefaultPrettyPrinter().writeValueAsString(result);
        } catch (Exception e) {
            logger.error("write object to String fail.", e);
            return new ResponseData<>(
                    StringUtils.EMPTY,
                    ErrorCode.getTypeByErrorCode(responseData.getErrorCode())
            );
        }
        dIDDocument =
                new StringBuffer()
                        .append(dIDDocument)
                        .insert(1, DIDConstant.DID_DOC_PROTOCOL_VERSION)
                        .toString();

        ResponseData<String> responseDataJson = new ResponseData<String>();
        responseDataJson.setResult(dIDDocument);
        responseDataJson.setErrorCode(ErrorCode.getTypeByErrorCode(responseData.getErrorCode()));

        return responseDataJson;
    }

    /**
     * Remove a public key enlisted in DID document together with the its authentication.
     *
     * @param dID           the DID to delete public key from
     * @param publicKeyArgs the public key args
     * @param privateKey    the private key to send blockchain transaction
     * @return true if succeeds, false otherwise
     */
    @Override
    public ResponseData<Boolean> revokePublicKeyWithAuthentication(
            String dID,
            PublicKeyArgs publicKeyArgs,
            DIDPrivateKey privateKey) {
        if (!verifyPublicKeyArgs(publicKeyArgs)) {
            logger.error("[removePublicKey]: input parameter setPublicKeyArgs is illegal.");
            return new ResponseData<>(false, ErrorCode.ILLEGAL_INPUT);
        }
        if (!DIDUtils.isPrivateKeyValid(privateKey)) {
            return new ResponseData<>(false, ErrorCode.DID_PRIVATEKEY_INVALID);
        }

        // TODO check this DID document that this pubkey MUST exist first
        String removedPubKeyToDID = DIDUtils
                .convertPublicKeyToDID(publicKeyArgs.getPublicKey());
        if (removedPubKeyToDID.equalsIgnoreCase(dID)) {
            logger.error("Cannot remove the owning public key of this DID: {}", dID);
            return new ResponseData<>(false,
                    ErrorCode.DID_CANNOT_REMOVE_ITS_OWN_PUB_KEY_WITHOUT_BACKUP);
        }
        ResponseData<DIDDocument> responseData = this.getDIDDocument(dID);
        if (responseData.getResult() == null) {
            return new ResponseData<>(false,
                    ErrorCode.getTypeByErrorCode(responseData.getErrorCode())
            );
        }
        List<PublicKeyProperty> publicKeys = responseData.getResult().getPublicKey();
        for (PublicKeyProperty pk : publicKeys) {
            if (pk.getPublicKey().equalsIgnoreCase(publicKeyArgs.getPublicKey())) {
                if (publicKeys.size() == 1) {
                    logger.error("Cannot remove the last public key of this DID: {}", dID);
                    return new ResponseData<>(false,
                            ErrorCode.DID_CANNOT_REMOVE_ITS_OWN_PUB_KEY_WITHOUT_BACKUP);
                }
            }
        }

        // Add correct tag by externally call revokeAuthentication once
        AuthenticationArgs authenticationArgs = new AuthenticationArgs();
        authenticationArgs.setPublicKey(publicKeyArgs.getPublicKey());
        authenticationArgs.setOwner(publicKeyArgs.getOwner());
        ResponseData<Boolean> removeAuthResp = this.revokeAuthentication(
                dID, authenticationArgs, privateKey);
        if (!removeAuthResp.getResult()) {
            logger.error("Failed to remove authentication: " + removeAuthResp.getErrorMessage());
            return removeAuthResp;
        }

        String owner = publicKeyArgs.getOwner();
        String dIDAddress = DIDUtils.convertDIDToAddress(dID);

        if (StringUtils.isEmpty(owner)) {
            owner = dIDAddress;
        } else {
            if (DIDUtils.isDIDValid(owner)) {
                owner = DIDUtils.convertDIDToAddress(owner);
            } else {
                logger.error("removePublicKey: owner : {} is invalid.", owner);
                return new ResponseData<>(false, ErrorCode.DID_INVALID);
            }
        }
        try {
            String attributeKey =
                    new StringBuffer()
                            .append(DIDConstant.DID_DOC_PUBLICKEY_PREFIX)
                            .append("/")
                            .append(publicKeyArgs.getType())
                            .append("/")
                            .append("base64")
                            .toString();
            String publicKey = publicKeyArgs.getPublicKey();
            String attrValue = new StringBuffer()
                    .append(publicKey)
                    .append(DIDConstant.REMOVED_PUBKEY_TAG).append(DIDConstant.SEPARATOR)
                    .append(owner)
                    .toString();
            return dIDServiceEngine.setAttribute(
                    dIDAddress,
                    attributeKey,
                    attrValue);
        } catch (Exception e) {
            logger.error("[removePublicKey] set PublicKey failed with exception. ", e);
            return new ResponseData<>(false, ErrorCode.UNKNOW_ERROR);
        }
    }

    /**
     * Remove an authentication tag in document only - will not affect its public key.
     *
     * @param dID                the DID to remove auth from
     * @param authenticationArgs A public key is needed
     * @param privateKey         the private key
     * @return true if succeeds, false otherwise
     */
    @Override
    public ResponseData<Boolean> revokeAuthentication(
            String dID,
            AuthenticationArgs authenticationArgs,
            DIDPrivateKey privateKey) {

        if (!verifyAuthenticationArgs(authenticationArgs)) {
            logger
                    .error("[revokeAuthentication]: input parameter setAuthenticationArgs is illegal.");
            return new ResponseData<>(false, ErrorCode.ILLEGAL_INPUT);
        }
        if (!DIDUtils.isPrivateKeyValid(privateKey)) {
            return new ResponseData<>(false, ErrorCode.DID_PRIVATEKEY_INVALID);
        }
        if (DIDUtils.isDIDValid(dID)) {
            ResponseData<Boolean> dIDExistsResp = this.dIDExists(dID);
            if (dIDExistsResp.getResult() == null || !dIDExistsResp.getResult()) {
                logger.error("[SetAuthentication]: failed, the DID :{} does not exist", dID);
                return new ResponseData<>(false, ErrorCode.DID_DOES_NOT_EXIST);
            }
            String dIDAddress = DIDUtils.convertDIDToAddress(dID);

            String owner = authenticationArgs.getOwner();
            if (StringUtils.isEmpty(owner)) {
                owner = dIDAddress;
            } else {
                if (DIDUtils.isDIDValid(owner)) {
                    owner = DIDUtils.convertDIDToAddress(owner);
                } else {
                    logger.error("[revokeAuthentication]: owner : {} is invalid.", owner);
                    return new ResponseData<>(false, ErrorCode.DID_INVALID);
                }
            }
            try {
                String attrValue = new StringBuffer()
                        .append(authenticationArgs.getPublicKey())
                        .append(DIDConstant.REMOVED_AUTHENTICATION_TAG)
                        .append(DIDConstant.SEPARATOR)
                        .append(owner)
                        .toString();
                return dIDServiceEngine
                        .setAttribute(dIDAddress,
                                DIDConstant.DID_DOC_AUTHENTICATE_PREFIX,
                                attrValue);
            } catch (Exception e) {
                logger.error("remove authenticate failed. Error message :{}", e);
                return new ResponseData<>(false, ErrorCode.UNKNOW_ERROR);
            }
        } else {
            logger.error("Set authenticate failed. DID: {} is invalid.", dID);
            return new ResponseData<>(false, ErrorCode.DID_INVALID);
        }
    }

    /**
     * Add a public key in the DID Document. If this key is already revoked, then it will
     * be un-revoked.
     *
     * @param dID           the DID to add public key to
     * @param publicKeyArgs the public key args
     * @param privateKey    the private key to send blockchain transaction
     * @return the public key ID, -1 if any error occurred
     */
    @Override
    public ResponseData<Integer> addPublicKey(
            String dID,
            PublicKeyArgs publicKeyArgs,
            DIDPrivateKey privateKey) {

        if (!verifyPublicKeyArgs(publicKeyArgs)) {
            logger.error("[addPublicKey]: input parameter setPublicKeyArgs is illegal.");
            return new ResponseData<>(DIDConstant.ADD_PUBKEY_FAILURE_CODE,
                    ErrorCode.ILLEGAL_INPUT);
        }
        if (!DIDUtils.isPrivateKeyValid(privateKey)) {
            return new ResponseData<>(DIDConstant.ADD_PUBKEY_FAILURE_CODE,
                    ErrorCode.DID_PRIVATEKEY_INVALID);
        }

        String dIDAddress = DIDUtils.convertDIDToAddress(dID);
        if (StringUtils.isEmpty(dIDAddress)) {
            logger.error("addPublicKey: dID : {} is invalid.", dID);
            return new ResponseData<>(DIDConstant.ADD_PUBKEY_FAILURE_CODE, ErrorCode.DID_INVALID);
        }
        ResponseData<DIDDocument> dIDDocResp = this.getDIDDocument(dID);
        if (dIDDocResp.getResult() == null) {
            logger.error("Failed to fetch DID document for DID: {}", dID);
            return new ResponseData<>(DIDConstant.ADD_PUBKEY_FAILURE_CODE,
                    ErrorCode.CREDENTIAL_DID_DOCUMENT_ILLEGAL);
        }
        String owner = publicKeyArgs.getOwner();
        if (StringUtils.isEmpty(owner)) {
            owner = dIDAddress;
        } else {
            if (DIDUtils.isDIDValid(owner)) {
                owner = DIDUtils.convertDIDToAddress(owner);
            } else {
                logger.error("addPublicKey: owner : {} is invalid.", owner);
                return new ResponseData<>(DIDConstant.ADD_PUBKEY_FAILURE_CODE,
                        ErrorCode.DID_INVALID);
            }
        }
        String pubKey = publicKeyArgs.getPublicKey();
        int currentPubKeyId = dIDDocResp.getResult().getPublicKey().size();
        for (PublicKeyProperty pkp : dIDDocResp.getResult().getPublicKey()) {
            if (pkp.getPublicKey().equalsIgnoreCase(pubKey)) {
                if (pkp.getRevoked()) {
                    currentPubKeyId = Integer
                            .valueOf(pkp.getId().substring(pkp.getId().length() - 1));
                    logger.info("Updating revocation for DID {}, ID: {}", dID, currentPubKeyId);
                } else {
                    // Already exists and is not revoked, hence return "already exists" error
                    return new ResponseData<>(DIDConstant.ADD_PUBKEY_FAILURE_CODE,
                            ErrorCode.DID_PUBLIC_KEY_ALREADY_EXISTS);
                }
            }
        }
        ResponseData<Boolean> processResp = processSetPubKey(
                publicKeyArgs.getType().getTypeName(),
                dIDAddress,
                owner,
                pubKey,
                privateKey.getPrivateKey());
        if (!processResp.getResult()) {
            return new ResponseData<>(DIDConstant.ADD_PUBKEY_FAILURE_CODE,
                    processResp.getErrorCode(), processResp.getErrorMessage());
        } else {
            return new ResponseData<>(currentPubKeyId, ErrorCode.SUCCESS);
        }
    }

    private ResponseData<Boolean> processSetPubKey(
            String type,
            String dIDAddress,
            String owner,
            String pubKey,
            String privateKey) {

        try {
            String attributeKey =
                    new StringBuffer()
                            .append(DIDConstant.DID_DOC_PUBLICKEY_PREFIX)
                            .append("/")
                            .append(type)
                            .append("/")
                            .append("base64")
                            .toString();
            String attrValue = new StringBuffer().append(pubKey).append(DIDConstant.SEPARATOR)
                    .append(owner).toString();
            return dIDServiceEngine.setAttribute(
                    dIDAddress,
                    attributeKey,
                    attrValue);
        } catch (Exception e) {
            logger.error("[addPublicKey] set PublicKey failed with exception. ", e);
            return new ResponseData<>(false, ErrorCode.UNKNOW_ERROR);
        }
    }

    @Override
    public ResponseData<Integer> getDIDCount() {
        return dIDServiceEngine.getDIDCount();
    }
}
