package common

import (
	"meca_did/constant"
	"strings"

	ethcommon "github.com/ethereum/go-ethereum/common"
)

func IsDidValid(did string) bool {
	return len(did) > 0 && strings.HasPrefix(did, constant.DID_PREFIX) && ethcommon.IsHexAddress(did[len(constant.DID_PREFIX):])
}
