// Code generated - DO NOT EDIT.
// This file is a generated binding and any manual changes will be lost.

package cpt

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

// CptMetaData contains all meta data concerning the Cpt contract.
var CptMetaData = &bind.MetaData{
	ABI: "[{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"retCode\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"int256\",\"name\":\"cptVersion\",\"type\":\"int256\"}],\"name\":\"RegisterCptRetLog\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"retCode\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"int256\",\"name\":\"cptVersion\",\"type\":\"int256\"}],\"name\":\"UpdateCptRetLog\",\"type\":\"event\"},{\"inputs\":[],\"name\":\"AUTHORITY_ISSUER_START_ID\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"NONE_AUTHORITY_ISSUER_START_ID\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"allocateCptId\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"},{\"internalType\":\"address\",\"name\":\"dataStorageAddress\",\"type\":\"address\"}],\"name\":\"getCptDynamicBytes32Array\",\"outputs\":[{\"internalType\":\"bytes32[]\",\"name\":\"\",\"type\":\"bytes32[]\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"},{\"internalType\":\"address\",\"name\":\"dataStorageAddress\",\"type\":\"address\"}],\"name\":\"getCptDynamicIntArray\",\"outputs\":[{\"internalType\":\"int256[]\",\"name\":\"\",\"type\":\"int256[]\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"},{\"internalType\":\"address\",\"name\":\"dataStorageAddress\",\"type\":\"address\"}],\"name\":\"getCptDynamicJsonSchemaArray\",\"outputs\":[{\"internalType\":\"bytes32[]\",\"name\":\"\",\"type\":\"bytes32[]\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"index\",\"type\":\"uint256\"}],\"name\":\"getCptIdFromIndex\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"startPos\",\"type\":\"uint256\"},{\"internalType\":\"uint256\",\"name\":\"num\",\"type\":\"uint256\"}],\"name\":\"getCptIdList\",\"outputs\":[{\"internalType\":\"uint256[]\",\"name\":\"\",\"type\":\"uint256[]\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"}],\"name\":\"getCptIntArray\",\"outputs\":[{\"internalType\":\"int256[8]\",\"name\":\"intArray\",\"type\":\"int256[8]\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"}],\"name\":\"getCptPublisher\",\"outputs\":[{\"internalType\":\"address\",\"name\":\"publisher\",\"type\":\"address\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"}],\"name\":\"getCptSignature\",\"outputs\":[{\"internalType\":\"uint8\",\"name\":\"v\",\"type\":\"uint8\"},{\"internalType\":\"bytes32\",\"name\":\"r\",\"type\":\"bytes32\"},{\"internalType\":\"bytes32\",\"name\":\"s\",\"type\":\"bytes32\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"getDatasetLength\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"getTotalCptId\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"}],\"name\":\"isCptExist\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"\",\"type\":\"bool\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"},{\"internalType\":\"address\",\"name\":\"cptPublisher\",\"type\":\"address\"},{\"internalType\":\"int256[8]\",\"name\":\"cptIntArray\",\"type\":\"int256[8]\"},{\"internalType\":\"bytes32[8]\",\"name\":\"cptBytes32Array\",\"type\":\"bytes32[8]\"},{\"internalType\":\"bytes32[32]\",\"name\":\"cptJsonSchemaArray\",\"type\":\"bytes32[32]\"},{\"internalType\":\"uint8\",\"name\":\"cptV\",\"type\":\"uint8\"},{\"internalType\":\"bytes32\",\"name\":\"cptR\",\"type\":\"bytes32\"},{\"internalType\":\"bytes32\",\"name\":\"cptS\",\"type\":\"bytes32\"}],\"name\":\"putCpt\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"\",\"type\":\"bool\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"}],\"name\":\"queryCpt\",\"outputs\":[{\"internalType\":\"address\",\"name\":\"publisher\",\"type\":\"address\"},{\"internalType\":\"int256[]\",\"name\":\"intArray\",\"type\":\"int256[]\"},{\"internalType\":\"bytes32[]\",\"name\":\"bytes32Array\",\"type\":\"bytes32[]\"},{\"internalType\":\"bytes32[]\",\"name\":\"jsonSchemaArray\",\"type\":\"bytes32[]\"},{\"internalType\":\"uint8\",\"name\":\"v\",\"type\":\"uint8\"},{\"internalType\":\"bytes32\",\"name\":\"r\",\"type\":\"bytes32\"},{\"internalType\":\"bytes32\",\"name\":\"s\",\"type\":\"bytes32\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"publisher\",\"type\":\"address\"},{\"internalType\":\"int256[8]\",\"name\":\"intArray\",\"type\":\"int256[8]\"},{\"internalType\":\"bytes32[8]\",\"name\":\"bytes32Array\",\"type\":\"bytes32[8]\"},{\"internalType\":\"bytes32[32]\",\"name\":\"jsonSchemaArray\",\"type\":\"bytes32[32]\"},{\"internalType\":\"uint8\",\"name\":\"v\",\"type\":\"uint8\"},{\"internalType\":\"bytes32\",\"name\":\"r\",\"type\":\"bytes32\"},{\"internalType\":\"bytes32\",\"name\":\"s\",\"type\":\"bytes32\"}],\"name\":\"registerCpt\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"\",\"type\":\"bool\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"},{\"internalType\":\"address\",\"name\":\"publisher\",\"type\":\"address\"},{\"internalType\":\"int256[8]\",\"name\":\"intArray\",\"type\":\"int256[8]\"},{\"internalType\":\"bytes32[8]\",\"name\":\"bytes32Array\",\"type\":\"bytes32[8]\"},{\"internalType\":\"bytes32[32]\",\"name\":\"jsonSchemaArray\",\"type\":\"bytes32[32]\"},{\"internalType\":\"uint8\",\"name\":\"v\",\"type\":\"uint8\"},{\"internalType\":\"bytes32\",\"name\":\"r\",\"type\":\"bytes32\"},{\"internalType\":\"bytes32\",\"name\":\"s\",\"type\":\"bytes32\"}],\"name\":\"updateCpt\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"\",\"type\":\"bool\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"}]",
	Bin: "0x60806040526103e85f55621e848060015534801561001b575f80fd5b5061228a806100295f395ff3fe608060405234801561000f575f80fd5b5060043610610114575f3560e01c80636fce6bb3116100a0578063d4eb8a421161006f578063d4eb8a4214610346578063d6edb44e14610376578063e083a3ad146103a6578063e5741ff3146103c4578063e5a34e6e146103f657610114565b80636fce6bb3146102aa578063744d6436146102c8578063a07bd9b5146102e6578063d2a3b53d1461031657610114565b806347b42f88116100e757806347b42f88146101b45780635ca35abf146101e457806362238a791461021a57806366d6a90b1461024a5780636da223b71461027a57610114565b80631e040fc71461011857806323b746f1146101485780632984fcc8146101785780632c0abe1d14610196575b5f80fd5b610132600480360381019061012d919061161b565b610426565b60405161013f9190611710565b60405180910390f35b610162600480360381019061015d9190611730565b61055c565b60405161016f9190611809565b60405180910390f35b6101806106f6565b60405161018d9190611832565b60405180910390f35b61019e610704565b6040516101ab9190611832565b60405180910390f35b6101ce60048036038101906101c99190611bd2565b61070b565b6040516101db9190611c8f565b60405180910390f35b6101fe60048036038101906101f99190611730565b61074a565b6040516102119796959493929190611e1d565b60405180910390f35b610234600480360381019061022f9190611e9f565b610797565b6040516102419190611edd565b60405180910390f35b610264600480360381019061025f9190611efd565b6109cf565b6040516102719190611c8f565b60405180910390f35b610294600480360381019061028f9190611730565b610a10565b6040516102a19190611fb3565b60405180910390f35b6102b2610ba2565b6040516102bf9190611832565b60405180910390f35b6102d0610ba8565b6040516102dd9190611832565b60405180910390f35b61030060048036038101906102fb9190611730565b610bf1565b60405161030d9190611832565b60405180910390f35b610330600480360381019061032b9190611efd565b610c16565b60405161033d9190611c8f565b60405180910390f35b610360600480360381019061035b9190611730565b610d89565b60405161036d9190611c8f565b60405180910390f35b610390600480360381019061038b9190611e9f565b610df3565b60405161039d9190611edd565b60405180910390f35b6103ae61102b565b6040516103bb9190611832565b60405180910390f35b6103de60048036038101906103d99190611730565b611037565b6040516103ed93929190611fcc565b60405180910390f35b610410600480360381019061040b9190611e9f565b6111e7565b60405161041d9190612001565b60405180910390f35b60605f61043161102b565b90505f8482101561048f57600167ffffffffffffffff811115610457576104566118b9565b5b6040519080825280602002602001820160405280156104855781602001602082028036833780820191505090505b5092505050610556565b838561049b919061204e565b82116104b45784826104ad9190612081565b90506104b8565b8390505b5f8167ffffffffffffffff8111156104d3576104d26118b9565b5b6040519080825280602002602001820160405280156105015781602001602082028036833780820191505090505b5090505f5b8281101561054e57610522818861051d919061204e565b610bf1565b828281518110610535576105346120b4565b5b6020026020010181815250508080600101915050610506565b508093505050505b92915050565b6105646114c2565b5f60025f8481526020019081526020015f206040518060a00160405290815f82015f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200160018201600880602002604051908101604052809291908260088015610611576020028201915b8154815260200190600101908083116105fd575b5050505050815260200160098201600880602002604051908101604052809291908260088015610656576020028201915b815481526020019060010190808311610642575b505050505081526020016011820160208060200260405190810160405280929190826020801561069b576020028201915b815481526020019060010190808311610687575b50505050508152602001603182016040518060600160405290815f82015f9054906101000a900460ff1660ff1660ff168152602001600182015481526020016002820154815250508152505090508060200151915050919050565b5f6106ff61102b565b905090565b621e848081565b5f61073d8888888888888860045f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff1661129d565b9050979650505050505050565b5f60608060605f805f61077e8860045f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff16611329565b9650965096509650965096509650919395979092949650565b60605f60025f8581526020019081526020015f206040518060a00160405290815f82015f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200160018201600880602002604051908101604052809291908260088015610846576020028201915b815481526020019060010190808311610832575b505050505081526020016009820160088060200260405190810160405280929190826008801561088b576020028201915b815481526020019060010190808311610877575b50505050508152602001601182016020806020026040519081016040528092919082602080156108d0576020028201915b8154815260200190600101908083116108bc575b50505050508152602001603182016040518060600160405290815f82015f9054906101000a900460ff1660ff1660ff168152602001600182015481526020016002820154815250508152505090505f816060015190505f602067ffffffffffffffff811115610942576109416118b9565b5b6040519080825280602002602001820160405280156109705781602001602082028036833780820191505090505b5090505f5b60208110156109c257828160208110610991576109906120b4565b5b60200201518282815181106109a9576109a86120b4565b5b6020026020010181815250508080600101915050610975565b5080935050505092915050565b5f610a02898989898989898960045f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff16611382565b905098975050505050505050565b5f8060025f8481526020019081526020015f206040518060a00160405290815f82015f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200160018201600880602002604051908101604052809291908260088015610abe576020028201915b815481526020019060010190808311610aaa575b5050505050815260200160098201600880602002604051908101604052809291908260088015610b03576020028201915b815481526020019060010190808311610aef575b5050505050815260200160118201602080602002604051908101604052809291908260208015610b48576020028201915b815481526020019060010190808311610b34575b50505050508152602001603182016040518060600160405290815f82015f9054906101000a900460ff1660ff1660ff16815260200160018201548152602001600282015481525050815250509050805f0151915050919050565b6103e881565b5f5b610bb5600154610d89565b15610bd65760015f815480929190610bcc906120e1565b9190505550610baa565b60015f815480929190610be8906120e1565b91905055905090565b5f60038281548110610c0657610c056120b4565b5b905f5260205f2001549050919050565b5f8060405180606001604052808660ff1681526020018581526020018481525090506040518060a001604052808a73ffffffffffffffffffffffffffffffffffffffff1681526020018981526020018881526020018781526020018281525060025f8c81526020019081526020015f205f820151815f015f6101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550602082015181600101906008610ce19291906114e5565b50604082015181600901906008610cf9929190611525565b50606082015181601101906020610d11929190611565565b506080820151816031015f820151815f015f6101000a81548160ff021916908360ff1602179055506020820151816001015560408201518160020155505090505060038a908060018154018082558091505060019003905f5260205f20015f9091909190915055600191505098975050505050505050565b5f8073ffffffffffffffffffffffffffffffffffffffff1660025f8481526020019081526020015f205f015f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614159050919050565b60605f60025f8581526020019081526020015f206040518060a00160405290815f82015f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200160018201600880602002604051908101604052809291908260088015610ea2576020028201915b815481526020019060010190808311610e8e575b5050505050815260200160098201600880602002604051908101604052809291908260088015610ee7576020028201915b815481526020019060010190808311610ed3575b5050505050815260200160118201602080602002604051908101604052809291908260208015610f2c576020028201915b815481526020019060010190808311610f18575b50505050508152602001603182016040518060600160405290815f82015f9054906101000a900460ff1660ff1660ff168152602001600182015481526020016002820154815250508152505090505f816040015190505f600867ffffffffffffffff811115610f9e57610f9d6118b9565b5b604051908082528060200260200182016040528015610fcc5781602001602082028036833780820191505090505b5090505f5b600881101561101e57828160088110610fed57610fec6120b4565b5b6020020151828281518110611005576110046120b4565b5b6020026020010181815250508080600101915050610fd1565b5080935050505092915050565b5f600380549050905090565b5f805f8060025f8681526020019081526020015f206040518060a00160405290815f82015f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001600182016008806020026040519081016040528092919082600880156110e7576020028201915b8154815260200190600101908083116110d3575b505050505081526020016009820160088060200260405190810160405280929190826008801561112c576020028201915b815481526020019060010190808311611118575b5050505050815260200160118201602080602002604051908101604052809291908260208015611171576020028201915b81548152602001906001019080831161115d575b50505050508152602001603182016040518060600160405290815f82015f9054906101000a900460ff1660ff1660ff1681526020016001820154815260200160028201548152505081525050905080608001515f0151935080608001516020015192508060800151604001519150509193909250565b60605f6111f38461055c565b90505f600867ffffffffffffffff811115611211576112106118b9565b5b60405190808252806020026020018201604052801561123f5781602001602082028036833780820191505090505b5090505f5b6008811015611291578281600881106112605761125f6120b4565b5b6020020151828281518110611278576112776120b4565b5b6020026020010181815250508080600101915050611244565b50809250505092915050565b5f806112a7610ba8565b90505f60019050808a5f600881106112c2576112c16120b4565b5b6020020181815250506112db828c8c8c8c8c8c8c610c16565b507fa17f6f29c43d53fdf8a8d5fc788d118621cdca690e8ee29962c3e2fbe70d5eb35f838360405161130f93929190612179565b60405180910390a160019250505098975050505050505050565b5f60608060605f805f61133b89610a10565b965061134789896111e7565b95506113538989610df3565b945061135f8989610797565b935061136a89611037565b80935081945082955050505092959891949750929550565b5f61138c8a610d89565b15611473575f61139b8b61055c565b90505f6001825f600881106113b3576113b26120b4565b5b60200201516113c291906121ae565b9050808a5f600881106113d8576113d76120b4565b5b6020020181815250505f826001600881106113f6576113f56120b4565b5b60200201519050808b600160088110611412576114116120b4565b5b60200201818152505061142b8d8d8d8d8d8d8d8d610c16565b507f2614d1ec3482cc2505bf211c39bee96c28940521311ec70c9ebf14d3896fd1965f8e8460405161145f93929190612179565b60405180910390a1600193505050506114b5565b7f2614d1ec3482cc2505bf211c39bee96c28940521311ec70c9ebf14d3896fd1966207a24d5f806040516114a99392919061221f565b60405180910390a15f90505b9998505050505050505050565b604051806101000160405280600890602082028036833780820191505090505090565b8260088101928215611514579160200282015b828111156115135782518255916020019190600101906114f8565b5b50905061152191906115a5565b5090565b8260088101928215611554579160200282015b82811115611553578251825591602001919060010190611538565b5b50905061156191906115c0565b5090565b8260208101928215611594579160200282015b82811115611593578251825591602001919060010190611578565b5b5090506115a191906115c0565b5090565b5b808211156115bc575f815f9055506001016115a6565b5090565b5b808211156115d7575f815f9055506001016115c1565b5090565b5f604051905090565b5f80fd5b5f819050919050565b6115fa816115e8565b8114611604575f80fd5b50565b5f81359050611615816115f1565b92915050565b5f8060408385031215611631576116306115e4565b5b5f61163e85828601611607565b925050602061164f85828601611607565b9150509250929050565b5f81519050919050565b5f82825260208201905092915050565b5f819050602082019050919050565b61168b816115e8565b82525050565b5f61169c8383611682565b60208301905092915050565b5f602082019050919050565b5f6116be82611659565b6116c88185611663565b93506116d383611673565b805f5b838110156117035781516116ea8882611691565b97506116f5836116a8565b9250506001810190506116d6565b5085935050505092915050565b5f6020820190508181035f83015261172881846116b4565b905092915050565b5f60208284031215611745576117446115e4565b5b5f61175284828501611607565b91505092915050565b5f60089050919050565b5f81905092915050565b5f819050919050565b5f819050919050565b61178a81611778565b82525050565b5f61179b8383611781565b60208301905092915050565b5f602082019050919050565b6117bc8161175b565b6117c68184611765565b92506117d18261176f565b805f5b838110156118015781516117e88782611790565b96506117f3836117a7565b9250506001810190506117d4565b505050505050565b5f6101008201905061181d5f8301846117b3565b92915050565b61182c816115e8565b82525050565b5f6020820190506118455f830184611823565b92915050565b5f73ffffffffffffffffffffffffffffffffffffffff82169050919050565b5f6118748261184b565b9050919050565b6118848161186a565b811461188e575f80fd5b50565b5f8135905061189f8161187b565b92915050565b5f80fd5b5f601f19601f8301169050919050565b7f4e487b71000000000000000000000000000000000000000000000000000000005f52604160045260245ffd5b6118ef826118a9565b810181811067ffffffffffffffff8211171561190e5761190d6118b9565b5b80604052505050565b5f6119206115db565b905061192c82826118e6565b919050565b5f67ffffffffffffffff82111561194b5761194a6118b9565b5b602082029050919050565b5f80fd5b61196381611778565b811461196d575f80fd5b50565b5f8135905061197e8161195a565b92915050565b5f61199661199184611931565b611917565b905080602084028301858111156119b0576119af611956565b5b835b818110156119d957806119c58882611970565b8452602084019350506020810190506119b2565b5050509392505050565b5f82601f8301126119f7576119f66118a5565b5b6008611a04848285611984565b91505092915050565b5f67ffffffffffffffff821115611a2757611a266118b9565b5b602082029050919050565b5f819050919050565b611a4481611a32565b8114611a4e575f80fd5b50565b5f81359050611a5f81611a3b565b92915050565b5f611a77611a7284611a0d565b611917565b90508060208402830185811115611a9157611a90611956565b5b835b81811015611aba5780611aa68882611a51565b845260208401935050602081019050611a93565b5050509392505050565b5f82601f830112611ad857611ad76118a5565b5b6008611ae5848285611a65565b91505092915050565b5f67ffffffffffffffff821115611b0857611b076118b9565b5b602082029050919050565b5f611b25611b2084611aee565b611917565b90508060208402830185811115611b3f57611b3e611956565b5b835b81811015611b685780611b548882611a51565b845260208401935050602081019050611b41565b5050509392505050565b5f82601f830112611b8657611b856118a5565b5b6020611b93848285611b13565b91505092915050565b5f60ff82169050919050565b611bb181611b9c565b8114611bbb575f80fd5b50565b5f81359050611bcc81611ba8565b92915050565b5f805f805f805f610680888a031215611bee57611bed6115e4565b5b5f611bfb8a828b01611891565b9750506020611c0c8a828b016119e3565b965050610120611c1e8a828b01611ac4565b955050610220611c308a828b01611b72565b945050610620611c428a828b01611bbe565b935050610640611c548a828b01611a51565b925050610660611c668a828b01611a51565b91505092959891949750929550565b5f8115159050919050565b611c8981611c75565b82525050565b5f602082019050611ca25f830184611c80565b92915050565b611cb18161186a565b82525050565b5f81519050919050565b5f82825260208201905092915050565b5f819050602082019050919050565b5f602082019050919050565b5f611cf682611cb7565b611d008185611cc1565b9350611d0b83611cd1565b805f5b83811015611d3b578151611d228882611790565b9750611d2d83611ce0565b925050600181019050611d0e565b5085935050505092915050565b5f81519050919050565b5f82825260208201905092915050565b5f819050602082019050919050565b611d7a81611a32565b82525050565b5f611d8b8383611d71565b60208301905092915050565b5f602082019050919050565b5f611dad82611d48565b611db78185611d52565b9350611dc283611d62565b805f5b83811015611df2578151611dd98882611d80565b9750611de483611d97565b925050600181019050611dc5565b5085935050505092915050565b611e0881611b9c565b82525050565b611e1781611a32565b82525050565b5f60e082019050611e305f83018a611ca8565b8181036020830152611e428189611cec565b90508181036040830152611e568188611da3565b90508181036060830152611e6a8187611da3565b9050611e796080830186611dff565b611e8660a0830185611e0e565b611e9360c0830184611e0e565b98975050505050505050565b5f8060408385031215611eb557611eb46115e4565b5b5f611ec285828601611607565b9250506020611ed385828601611891565b9150509250929050565b5f6020820190508181035f830152611ef58184611da3565b905092915050565b5f805f805f805f806106a0898b031215611f1a57611f196115e4565b5b5f611f278b828c01611607565b9850506020611f388b828c01611891565b9750506040611f498b828c016119e3565b965050610140611f5b8b828c01611ac4565b955050610240611f6d8b828c01611b72565b945050610640611f7f8b828c01611bbe565b935050610660611f918b828c01611a51565b925050610680611fa38b828c01611a51565b9150509295985092959890939650565b5f602082019050611fc65f830184611ca8565b92915050565b5f606082019050611fdf5f830186611dff565b611fec6020830185611e0e565b611ff96040830184611e0e565b949350505050565b5f6020820190508181035f8301526120198184611cec565b905092915050565b7f4e487b71000000000000000000000000000000000000000000000000000000005f52601160045260245ffd5b5f612058826115e8565b9150612063836115e8565b925082820190508082111561207b5761207a612021565b5b92915050565b5f61208b826115e8565b9150612096836115e8565b92508282039050818111156120ae576120ad612021565b5b92915050565b7f4e487b71000000000000000000000000000000000000000000000000000000005f52603260045260245ffd5b5f6120eb826115e8565b91507fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff820361211d5761211c612021565b5b600182019050919050565b5f819050919050565b5f819050919050565b5f61215461214f61214a84612128565b612131565b6115e8565b9050919050565b6121648161213a565b82525050565b61217381611778565b82525050565b5f60608201905061218c5f83018661215b565b6121996020830185611823565b6121a6604083018461216a565b949350505050565b5f6121b882611778565b91506121c383611778565b92508282019050828112155f8312168382125f8412151617156121e9576121e8612021565b5b92915050565b5f6122096122046121ff84612128565b612131565b611778565b9050919050565b612219816121ef565b82525050565b5f6060820190506122325f830186611823565b61223f602083018561215b565b61224c6040830184612210565b94935050505056fea26469706673582212208b3535b979b2c231d17ef8bbde0af7e87e3d9f2bd872681c09c5d0c180b08dbc64736f6c63430008180033",
}

