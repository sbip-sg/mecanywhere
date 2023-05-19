package com.meca.did.constant;

public class CredentialConstant {
    /**
     * The Constant default Credential Context.
     */
    public static final String DEFAULT_CREDENTIAL_CONTEXT =
            "https://www.w3.org/2018/credentials/v1";

    /**
     * The Constant default Credential Context field name in Credential Json String.
     */
    public static final String CREDENTIAL_CONTEXT_PORTABLE_JSON_FIELD = "@context";

    /**
     * The Constant default Credential type.
     */
    public static final String DEFAULT_CREDENTIAL_TYPE = "VerifiableCredential";

    /**
     * cpt type.
     */
    public static final String CPT_TYPE_KEY = "cptType";

    /**
     * key id.
     */
    public static final String ID = "id";

    /**
     * credential id.
     */
    public static final String CREDENTIAL_META_KEY_ID = "credentialId";

    /**
     * The issuer DID.
     */
    public static final String CREDENTIAL_META_KEY_ISSUER = "issuer";

    /**
     * The expire date.
     */
    public static final String CREDENTIAL_META_KEY_EXPIRATIONDATE = "expirationDate";

    /**
     * The issuance date of the credential.
     */
    public static final String CREDENTIAL_META_KEY_ISSUANCEDATE = "issuanceDate";

    /**
     * credential context.
     */
    public static final String CREDENTIAL_META_KEY_CONTEXT = "context";

    /**
     * The Constant is an field in claimPolicy.
     */
    public static final String CLAIM_POLICY_DISCLOSED_FIELD = "fieldsToBeDisclosed";

    public static final String PRESENTATION_PDF = "presentationFromPDF";

    /**
     * Default CPT ID for embedded credentialPojo subject (multi-sign support).
     */
    public static final Integer CREDENTIALPOJO_EMBEDDED_SIGNATURE_CPT = 107;
    /**
     * Embedded trusted timestamp default CPT ID.
     */
    public static final Integer EMBEDDED_TIMESTAMP_CPT = 108;

    /**
     * The Credential Proof Type Enumerate.
     */
    public static enum CredentialProofType {
        ECDSA("Secp256k1");

        /**
         * The Type Name of the Credential Proof.
         */
        private String typeName;

        /**
         * Constructor.
         */
        CredentialProofType(String typeName) {
            this.typeName = typeName;
        }

        /**
         * Getter.
         *
         * @return typeName
         */
        public String getTypeName() {
            return typeName;
        }
    }
}
