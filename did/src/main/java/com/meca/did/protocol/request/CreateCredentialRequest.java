package com.meca.did.protocol.request;

import io.swagger.annotations.ApiModelProperty;
import lombok.Data;

import java.util.Map;

@Data
public class CreateCredentialRequest {
    @ApiModelProperty(name = "issuer", value = "the DID issuer", required = true,
        example = "did:meca:0xfd340b5a30de452ae4a14dd1b92a7006868a29c8")
    private String issuer;

    @ApiModelProperty(name = "cptId", value = "CPT", required = true,
            example = "1001")
    private Integer cptId;

    @ApiModelProperty(name = "claimData", value = "claim to be issued", required = true,
            example = "{\n"
                    + "    \n"
                    + "    \"DID\": did:meca:0x0fa21fd3d11d2cd5e6cdef2c7cd6531a25a5964f,\n"
                    + "    \"name\": \"Chai\",\n"
                    + "    \"gender\": \"M\"\n"
                    + "}")
    private Map<String, Object> claimData;
}
