// Code generated - DO NOT EDIT.
// This file is a generated binding and any manual changes will be lost.

package did

import (
	"errors"
	"math/big"
	"strings"

	ethereum "github.com/ethereum/go-ethereum"
	"github.com/ethereum/go-ethereum/accounts/abi"
	"github.com/ethereum/go-ethereum/accounts/abi/bind"
	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/core/types"
	"github.com/ethereum/go-ethereum/event"
)

// Reference imports to suppress errors if they are not otherwise used.
var (
	_ = errors.New
	_ = big.NewInt
	_ = strings.NewReader
	_ = ethereum.NotFound
	_ = bind.Bind
	_ = common.Big1
	_ = types.BloomLookup
	_ = event.NewSubscription
	_ = abi.ConvertType
)

// DidMetaData contains all meta data concerning the Did contract.
var DidMetaData = &bind.MetaData{
	ABI: "[{\"inputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"constructor\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":true,\"internalType\":\"address\",\"name\":\"identity\",\"type\":\"address\"},{\"indexed\":false,\"internalType\":\"bytes32\",\"name\":\"key\",\"type\":\"bytes32\"},{\"indexed\":false,\"internalType\":\"bytes\",\"name\":\"value\",\"type\":\"bytes\"},{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"previousBlock\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"int256\",\"name\":\"updated\",\"type\":\"int256\"}],\"name\":\"DIDAttributeChanged\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":true,\"internalType\":\"address\",\"name\":\"identity\",\"type\":\"address\"},{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"previousBlock\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"int256\",\"name\":\"created\",\"type\":\"int256\"}],\"name\":\"DIDHistoryEvent\",\"type\":\"event\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"identity\",\"type\":\"address\"},{\"internalType\":\"bytes\",\"name\":\"auth\",\"type\":\"bytes\"},{\"internalType\":\"bytes\",\"name\":\"created\",\"type\":\"bytes\"},{\"internalType\":\"int256\",\"name\":\"updated\",\"type\":\"int256\"}],\"name\":\"createDID\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"getDIDCount\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"getFirstBlockNum\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"getLatestBlockNum\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"identity\",\"type\":\"address\"}],\"name\":\"getLatestRelatedBlock\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"currentBlockNum\",\"type\":\"uint256\"}],\"name\":\"getNextBlockNumByBlockNum\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"identity\",\"type\":\"address\"}],\"name\":\"identityExists\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"\",\"type\":\"bool\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"identity\",\"type\":\"address\"},{\"internalType\":\"bytes32\",\"name\":\"key\",\"type\":\"bytes32\"},{\"internalType\":\"bytes\",\"name\":\"value\",\"type\":\"bytes\"},{\"internalType\":\"int256\",\"name\":\"updated\",\"type\":\"int256\"}],\"name\":\"setAttribute\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"}]",
	Bin: "0x60806040525f600355348015610013575f80fd5b5043600181905550600154600281905550610b92806100315f395ff3fe608060405234801561000f575f80fd5b5060043610610086575f3560e01c80638cf592d6116100595780638cf592d614610124578063baf80dff14610142578063e49d8ece1461015e578063f03b7d5b1461017c57610086565b80631ba200c71461008a5780633cf239db146100a85780634298ab94146100c45780634d221b85146100f4575b5f80fd5b6100926101ac565b60405161009f91906105ea565b60405180910390f35b6100c260048036038101906100bd9190610810565b6101b5565b005b6100de60048036038101906100d99190610890565b61028c565b6040516100eb91906105ea565b60405180910390f35b61010e60048036038101906101099190610890565b6102d1565b60405161011b91906108d5565b60405180910390f35b61012c610361565b60405161013991906105ea565b60405180910390f35b61015c600480360381019061015791906108ee565b61036a565b005b6101666105af565b60405161017391906105ea565b60405180910390f35b610196600480360381019061019191906109b4565b6105b8565b6040516101a391906105ea565b60405180910390f35b5f600154905090565b8373ffffffffffffffffffffffffffffffffffffffff167fd4cc5e0d855780794bdbe124fca8f62006ed1c8d10ca9a460114d3c5d3b138b884845f808973ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f20548560405161023d9493929190610a77565b60405180910390a2435f808673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f208190555050505050565b5f805f8373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f20549050919050565b5f8173ffffffffffffffffffffffffffffffffffffffff165f73ffffffffffffffffffffffffffffffffffffffff161415801561034a57505f808373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f20545f14155b15610358576001905061035c565b5f90505b919050565b5f600354905090565b8373ffffffffffffffffffffffffffffffffffffffff167fd4cc5e0d855780794bdbe124fca8f62006ed1c8d10ca9a460114d3c5d3b138b87f6372656174656400000000000000000000000000000000000000000000000000845f808973ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f2054856040516104129493929190610a77565b60405180910390a28373ffffffffffffffffffffffffffffffffffffffff167fd4cc5e0d855780794bdbe124fca8f62006ed1c8d10ca9a460114d3c5d3b138b87f7075624b65790000000000000000000000000000000000000000000000000000855f808973ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f2054856040516104c29493929190610a77565b60405180910390a2435f808673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f208190555060025443111561052e574360045f60025481526020019081526020015f20819055505b8373ffffffffffffffffffffffffffffffffffffffff167fac7b90e309a0b0289d7b1e6a75fb7df9b0fc1b4a65e51b90cc47d9156d876f1e60025483604051610578929190610ac1565b60405180910390a260025443111561059257436002819055505b60035f8154809291906105a490610b15565b919050555050505050565b5f600254905090565b5f60045f8381526020019081526020015f20549050919050565b5f819050919050565b6105e4816105d2565b82525050565b5f6020820190506105fd5f8301846105db565b92915050565b5f604051905090565b5f80fd5b5f80fd5b5f73ffffffffffffffffffffffffffffffffffffffff82169050919050565b5f61063d82610614565b9050919050565b61064d81610633565b8114610657575f80fd5b50565b5f8135905061066881610644565b92915050565b5f819050919050565b6106808161066e565b811461068a575f80fd5b50565b5f8135905061069b81610677565b92915050565b5f80fd5b5f80fd5b5f601f19601f8301169050919050565b7f4e487b71000000000000000000000000000000000000000000000000000000005f52604160045260245ffd5b6106ef826106a9565b810181811067ffffffffffffffff8211171561070e5761070d6106b9565b5b80604052505050565b5f610720610603565b905061072c82826106e6565b919050565b5f67ffffffffffffffff82111561074b5761074a6106b9565b5b610754826106a9565b9050602081019050919050565b828183375f83830152505050565b5f61078161077c84610731565b610717565b90508281526020810184848401111561079d5761079c6106a5565b5b6107a8848285610761565b509392505050565b5f82601f8301126107c4576107c36106a1565b5b81356107d484826020860161076f565b91505092915050565b5f819050919050565b6107ef816107dd565b81146107f9575f80fd5b50565b5f8135905061080a816107e6565b92915050565b5f805f80608085870312156108285761082761060c565b5b5f6108358782880161065a565b94505060206108468782880161068d565b935050604085013567ffffffffffffffff81111561086757610866610610565b5b610873878288016107b0565b9250506060610884878288016107fc565b91505092959194509250565b5f602082840312156108a5576108a461060c565b5b5f6108b28482850161065a565b91505092915050565b5f8115159050919050565b6108cf816108bb565b82525050565b5f6020820190506108e85f8301846108c6565b92915050565b5f805f80608085870312156109065761090561060c565b5b5f6109138782880161065a565b945050602085013567ffffffffffffffff81111561093457610933610610565b5b610940878288016107b0565b935050604085013567ffffffffffffffff81111561096157610960610610565b5b61096d878288016107b0565b925050606061097e878288016107fc565b91505092959194509250565b610993816105d2565b811461099d575f80fd5b50565b5f813590506109ae8161098a565b92915050565b5f602082840312156109c9576109c861060c565b5b5f6109d6848285016109a0565b91505092915050565b6109e88161066e565b82525050565b5f81519050919050565b5f82825260208201905092915050565b5f5b83811015610a25578082015181840152602081019050610a0a565b5f8484015250505050565b5f610a3a826109ee565b610a4481856109f8565b9350610a54818560208601610a08565b610a5d816106a9565b840191505092915050565b610a71816107dd565b82525050565b5f608082019050610a8a5f8301876109df565b8181036020830152610a9c8186610a30565b9050610aab60408301856105db565b610ab86060830184610a68565b95945050505050565b5f604082019050610ad45f8301856105db565b610ae16020830184610a68565b9392505050565b7f4e487b71000000000000000000000000000000000000000000000000000000005f52601160045260245ffd5b5f610b1f826105d2565b91507fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8203610b5157610b50610ae8565b5b60018201905091905056fea2646970667358221220dced13f4a8d295f6db15f451318bec1e206e5de422365ebc1d6a8c8a831db5dc64736f6c63430008180033",
}

