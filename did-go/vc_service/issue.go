package vc_service

import (
	"crypto/ecdsa"
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"meca_did/common"
	"meca_did/constant"
	didservice "meca_did/did_service"
	"strings"
	"time"

	"github.com/ethereum/go-ethereum/crypto"
	"github.com/google/uuid"
)

type CreateCredentialResponse struct {
	VC VerifiableCredential
	common.ServiceResponseInfo
}

func getCredentialDataToSign(vc *VerifiableCredential) ([]byte, error) {
	data := &VerifiableCredential{
		Context:        vc.Context,
		Id:             vc.Id,
		CptId:          vc.CptId,
		Issuer:         vc.Issuer,
		IssuanceDate:   vc.IssuanceDate,
		ExpirationDate: vc.ExpirationDate,
		Claim:          vc.Claim,
	}
	return json.Marshal(data)
}

func CreateCredential(args *VerifiableCredentialArgs, didAuth common.DIDAuthentication, ds didservice.DidService) (CreateCredentialResponse, error) {
	resp := CreateCredentialResponse{}
	// input validation
	if args == nil {
		resp.ErrCode = constant.ILLEGAL_INPUT
		return resp, errors.New("args is nil")
	}

	if !common.IsDidValid(args.Issuer) {
		resp.ErrCode = constant.CREDENTIAL_ISSUER_INVALID
		return resp, errors.New("issuer is invalid (in args)")
	}

	if len(args.Claim) == 0 {
		resp.ErrCode = constant.CREDENTIAL_CLAIM_NOT_EXISTS
		return resp, errors.New("claim is empty")
	}

	if expirationErr := CheckVCExpirationDate(args.IssuanceDate, args.ExpirationDate); expirationErr != constant.SUCCESS {
		resp.ErrCode = expirationErr
		return resp, errors.New("expiration date is invalid")
	}

	if !strings.EqualFold(didAuth.DID, args.Issuer) || len(didAuth.DIDPrivateKey) == 0 || len(didAuth.DIDPublicKeyId) == 0 {
		fmt.Printf("DID (%d): %v, Issuer (%d): %v\n", len(didAuth.DID), didAuth.DID, len(args.Issuer), args.Issuer)
		resp.ErrCode = constant.CREDENTIAL_ISSUER_INVALID
		return resp, errors.New("issuer is invalid (auth vs args)")
	}

	ret, err := ds.DidExist(args.Issuer)
	if err != nil || ret.ErrCode != constant.SUCCESS {
		resp.ErrCode = constant.CREDENTIAL_ISSUER_NOT_EXISTS
		return resp, errors.New("issuer does not exist")
	}

	if args.Id == "" {
		args.Id = uuid.New().String()
	}

	if args.IssuanceDate == "" {
		args.IssuanceDate = fmt.Sprintf("%d", time.Now().UnixMilli())
	}

	vc := VerifiableCredential{
		Context:        args.Context,
		Id:             args.Id,
		CptId:          args.CptId,
		Issuer:         args.Issuer,
		IssuanceDate:   args.IssuanceDate,
		ExpirationDate: args.ExpirationDate,
		Claim:          args.Claim,
		Type:           []string{constant.DEFAULT_CREDENTIAL_TYPE, args.Type.String()},
	}

	vcData, err := getCredentialDataToSign(&vc)
	if err != nil {
		resp.ErrCode = constant.CREDENTIAL_SIGNATURE_BROKEN
		return resp, errors.New("signature is broken")
	}

	signKey, err := crypto.HexToECDSA(didAuth.DIDPrivateKey)
	pubBytes := crypto.FromECDSAPub(signKey.Public().(*ecdsa.PublicKey))
	pubKeyHex := hex.EncodeToString(pubBytes)
	log.Printf("Public Key: %v\n", pubKeyHex)
	if err != nil {
		resp.ErrCode = constant.DID_PRIVATEKEY_INVALID
		return resp, errors.New("private key is invalid")
	}
	signature, err := common.Sign(signKey, vcData)
	if err != nil {
		resp.ErrCode = constant.UNKNOW_ERROR
		return resp, errors.New("signature is invalid")
	}
	vc.Proof = Proof{
		Type:           constant.CREDENTIAL_PROOF_TYPE_ECDSA,
		Created:        time.Now().UnixMilli(),
		Creator:        didAuth.DIDPublicKeyId,
		Salt:           args.Claim,                                   // is it ok?
		SignatureValue: base64.StdEncoding.EncodeToString(signature), // just use base64.StdEncoding.EncodeToString(signature)
	}
	resp.VC = vc
	resp.ErrCode = constant.SUCCESS
	return resp, nil
}
