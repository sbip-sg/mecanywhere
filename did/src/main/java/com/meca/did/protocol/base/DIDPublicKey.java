package com.meca.did.protocol.base;

import lombok.Data;


@Data
public class DIDPublicKey {

    /**
     * Required: The public key.
     */
    private String publicKey;
}
