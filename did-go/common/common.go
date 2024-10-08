package common

import (
	"encoding/json"
	"math/big"
	"meca_did/constant"
	"strings"

	ethcommon "github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/core/types"
)

type TransactionInfo struct {
	BlockNumber big.Int `json:"blockNumber"`
	TxHash      string  `json:"txHash"`
	TxIndex     uint    `json:"txIndex"`
}

func (i *TransactionInfo) SetTxInfo(receipt *types.Receipt) {
	i.BlockNumber = *receipt.BlockNumber
	i.TxHash = receipt.TxHash.String()
	i.TxIndex = receipt.TransactionIndex
}

type ServiceResponseInfo struct {
	ErrCode constant.ErrorCode `json:"errCode"`
	ErrMsg  string             `json:"errMsg"`
	TxInfo  TransactionInfo    `json:"txInfo"`
}

func IsCptJsonSchemaValid(cptJsonSchema string) bool {
	if len(cptJsonSchema) == 0 || len(cptJsonSchema) > constant.JSON_SCHEMA_MAX_LENGTH {
		return false
	}
	return json.Unmarshal([]byte(cptJsonSchema), &map[string]interface{}{}) == nil
}

type DIDAuthentication struct {
	DID           string `json:"did"`
	DIDPrivateKey string `json:"didPrivateKey"`
}

func ConvertDIDToAddress(did string) string {
	if did == "" || !strings.HasPrefix(did, constant.DID_PREFIX) {
		return ""
	}
	return did[len(constant.DID_PREFIX):]
}

func ConvertAddressToDID(address string) string {
	if address == "" {
		return ""
	}
	if !strings.HasPrefix(address, "0x") {
		return constant.DID_PREFIX + "0x" + address
	}
	return constant.DID_PREFIX + address
}

func IsDidValid(did string) bool {
	return len(did) > 0 && strings.HasPrefix(did, constant.DID_PREFIX) && ethcommon.IsHexAddress(did[len(constant.DID_PREFIX):])
}
