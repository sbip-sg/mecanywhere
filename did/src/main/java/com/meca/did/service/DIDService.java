package com.meca.did.service;

import com.meca.did.protocol.base.DIDDocument;
import com.meca.did.protocol.base.DIDPrivateKey;
import com.meca.did.protocol.request.AuthenticationArgs;
import com.meca.did.protocol.request.CreateDIDArgs;
import com.meca.did.protocol.request.PublicKeyArgs;
import com.meca.did.protocol.response.CreateDIDDataResult;
import com.meca.did.protocol.response.ResponseData;

public interface DIDService {
    /**
     * Create a DID without a keypair. SDK will generate a keypair for the caller.
     *
     * @return a data set including a DID and a keypair
     */
    ResponseData<CreateDIDDataResult> createDID();

    ResponseData<CreateDIDDataResult> createDID(CreateDIDArgs createDIDArgs);

    /**
     * Set authentications in DID.
     *
     * @param DID the DID to set auth to
     * @param authenticationArgs A public key is needed
     * @return true if the "set" operation succeeds, false otherwise.
     */
    ResponseData<Boolean> setAuthentication(
            String DID,
            AuthenticationArgs authenticationArgs);

    /**
     * Check if the DID exists on chain.
     *
     * @param DID The DID.
     * @return true if exists, false otherwise.
     */
    ResponseData<Boolean> dIDExists(String DID);

    /**
     * Query DID document.
     *
     * @param DID the DID
     * @return DID document in java object type
     */
    ResponseData<DIDDocument> getDIDDocument(String DID);

    ResponseData<String> getDIDDocumentJson(String dID);

    ResponseData<Boolean> revokePublicKeyWithAuthentication(
            String dID,
            PublicKeyArgs publicKeyArgs,
            DIDPrivateKey privateKey);

    ResponseData<Boolean> revokeAuthentication(
            String dID,
            AuthenticationArgs authenticationArgs,
            DIDPrivateKey privateKey);

    ResponseData<Integer> addPublicKey(
            String dID,
            PublicKeyArgs publicKeyArgs,
            DIDPrivateKey privateKey);

    ResponseData<Integer> getDIDCount();
}