// CptABI is the input ABI used to generate the binding from.
// Deprecated: Use CptMetaData.ABI instead.
var CptABI = CptMetaData.ABI

// CptBin is the compiled bytecode used for deploying new contracts.
// Deprecated: Use CptMetaData.Bin instead.
var CptBin = CptMetaData.Bin

// DeployCpt deploys a new Ethereum contract, binding an instance of Cpt to it.
func DeployCpt(auth *bind.TransactOpts, backend bind.ContractBackend) (common.Address, *types.Transaction, *Cpt, error) {
	parsed, err := CptMetaData.GetAbi()
	if err != nil {
		return common.Address{}, nil, nil, err
	}
	if parsed == nil {
		return common.Address{}, nil, nil, errors.New("GetABI returned nil")
	}

	address, tx, contract, err := bind.DeployContract(auth, *parsed, common.FromHex(CptBin), backend)
	if err != nil {
		return common.Address{}, nil, nil, err
	}
	return address, tx, &Cpt{CptCaller: CptCaller{contract: contract}, CptTransactor: CptTransactor{contract: contract}, CptFilterer: CptFilterer{contract: contract}}, nil
}

// Cpt is an auto generated Go binding around an Ethereum contract.
type Cpt struct {
	CptCaller     // Read-only binding to the contract
	CptTransactor // Write-only binding to the contract
	CptFilterer   // Log filterer for contract events
}

