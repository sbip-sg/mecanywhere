package main

import (
	"crypto/ecdsa"
	"encoding/hex"
	"flag"
	"fmt"
	"meca_did/common"
	"meca_did/constant"
	didservice "meca_did/did_service"

	"github.com/ethereum/go-ethereum/crypto"
	"github.com/ethereum/go-ethereum/ethclient"
)

var (
	config = flag.String("config", "", "the executor config yaml (optional)")
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
	contractOwnerPrivateKey := "b751ca3c38c91528ff87cb04c98eb85f78693f8eaab5e45300270a9dc18168db"

	ds := didservice.NewDidService(client, contractAddr, contractOwnerPrivateKey)
	err = ds.Init()
	if err != nil {
		panic(err)
	}

	// candidatePrivateKeyStr := "af355f2914da0ea0361a5f93ca4224f60ae6a00d648e63f8fdebacc26e5a06f3"
	candidatePrivateKeyStr := "db4aa7094e4a444cfe44667e57c2110ac5174d6736dc36ecb45165a6c583523b"
	candidatePrivateKey, err := crypto.HexToECDSA(candidatePrivateKeyStr)
	if err != nil {
		panic(err)
	}
	candidatePublicKey := candidatePrivateKey.Public()
	// convert public key to hex string
	address := crypto.PubkeyToAddress(*candidatePublicKey.(*ecdsa.PublicKey)).Hex()
	fmt.Printf("address: %v\n", address)

	pubBytes := crypto.FromECDSAPub(candidatePublicKey.(*ecdsa.PublicKey))
	fmt.Printf("candidatePublicKey: %v\n", hex.EncodeToString(pubBytes))

	// create a did
	resp, err := ds.CreateDID(hex.EncodeToString(pubBytes))
	if resp.ErrCode == constant.SUCCESS {
		fmt.Printf("DID: %v\n", resp.Did)
	} else {
		fmt.Printf("Error: %v\n", resp.ErrCode)
	}

	resp2, err := ds.GetDIDDocumentJson(common.ConvertAddressToDID(address))
	if resp2.ErrCode == constant.SUCCESS {
		fmt.Printf("DID Document: %v\n", resp2.Doc)
	} else {
		fmt.Printf("Error: %v\n", resp2.ErrCode)
	}

	resp3, err := ds.GetDIDCount()
	if resp3.ErrCode == constant.SUCCESS {
		fmt.Printf("DID Count: %v\n", resp3.Count)
	} else {
		fmt.Printf("Error: %v\n", resp3.ErrCode)
	}

	// flag.Parse()
	// router := gin.Default()
	// router.GET("/health", func(c *gin.Context) {
	// 	c.JSON(http.StatusOK, gin.H{"status": "ok"})
	// })
	// router.Run(":2592")
}

// curl http://localhost:2592/health
