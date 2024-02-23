package main

import (
	"meca_did/common"
	"meca_did/vc_service"
)

type CreateDIDRequest struct {
	PublicKey string `json:"publicKey"`
}

type RegisterCptRequest struct {
	DidAuth       common.DIDAuthentication `json:"didAuth"`
	CptJsonSchema map[string]interface{}   `json:"cptJsonSchema"`
}

type QueryCptRequest struct {
	CptId int `json:"cptId"`
}

type IssueVCRequest struct {
	DidAuth common.DIDAuthentication            `json:"didAuth"`
	VcArgs  vc_service.VerifiableCredentialArgs `json:"vcArgs"`
}

type VerifyVCRequest struct {
	IssuerDID string                          `json:"issuerDID"`
	VcJson    vc_service.VerifiableCredential `json:"vc"`
}