// DidABI is the input ABI used to generate the binding from.
// Deprecated: Use DidMetaData.ABI instead.
var DidABI = DidMetaData.ABI

// DidBin is the compiled bytecode used for deploying new contracts.
// Deprecated: Use DidMetaData.Bin instead.
var DidBin = DidMetaData.Bin

// DeployDid deploys a new Ethereum contract, binding an instance of Did to it.
func DeployDid(auth *bind.TransactOpts, backend bind.ContractBackend) (common.Address, *types.Transaction, *Did, error) {
	parsed, err := DidMetaData.GetAbi()
	if err != nil {
		return common.Address{}, nil, nil, err
	}
	if parsed == nil {
		return common.Address{}, nil, nil, errors.New("GetABI returned nil")
	}

	address, tx, contract, err := bind.DeployContract(auth, *parsed, common.FromHex(DidBin), backend)
	if err != nil {
		return common.Address{}, nil, nil, err
	}
	return address, tx, &Did{DidCaller: DidCaller{contract: contract}, DidTransactor: DidTransactor{contract: contract}, DidFilterer: DidFilterer{contract: contract}}, nil
}

// Did is an auto generated Go binding around an Ethereum contract.
type Did struct {
	DidCaller     // Read-only binding to the contract
	DidTransactor // Write-only binding to the contract
	DidFilterer   // Log filterer for contract events
}

