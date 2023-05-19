package com.meca.did.protocol.request;

import com.meca.did.constant.DIDConstant;
import lombok.Data;

@Data
public class PublicKeyArgs {

    /**
     * Required: The type.
     */
    private DIDConstant.PublicKeyType type = DIDConstant.PublicKeyType.SECP256K1;

    /**
     * Required: The owner.
     */
    private String owner;

    /**
     * Required: The public key.
     */
    private String publicKey;
}
