package com.meca.did.protocol.base;

import lombok.Data;

@Data
public class DIDBaseInfo {
    /**
     * Required: The id.
     */
    private String id;

    /**
     * Required: The created.
     */
    private Long created;
}
