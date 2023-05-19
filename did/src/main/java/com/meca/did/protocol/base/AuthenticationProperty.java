package com.meca.did.protocol.base;

import com.meca.did.constant.DIDConstant;
import lombok.Data;

@Data
public class AuthenticationProperty {

    /**
     * Required: The type.
     */
    private String type = DIDConstant.PublicKeyType.SECP256K1.getTypeName();

    /**
     * Required: The public key.
     */
    private String publicKey;

    /**
     * Required: Revoked, or not.
     */
    private Boolean revoked = false;
}