// DidCaller is an auto generated read-only Go binding around an Ethereum contract.
type DidCaller struct {
	contract *bind.BoundContract // Generic contract wrapper for the low level calls
}

// DidTransactor is an auto generated write-only Go binding around an Ethereum contract.
type DidTransactor struct {
	contract *bind.BoundContract // Generic contract wrapper for the low level calls
}

// DidFilterer is an auto generated log filtering Go binding around an Ethereum contract events.
type DidFilterer struct {
	contract *bind.BoundContract // Generic contract wrapper for the low level calls
}

// DidSession is an auto generated Go binding around an Ethereum contract,
// with pre-set call and transact options.
type DidSession struct {
	Contract     *Did              // Generic contract binding to set the session for
	CallOpts     bind.CallOpts     // Call options to use throughout this session
	TransactOpts bind.TransactOpts // Transaction auth options to use throughout this session
}

// DidCallerSession is an auto generated read-only Go binding around an Ethereum contract,
// with pre-set call options.
type DidCallerSession struct {
	Contract *DidCaller    // Generic contract caller binding to set the session for
	CallOpts bind.CallOpts // Call options to use throughout this session
}

// DidTransactorSession is an auto generated write-only Go binding around an Ethereum contract,
// with pre-set transact options.
type DidTransactorSession struct {
	Contract     *DidTransactor    // Generic contract transactor binding to set the session for
	TransactOpts bind.TransactOpts // Transaction auth options to use throughout this session
}

// DidRaw is an auto generated low-level Go binding around an Ethereum contract.
type DidRaw struct {
	Contract *Did // Generic contract binding to access the raw methods on
}

// DidCallerRaw is an auto generated low-level read-only Go binding around an Ethereum contract.
type DidCallerRaw struct {
	Contract *DidCaller // Generic read-only contract binding to access the raw methods on
}

// DidTransactorRaw is an auto generated low-level write-only Go binding around an Ethereum contract.
type DidTransactorRaw struct {
	Contract *DidTransactor // Generic write-only contract binding to access the raw methods on
}

// NewDid creates a new instance of Did, bound to a specific deployed contract.
func NewDid(address common.Address, backend bind.ContractBackend) (*Did, error) {
	contract, err := bindDid(address, backend, backend, backend)
	if err != nil {
		return nil, err
	}
	return &Did{DidCaller: DidCaller{contract: contract}, DidTransactor: DidTransactor{contract: contract}, DidFilterer: DidFilterer{contract: contract}}, nil
}

// NewDidCaller creates a new read-only instance of Did, bound to a specific deployed contract.
func NewDidCaller(address common.Address, caller bind.ContractCaller) (*DidCaller, error) {
	contract, err := bindDid(address, caller, nil, nil)
	if err != nil {
		return nil, err
	}
	return &DidCaller{contract: contract}, nil
}

