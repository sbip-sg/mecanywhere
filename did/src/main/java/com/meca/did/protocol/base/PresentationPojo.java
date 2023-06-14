package com.meca.did.protocol.base;

import io.swagger.annotations.ApiModelProperty;
import lombok.Data;

@Data
public class PresentationPojo {
    @ApiModelProperty(example = "1")
    private String id;

    @ApiModelProperty(example = "did:meca:0x0fa21fd3d11d2cd5e6cdef2c7cd6531a25a5964f")
    private String holder;

    @ApiModelProperty(example = "VerifiablePresentation")
    private String type;

    private CredentialPojo vc;

    private Proof proof;
}
