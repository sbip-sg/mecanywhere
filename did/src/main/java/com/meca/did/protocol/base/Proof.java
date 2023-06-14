package com.meca.did.protocol.base;

import java.util.Map;

import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
@AllArgsConstructor
public class Proof {
    @ApiModelProperty(example = "Secp256k1")
    private String type;

    @ApiModelProperty(example = "1685412359")
    private Long created;

    @ApiModelProperty(example = "did:meca:0x52c328ef8b382b1d71cc262b868d803a137ab8d8")
    private String creator;

    @ApiModelProperty(example = "{\n"
            + "\"gender\": \"cXLBz\",\n"
            + "\"name\": \"hjusY\",\n"
            + "\"DID\": \"GA4Of\",\n"
            + "\"age\": \"1cgTm\"\n"
            + "}")
    private Map<String, Object> salt;

    @ApiModelProperty(example = "abVirKd3ZvGpJ20BR72SCkb18K/o4ZZT9BqDDU6W8lVv12ttuIfM3s9SAs5RbVJ4M3OrssB6DQ1Mj/YLi8Eq7Rw=")
    private String signatureValue;
}
