package com.meca.did.controller;

import com.meca.did.constant.ErrorCode;
import com.meca.did.protocol.base.CredentialPojo;
import com.meca.did.protocol.base.PresentationPojo;
import com.meca.did.protocol.request.VerifyCredentialRequest;
import com.meca.did.protocol.request.VerifyPresentationRequest;
import com.meca.did.protocol.response.ResponseData;
import com.meca.did.service.CredentialPojoService;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;
import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.web.bind.annotation.*;

@Api(tags = "Verifier")
@AllArgsConstructor
@CrossOrigin
@RestController
@ConditionalOnProperty(prefix = "is", name = "verifier")
@RequestMapping("api/v1/credential")
public class VerifierController {

    private static final Logger logger = LoggerFactory.getLogger(VerifierController.class);

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
            CredentialPojo credential = verifyCredentialRequest.getCredential();
            return credentialPojoService.verifyCredential(credential.getIssuer(), credential);
        } catch (Exception e) {
            logger.error("verifyCredential error", e);
            return new ResponseData<>(null, ErrorCode.TRANSACTION_EXECUTE_ERROR);
        }
    }

    @ApiOperation(value = "Verify a verifiable presentation")
    @PostMapping("/verifyVP")
    public ResponseData<Boolean> verifyPresentation(
            @ApiParam(name = "verifyPresentationRequest", value = "Presentation to be verified")
            @RequestBody VerifyPresentationRequest verifyPresentationRequest) {

        logger.info("verifyVPModel:{}", verifyPresentationRequest);

        if (null == verifyPresentationRequest) {
            return new ResponseData<>(null, ErrorCode.ILLEGAL_INPUT);
        }

        try {
            PresentationPojo presentation = verifyPresentationRequest.getPresentation();
            return credentialPojoService.verifyPresentation(presentation);
        } catch (Exception e) {
            logger.error("verifyPresentation error", e);
            return new ResponseData<>(null, ErrorCode.TRANSACTION_EXECUTE_ERROR);
        }
    }
}