// CptCaller is an auto generated read-only Go binding around an Ethereum contract.
type CptCaller struct {
	contract *bind.BoundContract // Generic contract wrapper for the low level calls
}

// CptTransactor is an auto generated write-only Go binding around an Ethereum contract.
type CptTransactor struct {
	contract *bind.BoundContract // Generic contract wrapper for the low level calls
}

// CptFilterer is an auto generated log filtering Go binding around an Ethereum contract events.
type CptFilterer struct {
	contract *bind.BoundContract // Generic contract wrapper for the low level calls
}

// CptSession is an auto generated Go binding around an Ethereum contract,
// with pre-set call and transact options.
type CptSession struct {
	Contract     *Cpt              // Generic contract binding to set the session for
	CallOpts     bind.CallOpts     // Call options to use throughout this session
	TransactOpts bind.TransactOpts // Transaction auth options to use throughout this session
}

// CptCallerSession is an auto generated read-only Go binding around an Ethereum contract,
// with pre-set call options.
type CptCallerSession struct {
	Contract *CptCaller    // Generic contract caller binding to set the session for
	CallOpts bind.CallOpts // Call options to use throughout this session
}

// CptTransactorSession is an auto generated write-only Go binding around an Ethereum contract,
// with pre-set transact options.
type CptTransactorSession struct {
	Contract     *CptTransactor    // Generic contract transactor binding to set the session for
	TransactOpts bind.TransactOpts // Transaction auth options to use throughout this session
}

