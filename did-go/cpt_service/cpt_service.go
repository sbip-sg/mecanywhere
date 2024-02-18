package cptservice

import (
	"context"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"log"
	"math/big"
	"meca_did/common"
	"meca_did/constant"
	"meca_did/contract/cpt"
	"time"

	"github.com/ethereum/go-ethereum/accounts/abi/bind"
	ethcommon "github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/core/types"
	"github.com/ethereum/go-ethereum/crypto"
	"github.com/ethereum/go-ethereum/ethclient"
)

type CptBaseInfo struct {
	CptId      int
	CptVersion int
}

type CptMetaData struct {
	CptPublisher string
	CptSignature string
	Created      uint64
	Updated      uint64
}

type Cpt struct {
	BaseInfo   CptBaseInfo
	JsonSchema string
	Meta       CptMetaData
}

type CptRegisterResponse struct {
	CptBaseInfo
	common.ServiceResponseInfo
}

type CptQueryResponse struct {
	Cpt
	common.ServiceResponseInfo
}

type CptService interface {
	Init() error
	RegisterCpt(auth *common.DIDAuthentication, schema map[string]interface{}, cptType constant.CptType) CptRegisterResponse
	QueryCpt(cptId int) CptQueryResponse
}

var _ CptService = (*CptServiceImpl)(nil)

type CptServiceImpl struct {
	client       *ethclient.Client
	contractAddr string

	contract *cpt.Cpt
	chainId  *big.Int
}

// NewCptService creates a new CptService instance
// client: ethclient instance
// contractAddr: contract address in hex
func NewCptService(client *ethclient.Client, contractAddr string) CptService {
	return &CptServiceImpl{
		client:       client,
		contractAddr: contractAddr,
	}
}

func (c *CptServiceImpl) Init() error {
	if chainId, err := c.client.ChainID(context.Background()); err != nil {
		return err
	} else if contract, err := cpt.NewCpt(ethcommon.HexToAddress(c.contractAddr), c.client); err != nil {
		return err
	} else {
		c.chainId = chainId
		c.contract = contract
		return nil
	}
}

