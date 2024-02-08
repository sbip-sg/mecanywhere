package didservice

import "encoding/json"

const (
	DidDocumentSerialVersionUid = 411522771907189878
)

type PublicKeyProperty struct {
	Id        string `json:"id"`
	Type      string `json:"type"`
	Owner     string `json:"owner"`
	PublicKey string `json:"publicKey"`
	Revoked   bool   `json:"revoked" default:"false"`
}

type AuthenticationProperty struct {
	Type      string `json:"type" default:"Secp256k1"`
	PublicKey string `json:"publicKey"`
	Revoked   bool   `json:"revoked" default:"false"`
}

type ServiceProperty struct {
	Type            string `json:"type"`
	ServiceEndpoint string `json:"serviceEndpoint"`
}

type DidDocument struct {
	ID               string                   `json:"id"`
	Created          uint64                   `json:"created"`
	SerialVersionUid uint64                   `json:"serialVersionUid"`
	Updated          uint64                   `json:"updated"`
	PublicKey        []PublicKeyProperty      `json:"publicKey"`
	Authentication   []AuthenticationProperty `json:"authentication"`
	Service          []ServiceProperty        `json:"service"`
}

func (d *DidDocument) Encode() ([]byte, error) {
	return json.Marshal(d)
}

func (d *DidDocument) Decode(data []byte) error {
	return json.Unmarshal(data, d)
}