// CptRaw is an auto generated low-level Go binding around an Ethereum contract.
type CptRaw struct {
	Contract *Cpt // Generic contract binding to access the raw methods on
}

// CptCallerRaw is an auto generated low-level read-only Go binding around an Ethereum contract.
type CptCallerRaw struct {
	Contract *CptCaller // Generic read-only contract binding to access the raw methods on
}

// CptTransactorRaw is an auto generated low-level write-only Go binding around an Ethereum contract.
type CptTransactorRaw struct {
	Contract *CptTransactor // Generic write-only contract binding to access the raw methods on
}

// NewCpt creates a new instance of Cpt, bound to a specific deployed contract.
func NewCpt(address common.Address, backend bind.ContractBackend) (*Cpt, error) {
	contract, err := bindCpt(address, backend, backend, backend)
	if err != nil {
		return nil, err
	}
	return &Cpt{CptCaller: CptCaller{contract: contract}, CptTransactor: CptTransactor{contract: contract}, CptFilterer: CptFilterer{contract: contract}}, nil
}

// NewCptCaller creates a new read-only instance of Cpt, bound to a specific deployed contract.
func NewCptCaller(address common.Address, caller bind.ContractCaller) (*CptCaller, error) {
	contract, err := bindCpt(address, caller, nil, nil)
	if err != nil {
		return nil, err
	}
	return &CptCaller{contract: contract}, nil
}

// NewCptTransactor creates a new write-only instance of Cpt, bound to a specific deployed contract.
func NewCptTransactor(address common.Address, transactor bind.ContractTransactor) (*CptTransactor, error) {
	contract, err := bindCpt(address, nil, transactor, nil)
	if err != nil {
		return nil, err
	}
	return &CptTransactor{contract: contract}, nil
}

// NewCptFilterer creates a new log filterer instance of Cpt, bound to a specific deployed contract.
func NewCptFilterer(address common.Address, filterer bind.ContractFilterer) (*CptFilterer, error) {
	contract, err := bindCpt(address, nil, nil, filterer)
	if err != nil {
		return nil, err
	}
	return &CptFilterer{contract: contract}, nil
}

// bindCpt binds a generic wrapper to an already deployed contract.
func bindCpt(address common.Address, caller bind.ContractCaller, transactor bind.ContractTransactor, filterer bind.ContractFilterer) (*bind.BoundContract, error) {
	parsed, err := CptMetaData.GetAbi()
	if err != nil {
		return nil, err
	}
	return bind.NewBoundContract(address, *parsed, caller, transactor, filterer), nil
}

// Call invokes the (constant) contract method with params as input values and
// sets the output to result. The result type might be a single field for simple
// returns, a slice of interfaces for anonymous returns and a struct for named
// returns.
func (_Cpt *CptRaw) Call(opts *bind.CallOpts, result *[]interface{}, method string, params ...interface{}) error {
	return _Cpt.Contract.CptCaller.contract.Call(opts, result, method, params...)
}

// Transfer initiates a plain transaction to move funds to the contract, calling
// its default method if one is available.
func (_Cpt *CptRaw) Transfer(opts *bind.TransactOpts) (*types.Transaction, error) {
	return _Cpt.Contract.CptTransactor.contract.Transfer(opts)
}

// Transact invokes the (paid) contract method with params as input values.
func (_Cpt *CptRaw) Transact(opts *bind.TransactOpts, method string, params ...interface{}) (*types.Transaction, error) {
	return _Cpt.Contract.CptTransactor.contract.Transact(opts, method, params...)
}

// Call invokes the (constant) contract method with params as input values and
// sets the output to result. The result type might be a single field for simple
// returns, a slice of interfaces for anonymous returns and a struct for named
// returns.
func (_Cpt *CptCallerRaw) Call(opts *bind.CallOpts, result *[]interface{}, method string, params ...interface{}) error {
	return _Cpt.Contract.contract.Call(opts, result, method, params...)
}

// Transfer initiates a plain transaction to move funds to the contract, calling
// its default method if one is available.
func (_Cpt *CptTransactorRaw) Transfer(opts *bind.TransactOpts) (*types.Transaction, error) {
	return _Cpt.Contract.contract.Transfer(opts)
}

// Transact invokes the (paid) contract method with params as input values.
func (_Cpt *CptTransactorRaw) Transact(opts *bind.TransactOpts, method string, params ...interface{}) (*types.Transaction, error) {
	return _Cpt.Contract.contract.Transact(opts, method, params...)
}

