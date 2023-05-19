package com.meca.did.controller;

import com.meca.did.constant.ErrorCode;
import com.meca.did.protocol.request.AddAuthenticationRequest;
import com.meca.did.protocol.request.AddPublicKeyRequest;
import com.meca.did.protocol.request.CreateDIDRequest;
import com.meca.did.protocol.request.RevokeAuthenticationRequest;
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
import com.meca.did.util.DataToolUtils;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import lombok.AllArgsConstructor;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.web.bind.annotation.*;
import org.web3j.crypto.ECKeyPair;
import org.web3j.crypto.Keys;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Api(tags = "DID")
@AllArgsConstructor
@CrossOrigin
@RestController
@ConditionalOnProperty(prefix = "is", name = "did.service")
@RequestMapping("api/v1/did")
public class DIDController {

    private static final Logger logger = LoggerFactory.getLogger(DIDController.class);

    private final DIDService dIDService;

    @ApiOperation(value = "Generate a new keypair for testing")
    @GetMapping("/genkey")
    public ResponseData<Map<String, String>> createKeyPair() {

        ECKeyPair keyPair;
        try {
            keyPair = Keys.createEcKeyPair();

        } catch (Exception e) {
            e.printStackTrace();
            return new ResponseData<>(null, ErrorCode.UNKNOW_ERROR);
        }
        HashMap<String, String> response = new HashMap<>();
        response.put("publicKey", String.valueOf(keyPair.getPublicKey()));
        response.put("privateKey", String.valueOf(keyPair.getPrivateKey()));

        return new ResponseData<>(response, ErrorCode.SUCCESS);
    }

    /**
     * create DID without parameters and call the settings property method.
     *
     * @return returns DID and public key
     */
    @ApiOperation(value = "Create a DID")
    @PostMapping("/create")
    public ResponseData<CreateDIDDataResult> createDID(
            @RequestBody CreateDIDRequest createDIDRequest) {

        ResponseData<CreateDIDDataResult> createDIDResult;
//        if (null == createDIDRequest) {
//            logger.info("begin create DID without parameter");
//            createDIDResult = dIDService.createDID();
//        } else {
        ErrorCode verifyPublicKey = DataToolUtils.verifyPublicKeyFormat(createDIDRequest.getPublicKey());
        if (verifyPublicKey != ErrorCode.SUCCESS) {
            return new ResponseData<>(null, ErrorCode.getTypeByErrorCode(verifyPublicKey.getCode()));
        }

        logger.info("begin create DID with supplied parameters");
        CreateDIDArgs createDIDArgs = new CreateDIDArgs();
        createDIDArgs.setDIDPublicKey(new DIDPublicKey());
        createDIDArgs.getDIDPublicKey().setPublicKey(createDIDRequest.getPublicKey());
        createDIDResult = dIDService.createDID(createDIDArgs);
//        }

        logger.info("createDIDAndSetAttr response:{}", createDIDResult);
        if (createDIDResult.getErrorCode() != ErrorCode.SUCCESS.getCode()) {
            return createDIDResult;
        }

        // 2, call set authentication
        ResponseData<Boolean> setAuthenticateRes = this.setAuthentication(createDIDResult.getResult());
        if (!setAuthenticateRes.getResult()) {
            createDIDResult.setErrorCode(
                    ErrorCode.getTypeByErrorCode(setAuthenticateRes.getErrorCode())
            );
            return createDIDResult;
        }

        // if DID is created successfully, save its private key.
//        PrivateKeyUtil.savePrivateKey(
//                PrivateKeyUtil.KEY_DIR,
//                createDIDResult.getResult().getDID(),
//                createDIDResult.getResult().getUserDIDPrivateKey().getPrivateKey()
//        );

//        createDIDResult.getResult().setDIDPrivateKey(null);
        return createDIDResult;
    }

    @ApiOperation(value = "Retrieve the number DID registered")
    @GetMapping("/count")
    public ResponseData<Integer> getDIDCount() {
        return dIDService.getDIDCount();
    }

    @ApiOperation(value = "Resolve DID Document")
    @GetMapping("/document/{DID}")
    public ResponseData<DIDDocument> getDIDDocument(
            @PathVariable String DID
    ) {
        return dIDService.getDIDDocument(DID);
    }

    @ApiOperation(value = "Resolve DID Document is JSON format")
    @GetMapping("/documentJson/{DID}")
    public ResponseData<String> getDIDDocumentJson(
            @PathVariable String DID
    ) {
        return dIDService.getDIDDocumentJson(DID);
    }

