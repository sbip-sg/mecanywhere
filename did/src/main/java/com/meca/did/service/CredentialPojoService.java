package com.meca.did.service;

import com.meca.did.protocol.base.CredentialPojo;
import com.meca.did.protocol.request.CreateCredentialPojoArgs;
import com.meca.did.protocol.response.ResponseData;

public interface CredentialPojoService {

    /**
     * Generate a credential for full claim content.
     *
     * @param args the args
     * @return CredentialPojo
     */
    ResponseData<CredentialPojo> createCredential(CreateCredentialPojoArgs args);

    /**
     * Verify the validity of a credential. Public key will be fetched from chain.
     *
     * @param issuerDID the issuer DID
     * @param credential the credential
     * @return the verification result. True if yes, false otherwise with exact verify error codes
     */
    ResponseData<Boolean> verify(String issuerDID, CredentialPojo credential);
}
