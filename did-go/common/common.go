package common

import (
	"math/big"
	"meca_did/constant"
	"strings"

	"github.com/ethereum/go-ethereum/core/types"
)

type TransactionInfo struct {
	BlockNumber big.Int
	TxHash      string
	TxIndex     uint
}

type ServiceResponseInfo struct {
	ErrCode constant.ErrorCode
	ErrMsg  string
	TxInfo  TransactionInfo
}

type DIDAuthentication struct {
	DID            string
	DIDPublicKeyId string
	DIDPrivateKey  string
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

func (i *TransactionInfo) SetTxInfo(receipt *types.Receipt) {
	i.BlockNumber = *receipt.BlockNumber
	i.TxHash = receipt.TxHash.String()
	i.TxIndex = receipt.TransactionIndex
}
