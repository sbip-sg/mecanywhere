package com.meca.did.protocol.base;

import lombok.Data;

@Data
public class DIDAuthentication {

    /**
     * Required: The DID.
     */
    private String DID;

    /**
     * the public key Id.
     */
    private String DIDPublicKeyId;

    /**
     * Required: The private key or The DID.
     */
    private DIDPrivateKey DIDPrivateKey;

    public DIDAuthentication() {
        super();
    }

    /**
     * Constructor with DID and privateKey.
     * @param DID the DID
     * @param privateKey the privateKey
     */
    public DIDAuthentication(String DID, String privateKey) {
        this.DID = DID;
        this.DIDPrivateKey = new DIDPrivateKey();
        this.DIDPrivateKey.setPrivateKey(privateKey);
    }

    /**
     * Constructor with DID, privateKey and DIDPublicKeyId.
     * @param DID the DID
     * @param privateKey the privateKey
     * @param DIDPublicKeyId the DIDPublicKeyId
     */
    public DIDAuthentication(String DID, String privateKey, String DIDPublicKeyId) {
        this(DID, privateKey);
        this.DIDPublicKeyId = DIDPublicKeyId;
    }
}
