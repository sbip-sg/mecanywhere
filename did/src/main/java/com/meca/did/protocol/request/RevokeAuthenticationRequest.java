package com.meca.did.protocol.request;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;

@Data
public class RevokeAuthenticationRequest {
    @JsonProperty("did")
    @ApiModelProperty(name = "DID", value = "DID to revoke authentication", example = "did:meca:0xfd340b5a30de452ae4a14dd1b92a7006868a29c8")
    private String dID;

    @ApiModelProperty(name = "Public key", value = "Public key", example = "\"12631759105999171451791452024899331347269411458337823904541697524484130520609380076684470728201027024563915823414135841187434152195100531039430833242820131\"")
    private String publicKey;

    @ApiModelProperty(name = "Private key", value = "Private key", example = "\"52877417529601665148217697683806210340993170902477981602240988772358952044134\"")
    private String privateKey;
}
