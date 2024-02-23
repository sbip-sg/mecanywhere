package main

import (
	"encoding/json"
	"os"
)

type ServerConfig struct {
	BlockChainAddr             string `json:"blockChainAddr"`
	DIDContract                string `json:"didContract"`
	DIDContractOwnerPrivateKey string `json:"didContractOwnerPrivateKey"`
	CPTContract                string `json:"cptContract"`
	Port                       int    `json:"port"`
}

func ParseServerConfig(filename string) (ServerConfig, error) {
	configData, err := os.ReadFile(filename)
	if err != nil {
		return ServerConfig{}, err
	}

	var cfg ServerConfig
	err = json.Unmarshal(configData, &cfg)
	if err != nil {
		return ServerConfig{}, err
	}
	return cfg, nil
}