// NewDidTransactor creates a new write-only instance of Did, bound to a specific deployed contract.
func NewDidTransactor(address common.Address, transactor bind.ContractTransactor) (*DidTransactor, error) {
	contract, err := bindDid(address, nil, transactor, nil)
	if err != nil {
		return nil, err
	}
	return &DidTransactor{contract: contract}, nil
}

// NewDidFilterer creates a new log filterer instance of Did, bound to a specific deployed contract.
func NewDidFilterer(address common.Address, filterer bind.ContractFilterer) (*DidFilterer, error) {
	contract, err := bindDid(address, nil, nil, filterer)
	if err != nil {
		return nil, err
	}
	return &DidFilterer{contract: contract}, nil
}

// bindDid binds a generic wrapper to an already deployed contract.
func bindDid(address common.Address, caller bind.ContractCaller, transactor bind.ContractTransactor, filterer bind.ContractFilterer) (*bind.BoundContract, error) {
	parsed, err := DidMetaData.GetAbi()
	if err != nil {
		return nil, err
	}
	return bind.NewBoundContract(address, *parsed, caller, transactor, filterer), nil
}

// Call invokes the (constant) contract method with params as input values and
// sets the output to result. The result type might be a single field for simple
// returns, a slice of interfaces for anonymous returns and a struct for named
// returns.
func (_Did *DidRaw) Call(opts *bind.CallOpts, result *[]interface{}, method string, params ...interface{}) error {
	return _Did.Contract.DidCaller.contract.Call(opts, result, method, params...)
}

// Transfer initiates a plain transaction to move funds to the contract, calling
// its default method if one is available.
func (_Did *DidRaw) Transfer(opts *bind.TransactOpts) (*types.Transaction, error) {
	return _Did.Contract.DidTransactor.contract.Transfer(opts)
}

// Transact invokes the (paid) contract method with params as input values.
func (_Did *DidRaw) Transact(opts *bind.TransactOpts, method string, params ...interface{}) (*types.Transaction, error) {
	return _Did.Contract.DidTransactor.contract.Transact(opts, method, params...)
}

// Call invokes the (constant) contract method with params as input values and
// sets the output to result. The result type might be a single field for simple
// returns, a slice of interfaces for anonymous returns and a struct for named
// returns.
func (_Did *DidCallerRaw) Call(opts *bind.CallOpts, result *[]interface{}, method string, params ...interface{}) error {
	return _Did.Contract.contract.Call(opts, result, method, params...)
}

// Transfer initiates a plain transaction to move funds to the contract, calling
// its default method if one is available.
func (_Did *DidTransactorRaw) Transfer(opts *bind.TransactOpts) (*types.Transaction, error) {
	return _Did.Contract.contract.Transfer(opts)
}

// Transact invokes the (paid) contract method with params as input values.
func (_Did *DidTransactorRaw) Transact(opts *bind.TransactOpts, method string, params ...interface{}) (*types.Transaction, error) {
	return _Did.Contract.contract.Transact(opts, method, params...)
}

