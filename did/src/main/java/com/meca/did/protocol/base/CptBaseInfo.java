package com.meca.did.protocol.base;

import lombok.Data;

@Data
public class CptBaseInfo {
    /**
     * Required: The id for the CPT.
     */
    private Integer cptId;

    /**
     * Required: The version of the CPT for the same CPT id.
     */
    private Integer cptVersion;
}
