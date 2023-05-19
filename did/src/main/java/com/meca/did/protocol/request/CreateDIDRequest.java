package com.meca.did.protocol.request;

import io.swagger.annotations.ApiModelProperty;
import lombok.Data;

@Data
public class CreateDIDRequest {
    @ApiModelProperty(name = "Public key", value = "Public key", example = "\"12631759105999171451791452024899331347269411458337823904541697524484130520609380076684470728201027024563915823414135841187434152195100531039430833242820131\"")
    private String publicKey;
}


