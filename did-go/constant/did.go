package constant

const (
	DID_DOC_PROTOCOL_VERSION     = "\"@context\" : \"https://www.w3.org/ns/did/v1\","
	DID_EMPTY_ADDRESS            = "0x0000000000000000000000000000000000000000"
	DID_PREFIX                   = "did:meca:"
	DID_DOC_PUBLICKEY_PREFIX     = "/meca/pubkey"
	DID_DOC_AUTHENTICATE_PREFIX  = "/meca/auth"
	DID_DOC_SERVICE_PREFIX       = "/meca/service"
	DID_DOC_CREATED              = "created"
	DID_DOC_PUBKEY               = "pubKey"
	UUID_PATTERN                 = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
	REMOVED_PUBKEY_TAG           = "OBSOLETE"
	REMOVED_AUTHENTICATION_TAG   = "OBSOLETEAUTH"
	JSON_SCHEMA_MAX_LENGTH       = 4096
	JSON_SCHEMA_ARRAY_LENGTH     = 32
	DID_PUBLICKEY_TYPE_SECP256K1 = "Secp256k1"
)
