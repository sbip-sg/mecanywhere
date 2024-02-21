package main

import (
	"crypto/ecdsa"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"log"
	"meca_did/common"
	"meca_did/constant"
	cptservice "meca_did/cpt_service"
	didservice "meca_did/did_service"
	"meca_did/vc_service"
	"os"

	"github.com/ethereum/go-ethereum/crypto"
	"github.com/ethereum/go-ethereum/ethclient"
)

type Request struct {
	ID    string `json:"id" binding:"required"`
	Input string `json:"input"`
}

type Response struct {
	Success bool   `json:"success"`
	Msg     string `json:"msg"`
}

func main() {
	client, err := ethclient.Dial("http://127.0.0.1:8545")
	if err != nil {
		panic(err)
	}
	contractAddr := "0x00404F73C76BC75b0D86F8AdDA8500e987BF8232"
	contractOwnerPrivateKeyStr := "b751ca3c38c91528ff87cb04c98eb85f78693f8eaab5e45300270a9dc18168db"

	ds := didservice.NewDidService(client, contractAddr, contractOwnerPrivateKeyStr)
	err = ds.Init()
	if err != nil {
		panic(err)
	}

	// register the owner himself
	contractOwnerPrivateKey, err := crypto.HexToECDSA(contractOwnerPrivateKeyStr)
	if err != nil {
		panic(err)
	}
	contractOwnerPublicKey := contractOwnerPrivateKey.Public()
	// convert public key to hex string
	contractOwnerAddress := crypto.PubkeyToAddress(*contractOwnerPublicKey.(*ecdsa.PublicKey)).Hex()
	fmt.Printf("contract owner address: %v\n", contractOwnerAddress)
	{
		pubBytes := crypto.FromECDSAPub(contractOwnerPublicKey.(*ecdsa.PublicKey))
		fmt.Printf("contractOwnerPublicKey: %v\n", hex.EncodeToString(pubBytes))
		resp0, err := ds.CreateDID(hex.EncodeToString(pubBytes))
		if err != nil {
			panic(err)
		} else if resp0.ErrCode == constant.SUCCESS {
			fmt.Printf("DID: %v\n", resp0.Did)
		} else {
			fmt.Printf("Error: %v\n", resp0.ErrCode)
		}
	}

	// candidatePrivateKeyStr := "af355f2914da0ea0361a5f93ca4224f60ae6a00d648e63f8fdebacc26e5a06f3"
	candidatePrivateKeyStr := "db4aa7094e4a444cfe44667e57c2110ac5174d6736dc36ecb45165a6c583523b"
	candidatePrivateKey, err := crypto.HexToECDSA(candidatePrivateKeyStr)
	if err != nil {
		panic(err)
	}
	candidatePublicKey := candidatePrivateKey.Public()
	// convert public key to hex string
	candidateAddress := crypto.PubkeyToAddress(*candidatePublicKey.(*ecdsa.PublicKey)).Hex()
	fmt.Printf("address: %v\n", candidateAddress)
	{

		pubBytes := crypto.FromECDSAPub(candidatePublicKey.(*ecdsa.PublicKey))
		fmt.Printf("candidatePublicKey: %v\n", hex.EncodeToString(pubBytes))

		// create a did
		resp1, err := ds.CreateDID(hex.EncodeToString(pubBytes))
		if err != nil {
			panic(err)
		} else if resp1.ErrCode == constant.SUCCESS {
			fmt.Printf("DID: %v\n", resp1.Did)
		} else {
			fmt.Printf("Error: %v\n", resp1.ErrCode)
		}

		resp2, err := ds.GetDIDDocumentJson(common.ConvertAddressToDID(candidateAddress))
		if err != nil {
			panic(err)
		} else if resp2.ErrCode == constant.SUCCESS {
			fmt.Printf("DID Document: %v\n", resp2.Doc)
		} else {
			fmt.Printf("Error: %v\n", resp2.ErrCode)
		}

		resp3, err := ds.GetDIDCount()
		if err != nil {
			panic(err)
		} else if resp3.ErrCode == constant.SUCCESS {
			fmt.Printf("DID Count: %v\n", resp3.Count)
		} else {
			fmt.Printf("Error: %v\n", resp3.ErrCode)
		}
	}

	// test cs, issue and verify
	cptContractAddr := "0xa1f89ddAD60FCA19a62a953a596C9FCF763396eE"
	cs := cptservice.NewCptService(client, cptContractAddr)
	err = cs.Init()
	if err != nil {
		panic(err)
	}

	// register cpt
	cptSchema, err := os.ReadFile("cpt_schema.json")
	if err != nil {
		panic(err)
	}
	var cptSchemaMap map[string]interface{}
	err = json.Unmarshal(cptSchema, &cptSchemaMap)
	if err != nil {
		panic(err)
	}

	didAuth := common.DIDAuthentication{
		DID:            common.ConvertAddressToDID(contractOwnerAddress),
		DIDPrivateKey:  contractOwnerPrivateKeyStr,
		DIDPublicKeyId: contractOwnerAddress,
	}

	cptid := 2000000

	{
		resp4 := cs.RegisterCpt(&didAuth, cptSchemaMap, constant.ORIGINAL)
		if resp4.ErrCode != constant.SUCCESS {
			log.Fatalf("Error: %v\n", resp4.ErrCode)
		} else {
			fmt.Printf("CPT ID: %v\n", resp4.CptBaseInfo)
			cptid = resp4.CptBaseInfo.CptId
		}
	}

	// issue vc
	claim := fmt.Sprintf(`{"info": "Chai", "DID": "%s"}`, candidateAddress)
	issueArgs := &vc_service.VerifiableCredentialArgs{
		Context:        constant.DEFAULT_CREDENTIAL_CONTEXT,
		Id:             "234508ed-fc5b-4ea4-88ac-f04bc657f470",
		CptId:          cptid,
		Issuer:         common.ConvertAddressToDID(contractOwnerAddress),
		IssuanceDate:   "1680058078",
		ExpirationDate: "4833658078",
		Claim:          claim,
		Type:           constant.ORIGINAL_CREDENTIAL_TYPE,
	}

	resp5, err := vc_service.CreateCredential(issueArgs, didAuth, ds)
	if err != nil {
		panic(err)
	} else if resp5.ErrCode != constant.SUCCESS {
		fmt.Printf("Error: %v\n", resp5.ErrCode)
	} else {
		fmt.Printf("VC: %v\n", resp5.VC)
	}

	// verify vc
	resp6, err := vc_service.VerifyCredential(common.ConvertAddressToDID(contractOwnerAddress), &resp5.VC, ds, cs)
	if err != nil {
		panic(err)
	} else if resp6.ErrCode != constant.SUCCESS {
		fmt.Printf("Error: %v\n", resp6.ErrCode)
	} else {
		fmt.Printf("VC: %v\n", resp6.Claim)
	}

	// flag.Parse()
	// router := gin.Default()
	// router.GET("/health", func(c *gin.Context) {
	// 	c.JSON(http.StatusOK, gin.H{"status": "ok"})
	// })
	// router.Run(":2592")
}

// curl http://localhost:2592/health
