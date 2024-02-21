package vc_service

import (
	"encoding/base64"
	"meca_did/common"
	"meca_did/constant"
	"regexp"
	"strconv"
	"time"
)

type Proof struct {
	Type           string `json:"type"`           // eg: "Secp256k1"
	SignatureValue string `json:"signatureValue"` // eg: "abVirKd3ZvGpJ20BR72SCkb18K/o4ZZT9BqDDU6W8lVv12ttuIfM3s9SAs5RbVJ4M3OrssB6DQ1Mj/YLi8Eq7Rw=""
}

type VerifiableCredential struct {
	Context        string   `json:"context"`         // eg: "https://www.w3.org/2018/credentials/v1"
	Id             string   `json:"id"`              // eg: "ae559160-c1bb-4f15-845e-af7d7912e07b"
	CptId          int      `json:"cptId"`           // eg: 1
	Issuer         string   `json:"issuer"`          // eg: "did:meca:0xfd340b5a30de452ae4a14dd1b92a7006868a29c8"
	IssuanceDate   string   `json:"issuance-date"`   // eg: "1644379660"
	ExpirationDate string   `json:"expiration-date"` // eg: "4797979660"
	Claim          string   `json:"claim"`           // eg: "name:John Doe"
	Proof          Proof    `json:"proof"`
	Type           []string `json:"type"` // eg: ["VerifiableCredential"]
}

type VerifiableCredentialArgs struct {
	Context        string `json:"context"`        // eg: "https://www.w3.org/2018/credentials/v1"
	Id             string `json:"id"`             // eg: "ae559160-c1bb-4f15-845e-af7d7912e07b"
	CptId          int    `json:"cptId"`          // eg: 1
	Issuer         string `json:"issuer"`         // eg: "did:meca:0xfd340b5a30de452ae4a14dd1b92a7006868a29c8"
	IssuanceDate   string `json:"issuanceDate"`   // eg: 1644379660
	ExpirationDate string `json:"expirationDate"` // eg: 4797979660
	Claim          string `json:"claim"`          // eg: "name:John Doe"
	Type           constant.CredentialType
}

func NewVerifiableCredentialArgs() *VerifiableCredentialArgs {
	return &VerifiableCredentialArgs{
		Context: constant.DEFAULT_CREDENTIAL_CONTEXT,
		Type:    constant.ORIGINAL_CREDENTIAL_TYPE,
	}
}

func CheckVCExpirationDate(issurance, expiration string) constant.ErrorCode {
	if len(issurance) == 0 || len(expiration) == 0 {
		return constant.CREDENTIAL_EXPIRE_DATE_ILLEGAL
	}
	iv, err := strconv.ParseInt(issurance, 10, 64)
	if err != nil {
		return constant.CREDENTIAL_ISSUANCE_DATE_ILLEGAL
	}
	ev, err := strconv.ParseInt(expiration, 10, 64)
	if err != nil {
		return constant.CREDENTIAL_EXPIRE_DATE_ILLEGAL
	}
	if ev <= iv {
		return constant.CREDENTIAL_EXPIRE_DATE_ILLEGAL
	}
	if time.Now().UnixMilli() < ev {
		return constant.CREDENTIAL_EXPIRED
	}
	return constant.SUCCESS
}

func isValidUUID(uuid string) bool {
	regex, err := regexp.Compile(constant.UUID_PATTERN)
	if err != nil {
		return false
	}
	return regex.MatchString(uuid)
}

func IsProofValid(proof *Proof) constant.ErrorCode {
	if proof == nil {
		return constant.ILLEGAL_INPUT
	}
	if len(proof.Type) == 0 || proof.Type != constant.CREDENTIAL_PROOF_TYPE_ECDSA {
		return constant.CREDENTIAL_SIGNATURE_TYPE_ILLEGAL
	}
	if len(proof.SignatureValue) == 0 {
		return constant.CREDENTIAL_SIGNATURE_BROKEN
	}
	if _, err := base64.StdEncoding.DecodeString(proof.SignatureValue); err != nil {
		return constant.CREDENTIAL_SIGNATURE_BROKEN
	}
	return constant.SUCCESS
}

func IsVerifiableCredentialValid(vc *VerifiableCredential) constant.ErrorCode {
	if vc == nil {
		return constant.ILLEGAL_INPUT
	}
	if !common.IsDidValid(vc.Issuer) {
		return constant.CREDENTIAL_ISSUER_INVALID
	}
	if len(vc.Claim) == 0 {
		return constant.CREDENTIAL_CLAIM_NOT_EXISTS
	}
	if len(vc.IssuanceDate) == 0 {
		return constant.CREDENTIAL_ISSUANCE_DATE_ILLEGAL
	}
	if ec := CheckVCExpirationDate(vc.IssuanceDate, vc.ExpirationDate); ec != constant.SUCCESS {
		return ec
	}
	if len(vc.Id) == 0 || !isValidUUID(vc.Id) {
		return constant.CREDENTIAL_ID_NOT_EXISTS
	}

	if len(vc.Context) == 0 {
		return constant.CREDENTIAL_CONTEXT_NOT_EXISTS
	}
	if len(vc.Type) == 0 {
		return constant.CREDENTIAL_TYPE_IS_NULL
	}

	// check proof validity
	return IsProofValid(&vc.Proof)
}
