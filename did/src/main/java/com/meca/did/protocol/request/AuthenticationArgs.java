package com.meca.did.protocol.request;

import lombok.Data;

@Data
public class AuthenticationArgs {

    /**
     * Required: The owner.
     */
    private String owner;

    /**
     * Required: The public key.
     */
    private String publicKey;

}
