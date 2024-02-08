package constant

const (
	DEFAULT_CREDENTIAL_CONTEXT            = "https://www.w3.org/2018/credentials/v1"
	DEFAULT_CREDENTIAL_TYPE               = "VerifiableCredential"
	CPT_TYPE_KEY                          = "cptType"
	CREDENTIALPOJO_EMBEDDED_SIGNATURE_CPT = 107 // default cpt id
	EMBEDDED_TIMESTAMP_CPT                = 108 // embedded trusted timestamp cpt
	CREDENTIAL_PROOF_TYPE_ECDSA           = "Secp256k1"
)

type CredentialType struct {
	code int
	name string
}

func (c CredentialType) String() string {
	return c.name
}

func (c CredentialType) Code() int {
	return c.code
}

var (
	ORIGINAL_CREDENTIAL_TYPE = CredentialType{code: 0, name: "original"}
	ZKP_CREDENTIAL_TYPE      = CredentialType{code: 1, name: "zkp"}
	LITE1_CREDENTIAL_TYPE    = CredentialType{code: 2, name: "lite1"}
)
