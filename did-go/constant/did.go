package constant

const (
	DID_DOC_PROTOCOL_VERSION         = "\"@context\" : \"https://www.w3.org/ns/did/v1\","
	DID_EMPTY_ADDRESS                = "0x0000000000000000000000000000000000000000"
	DID_PREFIX                       = "did:meca:"
	DID_DOC_PUBLICKEY_PREFIX         = "/meca/pubkey"
	DID_DOC_AUTHENTICATE_PREFIX      = "/meca/auth"
	DID_DOC_SERVICE_PREFIX           = "/meca/service"
	DID_DOC_CREATED                  = "created"
	DID_DOC_PUBKEY                   = "pubKey"
	DID_PIPELINE                     = "|"
	DID_SEPARATOR                    = ":"
	DID_EVENT_ATTRIBUTE_CHANGE       = "DIDAttributeChanged"
	SEPARATOR                        = "|"
	HEX_PREFIX                       = "0x"
	UUID_PATTERN                     = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
	ADDRESS_PATTERN                  = "0x[a-fA-f0-9]{40}"
	REMOVED_PUBKEY_TAG               = "OBSOLETE"
	REMOVED_AUTHENTICATION_TAG       = "OBSOLETEAUTH"
	ADD_PUBKEY_FAILURE_CODE          = -1
	JSON_SCHEMA_MAX_LENGTH           = 4096
	TRANSACTION_RECEIPT_TIMEOUT      = 13
	CPT_DATA_INDEX                   = 0
	CPT_LONG_ARRAY_LENGTH            = 8
	CPT_STRING_ARRAY_LENGTH          = 8
	JSON_SCHEMA_ARRAY_LENGTH         = 32
	MAX_AUTHORITY_ISSUER_NAME_LENGTH = 32
	DID_PUBLICKEY_TYPE_RSA           = "RSA"
	DID_PUBLICKEY_TYPE_SECP256K1     = "Secp256k1"
)
