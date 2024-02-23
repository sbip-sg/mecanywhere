package main

import (
	"flag"
	"fmt"
	"log"
	"meca_did/constant"
	cptservice "meca_did/cpt_service"
	didservice "meca_did/did_service"
	"meca_did/vc_service"
	"net/http"

	"github.com/ethereum/go-ethereum/ethclient"
	"github.com/gin-gonic/gin"
)

var (
	config = flag.String("config", "", "the server config json (optional)")
)

func main() {
	flag.Parse()

	// config
	chainAddr := "http://localhost:8545"
	contractAddr := "0x00404F73C76BC75b0D86F8AdDA8500e987BF8232"
	contractOwnerPrivateKeyStr := "b751ca3c38c91528ff87cb04c98eb85f78693f8eaab5e45300270a9dc18168db"
	cptContractAddr := "0xa1f89ddAD60FCA19a62a953a596C9FCF763396eE"
	port := 2592

	if len(*config) > 0 {
		// overwrite the default
		if parsed, err := ParseServerConfig(*config); err != nil {
			log.Printf("failed to parse config: %v; using default", err.Error())
		} else {
			log.Printf("Using config %s: %v", *config, parsed)
			chainAddr = parsed.BlockChainAddr
			contractAddr = parsed.DIDContract
			contractOwnerPrivateKeyStr = parsed.DIDContractOwnerPrivateKey
			cptContractAddr = parsed.CPTContract
			port = parsed.Port
		}
	}

	// setup connection to contract
	client, err := ethclient.Dial(chainAddr)
	if err != nil {
		panic(err)
	}
	ds := didservice.NewDidService(client, contractAddr, contractOwnerPrivateKeyStr)
	err = ds.Init()
	if err != nil {
		panic(err)
	}
	cs := cptservice.NewCptService(client, cptContractAddr)
	err = cs.Init()
	if err != nil {
		panic(err)
	}

	create_did := func(c *gin.Context) {
		var req CreateDIDRequest
		if err := c.ShouldBindJSON(&req); err != nil {
			c.IndentedJSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		ret, err := ds.CreateDID(req.PublicKey)
		if err != nil {
			c.IndentedJSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		c.IndentedJSON(http.StatusOK, ret)
	}

	register_cpt := func(c *gin.Context) {
		var req RegisterCptRequest
		if err := c.ShouldBindJSON(&req); err != nil {
			c.IndentedJSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		ret := cs.RegisterCpt(&req.DidAuth, req.CptJsonSchema, constant.ORIGINAL)
		if ret.ErrCode != constant.SUCCESS {
			c.IndentedJSON(http.StatusInternalServerError, gin.H{"error": ret.ErrCode})
			return
		}
		c.IndentedJSON(http.StatusOK, ret)
	}

	issue_vc := func(c *gin.Context) {
		var req IssueVCRequest
		if err := c.ShouldBindJSON(&req); err != nil {
			c.IndentedJSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		ret, err := vc_service.CreateCredential(&req.VcArgs, req.DidAuth, ds)
		if err != nil {
			c.IndentedJSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		c.IndentedJSON(http.StatusOK, ret)
	}

	verify_vc := func(c *gin.Context) {
		var req VerifyVCRequest
		if err := c.ShouldBindJSON(&req); err != nil {
			c.IndentedJSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		ret, err := vc_service.VerifyCredential(req.IssuerDID, &req.VcJson, ds, cs)
		if err != nil {
			c.IndentedJSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		c.IndentedJSON(http.StatusOK, ret)
	}

	router := gin.Default()
	router.GET("/health", func(c *gin.Context) {
		c.IndentedJSON(http.StatusOK, gin.H{"status": "ok"})
	})
	router.POST("/create-did", create_did)
	router.POST("/register-cpt", register_cpt)
	router.POST("/issue-vc", issue_vc)
	router.POST("/verify-vc", verify_vc)
	router.Run(fmt.Sprintf(":%d", port))
}
