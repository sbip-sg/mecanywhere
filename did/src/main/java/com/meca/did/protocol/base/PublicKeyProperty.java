package com.meca.did.protocol.base;

import lombok.Data;

@Data
public class PublicKeyProperty {

    /**
     * Required: The id.
     */
    private String id;

    /**
     * Required: The type.
     */
    private String type;

    /**
     * Required: The owner.
     */
    private String owner;

    /**
     * Required: The public key.
     */
    private String publicKey;

    /**
     * Required: Revoked or not.
     */
    private Boolean revoked = false;
}
