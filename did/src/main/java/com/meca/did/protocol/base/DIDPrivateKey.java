package com.meca.did.protocol.base;

import lombok.Data;

@Data
public class DIDPrivateKey {

    private String privateKey;

    public DIDPrivateKey() {
        super();
    }

    public DIDPrivateKey(String privateKey) {
        this.privateKey = privateKey;
    }
}