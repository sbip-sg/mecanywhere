package com.meca.did.protocol.request;

import com.meca.did.constant.CredentialType;
import com.meca.did.util.CredentialUtils;
import com.meca.did.protocol.base.DIDAuthentication;
import lombok.Data;

@Data
public class CreateCredentialPojoArgs<T> {

    /**
     * Required: The CPT type in standard integer format.
     */
    private Integer cptId;

    /**
     * Required: The issuer DID.
     */
    private String issuer;

    /**
     * Required: The expire date.
     */
    private Long expirationDate;

    /**
     * Required: The claim data.
     */
    private T claim;

    /**
     * Required: The private key structure used for signing.
     */
    private DIDAuthentication DIDAuthentication;

    /**
     * Optional: The issuance date of the credential.
     */
    private Long issuanceDate = null;

    /**
     * 新增字段，issuer提前生成好的credential ID，对应credentialPojo里的ID.
     */
    private String id = null;

    /**
     * Optional:credential context.
     */
    private String context = CredentialUtils.getDefaultCredentialContext();

    /**
     * credential type.
     */
    private CredentialType type = CredentialType.ORIGINAL;

}