// GetDIDCount is a free data retrieval call binding the contract method 0x8cf592d6.
//
// Solidity: function getDIDCount() view returns(uint256)
func (_Did *DidCaller) GetDIDCount(opts *bind.CallOpts) (*big.Int, error) {
	var out []interface{}
	err := _Did.contract.Call(opts, &out, "getDIDCount")

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// GetDIDCount is a free data retrieval call binding the contract method 0x8cf592d6.
//
// Solidity: function getDIDCount() view returns(uint256)
func (_Did *DidSession) GetDIDCount() (*big.Int, error) {
	return _Did.Contract.GetDIDCount(&_Did.CallOpts)
}

// GetDIDCount is a free data retrieval call binding the contract method 0x8cf592d6.
//
// Solidity: function getDIDCount() view returns(uint256)
func (_Did *DidCallerSession) GetDIDCount() (*big.Int, error) {
	return _Did.Contract.GetDIDCount(&_Did.CallOpts)
}

// GetFirstBlockNum is a free data retrieval call binding the contract method 0x1ba200c7.
//
// Solidity: function getFirstBlockNum() view returns(uint256)
func (_Did *DidCaller) GetFirstBlockNum(opts *bind.CallOpts) (*big.Int, error) {
	var out []interface{}
	err := _Did.contract.Call(opts, &out, "getFirstBlockNum")

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// GetFirstBlockNum is a free data retrieval call binding the contract method 0x1ba200c7.
//
// Solidity: function getFirstBlockNum() view returns(uint256)
func (_Did *DidSession) GetFirstBlockNum() (*big.Int, error) {
	return _Did.Contract.GetFirstBlockNum(&_Did.CallOpts)
}

// GetFirstBlockNum is a free data retrieval call binding the contract method 0x1ba200c7.
//
// Solidity: function getFirstBlockNum() view returns(uint256)
func (_Did *DidCallerSession) GetFirstBlockNum() (*big.Int, error) {
	return _Did.Contract.GetFirstBlockNum(&_Did.CallOpts)
}

// GetLatestBlockNum is a free data retrieval call binding the contract method 0xe49d8ece.
//
// Solidity: function getLatestBlockNum() view returns(uint256)
func (_Did *DidCaller) GetLatestBlockNum(opts *bind.CallOpts) (*big.Int, error) {
	var out []interface{}
	err := _Did.contract.Call(opts, &out, "getLatestBlockNum")

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// GetLatestBlockNum is a free data retrieval call binding the contract method 0xe49d8ece.
//
// Solidity: function getLatestBlockNum() view returns(uint256)
func (_Did *DidSession) GetLatestBlockNum() (*big.Int, error) {
	return _Did.Contract.GetLatestBlockNum(&_Did.CallOpts)
}

// GetLatestBlockNum is a free data retrieval call binding the contract method 0xe49d8ece.
//
// Solidity: function getLatestBlockNum() view returns(uint256)
func (_Did *DidCallerSession) GetLatestBlockNum() (*big.Int, error) {
	return _Did.Contract.GetLatestBlockNum(&_Did.CallOpts)
}

// GetLatestRelatedBlock is a free data retrieval call binding the contract method 0x4298ab94.
//
// Solidity: function getLatestRelatedBlock(address identity) view returns(uint256)
func (_Did *DidCaller) GetLatestRelatedBlock(opts *bind.CallOpts, identity common.Address) (*big.Int, error) {
	var out []interface{}
	err := _Did.contract.Call(opts, &out, "getLatestRelatedBlock", identity)

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// GetLatestRelatedBlock is a free data retrieval call binding the contract method 0x4298ab94.
//
// Solidity: function getLatestRelatedBlock(address identity) view returns(uint256)
func (_Did *DidSession) GetLatestRelatedBlock(identity common.Address) (*big.Int, error) {
	return _Did.Contract.GetLatestRelatedBlock(&_Did.CallOpts, identity)
}

// GetLatestRelatedBlock is a free data retrieval call binding the contract method 0x4298ab94.
//
// Solidity: function getLatestRelatedBlock(address identity) view returns(uint256)
func (_Did *DidCallerSession) GetLatestRelatedBlock(identity common.Address) (*big.Int, error) {
	return _Did.Contract.GetLatestRelatedBlock(&_Did.CallOpts, identity)
}

// GetNextBlockNumByBlockNum is a free data retrieval call binding the contract method 0xf03b7d5b.
//
// Solidity: function getNextBlockNumByBlockNum(uint256 currentBlockNum) view returns(uint256)
func (_Did *DidCaller) GetNextBlockNumByBlockNum(opts *bind.CallOpts, currentBlockNum *big.Int) (*big.Int, error) {
	var out []interface{}
	err := _Did.contract.Call(opts, &out, "getNextBlockNumByBlockNum", currentBlockNum)

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// GetNextBlockNumByBlockNum is a free data retrieval call binding the contract method 0xf03b7d5b.
//
// Solidity: function getNextBlockNumByBlockNum(uint256 currentBlockNum) view returns(uint256)
func (_Did *DidSession) GetNextBlockNumByBlockNum(currentBlockNum *big.Int) (*big.Int, error) {
	return _Did.Contract.GetNextBlockNumByBlockNum(&_Did.CallOpts, currentBlockNum)
}

// GetNextBlockNumByBlockNum is a free data retrieval call binding the contract method 0xf03b7d5b.
//
// Solidity: function getNextBlockNumByBlockNum(uint256 currentBlockNum) view returns(uint256)
func (_Did *DidCallerSession) GetNextBlockNumByBlockNum(currentBlockNum *big.Int) (*big.Int, error) {
	return _Did.Contract.GetNextBlockNumByBlockNum(&_Did.CallOpts, currentBlockNum)
}

// IdentityExists is a free data retrieval call binding the contract method 0x4d221b85.
//
// Solidity: function identityExists(address identity) view returns(bool)
func (_Did *DidCaller) IdentityExists(opts *bind.CallOpts, identity common.Address) (bool, error) {
	var out []interface{}
	err := _Did.contract.Call(opts, &out, "identityExists", identity)

	if err != nil {
		return *new(bool), err
	}

	out0 := *abi.ConvertType(out[0], new(bool)).(*bool)

	return out0, err

}

// IdentityExists is a free data retrieval call binding the contract method 0x4d221b85.
//
// Solidity: function identityExists(address identity) view returns(bool)
func (_Did *DidSession) IdentityExists(identity common.Address) (bool, error) {
	return _Did.Contract.IdentityExists(&_Did.CallOpts, identity)
}

// IdentityExists is a free data retrieval call binding the contract method 0x4d221b85.
//
// Solidity: function identityExists(address identity) view returns(bool)
func (_Did *DidCallerSession) IdentityExists(identity common.Address) (bool, error) {
	return _Did.Contract.IdentityExists(&_Did.CallOpts, identity)
}

// CreateDID is a paid mutator transaction binding the contract method 0xbaf80dff.
//
// Solidity: function createDID(address identity, bytes auth, bytes created, int256 updated) returns()
func (_Did *DidTransactor) CreateDID(opts *bind.TransactOpts, identity common.Address, auth []byte, created []byte, updated *big.Int) (*types.Transaction, error) {
	return _Did.contract.Transact(opts, "createDID", identity, auth, created, updated)
}

// CreateDID is a paid mutator transaction binding the contract method 0xbaf80dff.
//
// Solidity: function createDID(address identity, bytes auth, bytes created, int256 updated) returns()
func (_Did *DidSession) CreateDID(identity common.Address, auth []byte, created []byte, updated *big.Int) (*types.Transaction, error) {
	return _Did.Contract.CreateDID(&_Did.TransactOpts, identity, auth, created, updated)
}

// CreateDID is a paid mutator transaction binding the contract method 0xbaf80dff.
//
// Solidity: function createDID(address identity, bytes auth, bytes created, int256 updated) returns()
func (_Did *DidTransactorSession) CreateDID(identity common.Address, auth []byte, created []byte, updated *big.Int) (*types.Transaction, error) {
	return _Did.Contract.CreateDID(&_Did.TransactOpts, identity, auth, created, updated)
}

// SetAttribute is a paid mutator transaction binding the contract method 0x3cf239db.
//
// Solidity: function setAttribute(address identity, bytes32 key, bytes value, int256 updated) returns()
func (_Did *DidTransactor) SetAttribute(opts *bind.TransactOpts, identity common.Address, key [32]byte, value []byte, updated *big.Int) (*types.Transaction, error) {
	return _Did.contract.Transact(opts, "setAttribute", identity, key, value, updated)
}

// SetAttribute is a paid mutator transaction binding the contract method 0x3cf239db.
//
// Solidity: function setAttribute(address identity, bytes32 key, bytes value, int256 updated) returns()
func (_Did *DidSession) SetAttribute(identity common.Address, key [32]byte, value []byte, updated *big.Int) (*types.Transaction, error) {
	return _Did.Contract.SetAttribute(&_Did.TransactOpts, identity, key, value, updated)
}

// SetAttribute is a paid mutator transaction binding the contract method 0x3cf239db.
//
// Solidity: function setAttribute(address identity, bytes32 key, bytes value, int256 updated) returns()
func (_Did *DidTransactorSession) SetAttribute(identity common.Address, key [32]byte, value []byte, updated *big.Int) (*types.Transaction, error) {
	return _Did.Contract.SetAttribute(&_Did.TransactOpts, identity, key, value, updated)
}

// DidDIDAttributeChangedIterator is returned from FilterDIDAttributeChanged and is used to iterate over the raw logs and unpacked data for DIDAttributeChanged events raised by the Did contract.
type DidDIDAttributeChangedIterator struct {
	Event *DidDIDAttributeChanged // Event containing the contract specifics and raw log

	contract *bind.BoundContract // Generic contract to use for unpacking event data
	event    string              // Event name to use for unpacking event data

	logs chan types.Log        // Log channel receiving the found contract events
	sub  ethereum.Subscription // Subscription for errors, completion and termination
	done bool                  // Whether the subscription completed delivering logs
	fail error                 // Occurred error to stop iteration
}

// Next advances the iterator to the subsequent event, returning whether there
// are any more events found. In case of a retrieval or parsing error, false is
// returned and Error() can be queried for the exact failure.
func (it *DidDIDAttributeChangedIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(DidDIDAttributeChanged)
			if err := it.contract.UnpackLog(it.Event, it.event, log); err != nil {
				it.fail = err
				return false
			}
			it.Event.Raw = log
			return true

		default:
			return false
		}
	}
	// Iterator still in progress, wait for either a data or an error event
	select {
	case log := <-it.logs:
		it.Event = new(DidDIDAttributeChanged)
		if err := it.contract.UnpackLog(it.Event, it.event, log); err != nil {
			it.fail = err
			return false
		}
		it.Event.Raw = log
		return true

	case err := <-it.sub.Err():
		it.done = true
		it.fail = err
		return it.Next()
	}
}

// Error returns any retrieval or parsing error occurred during filtering.
func (it *DidDIDAttributeChangedIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *DidDIDAttributeChangedIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// DidDIDAttributeChanged represents a DIDAttributeChanged event raised by the Did contract.
type DidDIDAttributeChanged struct {
	Identity      common.Address
	Key           [32]byte
	Value         []byte
	PreviousBlock *big.Int
	Updated       *big.Int
	Raw           types.Log // Blockchain specific contextual infos
}

// FilterDIDAttributeChanged is a free log retrieval operation binding the contract event 0xd4cc5e0d855780794bdbe124fca8f62006ed1c8d10ca9a460114d3c5d3b138b8.
//
// Solidity: event DIDAttributeChanged(address indexed identity, bytes32 key, bytes value, uint256 previousBlock, int256 updated)
func (_Did *DidFilterer) FilterDIDAttributeChanged(opts *bind.FilterOpts, identity []common.Address) (*DidDIDAttributeChangedIterator, error) {

	var identityRule []interface{}
	for _, identityItem := range identity {
		identityRule = append(identityRule, identityItem)
	}

	logs, sub, err := _Did.contract.FilterLogs(opts, "DIDAttributeChanged", identityRule)
	if err != nil {
		return nil, err
	}
	return &DidDIDAttributeChangedIterator{contract: _Did.contract, event: "DIDAttributeChanged", logs: logs, sub: sub}, nil
}

// WatchDIDAttributeChanged is a free log subscription operation binding the contract event 0xd4cc5e0d855780794bdbe124fca8f62006ed1c8d10ca9a460114d3c5d3b138b8.
//
// Solidity: event DIDAttributeChanged(address indexed identity, bytes32 key, bytes value, uint256 previousBlock, int256 updated)
func (_Did *DidFilterer) WatchDIDAttributeChanged(opts *bind.WatchOpts, sink chan<- *DidDIDAttributeChanged, identity []common.Address) (event.Subscription, error) {

	var identityRule []interface{}
	for _, identityItem := range identity {
		identityRule = append(identityRule, identityItem)
	}

	logs, sub, err := _Did.contract.WatchLogs(opts, "DIDAttributeChanged", identityRule)
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(DidDIDAttributeChanged)
				if err := _Did.contract.UnpackLog(event, "DIDAttributeChanged", log); err != nil {
					return err
				}
				event.Raw = log

				select {
				case sink <- event:
				case err := <-sub.Err():
					return err
				case <-quit:
					return nil
				}
			case err := <-sub.Err():
				return err
			case <-quit:
				return nil
			}
		}
	}), nil
}

