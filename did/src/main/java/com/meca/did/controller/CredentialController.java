package com.meca.did.controller;

import com.meca.did.constant.CredentialType;
import com.meca.did.constant.ErrorCode;
import com.meca.did.protocol.base.CredentialPojo;
import com.meca.did.protocol.base.DIDAuthentication;
import com.meca.did.protocol.base.DIDPrivateKey;
import com.meca.did.protocol.request.CreateCredentialPojoArgs;
import com.meca.did.protocol.request.CreateCredentialRequest;
import com.meca.did.protocol.request.VerifyCredentialRequest;
import com.meca.did.protocol.response.ResponseData;
import com.meca.did.service.CredentialPojoService;
import com.meca.did.util.DataToolUtils;
import com.meca.did.util.PrivateKeyUtil;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;
import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

@Api(tags = "Credential")
@AllArgsConstructor
@CrossOrigin
@RestController
@ConditionalOnProperty(prefix = "is", name = "issuer")
@RequestMapping("api/v1/credential")
public class CredentialController {

    private static final Logger logger = LoggerFactory.getLogger(CredentialController.class);

    private static final long EXPIRATION_DATE = 1000L * 60 * 60 * 24 * 365 * 100;

    private final CredentialPojoService credentialPojoService;

    @ApiOperation(value = "Verify a credential")
    @PostMapping("/verify")
    public ResponseData<Boolean> verifyCredential(
            @ApiParam(name = "verifyCredentialRequest", value = "Credential to be verified")
            @RequestBody VerifyCredentialRequest verifyCredentialRequest) {

        logger.info("verifyCredentialModel:{}", verifyCredentialRequest);

        if (null == verifyCredentialRequest) {
            return new ResponseData<>(null, ErrorCode.ILLEGAL_INPUT);
        }
        // call method to verifyEvidence credential.
        try {
            CredentialPojo credential = DataToolUtils.deserialize(
                    DataToolUtils.mapToCompactJson(verifyCredentialRequest.getCredential()),
                    CredentialPojo.class);
            return credentialPojoService.verify(credential.getIssuer(), credential);
        } catch (Exception e) {
            logger.error("verifyCredential error", e);
            return new ResponseData<>(null, ErrorCode.TRANSACTION_EXECUTE_ERROR);
        }
    }

    /**
     * institutional publication of Credential.
     *
     * @return returns  credential
     * @throws IOException it's possible to throw an exception
     */
    @ApiOperation(value = "Create a credential")
    @PostMapping("/create")
    public ResponseData<CredentialPojo> createCredential(
            @ApiParam(name = "createCredentialRequest", value = "Specify the issuer DID and claim to be issued")
            @RequestBody CreateCredentialRequest createCredentialRequest) {

        try {

            if (null == createCredentialRequest) {
                return new ResponseData<>(null, ErrorCode.ILLEGAL_INPUT);
            }
            // getting cptId data.
            Integer cptId = createCredentialRequest.getCptId();
            // getting issuer data.
            String issuer = createCredentialRequest.getIssuer();
            // getting claimData data.
            String claimData = DataToolUtils.mapToCompactJson(createCredentialRequest.getClaimData());

            // get the private key from the file according to DID.
            String privateKey = PrivateKeyUtil.getPrivateKeyByDID(PrivateKeyUtil.KEY_DIR, issuer);
            logger.info(
                    "param,issuer:{},privateKey:{},claimData:{}",
                    issuer,
                    privateKey,
                    claimData
            );

            // converting claimData in JSON format to map.
            Map<String, Object> claimDataMap = new HashMap<String, Object>();
            claimDataMap =
                    (Map<String, Object>) DataToolUtils.deserialize(
                            claimData,
                            claimDataMap.getClass()
                    );

            // call method to create credentials.
            // build createCredential parameters.
            CreateCredentialPojoArgs<Map<String, Object>> args = new CreateCredentialPojoArgs<>();
            args.setCptId(cptId);
            args.setIssuer(issuer);
            args.setType(CredentialType.ORIGINAL);
            args.setClaim(claimDataMap);
            // the validity period is 360 days
            args.setExpirationDate(System.currentTimeMillis() + EXPIRATION_DATE);

            DIDAuthentication dIDAuthentication = new DIDAuthentication();
            dIDAuthentication.setDIDPrivateKey(new DIDPrivateKey());
            dIDAuthentication.getDIDPrivateKey().setPrivateKey(privateKey);
            dIDAuthentication.setDID(issuer);
            dIDAuthentication.setDIDPublicKeyId(issuer);
            args.setDIDAuthentication(dIDAuthentication);

            return credentialPojoService.createCredential(args);
        } catch (Exception e) {
            logger.error("createCredential error", e);
            return new ResponseData<CredentialPojo>(null, ErrorCode.CREDENTIAL_ERROR);
        }
    }

}
