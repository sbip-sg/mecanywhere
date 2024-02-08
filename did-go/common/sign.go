package common

import (
	"crypto/ecdsa"

	"github.com/ethereum/go-ethereum/crypto"
)

func Sign(privateKey *ecdsa.PrivateKey, data []byte) ([]byte, error) {
	hash := crypto.Keccak256Hash(data)
	if signature, err := crypto.Sign(hash.Bytes(), privateKey); err != nil {
		return nil, err
	} else {
		return signature, nil
	}
}

func SignatureToRSV(signature []byte) (r, s [32]byte, v uint8) {
	copy(r[:], signature[:32])
	copy(s[:], signature[32:64])
	v = uint8(signature[64])
	return
}

func RSVToSignature(r, s [32]byte, v uint8) []byte {
	signature := make([]byte, 65)
	copy(signature[:32], r[:])
	copy(signature[32:64], s[:])
	signature[64] = byte(v)
	return signature
}

func VerifySignature(publicKey *ecdsa.PublicKey, data []byte, signature []byte) bool {
	return crypto.VerifySignature(crypto.FromECDSAPub(publicKey), data, signature[:len(signature)-1])
}
