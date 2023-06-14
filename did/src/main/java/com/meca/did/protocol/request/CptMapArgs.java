package com.meca.did.protocol.request;

import com.meca.did.constant.CptType;
import com.meca.did.protocol.base.DIDAuthentication;
import lombok.Data;

import java.util.Map;

@Data
public class CptMapArgs {

    /**
     * Required: weId authority  for this CPT.
     */
    private DIDAuthentication dIDAuthentication;

    /**
     * Required: The json schema content defined for this CPT.
     */
    private Map<String, Object> cptJsonSchema;

    /**
     * cpt type, "ORIGINAL" or "ZKP". default:"ORIGINAL".
     */
    private CptType cptType = CptType.ORIGINAL;
}