// AUTHORITYISSUERSTARTID is a free data retrieval call binding the contract method 0x6fce6bb3.
//
// Solidity: function AUTHORITY_ISSUER_START_ID() view returns(uint256)
func (_Cpt *CptCaller) AUTHORITYISSUERSTARTID(opts *bind.CallOpts) (*big.Int, error) {
	var out []interface{}
	err := _Cpt.contract.Call(opts, &out, "AUTHORITY_ISSUER_START_ID")

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// AUTHORITYISSUERSTARTID is a free data retrieval call binding the contract method 0x6fce6bb3.
//
// Solidity: function AUTHORITY_ISSUER_START_ID() view returns(uint256)
func (_Cpt *CptSession) AUTHORITYISSUERSTARTID() (*big.Int, error) {
	return _Cpt.Contract.AUTHORITYISSUERSTARTID(&_Cpt.CallOpts)
}

// AUTHORITYISSUERSTARTID is a free data retrieval call binding the contract method 0x6fce6bb3.
//
// Solidity: function AUTHORITY_ISSUER_START_ID() view returns(uint256)
func (_Cpt *CptCallerSession) AUTHORITYISSUERSTARTID() (*big.Int, error) {
	return _Cpt.Contract.AUTHORITYISSUERSTARTID(&_Cpt.CallOpts)
}

// NONEAUTHORITYISSUERSTARTID is a free data retrieval call binding the contract method 0x2c0abe1d.
//
// Solidity: function NONE_AUTHORITY_ISSUER_START_ID() view returns(uint256)
func (_Cpt *CptCaller) NONEAUTHORITYISSUERSTARTID(opts *bind.CallOpts) (*big.Int, error) {
	var out []interface{}
	err := _Cpt.contract.Call(opts, &out, "NONE_AUTHORITY_ISSUER_START_ID")

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// NONEAUTHORITYISSUERSTARTID is a free data retrieval call binding the contract method 0x2c0abe1d.
//
// Solidity: function NONE_AUTHORITY_ISSUER_START_ID() view returns(uint256)
func (_Cpt *CptSession) NONEAUTHORITYISSUERSTARTID() (*big.Int, error) {
	return _Cpt.Contract.NONEAUTHORITYISSUERSTARTID(&_Cpt.CallOpts)
}

// NONEAUTHORITYISSUERSTARTID is a free data retrieval call binding the contract method 0x2c0abe1d.
//
// Solidity: function NONE_AUTHORITY_ISSUER_START_ID() view returns(uint256)
func (_Cpt *CptCallerSession) NONEAUTHORITYISSUERSTARTID() (*big.Int, error) {
	return _Cpt.Contract.NONEAUTHORITYISSUERSTARTID(&_Cpt.CallOpts)
}

// GetCptDynamicBytes32Array is a free data retrieval call binding the contract method 0xd6edb44e.
//
// Solidity: function getCptDynamicBytes32Array(uint256 cptId, address dataStorageAddress) view returns(bytes32[])
func (_Cpt *CptCaller) GetCptDynamicBytes32Array(opts *bind.CallOpts, cptId *big.Int, dataStorageAddress common.Address) ([][32]byte, error) {
	var out []interface{}
	err := _Cpt.contract.Call(opts, &out, "getCptDynamicBytes32Array", cptId, dataStorageAddress)

	if err != nil {
		return *new([][32]byte), err
	}

	out0 := *abi.ConvertType(out[0], new([][32]byte)).(*[][32]byte)

	return out0, err

}

// GetCptDynamicBytes32Array is a free data retrieval call binding the contract method 0xd6edb44e.
//
// Solidity: function getCptDynamicBytes32Array(uint256 cptId, address dataStorageAddress) view returns(bytes32[])
func (_Cpt *CptSession) GetCptDynamicBytes32Array(cptId *big.Int, dataStorageAddress common.Address) ([][32]byte, error) {
	return _Cpt.Contract.GetCptDynamicBytes32Array(&_Cpt.CallOpts, cptId, dataStorageAddress)
}

// GetCptDynamicBytes32Array is a free data retrieval call binding the contract method 0xd6edb44e.
//
// Solidity: function getCptDynamicBytes32Array(uint256 cptId, address dataStorageAddress) view returns(bytes32[])
func (_Cpt *CptCallerSession) GetCptDynamicBytes32Array(cptId *big.Int, dataStorageAddress common.Address) ([][32]byte, error) {
	return _Cpt.Contract.GetCptDynamicBytes32Array(&_Cpt.CallOpts, cptId, dataStorageAddress)
}

// GetCptDynamicIntArray is a free data retrieval call binding the contract method 0xe5a34e6e.
//
// Solidity: function getCptDynamicIntArray(uint256 cptId, address dataStorageAddress) view returns(int256[])
func (_Cpt *CptCaller) GetCptDynamicIntArray(opts *bind.CallOpts, cptId *big.Int, dataStorageAddress common.Address) ([]*big.Int, error) {
	var out []interface{}
	err := _Cpt.contract.Call(opts, &out, "getCptDynamicIntArray", cptId, dataStorageAddress)

	if err != nil {
		return *new([]*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new([]*big.Int)).(*[]*big.Int)

	return out0, err

}

// GetCptDynamicIntArray is a free data retrieval call binding the contract method 0xe5a34e6e.
//
// Solidity: function getCptDynamicIntArray(uint256 cptId, address dataStorageAddress) view returns(int256[])
func (_Cpt *CptSession) GetCptDynamicIntArray(cptId *big.Int, dataStorageAddress common.Address) ([]*big.Int, error) {
	return _Cpt.Contract.GetCptDynamicIntArray(&_Cpt.CallOpts, cptId, dataStorageAddress)
}

// GetCptDynamicIntArray is a free data retrieval call binding the contract method 0xe5a34e6e.
//
// Solidity: function getCptDynamicIntArray(uint256 cptId, address dataStorageAddress) view returns(int256[])
func (_Cpt *CptCallerSession) GetCptDynamicIntArray(cptId *big.Int, dataStorageAddress common.Address) ([]*big.Int, error) {
	return _Cpt.Contract.GetCptDynamicIntArray(&_Cpt.CallOpts, cptId, dataStorageAddress)
}

// GetCptDynamicJsonSchemaArray is a free data retrieval call binding the contract method 0x62238a79.
//
// Solidity: function getCptDynamicJsonSchemaArray(uint256 cptId, address dataStorageAddress) view returns(bytes32[])
func (_Cpt *CptCaller) GetCptDynamicJsonSchemaArray(opts *bind.CallOpts, cptId *big.Int, dataStorageAddress common.Address) ([][32]byte, error) {
	var out []interface{}
	err := _Cpt.contract.Call(opts, &out, "getCptDynamicJsonSchemaArray", cptId, dataStorageAddress)

	if err != nil {
		return *new([][32]byte), err
	}

	out0 := *abi.ConvertType(out[0], new([][32]byte)).(*[][32]byte)

	return out0, err

}

// GetCptDynamicJsonSchemaArray is a free data retrieval call binding the contract method 0x62238a79.
//
// Solidity: function getCptDynamicJsonSchemaArray(uint256 cptId, address dataStorageAddress) view returns(bytes32[])
func (_Cpt *CptSession) GetCptDynamicJsonSchemaArray(cptId *big.Int, dataStorageAddress common.Address) ([][32]byte, error) {
	return _Cpt.Contract.GetCptDynamicJsonSchemaArray(&_Cpt.CallOpts, cptId, dataStorageAddress)
}

// GetCptDynamicJsonSchemaArray is a free data retrieval call binding the contract method 0x62238a79.
//
// Solidity: function getCptDynamicJsonSchemaArray(uint256 cptId, address dataStorageAddress) view returns(bytes32[])
func (_Cpt *CptCallerSession) GetCptDynamicJsonSchemaArray(cptId *big.Int, dataStorageAddress common.Address) ([][32]byte, error) {
	return _Cpt.Contract.GetCptDynamicJsonSchemaArray(&_Cpt.CallOpts, cptId, dataStorageAddress)
}

// GetCptIdFromIndex is a free data retrieval call binding the contract method 0xa07bd9b5.
//
// Solidity: function getCptIdFromIndex(uint256 index) view returns(uint256)
func (_Cpt *CptCaller) GetCptIdFromIndex(opts *bind.CallOpts, index *big.Int) (*big.Int, error) {
	var out []interface{}
	err := _Cpt.contract.Call(opts, &out, "getCptIdFromIndex", index)

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// GetCptIdFromIndex is a free data retrieval call binding the contract method 0xa07bd9b5.
//
// Solidity: function getCptIdFromIndex(uint256 index) view returns(uint256)
func (_Cpt *CptSession) GetCptIdFromIndex(index *big.Int) (*big.Int, error) {
	return _Cpt.Contract.GetCptIdFromIndex(&_Cpt.CallOpts, index)
}

// GetCptIdFromIndex is a free data retrieval call binding the contract method 0xa07bd9b5.
//
// Solidity: function getCptIdFromIndex(uint256 index) view returns(uint256)
func (_Cpt *CptCallerSession) GetCptIdFromIndex(index *big.Int) (*big.Int, error) {
	return _Cpt.Contract.GetCptIdFromIndex(&_Cpt.CallOpts, index)
}

// GetCptIdList is a free data retrieval call binding the contract method 0x1e040fc7.
//
// Solidity: function getCptIdList(uint256 startPos, uint256 num) view returns(uint256[])
func (_Cpt *CptCaller) GetCptIdList(opts *bind.CallOpts, startPos *big.Int, num *big.Int) ([]*big.Int, error) {
	var out []interface{}
	err := _Cpt.contract.Call(opts, &out, "getCptIdList", startPos, num)

	if err != nil {
		return *new([]*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new([]*big.Int)).(*[]*big.Int)

	return out0, err

}

// GetCptIdList is a free data retrieval call binding the contract method 0x1e040fc7.
//
// Solidity: function getCptIdList(uint256 startPos, uint256 num) view returns(uint256[])
func (_Cpt *CptSession) GetCptIdList(startPos *big.Int, num *big.Int) ([]*big.Int, error) {
	return _Cpt.Contract.GetCptIdList(&_Cpt.CallOpts, startPos, num)
}

// GetCptIdList is a free data retrieval call binding the contract method 0x1e040fc7.
//
// Solidity: function getCptIdList(uint256 startPos, uint256 num) view returns(uint256[])
func (_Cpt *CptCallerSession) GetCptIdList(startPos *big.Int, num *big.Int) ([]*big.Int, error) {
	return _Cpt.Contract.GetCptIdList(&_Cpt.CallOpts, startPos, num)
}

// GetCptIntArray is a free data retrieval call binding the contract method 0x23b746f1.
//
// Solidity: function getCptIntArray(uint256 cptId) view returns(int256[8] intArray)
func (_Cpt *CptCaller) GetCptIntArray(opts *bind.CallOpts, cptId *big.Int) ([8]*big.Int, error) {
	var out []interface{}
	err := _Cpt.contract.Call(opts, &out, "getCptIntArray", cptId)

	if err != nil {
		return *new([8]*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new([8]*big.Int)).(*[8]*big.Int)

	return out0, err

}

// GetCptIntArray is a free data retrieval call binding the contract method 0x23b746f1.
//
// Solidity: function getCptIntArray(uint256 cptId) view returns(int256[8] intArray)
func (_Cpt *CptSession) GetCptIntArray(cptId *big.Int) ([8]*big.Int, error) {
	return _Cpt.Contract.GetCptIntArray(&_Cpt.CallOpts, cptId)
}

// GetCptIntArray is a free data retrieval call binding the contract method 0x23b746f1.
//
// Solidity: function getCptIntArray(uint256 cptId) view returns(int256[8] intArray)
func (_Cpt *CptCallerSession) GetCptIntArray(cptId *big.Int) ([8]*big.Int, error) {
	return _Cpt.Contract.GetCptIntArray(&_Cpt.CallOpts, cptId)
}

// GetCptPublisher is a free data retrieval call binding the contract method 0x6da223b7.
//
// Solidity: function getCptPublisher(uint256 cptId) view returns(address publisher)
func (_Cpt *CptCaller) GetCptPublisher(opts *bind.CallOpts, cptId *big.Int) (common.Address, error) {
	var out []interface{}
	err := _Cpt.contract.Call(opts, &out, "getCptPublisher", cptId)

	if err != nil {
		return *new(common.Address), err
	}

	out0 := *abi.ConvertType(out[0], new(common.Address)).(*common.Address)

	return out0, err

}

// GetCptPublisher is a free data retrieval call binding the contract method 0x6da223b7.
//
// Solidity: function getCptPublisher(uint256 cptId) view returns(address publisher)
func (_Cpt *CptSession) GetCptPublisher(cptId *big.Int) (common.Address, error) {
	return _Cpt.Contract.GetCptPublisher(&_Cpt.CallOpts, cptId)
}

// GetCptPublisher is a free data retrieval call binding the contract method 0x6da223b7.
//
// Solidity: function getCptPublisher(uint256 cptId) view returns(address publisher)
func (_Cpt *CptCallerSession) GetCptPublisher(cptId *big.Int) (common.Address, error) {
	return _Cpt.Contract.GetCptPublisher(&_Cpt.CallOpts, cptId)
}

// GetCptSignature is a free data retrieval call binding the contract method 0xe5741ff3.
//
// Solidity: function getCptSignature(uint256 cptId) view returns(uint8 v, bytes32 r, bytes32 s)
func (_Cpt *CptCaller) GetCptSignature(opts *bind.CallOpts, cptId *big.Int) (struct {
	V uint8
	R [32]byte
	S [32]byte
}, error) {
	var out []interface{}
	err := _Cpt.contract.Call(opts, &out, "getCptSignature", cptId)

	outstruct := new(struct {
		V uint8
		R [32]byte
		S [32]byte
	})
	if err != nil {
		return *outstruct, err
	}

	outstruct.V = *abi.ConvertType(out[0], new(uint8)).(*uint8)
	outstruct.R = *abi.ConvertType(out[1], new([32]byte)).(*[32]byte)
	outstruct.S = *abi.ConvertType(out[2], new([32]byte)).(*[32]byte)

	return *outstruct, err

}

// GetCptSignature is a free data retrieval call binding the contract method 0xe5741ff3.
//
// Solidity: function getCptSignature(uint256 cptId) view returns(uint8 v, bytes32 r, bytes32 s)
func (_Cpt *CptSession) GetCptSignature(cptId *big.Int) (struct {
	V uint8
	R [32]byte
	S [32]byte
}, error) {
	return _Cpt.Contract.GetCptSignature(&_Cpt.CallOpts, cptId)
}

// GetCptSignature is a free data retrieval call binding the contract method 0xe5741ff3.
//
// Solidity: function getCptSignature(uint256 cptId) view returns(uint8 v, bytes32 r, bytes32 s)
func (_Cpt *CptCallerSession) GetCptSignature(cptId *big.Int) (struct {
	V uint8
	R [32]byte
	S [32]byte
}, error) {
	return _Cpt.Contract.GetCptSignature(&_Cpt.CallOpts, cptId)
}

// GetDatasetLength is a free data retrieval call binding the contract method 0xe083a3ad.
//
// Solidity: function getDatasetLength() view returns(uint256)
func (_Cpt *CptCaller) GetDatasetLength(opts *bind.CallOpts) (*big.Int, error) {
	var out []interface{}
	err := _Cpt.contract.Call(opts, &out, "getDatasetLength")

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// GetDatasetLength is a free data retrieval call binding the contract method 0xe083a3ad.
//
// Solidity: function getDatasetLength() view returns(uint256)
func (_Cpt *CptSession) GetDatasetLength() (*big.Int, error) {
	return _Cpt.Contract.GetDatasetLength(&_Cpt.CallOpts)
}

// GetDatasetLength is a free data retrieval call binding the contract method 0xe083a3ad.
//
// Solidity: function getDatasetLength() view returns(uint256)
func (_Cpt *CptCallerSession) GetDatasetLength() (*big.Int, error) {
	return _Cpt.Contract.GetDatasetLength(&_Cpt.CallOpts)
}

// GetTotalCptId is a free data retrieval call binding the contract method 0x2984fcc8.
//
// Solidity: function getTotalCptId() view returns(uint256)
func (_Cpt *CptCaller) GetTotalCptId(opts *bind.CallOpts) (*big.Int, error) {
	var out []interface{}
	err := _Cpt.contract.Call(opts, &out, "getTotalCptId")

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// GetTotalCptId is a free data retrieval call binding the contract method 0x2984fcc8.
//
// Solidity: function getTotalCptId() view returns(uint256)
func (_Cpt *CptSession) GetTotalCptId() (*big.Int, error) {
	return _Cpt.Contract.GetTotalCptId(&_Cpt.CallOpts)
}

// GetTotalCptId is a free data retrieval call binding the contract method 0x2984fcc8.
//
// Solidity: function getTotalCptId() view returns(uint256)
func (_Cpt *CptCallerSession) GetTotalCptId() (*big.Int, error) {
	return _Cpt.Contract.GetTotalCptId(&_Cpt.CallOpts)
}

// IsCptExist is a free data retrieval call binding the contract method 0xd4eb8a42.
//
// Solidity: function isCptExist(uint256 cptId) view returns(bool)
func (_Cpt *CptCaller) IsCptExist(opts *bind.CallOpts, cptId *big.Int) (bool, error) {
	var out []interface{}
	err := _Cpt.contract.Call(opts, &out, "isCptExist", cptId)

	if err != nil {
		return *new(bool), err
	}

	out0 := *abi.ConvertType(out[0], new(bool)).(*bool)

	return out0, err

}

// IsCptExist is a free data retrieval call binding the contract method 0xd4eb8a42.
//
// Solidity: function isCptExist(uint256 cptId) view returns(bool)
func (_Cpt *CptSession) IsCptExist(cptId *big.Int) (bool, error) {
	return _Cpt.Contract.IsCptExist(&_Cpt.CallOpts, cptId)
}

// IsCptExist is a free data retrieval call binding the contract method 0xd4eb8a42.
//
// Solidity: function isCptExist(uint256 cptId) view returns(bool)
func (_Cpt *CptCallerSession) IsCptExist(cptId *big.Int) (bool, error) {
	return _Cpt.Contract.IsCptExist(&_Cpt.CallOpts, cptId)
}

// QueryCpt is a free data retrieval call binding the contract method 0x5ca35abf.
//
// Solidity: function queryCpt(uint256 cptId) view returns(address publisher, int256[] intArray, bytes32[] bytes32Array, bytes32[] jsonSchemaArray, uint8 v, bytes32 r, bytes32 s)
func (_Cpt *CptCaller) QueryCpt(opts *bind.CallOpts, cptId *big.Int) (struct {
	Publisher       common.Address
	IntArray        []*big.Int
	Bytes32Array    [][32]byte
	JsonSchemaArray [][32]byte
	V               uint8
	R               [32]byte
	S               [32]byte
}, error) {
	var out []interface{}
	err := _Cpt.contract.Call(opts, &out, "queryCpt", cptId)

	outstruct := new(struct {
		Publisher       common.Address
		IntArray        []*big.Int
		Bytes32Array    [][32]byte
		JsonSchemaArray [][32]byte
		V               uint8
		R               [32]byte
		S               [32]byte
	})
	if err != nil {
		return *outstruct, err
	}

	outstruct.Publisher = *abi.ConvertType(out[0], new(common.Address)).(*common.Address)
	outstruct.IntArray = *abi.ConvertType(out[1], new([]*big.Int)).(*[]*big.Int)
	outstruct.Bytes32Array = *abi.ConvertType(out[2], new([][32]byte)).(*[][32]byte)
	outstruct.JsonSchemaArray = *abi.ConvertType(out[3], new([][32]byte)).(*[][32]byte)
	outstruct.V = *abi.ConvertType(out[4], new(uint8)).(*uint8)
	outstruct.R = *abi.ConvertType(out[5], new([32]byte)).(*[32]byte)
	outstruct.S = *abi.ConvertType(out[6], new([32]byte)).(*[32]byte)

	return *outstruct, err

}

// QueryCpt is a free data retrieval call binding the contract method 0x5ca35abf.
//
// Solidity: function queryCpt(uint256 cptId) view returns(address publisher, int256[] intArray, bytes32[] bytes32Array, bytes32[] jsonSchemaArray, uint8 v, bytes32 r, bytes32 s)
func (_Cpt *CptSession) QueryCpt(cptId *big.Int) (struct {
	Publisher       common.Address
	IntArray        []*big.Int
	Bytes32Array    [][32]byte
	JsonSchemaArray [][32]byte
	V               uint8
	R               [32]byte
	S               [32]byte
}, error) {
	return _Cpt.Contract.QueryCpt(&_Cpt.CallOpts, cptId)
}

// QueryCpt is a free data retrieval call binding the contract method 0x5ca35abf.
//
// Solidity: function queryCpt(uint256 cptId) view returns(address publisher, int256[] intArray, bytes32[] bytes32Array, bytes32[] jsonSchemaArray, uint8 v, bytes32 r, bytes32 s)
func (_Cpt *CptCallerSession) QueryCpt(cptId *big.Int) (struct {
	Publisher       common.Address
	IntArray        []*big.Int
	Bytes32Array    [][32]byte
	JsonSchemaArray [][32]byte
	V               uint8
	R               [32]byte
	S               [32]byte
}, error) {
	return _Cpt.Contract.QueryCpt(&_Cpt.CallOpts, cptId)
}

// AllocateCptId is a paid mutator transaction binding the contract method 0x744d6436.
//
// Solidity: function allocateCptId() returns(uint256 cptId)
func (_Cpt *CptTransactor) AllocateCptId(opts *bind.TransactOpts) (*types.Transaction, error) {
	return _Cpt.contract.Transact(opts, "allocateCptId")
}

// AllocateCptId is a paid mutator transaction binding the contract method 0x744d6436.
//
// Solidity: function allocateCptId() returns(uint256 cptId)
func (_Cpt *CptSession) AllocateCptId() (*types.Transaction, error) {
	return _Cpt.Contract.AllocateCptId(&_Cpt.TransactOpts)
}

// AllocateCptId is a paid mutator transaction binding the contract method 0x744d6436.
//
// Solidity: function allocateCptId() returns(uint256 cptId)
func (_Cpt *CptTransactorSession) AllocateCptId() (*types.Transaction, error) {
	return _Cpt.Contract.AllocateCptId(&_Cpt.TransactOpts)
}

// PutCpt is a paid mutator transaction binding the contract method 0xd2a3b53d.
//
// Solidity: function putCpt(uint256 cptId, address cptPublisher, int256[8] cptIntArray, bytes32[8] cptBytes32Array, bytes32[32] cptJsonSchemaArray, uint8 cptV, bytes32 cptR, bytes32 cptS) returns(bool)
func (_Cpt *CptTransactor) PutCpt(opts *bind.TransactOpts, cptId *big.Int, cptPublisher common.Address, cptIntArray [8]*big.Int, cptBytes32Array [8][32]byte, cptJsonSchemaArray [32][32]byte, cptV uint8, cptR [32]byte, cptS [32]byte) (*types.Transaction, error) {
	return _Cpt.contract.Transact(opts, "putCpt", cptId, cptPublisher, cptIntArray, cptBytes32Array, cptJsonSchemaArray, cptV, cptR, cptS)
}

// PutCpt is a paid mutator transaction binding the contract method 0xd2a3b53d.
//
// Solidity: function putCpt(uint256 cptId, address cptPublisher, int256[8] cptIntArray, bytes32[8] cptBytes32Array, bytes32[32] cptJsonSchemaArray, uint8 cptV, bytes32 cptR, bytes32 cptS) returns(bool)
func (_Cpt *CptSession) PutCpt(cptId *big.Int, cptPublisher common.Address, cptIntArray [8]*big.Int, cptBytes32Array [8][32]byte, cptJsonSchemaArray [32][32]byte, cptV uint8, cptR [32]byte, cptS [32]byte) (*types.Transaction, error) {
	return _Cpt.Contract.PutCpt(&_Cpt.TransactOpts, cptId, cptPublisher, cptIntArray, cptBytes32Array, cptJsonSchemaArray, cptV, cptR, cptS)
}

// PutCpt is a paid mutator transaction binding the contract method 0xd2a3b53d.
//
// Solidity: function putCpt(uint256 cptId, address cptPublisher, int256[8] cptIntArray, bytes32[8] cptBytes32Array, bytes32[32] cptJsonSchemaArray, uint8 cptV, bytes32 cptR, bytes32 cptS) returns(bool)
func (_Cpt *CptTransactorSession) PutCpt(cptId *big.Int, cptPublisher common.Address, cptIntArray [8]*big.Int, cptBytes32Array [8][32]byte, cptJsonSchemaArray [32][32]byte, cptV uint8, cptR [32]byte, cptS [32]byte) (*types.Transaction, error) {
	return _Cpt.Contract.PutCpt(&_Cpt.TransactOpts, cptId, cptPublisher, cptIntArray, cptBytes32Array, cptJsonSchemaArray, cptV, cptR, cptS)
}

// RegisterCpt is a paid mutator transaction binding the contract method 0x47b42f88.
//
// Solidity: function registerCpt(address publisher, int256[8] intArray, bytes32[8] bytes32Array, bytes32[32] jsonSchemaArray, uint8 v, bytes32 r, bytes32 s) returns(bool)
func (_Cpt *CptTransactor) RegisterCpt(opts *bind.TransactOpts, publisher common.Address, intArray [8]*big.Int, bytes32Array [8][32]byte, jsonSchemaArray [32][32]byte, v uint8, r [32]byte, s [32]byte) (*types.Transaction, error) {
	return _Cpt.contract.Transact(opts, "registerCpt", publisher, intArray, bytes32Array, jsonSchemaArray, v, r, s)
}

// RegisterCpt is a paid mutator transaction binding the contract method 0x47b42f88.
//
// Solidity: function registerCpt(address publisher, int256[8] intArray, bytes32[8] bytes32Array, bytes32[32] jsonSchemaArray, uint8 v, bytes32 r, bytes32 s) returns(bool)
func (_Cpt *CptSession) RegisterCpt(publisher common.Address, intArray [8]*big.Int, bytes32Array [8][32]byte, jsonSchemaArray [32][32]byte, v uint8, r [32]byte, s [32]byte) (*types.Transaction, error) {
	return _Cpt.Contract.RegisterCpt(&_Cpt.TransactOpts, publisher, intArray, bytes32Array, jsonSchemaArray, v, r, s)
}

// RegisterCpt is a paid mutator transaction binding the contract method 0x47b42f88.
//
// Solidity: function registerCpt(address publisher, int256[8] intArray, bytes32[8] bytes32Array, bytes32[32] jsonSchemaArray, uint8 v, bytes32 r, bytes32 s) returns(bool)
func (_Cpt *CptTransactorSession) RegisterCpt(publisher common.Address, intArray [8]*big.Int, bytes32Array [8][32]byte, jsonSchemaArray [32][32]byte, v uint8, r [32]byte, s [32]byte) (*types.Transaction, error) {
	return _Cpt.Contract.RegisterCpt(&_Cpt.TransactOpts, publisher, intArray, bytes32Array, jsonSchemaArray, v, r, s)
}

// UpdateCpt is a paid mutator transaction binding the contract method 0x66d6a90b.
//
// Solidity: function updateCpt(uint256 cptId, address publisher, int256[8] intArray, bytes32[8] bytes32Array, bytes32[32] jsonSchemaArray, uint8 v, bytes32 r, bytes32 s) returns(bool)
func (_Cpt *CptTransactor) UpdateCpt(opts *bind.TransactOpts, cptId *big.Int, publisher common.Address, intArray [8]*big.Int, bytes32Array [8][32]byte, jsonSchemaArray [32][32]byte, v uint8, r [32]byte, s [32]byte) (*types.Transaction, error) {
	return _Cpt.contract.Transact(opts, "updateCpt", cptId, publisher, intArray, bytes32Array, jsonSchemaArray, v, r, s)
}

// UpdateCpt is a paid mutator transaction binding the contract method 0x66d6a90b.
//
// Solidity: function updateCpt(uint256 cptId, address publisher, int256[8] intArray, bytes32[8] bytes32Array, bytes32[32] jsonSchemaArray, uint8 v, bytes32 r, bytes32 s) returns(bool)
func (_Cpt *CptSession) UpdateCpt(cptId *big.Int, publisher common.Address, intArray [8]*big.Int, bytes32Array [8][32]byte, jsonSchemaArray [32][32]byte, v uint8, r [32]byte, s [32]byte) (*types.Transaction, error) {
	return _Cpt.Contract.UpdateCpt(&_Cpt.TransactOpts, cptId, publisher, intArray, bytes32Array, jsonSchemaArray, v, r, s)
}

// UpdateCpt is a paid mutator transaction binding the contract method 0x66d6a90b.
//
// Solidity: function updateCpt(uint256 cptId, address publisher, int256[8] intArray, bytes32[8] bytes32Array, bytes32[32] jsonSchemaArray, uint8 v, bytes32 r, bytes32 s) returns(bool)
func (_Cpt *CptTransactorSession) UpdateCpt(cptId *big.Int, publisher common.Address, intArray [8]*big.Int, bytes32Array [8][32]byte, jsonSchemaArray [32][32]byte, v uint8, r [32]byte, s [32]byte) (*types.Transaction, error) {
	return _Cpt.Contract.UpdateCpt(&_Cpt.TransactOpts, cptId, publisher, intArray, bytes32Array, jsonSchemaArray, v, r, s)
}

// CptRegisterCptRetLogIterator is returned from FilterRegisterCptRetLog and is used to iterate over the raw logs and unpacked data for RegisterCptRetLog events raised by the Cpt contract.
type CptRegisterCptRetLogIterator struct {
	Event *CptRegisterCptRetLog // Event containing the contract specifics and raw log

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
func (it *CptRegisterCptRetLogIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(CptRegisterCptRetLog)
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
		it.Event = new(CptRegisterCptRetLog)
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
func (it *CptRegisterCptRetLogIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *CptRegisterCptRetLogIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// CptRegisterCptRetLog represents a RegisterCptRetLog event raised by the Cpt contract.
type CptRegisterCptRetLog struct {
	RetCode    *big.Int
	CptId      *big.Int
	CptVersion *big.Int
	Raw        types.Log // Blockchain specific contextual infos
}

// FilterRegisterCptRetLog is a free log retrieval operation binding the contract event 0xa17f6f29c43d53fdf8a8d5fc788d118621cdca690e8ee29962c3e2fbe70d5eb3.
//
// Solidity: event RegisterCptRetLog(uint256 retCode, uint256 cptId, int256 cptVersion)
func (_Cpt *CptFilterer) FilterRegisterCptRetLog(opts *bind.FilterOpts) (*CptRegisterCptRetLogIterator, error) {

	logs, sub, err := _Cpt.contract.FilterLogs(opts, "RegisterCptRetLog")
	if err != nil {
		return nil, err
	}
	return &CptRegisterCptRetLogIterator{contract: _Cpt.contract, event: "RegisterCptRetLog", logs: logs, sub: sub}, nil
}

// WatchRegisterCptRetLog is a free log subscription operation binding the contract event 0xa17f6f29c43d53fdf8a8d5fc788d118621cdca690e8ee29962c3e2fbe70d5eb3.
//
// Solidity: event RegisterCptRetLog(uint256 retCode, uint256 cptId, int256 cptVersion)
func (_Cpt *CptFilterer) WatchRegisterCptRetLog(opts *bind.WatchOpts, sink chan<- *CptRegisterCptRetLog) (event.Subscription, error) {

	logs, sub, err := _Cpt.contract.WatchLogs(opts, "RegisterCptRetLog")
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(CptRegisterCptRetLog)
				if err := _Cpt.contract.UnpackLog(event, "RegisterCptRetLog", log); err != nil {
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

// ParseRegisterCptRetLog is a log parse operation binding the contract event 0xa17f6f29c43d53fdf8a8d5fc788d118621cdca690e8ee29962c3e2fbe70d5eb3.
//
// Solidity: event RegisterCptRetLog(uint256 retCode, uint256 cptId, int256 cptVersion)
func (_Cpt *CptFilterer) ParseRegisterCptRetLog(log types.Log) (*CptRegisterCptRetLog, error) {
	event := new(CptRegisterCptRetLog)
	if err := _Cpt.contract.UnpackLog(event, "RegisterCptRetLog", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}

// CptUpdateCptRetLogIterator is returned from FilterUpdateCptRetLog and is used to iterate over the raw logs and unpacked data for UpdateCptRetLog events raised by the Cpt contract.
type CptUpdateCptRetLogIterator struct {
	Event *CptUpdateCptRetLog // Event containing the contract specifics and raw log

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
func (it *CptUpdateCptRetLogIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(CptUpdateCptRetLog)
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
		it.Event = new(CptUpdateCptRetLog)
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
func (it *CptUpdateCptRetLogIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *CptUpdateCptRetLogIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// CptUpdateCptRetLog represents a UpdateCptRetLog event raised by the Cpt contract.
type CptUpdateCptRetLog struct {
	RetCode    *big.Int
	CptId      *big.Int
	CptVersion *big.Int
	Raw        types.Log // Blockchain specific contextual infos
}

// FilterUpdateCptRetLog is a free log retrieval operation binding the contract event 0x2614d1ec3482cc2505bf211c39bee96c28940521311ec70c9ebf14d3896fd196.
//
// Solidity: event UpdateCptRetLog(uint256 retCode, uint256 cptId, int256 cptVersion)
func (_Cpt *CptFilterer) FilterUpdateCptRetLog(opts *bind.FilterOpts) (*CptUpdateCptRetLogIterator, error) {

	logs, sub, err := _Cpt.contract.FilterLogs(opts, "UpdateCptRetLog")
	if err != nil {
		return nil, err
	}
	return &CptUpdateCptRetLogIterator{contract: _Cpt.contract, event: "UpdateCptRetLog", logs: logs, sub: sub}, nil
}

// WatchUpdateCptRetLog is a free log subscription operation binding the contract event 0x2614d1ec3482cc2505bf211c39bee96c28940521311ec70c9ebf14d3896fd196.
//
// Solidity: event UpdateCptRetLog(uint256 retCode, uint256 cptId, int256 cptVersion)
func (_Cpt *CptFilterer) WatchUpdateCptRetLog(opts *bind.WatchOpts, sink chan<- *CptUpdateCptRetLog) (event.Subscription, error) {

	logs, sub, err := _Cpt.contract.WatchLogs(opts, "UpdateCptRetLog")
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(CptUpdateCptRetLog)
				if err := _Cpt.contract.UnpackLog(event, "UpdateCptRetLog", log); err != nil {
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

// ParseUpdateCptRetLog is a log parse operation binding the contract event 0x2614d1ec3482cc2505bf211c39bee96c28940521311ec70c9ebf14d3896fd196.
//
// Solidity: event UpdateCptRetLog(uint256 retCode, uint256 cptId, int256 cptVersion)
func (_Cpt *CptFilterer) ParseUpdateCptRetLog(log types.Log) (*CptUpdateCptRetLog, error) {
	event := new(CptUpdateCptRetLog)
	if err := _Cpt.contract.UnpackLog(event, "UpdateCptRetLog", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}
