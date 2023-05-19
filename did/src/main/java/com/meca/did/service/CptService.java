package com.meca.did.service;

import com.meca.did.protocol.base.Cpt;
import com.meca.did.protocol.base.CptBaseInfo;
import com.meca.did.protocol.request.CptMapArgs;
import com.meca.did.protocol.request.CptStringArgs;
import com.meca.did.protocol.response.ResponseData;

public interface CptService {
    /**
     * Register a new CPT to the blockchain.
     *
     * @param args the args
     * @return The registered CPT info
     */
    ResponseData<CptBaseInfo> registerCpt(CptMapArgs args);

    /**
     * Register a new CPT with a pre-set CPT ID, to the blockchain.
     *
     * @param args the args
     * @param cptId the CPT ID
     * @return The registered CPT info
     */
    ResponseData<CptBaseInfo> registerCpt(CptMapArgs args, Integer cptId);

    /**
     * Register a new CPT to the blockchain.
     *
     * @param args the args
     * @return The registered CPT info
     */
    ResponseData<CptBaseInfo> registerCpt(CptStringArgs args);

    /**
     * Register a new CPT with a pre-set CPT ID, to the blockchain.
     *
     * @param args the args
     * @param cptId the CPT ID
     * @return The registered CPT info
     */
    ResponseData<CptBaseInfo> registerCpt(CptStringArgs args, Integer cptId);

    /**
     * Query the latest CPT version.
     *
     * @param cptId the cpt id
     * @return The registered CPT info
     */
    ResponseData<Cpt> queryCpt(Integer cptId);

}
