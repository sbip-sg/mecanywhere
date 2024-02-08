package main

import (
	"crypto/ecdsa"
	"encoding/hex"
	"fmt"
	"math/big"
	"testing"

	"github.com/ethereum/go-ethereum/crypto"
)

type PROP struct {
	Val    string `json:"val"`
	Intval int    `json:"intval"`
}

// write a unit test wrapper

// the go-etherum library output public key in hex format has an additional 0x04 prefix compared to the java web3j package.
// checkout the below example to see how to convert between them
func TestKey(t *testing.T) {
	// test the old pair
	fmt.Printf("test the readme wallet pair\n")
	// testPrivateKeyStr := "0d8c2fee2d85f6f8dc47f36da23ea1fd29b1126c48bac505d159bbf3f3c8e0bf"
	testPrivateKeyStr := "41055558ff6c8d5340d9c6ebfbaa2aa96db811254cc8be8440f5a4abf54f51e6"
	testPrivateKey, err := crypto.HexToECDSA(testPrivateKeyStr)
	if err != nil {
		panic(err)
	}
	fmt.Printf("testPrivateKey: %v\n", testPrivateKey)
	// get the public key
	testPublicKey := testPrivateKey.Public()
	// convert public key to hex string
	address := crypto.PubkeyToAddress(*testPublicKey.(*ecdsa.PublicKey)).Hex()
	fmt.Printf("address: %v\n", address)
	pubBytes := crypto.FromECDSAPub(testPublicKey.(*ecdsa.PublicKey))
	fmt.Printf("testPublicKey: %v\n", hex.EncodeToString(pubBytes))
	// encode bytes to an integer: this is the format of stringify public key in the java did service
	pubInt := new(big.Int).SetBytes(pubBytes)
	fmt.Printf("pubInt: %v\n", pubInt)

	// remove the first byte that corresponds to the prefix 0x04
	fmt.Printf("\nremove the first byte\n")
	fmt.Printf("testPublicKey: %v\n", hex.EncodeToString(pubBytes[1:]))
	// encode bytes to an integer: this is the format of stringify public key in the java did service
	fmt.Printf("pubInt: %v\n", new(big.Int).SetBytes(pubBytes[1:]))

	// reverse the process
	fmt.Printf("\nreverse the process\n")
	pubBytes = pubInt.Bytes()
	fmt.Printf("testPublicKey: %v\n", hex.EncodeToString(pubBytes))
	pubKey, err := crypto.UnmarshalPubkey(pubBytes)
	if err != nil {
		panic(err)
	}
	address = crypto.PubkeyToAddress(*pubKey).Hex()
	fmt.Printf("address: %v\n", address)
	// from the hex string
	hexStr := hex.EncodeToString(pubBytes)
	bytes := make([]byte, hex.DecodedLen(len(hexStr)))
	_, err = hex.Decode(bytes, []byte(hexStr))
	if err != nil {
		panic(err)
	}
	fmt.Printf("address: %v\n", crypto.PubkeyToAddress(*pubKey).Hex())

	// test the new pair
	fmt.Printf("\ntest the readme registered pair, a public key generated from web3j\n")
	pubStr2 := "9162489900438906348702968436157779450275819589845486784832046751964054847774610311218195072132906483269992698213206439837565459982787113366244600208153925"

	pubInt2 := new(big.Int)
	pubInt2.SetString(pubStr2, 10)
	fmt.Printf("pubInt2: %v\n", pubInt2)
	pubBytes2 := pubInt2.Bytes()
	fmt.Printf("pubBytes2: %v\n", hex.EncodeToString(pubBytes2))
	// need to add the prefix 0x04 to allow go-ethereum to parse it.
	pubBytes2 = append([]byte{0x04}, pubBytes2...)
	pubKey2, err := crypto.UnmarshalPubkey(pubBytes2)
	if err != nil {
		panic(err)
	}
	fmt.Printf("pubKey2: %v\n", pubKey2)
	// convert public key to hex string
	address2 := crypto.PubkeyToAddress(*pubKey2).Hex()
	fmt.Printf("address2: %v\n", address2)

}
