package com.meca.did.protocol.response;

import com.meca.did.protocol.base.DIDPrivateKey;
import com.meca.did.protocol.base.DIDPublicKey;
import lombok.Data;

@Data
public class CreateDIDDataResult {
    private String dID;

    private DIDPublicKey dIDPublicKey;

    private DIDPrivateKey dIDPrivateKey;
}