func (c *CptServiceImpl) RegisterCpt(auth *common.DIDAuthentication, schema map[string]interface{}, cptType constant.CptType) CptRegisterResponse {
	resp := CptRegisterResponse{}
	// TODO: implement input validation
	did := auth.DID
	publicKeyId := auth.DIDPublicKeyId
	privateKey, err := crypto.HexToECDSA(auth.DIDPrivateKey)
	if err != nil {
		resp.ErrCode = constant.DID_PRIVATEKEY_INVALID
		return resp
	}
	data := fmt.Sprintf("%s|%s", did, publicKeyId)
	signature, err := common.Sign(privateKey, []byte(data))
	if err != nil {
		resp.ErrCode = constant.TRANSACTION_EXECUTE_ERROR
		return resp
	}
	address := common.ConvertDIDToAddress(did)

	// tx := bind.NewKeyedTransactor(privateKey)

	tx, err := bind.NewKeyedTransactorWithChainID(privateKey, c.chainId)
	if err != nil {
		resp.ErrCode = constant.TRANSACTION_EXECUTE_ERROR
		return resp
	}
	fromAddress := crypto.PubkeyToAddress(privateKey.PublicKey)
	nonce, err := c.client.PendingNonceAt(context.Background(), fromAddress)
	if err != nil {
		resp.ErrCode = constant.DID_INVALID
		return resp
	}
	gasPrice, err := c.client.SuggestGasPrice(context.Background())
	if err != nil {
		resp.ErrCode = constant.TRANSACTION_EXECUTE_ERROR
		return resp
	}
	tx.Nonce = big.NewInt(int64(nonce))
	tx.Value = big.NewInt(0)
	tx.GasLimit = uint64(3000000)
	tx.GasPrice = gasPrice

	// to change to just one big int in contract
	created := [8]*big.Int{}
	for i := 0; i < 8; i++ {
		created[i] = big.NewInt(0)
	}
	created[1] = big.NewInt(time.Now().UnixMilli())

	// to remove from the contract
	byteArray := [8][32]byte{}

	// prepare schema bytes
	schema[constant.JSON_SCHEMA_KEY] = constant.JSON_SCHEMA_VALUE
	schema[constant.JSON_SCHMEA_TYPE_KEY] = constant.JSON_SCHEMA_DATA_TYPE_OBJECT
	schema[constant.CPT_TYPE_KEY] = cptType.String()
	schemaBytes, err := json.Marshal(schema)
	if err != nil || len(schemaBytes) > 32*32 {
		resp.ErrCode = constant.CPT_JSON_SCHEMA_INVALID
		return resp
	}

	schemaBytesArray := [constant.JSON_SCHEMA_ARRAY_LENGTH][32]byte{}
	for i := 0; i < len(schemaBytes); i += 32 {
		copy(schemaBytesArray[i/32][:], schemaBytes[i:i+32])
	}
	r, s, v := common.SignatureToRSV(signature)

	log.Printf("inputs for registerCpt: %v, %v, %v, %v, %v, %v, %v\n", address, created, byteArray, schemaBytesArray, v, r, s)
	txRet, err := c.contract.RegisterCpt(tx, ethcommon.HexToAddress(address), created, byteArray, schemaBytesArray, v, r, s)
	if err != nil {
		resp.ErrCode = constant.TRANSACTION_EXECUTE_ERROR
		return resp
	}

	receipt, err := bind.WaitMined(context.Background(), c.client, txRet)
	if err != nil || receipt.Status != types.ReceiptStatusSuccessful {
		resp.ErrCode = constant.TRANSACTION_TIMEOUT
		return resp
	}

	txBlockNumber := receipt.BlockNumber.Uint64()
	it, err := c.contract.FilterRegisterCptRetLog(&bind.FilterOpts{Start: txBlockNumber, End: &txBlockNumber, Context: context.Background()})
	if err != nil {
		resp.ErrCode = constant.TRANSACTION_EXECUTE_ERROR
		return resp
	}

	it.Next()
	log := it.Event
	if log == nil {
		resp.ErrCode = constant.TRANSACTION_EXECUTE_ERROR
		return resp
	}

	// fill up the response
	resp.CptId = int(log.CptId.Int64())
	resp.CptVersion = int(log.CptVersion.Int64())
	resp.ErrCode = constant.SUCCESS
	resp.TxInfo.SetTxInfo(receipt)

	return resp
}

func parseJsonSchema(schemaBytes [][32]byte) string {
	if len(schemaBytes) != constant.JSON_SCHEMA_ARRAY_LENGTH {
		log.Printf("invalid schema bytes length: %v\n", len(schemaBytes))
		return ""
	}
	data := make([]byte, 0, constant.JSON_SCHEMA_MAX_LENGTH*32)
	for i := 0; i < len(schemaBytes); i++ {
		data = append(data, schemaBytes[i][:]...)
	}
	return string(data)
}

func (c *CptServiceImpl) QueryCpt(cptId int) CptQueryResponse {
	resp := CptQueryResponse{}
	if cptId < 0 {
		resp.ErrCode = constant.CPT_ID_ILLEGAL
		return resp
	}

	values, err := c.contract.QueryCpt(nil, big.NewInt(int64(cptId)))
	if err != nil {
		resp.ErrCode = constant.TRANSACTION_EXECUTE_ERROR
		return resp
	}

	if values.Publisher.Hex() == constant.DID_EMPTY_ADDRESS {
		log.Printf("cpt not exist: %v\n", cptId)
		resp.ErrCode = constant.CPT_NOT_EXIST
		return resp
	}

	jsonSchema := parseJsonSchema(values.JsonSchemaArray)

	cpt := Cpt{
		BaseInfo: CptBaseInfo{
			CptId:      cptId,
			CptVersion: int(values.IntArray[0].Int64()),
		},
		JsonSchema: jsonSchema,
		Meta: CptMetaData{
			CptPublisher: common.ConvertAddressToDID(values.Publisher.Hex()),
			CptSignature: hex.EncodeToString(common.RSVToSignature(values.R, values.S, values.V)),
			Created:      values.IntArray[1].Uint64(),
			Updated:      values.IntArray[2].Uint64(),
		},
	}
	resp.Cpt = cpt
	resp.ErrCode = constant.SUCCESS
	return resp
}