// ParseDIDAttributeChanged is a log parse operation binding the contract event 0xd4cc5e0d855780794bdbe124fca8f62006ed1c8d10ca9a460114d3c5d3b138b8.
//
// Solidity: event DIDAttributeChanged(address indexed identity, bytes32 key, bytes value, uint256 previousBlock, int256 updated)
func (_Did *DidFilterer) ParseDIDAttributeChanged(log types.Log) (*DidDIDAttributeChanged, error) {
	event := new(DidDIDAttributeChanged)
	if err := _Did.contract.UnpackLog(event, "DIDAttributeChanged", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}

// DidDIDHistoryEventIterator is returned from FilterDIDHistoryEvent and is used to iterate over the raw logs and unpacked data for DIDHistoryEvent events raised by the Did contract.
type DidDIDHistoryEventIterator struct {
	Event *DidDIDHistoryEvent // Event containing the contract specifics and raw log

	contract *bind.BoundContract // Generic contract to use for unpacking event data
	event    string              // Event name to use for unpacking event data

	logs chan types.Log        // Log channel receiving the found contract events
	sub  ethereum.Subscription // Subscription for errors, completion and termination
	done bool                  // Whether the subscription completed delivering logs
	fail error                 // Occurred error to stop iteration
}

// Next advances the iterator to the subsequent event, returning whether there
// are any more events found. In case of a retrieval or parsing error, false is
// returned and Error() can be queried for the exact failure.
func (it *DidDIDHistoryEventIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(DidDIDHistoryEvent)
			if err := it.contract.UnpackLog(it.Event, it.event, log); err != nil {
				it.fail = err
				return false
			}
			it.Event.Raw = log
			return true

		default:
			return false
		}
	}
	// Iterator still in progress, wait for either a data or an error event
	select {
	case log := <-it.logs:
		it.Event = new(DidDIDHistoryEvent)
		if err := it.contract.UnpackLog(it.Event, it.event, log); err != nil {
			it.fail = err
			return false
		}
		it.Event.Raw = log
		return true

	case err := <-it.sub.Err():
		it.done = true
		it.fail = err
		return it.Next()
	}
}

