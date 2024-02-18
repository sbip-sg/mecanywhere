package vc_service

import (
	"encoding/base64"
	"errors"
	"fmt"
	"log"
	"meca_did/common"
	"meca_did/constant"
	cptservice "meca_did/cpt_service"
	didservice "meca_did/did_service"
	"strings"

	"github.com/xeipuuv/gojsonschema"
)

type VerifyCredentialResponse struct {
	Claim string
	common.ServiceResponseInfo
}

func verifyCptFormat(cptId int, claim string, cs cptservice.CptService) constant.ErrorCode {
	ret := cs.QueryCpt(cptId)
	if ret.ErrCode != constant.SUCCESS {
		return ret.ErrCode
	}
	cptSchema := gojsonschema.NewStringLoader(ret.Cpt.JsonSchema)
	log.Printf("CPT Schema: %v\n", cptSchema)
	claimData := gojsonschema.NewStringLoader(claim)
	log.Printf("Claim Data: %v\n", claimData)
	if result, err := gojsonschema.Validate(cptSchema, claimData); err != nil || !result.Valid() {
		return constant.CPT_JSON_SCHEMA_INVALID
	}
	return constant.SUCCESS
}

func VerifyCredential(issuerDID string, vc *VerifiableCredential, ds didservice.DidService, cs cptservice.CptService) (VerifyCredentialResponse, error) {
	resp := VerifyCredentialResponse{}
	if vc == nil {
		resp.ErrCode = constant.ILLEGAL_INPUT
		return resp, errors.New("vc is nil")
	}

	if !strings.EqualFold(issuerDID, vc.Issuer) {
		resp.ErrCode = constant.CREDENTIAL_ISSUER_MISMATCH
		return resp, errors.New("issuer mismatch")
	}

	// verify credential content
	if ec := IsVerifiableCredentialValid(vc); ec != constant.SUCCESS {
		resp.ErrCode = ec
		fmt.Printf("Error: %v\n", ec)
		return resp, errors.New("vc is invalid")
	}

	// verify signature
	signature, _ := base64.StdEncoding.DecodeString(vc.Proof.SignatureValue)
	didDoc, err := ds.GetDIDDocument(vc.Issuer)
	if err != nil {
		resp.ErrCode = constant.DID_INVALID
		return resp, errors.New("did document does not exist")
	}
	issuerKey := strings.Split(didDoc.Doc.CreatePubKey, "|")[0]
	fmt.Printf("Issuer Key: %v\n", issuerKey)
	loadedKey, err := common.LoadPublicKey(issuerKey)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		resp.ErrCode = constant.CREDENTIAL_SIGNATURE_BROKEN
		return resp, errors.New("signature is broken")
	}

	// verify signature
	vcData, err := getCredentialDataToSign(vc)
	if err != nil {
		log.Printf("get vc data to sign failed\n")
		resp.ErrCode = constant.CREDENTIAL_SIGNATURE_BROKEN
		return resp, errors.New("signature is broken")
	}
	if !common.VerifySignature(loadedKey, vcData, signature) {
		log.Printf("signature verification failed\n")
		resp.ErrCode = constant.CREDENTIAL_SIGNATURE_BROKEN
		return resp, errors.New("signature is broken")
	}

	// verify Cpt format
	if ec := verifyCptFormat(vc.CptId, vc.Claim, cs); ec != constant.SUCCESS {
		resp.ErrCode = ec
		return resp, errors.New("cpt format is invalid")
	} else {
		resp.Claim = vc.Claim
		resp.ErrCode = constant.SUCCESS
		return resp, nil
	}
}