    @ApiOperation(value = "Retrieve the associated public key list from DID")
    @GetMapping("/publicKey/{DID}")
    public ResponseData<List<PublicKeyProperty>> getPublicKeyList(
            @PathVariable String DID
    ) {
        ResponseData<DIDDocument> dIDDocumentResult = getDIDDocument(DID);
        if (dIDDocumentResult.getErrorCode() != ErrorCode.SUCCESS.getCode()) {
            return new ResponseData<>(null,
                    ErrorCode.getTypeByErrorCode(dIDDocumentResult.getErrorCode()));
        }

        return new ResponseData<>(dIDDocumentResult.getResult().getPublicKey(), ErrorCode.SUCCESS);
    }

    @ApiOperation(value = "Add a new public key to DID")
    @PostMapping("/addPublicKey")
    public ResponseData<Integer> addPublicKey(
            @RequestBody AddPublicKeyRequest addPublicKeyRequest
    ) {
        if (null == addPublicKeyRequest
                || StringUtils.isBlank(addPublicKeyRequest.getDID())
                || StringUtils.isBlank(addPublicKeyRequest.getPublicKey())
                || StringUtils.isBlank(addPublicKeyRequest.getPrivateKey())) {
            return new ResponseData<>(null, ErrorCode.ILLEGAL_INPUT);
        }

        PublicKeyArgs publicKeyArgs = new PublicKeyArgs();
        publicKeyArgs.setPublicKey(addPublicKeyRequest.getPublicKey());

        DIDPrivateKey privateKeyArgs = new DIDPrivateKey();
        privateKeyArgs.setPrivateKey(addPublicKeyRequest.getPrivateKey());

        return dIDService.addPublicKey(
                addPublicKeyRequest.getDID(),
                publicKeyArgs,
                privateKeyArgs);
    }

    @ApiOperation(value = "Add a new authentication")
    @PostMapping("/addAuthentication")
    public ResponseData<Boolean> addAuthentication(
            @RequestBody AddAuthenticationRequest addAuthenticationRequest
    ) {
        if (null == addAuthenticationRequest
                || StringUtils.isBlank(addAuthenticationRequest.getDID())
                || StringUtils.isBlank(addAuthenticationRequest.getPublicKey())
                || StringUtils.isBlank(addAuthenticationRequest.getPrivateKey())) {
            return new ResponseData<>(null, ErrorCode.ILLEGAL_INPUT);
        }

        CreateDIDDataResult result = new CreateDIDDataResult();
        result.setDID(addAuthenticationRequest.getDID());
        result.setDIDPublicKey(new DIDPublicKey());
        result.getDIDPublicKey().setPublicKey(addAuthenticationRequest.getPublicKey());

        return this.setAuthentication(result);
    }

    @ApiOperation(value = "Revoke authentication")
    @PostMapping("/revokeAuthentication")
    public ResponseData<Boolean> revokeAuthentication(
            @RequestBody RevokeAuthenticationRequest revokeAuthenticationRequest
    ) {
        if (null == revokeAuthenticationRequest
                || StringUtils.isBlank(revokeAuthenticationRequest.getDID())
                || StringUtils.isBlank(revokeAuthenticationRequest.getPublicKey())
                || StringUtils.isBlank(revokeAuthenticationRequest.getPrivateKey())) {
            return new ResponseData<>(null, ErrorCode.ILLEGAL_INPUT);
        }

        AuthenticationArgs authenticationArgs = new AuthenticationArgs();
        authenticationArgs.setOwner(revokeAuthenticationRequest.getDID());
        authenticationArgs.setPublicKey(revokeAuthenticationRequest.getPublicKey());

        DIDPrivateKey privateKeyArgs = new DIDPrivateKey();
        privateKeyArgs.setPrivateKey(revokeAuthenticationRequest.getPrivateKey());

        return dIDService.revokeAuthentication(
                revokeAuthenticationRequest.getDID(),
                authenticationArgs,
                privateKeyArgs);
    }

    private ResponseData<Boolean> setAuthentication(CreateDIDDataResult createDIDDataResult) {

        AuthenticationArgs authenticationArgs = new AuthenticationArgs();
        authenticationArgs.setPublicKey(createDIDDataResult.getDIDPublicKey().getPublicKey());

        ResponseData<Boolean> setResponse = dIDService.setAuthentication(
                createDIDDataResult.getDID(),
                authenticationArgs);

        logger.info(
                "setAuthentication is result,errorCode:{},errorMessage:{}",
                setResponse.getErrorCode(),
                setResponse.getErrorMessage()
        );
        return setResponse;
    }
}