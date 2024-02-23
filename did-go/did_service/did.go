package didservice

import (
	"fmt"
	"math/big"
	"meca_did/contract/did"

	"github.com/ethereum/go-ethereum/core/types"
)

func printDIDAttributeChangedEvent(event *did.DidDIDAttributeChanged) {
	fmt.Printf("event.Identity: %v\nevent.Key: %v\nevent.Value: %v\nevent.PreviousBlock: %v\nevent.Updated: %v\n", event.Identity.Hex(), string(event.Key[:]), string(event.Value[:]), event.PreviousBlock, event.Updated)
}

type DIDAttributeChangedEventResponse struct {
	// don't know how to get event log
	Log           types.Log
	Identity      string
	Key           []byte
	Value         []byte
	PreviousBlock *big.Int
	Updated       *big.Int
}

func SerializeDIDAttributeChangedEvent(event *did.DidDIDAttributeChanged) DIDAttributeChangedEventResponse {
	return DIDAttributeChangedEventResponse{
		Log:           event.Raw,
		Identity:      event.Identity.Hex(),
		Key:           event.Key[:],
		Value:         event.Value,
		PreviousBlock: event.PreviousBlock,
		Updated:       event.Updated,
	}
}

func ReadDIDAttributeChangedEvent(it *did.DidDIDAttributeChangedIterator) (resp []DIDAttributeChangedEventResponse) {
	for it.Next() {
		// get the current log
		event := it.Event
		// do something with the log
		resp = append(resp, SerializeDIDAttributeChangedEvent(event))
	}
	return resp
}
