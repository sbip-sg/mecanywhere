package com.meca.did.protocol.request;
import com.meca.did.protocol.base.DIDPublicKey;
import lombok.Data;

@Data
public class CreateDIDArgs {

    /**
     * Required: Public Key.
     */
    private DIDPublicKey DIDPublicKey;
}
