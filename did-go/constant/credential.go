package constant

const (
	DEFAULT_CREDENTIAL_CONTEXT  = "https://www.w3.org/2018/credentials/v1"
	DEFAULT_CREDENTIAL_TYPE     = "VerifiableCredential"
	CPT_TYPE_KEY                = "cptType"
	CREDENTIAL_PROOF_TYPE_ECDSA = "Secp256k1"
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
)
