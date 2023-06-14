package com.meca.did.protocol.request;

import io.swagger.annotations.ApiModelProperty;
import lombok.Data;

import com.meca.did.protocol.base.PresentationPojo;

@Data
public class VerifyPresentationRequest {
    @ApiModelProperty(name = "presentation", value = "Presentation to be verified", required = true)
    private PresentationPojo presentation;
}
