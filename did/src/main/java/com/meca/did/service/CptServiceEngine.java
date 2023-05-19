package com.meca.did.service;

import com.meca.did.protocol.base.Cpt;
import com.meca.did.protocol.base.CptBaseInfo;
import com.meca.did.protocol.response.ResponseData;
import com.meca.did.protocol.response.RsvSignature;

public interface CptServiceEngine {
    /**
     * call cpt contract to register cpt.
     *
     * @param address publisher's address
     * @param cptJsonSchemaNew cpt content
     * @param rsvSignature signature
     * @param privateKey private key
     * @param dataStorageIndex 0 is cpt, 1 is policy
     * @return result
     */
    ResponseData<CptBaseInfo> registerCpt(
            String address,
            String cptJsonSchemaNew,
            RsvSignature rsvSignature,
            String privateKey,
            int dataStorageIndex
    );

    /**
     * call cpt contract method to query cpt info from blockchain.
     *
     * @param cptId the id of the cpt
     * @param dataStorageIndex 0 is cpt, 1 is policy
     * @return cpt info
     */
    ResponseData<Cpt> queryCpt(int cptId, int dataStorageIndex);
}