// Error returns any retrieval or parsing error occurred during filtering.
func (it *DidDIDHistoryEventIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *DidDIDHistoryEventIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// DidDIDHistoryEvent represents a DIDHistoryEvent event raised by the Did contract.
type DidDIDHistoryEvent struct {
	Identity      common.Address
	PreviousBlock *big.Int
	Created       *big.Int
	Raw           types.Log // Blockchain specific contextual infos
}

// FilterDIDHistoryEvent is a free log retrieval operation binding the contract event 0xac7b90e309a0b0289d7b1e6a75fb7df9b0fc1b4a65e51b90cc47d9156d876f1e.
//
// Solidity: event DIDHistoryEvent(address indexed identity, uint256 previousBlock, int256 created)
func (_Did *DidFilterer) FilterDIDHistoryEvent(opts *bind.FilterOpts, identity []common.Address) (*DidDIDHistoryEventIterator, error) {

	var identityRule []interface{}
	for _, identityItem := range identity {
		identityRule = append(identityRule, identityItem)
	}

	logs, sub, err := _Did.contract.FilterLogs(opts, "DIDHistoryEvent", identityRule)
	if err != nil {
		return nil, err
	}
	return &DidDIDHistoryEventIterator{contract: _Did.contract, event: "DIDHistoryEvent", logs: logs, sub: sub}, nil
}

// WatchDIDHistoryEvent is a free log subscription operation binding the contract event 0xac7b90e309a0b0289d7b1e6a75fb7df9b0fc1b4a65e51b90cc47d9156d876f1e.
//
// Solidity: event DIDHistoryEvent(address indexed identity, uint256 previousBlock, int256 created)
func (_Did *DidFilterer) WatchDIDHistoryEvent(opts *bind.WatchOpts, sink chan<- *DidDIDHistoryEvent, identity []common.Address) (event.Subscription, error) {

	var identityRule []interface{}
	for _, identityItem := range identity {
		identityRule = append(identityRule, identityItem)
	}

	logs, sub, err := _Did.contract.WatchLogs(opts, "DIDHistoryEvent", identityRule)
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(DidDIDHistoryEvent)
				if err := _Did.contract.UnpackLog(event, "DIDHistoryEvent", log); err != nil {
					return err
				}
				event.Raw = log

				select {
				case sink <- event:
				case err := <-sub.Err():
					return err
				case <-quit:
					return nil
				}
			case err := <-sub.Err():
				return err
			case <-quit:
				return nil
			}
		}
	}), nil
}

// ParseDIDHistoryEvent is a log parse operation binding the contract event 0xac7b90e309a0b0289d7b1e6a75fb7df9b0fc1b4a65e51b90cc47d9156d876f1e.
//
// Solidity: event DIDHistoryEvent(address indexed identity, uint256 previousBlock, int256 created)
func (_Did *DidFilterer) ParseDIDHistoryEvent(log types.Log) (*DidDIDHistoryEvent, error) {
	event := new(DidDIDHistoryEvent)
	if err := _Did.contract.UnpackLog(event, "DIDHistoryEvent", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}
