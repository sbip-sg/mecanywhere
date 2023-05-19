package com.meca.did.constant;

import java.math.BigInteger;

public final class DIDConstant {

    /**
     * The Constant DID Document Protocol Version.
     */
    public static final String DID_DOC_PROTOCOL_VERSION =
            "\"@context\" : \"https://www.w3.org/ns/did/v1\",";

    /**
     * The Constant GAS_PRICE.
     */
    public static final BigInteger GAS_PRICE = new BigInteger("99999999999");

    /**
     * The Constant GAS_LIMIT.
     */
    public static final BigInteger GAS_LIMIT = new BigInteger("9999999999999");

    /**
     * The Constant EMPTY_ADDRESS.
     */
    public static final String EMPTY_ADDRESS = "0x0000000000000000000000000000000000000000";

    /**
     * The Constant INIIIAL_VALUE.
     */
    public static final BigInteger INILITIAL_VALUE = new BigInteger("0");

    /**
     * The Constant DID String Prefix.
     */
    public static final String DID_PREFIX = "did:meca:";

    /**
     * The Constant DID Document PublicKey Prefix.
     */
    public static final String DID_DOC_PUBLICKEY_PREFIX = "/meca/pubkey";

    /**
     * The Constant DID Document Authentication Prefix.
     */
    public static final String DID_DOC_AUTHENTICATE_PREFIX = "/meca/auth";

    /**
     * The Constant DID Document Service Prefix.
     */
    public static final String DID_DOC_SERVICE_PREFIX = "/meca/service";

    /**
     * The Constant DID Document Create Date Attribute String Name.
     */
    public static final String DID_DOC_CREATED = "created";

    /**
     * The Constant pipeline character.
     */
    public static final String PIPELINE = "|";

    /**
     * DID Separator.
     */
    public static final String DID_SEPARATOR = ":";

    /**
     * The Constant DID Event Attribute Change String Name.
     */
    public static final String DID_EVENT_ATTRIBUTE_CHANGE = "DIDAttributeChanged";

    /**
     * The Constant separator character.
     */
    public static final String SEPARATOR = "|";

    /**
     * Hex Prefix.
     */
    public static final String HEX_PREFIX = "0x";

    /**
     * UUID Separator.
     */
    public static final String UUID_SEPARATOR = "-";

    /**
     * UUID Pattern.
     */
    public static final String UUID_PATTERN =
            "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$";

    /**
     * The Address pattern.
     */
    public static final String ADDRESS_PATTERN = "0x[a-fA-f0-9]{40}";

    /**
     * The hash value pattern.
     */
    public static final String HASH_VALUE_PATTERN = "0x[a-fA-f0-9]{64}";

    /**
     * Removed DID public key specified tag.
     */
    public static final String REMOVED_PUBKEY_TAG = "OBSOLETE";

    /**
     * Removed DID authentication specified tag.
     */
    public static final String REMOVED_AUTHENTICATION_TAG = "OBSOLETEAUTH";

    public static final Integer ADD_PUBKEY_FAILURE_CODE = -1;

    /**
     * The Constant WeIdentity DID Maximum Json Schema Array Length.
     */
    public static final Integer JSON_SCHEMA_MAX_LENGTH = 4096;

    /**
     * The Constant default timeout for getting transaction.
     */
    public static final Integer TRANSACTION_RECEIPT_TIMEOUT = 13;

    public static final Integer CPT_DATA_INDEX = 0;

    /**
     * The Constant WeIdentity DID Long Array Length.
     */
    public static final Integer CPT_LONG_ARRAY_LENGTH = 8;

    /**
     * The Constant WeIdentity DID String Array Length.
     */
    public static final Integer CPT_STRING_ARRAY_LENGTH = 8;

    /**
     * The Constant Authority Issuer contract array length.
     */
    public static final Integer AUTHORITY_ISSUER_ARRAY_LEGNTH = 16;

    /**
     * The Constant Authority Issuer extra param list max length.
     */
    public static final Integer AUTHORITY_ISSUER_EXTRA_PARAM_LENGTH = 10;

    /**
     * The Constant WeIdentity DID Json Schema Array Length.
     */
    public static final Integer JSON_SCHEMA_ARRAY_LENGTH = 32;

    /**
     * The Constant Max authority issuer name length in Chars.
     */
    public static final Integer MAX_AUTHORITY_ISSUER_NAME_LENGTH = 32;


    public static enum PublicKeyType {
        RSA("RSA"),
        SECP256K1("Secp256k1");

        /**
         * The Type Name of the Credential Proof.
         */
        private String typeName;

        /**
         * Constructor.
         */
        PublicKeyType(String typeName) {
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
