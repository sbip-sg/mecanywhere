package com.meca.did.protocol.request;

import io.swagger.annotations.ApiModelProperty;
import lombok.Data;

import com.meca.did.protocol.base.CredentialPojo;

@Data
public class VerifyCredentialRequest {
    @ApiModelProperty(name = "credential", value = "Credential to be verified", required = true)
    private CredentialPojo credential;
}
