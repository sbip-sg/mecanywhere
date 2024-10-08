package constant

type ErrorCode struct {
	code     int
	codeDesc string
}

func (e ErrorCode) Code() int {
	return e.code
}

func (e ErrorCode) CodeDesc() string {
	return e.codeDesc
}

var (
	SUCCESS                                          = ErrorCode{code: 0, codeDesc: "success"}
	CPT_NOT_EXIST                                    = ErrorCode{code: 500301, codeDesc: "cpt not exist"}
	CPT_JSON_SCHEMA_INVALID                          = ErrorCode{code: 500306, codeDesc: "cpt json schema invalid"}
	CPT_ID_ILLEGAL                                   = ErrorCode{code: 100303, codeDesc: "cpt id illegal"}
	CREDENTIAL_EXPIRED                               = ErrorCode{code: 100402, codeDesc: "credential expired"}
	CREDENTIAL_ISSUER_MISMATCH                       = ErrorCode{code: 100403, codeDesc: "credential issuer mismatch"}
	CREDENTIAL_SIGNATURE_BROKEN                      = ErrorCode{code: 100405, codeDesc: "credential signature broken"}
	CREDENTIAL_ISSUER_NOT_EXISTS                     = ErrorCode{code: 100407, codeDesc: "credential issuer not exists"}
	CREDENTIAL_ISSUANCE_DATE_ILLEGAL                 = ErrorCode{code: 100408, codeDesc: "credential issuance date illegal"}
	CREDENTIAL_EXPIRE_DATE_ILLEGAL                   = ErrorCode{code: 100409, codeDesc: "credential expire date illegal"}
	CREDENTIAL_CLAIM_NOT_EXISTS                      = ErrorCode{code: 100410, codeDesc: "credential claim not exists"}
	CREDENTIAL_ID_NOT_EXISTS                         = ErrorCode{code: 100412, codeDesc: "credential id not exists"}
	CREDENTIAL_CONTEXT_NOT_EXISTS                    = ErrorCode{code: 100413, codeDesc: "credential context not exists"}
	CREDENTIAL_TYPE_IS_NULL                          = ErrorCode{code: 100414, codeDesc: "credential type is null"}
	CREDENTIAL_ISSUER_INVALID                        = ErrorCode{code: 100418, codeDesc: "credential issuer invalid"}
	CREDENTIAL_SIGNATURE_TYPE_ILLEGAL                = ErrorCode{code: 100429, codeDesc: "credential signature type illegal"}
	DID_INVALID                                      = ErrorCode{code: 100101, codeDesc: "did invalid"}
	DID_PUBLICKEY_INVALID                            = ErrorCode{code: 100102, codeDesc: "did publickey invalid"}
	DID_PRIVATEKEY_INVALID                           = ErrorCode{code: 100103, codeDesc: "did privatekey invalid"}
	DID_DOES_NOT_EXIST                               = ErrorCode{code: 100104, codeDesc: "did does not exist"}
	DID_ALREADY_EXIST                                = ErrorCode{code: 100105, codeDesc: "did already exist"}
	DID_PRIVATEKEY_DOES_NOT_MATCH                    = ErrorCode{code: 100106, codeDesc: "did privatekey does not match"}
	DID_CANNOT_REMOVE_ITS_OWN_PUB_KEY_WITHOUT_BACKUP = ErrorCode{code: 100111, codeDesc: "did cannot remove its own pub key without backup"}
	DID_PUBLIC_KEY_ALREADY_EXISTS                    = ErrorCode{code: 100116, codeDesc: "did public key already exists"}
	DID_PUBLIC_KEY_NOT_EXIST                         = ErrorCode{code: 100117, codeDesc: "did public key not exist"}
	DID_PUBLIC_KEY_LENGTH_INVALID                    = ErrorCode{code: 100118, codeDesc: "did public key length invalid"}
	TRANSACTION_TIMEOUT                              = ErrorCode{code: 160001, codeDesc: "transaction timeout"}
	TRANSACTION_EXECUTE_ERROR                        = ErrorCode{code: 160002, codeDesc: "transaction execute error"}
	ILLEGAL_INPUT                                    = ErrorCode{code: 160004, codeDesc: "illegal input"}
	UNKNOWN_ERROR                                    = ErrorCode{code: 160003, codeDesc: "unknown error"}
)
