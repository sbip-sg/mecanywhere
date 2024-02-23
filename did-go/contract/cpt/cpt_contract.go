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
	ABI: "[{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"retCode\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"int256\",\"name\":\"cptVersion\",\"type\":\"int256\"}],\"name\":\"RegisterCptRetLog\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"retCode\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"int256\",\"name\":\"cptVersion\",\"type\":\"int256\"}],\"name\":\"UpdateCptRetLog\",\"type\":\"event\"},{\"inputs\":[],\"name\":\"CPT_ISSUE_MAX_ID\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"CPT_ISSUE_START_ID\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"allocateCptId\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"},{\"internalType\":\"bool\",\"name\":\"success\",\"type\":\"bool\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"getCptCounts\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"}],\"name\":\"getCptDynamicBytes32Array\",\"outputs\":[{\"internalType\":\"bytes32[]\",\"name\":\"\",\"type\":\"bytes32[]\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"}],\"name\":\"getCptDynamicIntArray\",\"outputs\":[{\"internalType\":\"int256[]\",\"name\":\"\",\"type\":\"int256[]\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"}],\"name\":\"getCptDynamicJsonSchemaArray\",\"outputs\":[{\"internalType\":\"bytes32[]\",\"name\":\"\",\"type\":\"bytes32[]\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"index\",\"type\":\"uint256\"}],\"name\":\"getCptIdFromIndex\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"startPos\",\"type\":\"uint256\"},{\"internalType\":\"uint256\",\"name\":\"num\",\"type\":\"uint256\"}],\"name\":\"getCptIdList\",\"outputs\":[{\"internalType\":\"uint256[]\",\"name\":\"\",\"type\":\"uint256[]\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"}],\"name\":\"getCptIntArray\",\"outputs\":[{\"internalType\":\"int256[8]\",\"name\":\"intArray\",\"type\":\"int256[8]\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"}],\"name\":\"getCptPublisher\",\"outputs\":[{\"internalType\":\"address\",\"name\":\"publisher\",\"type\":\"address\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"}],\"name\":\"getCptSignature\",\"outputs\":[{\"internalType\":\"uint8\",\"name\":\"v\",\"type\":\"uint8\"},{\"internalType\":\"bytes32\",\"name\":\"r\",\"type\":\"bytes32\"},{\"internalType\":\"bytes32\",\"name\":\"s\",\"type\":\"bytes32\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"getTotalCptId\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"}],\"name\":\"isCptExist\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"\",\"type\":\"bool\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"},{\"internalType\":\"address\",\"name\":\"cptPublisher\",\"type\":\"address\"},{\"internalType\":\"int256[8]\",\"name\":\"cptIntArray\",\"type\":\"int256[8]\"},{\"internalType\":\"bytes32[8]\",\"name\":\"cptBytes32Array\",\"type\":\"bytes32[8]\"},{\"internalType\":\"bytes32[32]\",\"name\":\"cptJsonSchemaArray\",\"type\":\"bytes32[32]\"},{\"internalType\":\"uint8\",\"name\":\"cptV\",\"type\":\"uint8\"},{\"internalType\":\"bytes32\",\"name\":\"cptR\",\"type\":\"bytes32\"},{\"internalType\":\"bytes32\",\"name\":\"cptS\",\"type\":\"bytes32\"}],\"name\":\"putCpt\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"\",\"type\":\"bool\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"}],\"name\":\"queryCpt\",\"outputs\":[{\"internalType\":\"address\",\"name\":\"publisher\",\"type\":\"address\"},{\"internalType\":\"int256[]\",\"name\":\"intArray\",\"type\":\"int256[]\"},{\"internalType\":\"bytes32[]\",\"name\":\"bytes32Array\",\"type\":\"bytes32[]\"},{\"internalType\":\"bytes32[]\",\"name\":\"jsonSchemaArray\",\"type\":\"bytes32[]\"},{\"internalType\":\"uint8\",\"name\":\"v\",\"type\":\"uint8\"},{\"internalType\":\"bytes32\",\"name\":\"r\",\"type\":\"bytes32\"},{\"internalType\":\"bytes32\",\"name\":\"s\",\"type\":\"bytes32\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"publisher\",\"type\":\"address\"},{\"internalType\":\"int256[8]\",\"name\":\"intArray\",\"type\":\"int256[8]\"},{\"internalType\":\"bytes32[8]\",\"name\":\"bytes32Array\",\"type\":\"bytes32[8]\"},{\"internalType\":\"bytes32[32]\",\"name\":\"jsonSchemaArray\",\"type\":\"bytes32[32]\"},{\"internalType\":\"uint8\",\"name\":\"v\",\"type\":\"uint8\"},{\"internalType\":\"bytes32\",\"name\":\"r\",\"type\":\"bytes32\"},{\"internalType\":\"bytes32\",\"name\":\"s\",\"type\":\"bytes32\"}],\"name\":\"registerCpt\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"\",\"type\":\"bool\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"},{\"internalType\":\"address\",\"name\":\"publisher\",\"type\":\"address\"},{\"internalType\":\"int256[8]\",\"name\":\"intArray\",\"type\":\"int256[8]\"},{\"internalType\":\"bytes32[8]\",\"name\":\"bytes32Array\",\"type\":\"bytes32[8]\"},{\"internalType\":\"bytes32[32]\",\"name\":\"jsonSchemaArray\",\"type\":\"bytes32[32]\"},{\"internalType\":\"uint8\",\"name\":\"v\",\"type\":\"uint8\"},{\"internalType\":\"bytes32\",\"name\":\"r\",\"type\":\"bytes32\"},{\"internalType\":\"bytes32\",\"name\":\"s\",\"type\":\"bytes32\"}],\"name\":\"updateCpt\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"\",\"type\":\"bool\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"}]",
	Bin: "0x60806040526103e85f55348015610014575f80fd5b50612249806100225f395ff3fe608060405234801561000f575f80fd5b5060043610610114575f3560e01c8063672ddcf0116100a0578063b4af70901161006f578063b4af709014610347578063b776755b14610377578063d2a3b53d14610395578063d4eb8a42146103c5578063e5741ff3146103f557610114565b8063672ddcf0146102985780636da223b7146102c8578063744d6436146102f8578063a07bd9b51461031757610114565b80632984fcc8116100e75780632984fcc8146101c657806347b42f88146101e45780634cf5e2d5146102145780635ca35abf1461023257806366d6a90b1461026857610114565b80630d7aad0314610118578063102b508d146101365780631e040fc71461016657806323b746f114610196575b5f80fd5b610120610427565b60405161012d91906115c9565b60405180910390f35b610150600480360381019061014b9190611619565b61042f565b60405161015d9190611704565b60405180910390f35b610180600480360381019061017b9190611724565b610666565b60405161018d9190611819565b60405180910390f35b6101b060048036038101906101ab9190611619565b61079c565b6040516101bd91906118e7565b60405180910390f35b6101ce610936565b6040516101db91906115c9565b60405180910390f35b6101fe60048036038101906101f99190611c7f565b610944565b60405161020b9190611d3c565b60405180910390f35b61021c610961565b60405161022991906115c9565b60405180910390f35b61024c60048036038101906102479190611619565b61096d565b60405161025f9796959493929190611e13565b60405180910390f35b610282600480360381019061027d9190611e95565b610998565b60405161028f9190611d3c565b60405180910390f35b6102b260048036038101906102ad9190611619565b6109b7565b6040516102bf9190611f4b565b60405180910390f35b6102e260048036038101906102dd9190611619565b610a6c565b6040516102ef9190611f6b565b60405180910390f35b610300610bfe565b60405161030e929190611f84565b60405180910390f35b610331600480360381019061032c9190611619565b610c38565b60405161033e91906115c9565b60405180910390f35b610361600480360381019061035c9190611619565b610c5d565b60405161036e9190611704565b60405180910390f35b61037f610e94565b60405161038c91906115c9565b60405180910390f35b6103af60048036038101906103aa9190611e95565b610e9a565b6040516103bc9190611d3c565b60405180910390f35b6103df60048036038101906103da9190611619565b61100d565b6040516103ec9190611d3c565b60405180910390f35b61040f600480360381019061040a9190611619565b611077565b60405161041e93929190611fab565b60405180910390f35b633b9ac9ff81565b60605f60015f8481526020019081526020015f206040518060a00160405290815f82015f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001600182016008806020026040519081016040528092919082600880156104de576020028201915b8154815260200190600101908083116104ca575b5050505050815260200160098201600880602002604051908101604052809291908260088015610523576020028201915b81548152602001906001019080831161050f575b5050505050815260200160118201602080602002604051908101604052809291908260208015610568576020028201915b815481526020019060010190808311610554575b50505050508152602001603182016040518060600160405290815f82015f9054906101000a900460ff1660ff1660ff168152602001600182015481526020016002820154815250508152505090505f816040015190505f600867ffffffffffffffff8111156105da576105d961196f565b5b6040519080825280602002602001820160405280156106085781602001602082028036833780820191505090505b5090505f5b600881101561065a5782816008811061062957610628611fe0565b5b602002015182828151811061064157610640611fe0565b5b602002602001018181525050808060010191505061060d565b50809350505050919050565b60605f610671610961565b90505f848210156106cf57600167ffffffffffffffff8111156106975761069661196f565b5b6040519080825280602002602001820160405280156106c55781602001602082028036833780820191505090505b5092505050610796565b83856106db919061203a565b82116106f45784826106ed919061206d565b90506106f8565b8390505b5f8167ffffffffffffffff8111156107135761071261196f565b5b6040519080825280602002602001820160405280156107415781602001602082028036833780820191505090505b5090505f5b8281101561078e57610762818861075d919061203a565b610c38565b82828151811061077557610774611fe0565b5b6020026020010181815250508080600101915050610746565b508093505050505b92915050565b6107a4611498565b5f60015f8481526020019081526020015f206040518060a00160405290815f82015f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200160018201600880602002604051908101604052809291908260088015610851576020028201915b81548152602001906001019080831161083d575b5050505050815260200160098201600880602002604051908101604052809291908260088015610896576020028201915b815481526020019060010190808311610882575b50505050508152602001601182016020806020026040519081016040528092919082602080156108db576020028201915b8154815260200190600101908083116108c7575b50505050508152602001603182016040518060600160405290815f82015f9054906101000a900460ff1660ff1660ff168152602001600182015481526020016002820154815250508152505090508060200151915050919050565b5f61093f610961565b905090565b5f61095488888888888888611227565b9050979650505050505050565b5f600280549050905090565b5f60608060605f805f61097f88611304565b9650965096509650965096509650919395979092949650565b5f6109a98989898989898989611359565b905098975050505050505050565b60605f6109c38361079c565b90505f600867ffffffffffffffff8111156109e1576109e061196f565b5b604051908082528060200260200182016040528015610a0f5781602001602082028036833780820191505090505b5090505f5b6008811015610a6157828160088110610a3057610a2f611fe0565b5b6020020151828281518110610a4857610a47611fe0565b5b6020026020010181815250508080600101915050610a14565b508092505050919050565b5f8060015f8481526020019081526020015f206040518060a00160405290815f82015f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200160018201600880602002604051908101604052809291908260088015610b1a576020028201915b815481526020019060010190808311610b06575b5050505050815260200160098201600880602002604051908101604052809291908260088015610b5f576020028201915b815481526020019060010190808311610b4b575b5050505050815260200160118201602080602002604051908101604052809291908260208015610ba4576020028201915b815481526020019060010190808311610b90575b50505050508152602001603182016040518060600160405290815f82015f9054906101000a900460ff1660ff1660ff16815260200160018201548152602001600282015481525050815250509050805f0151915050919050565b5f80633b9ac9ff5f541115610c18575f8091509150610c34565b5f80815480929190610c29906120a0565b919050559150600190505b9091565b5f60028281548110610c4d57610c4c611fe0565b5b905f5260205f2001549050919050565b60605f60015f8481526020019081526020015f206040518060a00160405290815f82015f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200160018201600880602002604051908101604052809291908260088015610d0c576020028201915b815481526020019060010190808311610cf8575b5050505050815260200160098201600880602002604051908101604052809291908260088015610d51576020028201915b815481526020019060010190808311610d3d575b5050505050815260200160118201602080602002604051908101604052809291908260208015610d96576020028201915b815481526020019060010190808311610d82575b50505050508152602001603182016040518060600160405290815f82015f9054906101000a900460ff1660ff1660ff168152602001600182015481526020016002820154815250508152505090505f816060015190505f602067ffffffffffffffff811115610e0857610e0761196f565b5b604051908082528060200260200182016040528015610e365781602001602082028036833780820191505090505b5090505f5b6020811015610e8857828160208110610e5757610e56611fe0565b5b6020020151828281518110610e6f57610e6e611fe0565b5b6020026020010181815250508080600101915050610e3b565b50809350505050919050565b6103e881565b5f8060405180606001604052808660ff1681526020018581526020018481525090506040518060a001604052808a73ffffffffffffffffffffffffffffffffffffffff1681526020018981526020018881526020018781526020018281525060015f8c81526020019081526020015f205f820151815f015f6101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550602082015181600101906008610f659291906114bb565b50604082015181600901906008610f7d9291906114fb565b50606082015181601101906020610f9592919061153b565b506080820151816031015f820151815f015f6101000a81548160ff021916908360ff1602179055506020820151816001015560408201518160020155505090505060028a908060018154018082558091505060019003905f5260205f20015f9091909190915055600191505098975050505050505050565b5f8073ffffffffffffffffffffffffffffffffffffffff1660015f8481526020019081526020015f205f015f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614159050919050565b5f805f8060015f8681526020019081526020015f206040518060a00160405290815f82015f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200160018201600880602002604051908101604052809291908260088015611127576020028201915b815481526020019060010190808311611113575b505050505081526020016009820160088060200260405190810160405280929190826008801561116c576020028201915b815481526020019060010190808311611158575b50505050508152602001601182016020806020026040519081016040528092919082602080156111b1576020028201915b81548152602001906001019080831161119d575b50505050508152602001603182016040518060600160405290815f82015f9054906101000a900460ff1660ff1660ff1681526020016001820154815260200160028201548152505081525050905080608001515f0151935080608001516020015192508060800151604001519150509193909250565b5f805f611232610bfe565b9150915080611283577fa17f6f29c43d53fdf8a8d5fc788d118621cdca690e8ee29962c3e2fbe70d5eb36207a24e5f8060405161127193929190612159565b60405180910390a15f925050506112f9565b5f60019050808a5f6008811061129c5761129b611fe0565b5b6020020181815250506112b5838c8c8c8c8c8c8c610e9a565b507fa17f6f29c43d53fdf8a8d5fc788d118621cdca690e8ee29962c3e2fbe70d5eb35f84836040516112e99392919061219d565b60405180910390a1600193505050505b979650505050505050565b5f60608060605f805f61131688610a6c565b9650611321886109b7565b955061132c8861042f565b945061133788610c5d565b935061134288611077565b809350819450829550505050919395979092949650565b5f6113638961100d565b1561144a575f6113728a61079c565b90505f6001825f6008811061138a57611389611fe0565b5b602002015161139991906121d2565b905080895f600881106113af576113ae611fe0565b5b6020020181815250505f826001600881106113cd576113cc611fe0565b5b60200201519050808a6001600881106113e9576113e8611fe0565b5b6020020181815250506114028c8c8c8c8c8c8c8c610e9a565b507f2614d1ec3482cc2505bf211c39bee96c28940521311ec70c9ebf14d3896fd1965f8d846040516114369392919061219d565b60405180910390a16001935050505061148c565b7f2614d1ec3482cc2505bf211c39bee96c28940521311ec70c9ebf14d3896fd1966207a24d5f8060405161148093929190612159565b60405180910390a15f90505b98975050505050505050565b604051806101000160405280600890602082028036833780820191505090505090565b82600881019282156114ea579160200282015b828111156114e95782518255916020019190600101906114ce565b5b5090506114f7919061157b565b5090565b826008810192821561152a579160200282015b8281111561152957825182559160200191906001019061150e565b5b5090506115379190611596565b5090565b826020810192821561156a579160200282015b8281111561156957825182559160200191906001019061154e565b5b5090506115779190611596565b5090565b5b80821115611592575f815f90555060010161157c565b5090565b5b808211156115ad575f815f905550600101611597565b5090565b5f819050919050565b6115c3816115b1565b82525050565b5f6020820190506115dc5f8301846115ba565b92915050565b5f604051905090565b5f80fd5b6115f8816115b1565b8114611602575f80fd5b50565b5f81359050611613816115ef565b92915050565b5f6020828403121561162e5761162d6115eb565b5b5f61163b84828501611605565b91505092915050565b5f81519050919050565b5f82825260208201905092915050565b5f819050602082019050919050565b5f819050919050565b61167f8161166d565b82525050565b5f6116908383611676565b60208301905092915050565b5f602082019050919050565b5f6116b282611644565b6116bc818561164e565b93506116c78361165e565b805f5b838110156116f75781516116de8882611685565b97506116e98361169c565b9250506001810190506116ca565b5085935050505092915050565b5f6020820190508181035f83015261171c81846116a8565b905092915050565b5f806040838503121561173a576117396115eb565b5b5f61174785828601611605565b925050602061175885828601611605565b9150509250929050565b5f81519050919050565b5f82825260208201905092915050565b5f819050602082019050919050565b611794816115b1565b82525050565b5f6117a5838361178b565b60208301905092915050565b5f602082019050919050565b5f6117c782611762565b6117d1818561176c565b93506117dc8361177c565b805f5b8381101561180c5781516117f3888261179a565b97506117fe836117b1565b9250506001810190506117df565b5085935050505092915050565b5f6020820190508181035f83015261183181846117bd565b905092915050565b5f60089050919050565b5f81905092915050565b5f819050919050565b5f819050919050565b61186881611856565b82525050565b5f611879838361185f565b60208301905092915050565b5f602082019050919050565b61189a81611839565b6118a48184611843565b92506118af8261184d565b805f5b838110156118df5781516118c6878261186e565b96506118d183611885565b9250506001810190506118b2565b505050505050565b5f610100820190506118fb5f830184611891565b92915050565b5f73ffffffffffffffffffffffffffffffffffffffff82169050919050565b5f61192a82611901565b9050919050565b61193a81611920565b8114611944575f80fd5b50565b5f8135905061195581611931565b92915050565b5f80fd5b5f601f19601f8301169050919050565b7f4e487b71000000000000000000000000000000000000000000000000000000005f52604160045260245ffd5b6119a58261195f565b810181811067ffffffffffffffff821117156119c4576119c361196f565b5b80604052505050565b5f6119d66115e2565b90506119e2828261199c565b919050565b5f67ffffffffffffffff821115611a0157611a0061196f565b5b602082029050919050565b5f80fd5b611a1981611856565b8114611a23575f80fd5b50565b5f81359050611a3481611a10565b92915050565b5f611a4c611a47846119e7565b6119cd565b90508060208402830185811115611a6657611a65611a0c565b5b835b81811015611a8f5780611a7b8882611a26565b845260208401935050602081019050611a68565b5050509392505050565b5f82601f830112611aad57611aac61195b565b5b6008611aba848285611a3a565b91505092915050565b5f67ffffffffffffffff821115611add57611adc61196f565b5b602082029050919050565b611af18161166d565b8114611afb575f80fd5b50565b5f81359050611b0c81611ae8565b92915050565b5f611b24611b1f84611ac3565b6119cd565b90508060208402830185811115611b3e57611b3d611a0c565b5b835b81811015611b675780611b538882611afe565b845260208401935050602081019050611b40565b5050509392505050565b5f82601f830112611b8557611b8461195b565b5b6008611b92848285611b12565b91505092915050565b5f67ffffffffffffffff821115611bb557611bb461196f565b5b602082029050919050565b5f611bd2611bcd84611b9b565b6119cd565b90508060208402830185811115611bec57611beb611a0c565b5b835b81811015611c155780611c018882611afe565b845260208401935050602081019050611bee565b5050509392505050565b5f82601f830112611c3357611c3261195b565b5b6020611c40848285611bc0565b91505092915050565b5f60ff82169050919050565b611c5e81611c49565b8114611c68575f80fd5b50565b5f81359050611c7981611c55565b92915050565b5f805f805f805f610680888a031215611c9b57611c9a6115eb565b5b5f611ca88a828b01611947565b9750506020611cb98a828b01611a99565b965050610120611ccb8a828b01611b71565b955050610220611cdd8a828b01611c1f565b945050610620611cef8a828b01611c6b565b935050610640611d018a828b01611afe565b925050610660611d138a828b01611afe565b91505092959891949750929550565b5f8115159050919050565b611d3681611d22565b82525050565b5f602082019050611d4f5f830184611d2d565b92915050565b611d5e81611920565b82525050565b5f81519050919050565b5f82825260208201905092915050565b5f819050602082019050919050565b5f602082019050919050565b5f611da382611d64565b611dad8185611d6e565b9350611db883611d7e565b805f5b83811015611de8578151611dcf888261186e565b9750611dda83611d8d565b925050600181019050611dbb565b5085935050505092915050565b611dfe81611c49565b82525050565b611e0d8161166d565b82525050565b5f60e082019050611e265f83018a611d55565b8181036020830152611e388189611d99565b90508181036040830152611e4c81886116a8565b90508181036060830152611e6081876116a8565b9050611e6f6080830186611df5565b611e7c60a0830185611e04565b611e8960c0830184611e04565b98975050505050505050565b5f805f805f805f806106a0898b031215611eb257611eb16115eb565b5b5f611ebf8b828c01611605565b9850506020611ed08b828c01611947565b9750506040611ee18b828c01611a99565b965050610140611ef38b828c01611b71565b955050610240611f058b828c01611c1f565b945050610640611f178b828c01611c6b565b935050610660611f298b828c01611afe565b925050610680611f3b8b828c01611afe565b9150509295985092959890939650565b5f6020820190508181035f830152611f638184611d99565b905092915050565b5f602082019050611f7e5f830184611d55565b92915050565b5f604082019050611f975f8301856115ba565b611fa46020830184611d2d565b9392505050565b5f606082019050611fbe5f830186611df5565b611fcb6020830185611e04565b611fd86040830184611e04565b949350505050565b7f4e487b71000000000000000000000000000000000000000000000000000000005f52603260045260245ffd5b7f4e487b71000000000000000000000000000000000000000000000000000000005f52601160045260245ffd5b5f612044826115b1565b915061204f836115b1565b92508282019050808211156120675761206661200d565b5b92915050565b5f612077826115b1565b9150612082836115b1565b925082820390508181111561209a5761209961200d565b5b92915050565b5f6120aa826115b1565b91507fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff82036120dc576120db61200d565b5b600182019050919050565b5f819050919050565b5f819050919050565b5f61211361210e612109846120e7565b6120f0565b6115b1565b9050919050565b612123816120f9565b82525050565b5f61214361213e612139846120e7565b6120f0565b611856565b9050919050565b61215381612129565b82525050565b5f60608201905061216c5f8301866115ba565b612179602083018561211a565b612186604083018461214a565b949350505050565b61219781611856565b82525050565b5f6060820190506121b05f83018661211a565b6121bd60208301856115ba565b6121ca604083018461218e565b949350505050565b5f6121dc82611856565b91506121e783611856565b92508282019050828112155f8312168382125f84121516171561220d5761220c61200d565b5b9291505056fea26469706673582212201024cc40bf4a9b0a69cf02bd67586aeef1492c070c22d7157e6bb8bbfea1017064736f6c63430008180033",
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

// CPTISSUEMAXID is a free data retrieval call binding the contract method 0x0d7aad03.
//
// Solidity: function CPT_ISSUE_MAX_ID() view returns(uint256)
func (_Cpt *CptCaller) CPTISSUEMAXID(opts *bind.CallOpts) (*big.Int, error) {
	var out []interface{}
	err := _Cpt.contract.Call(opts, &out, "CPT_ISSUE_MAX_ID")

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// CPTISSUEMAXID is a free data retrieval call binding the contract method 0x0d7aad03.
//
// Solidity: function CPT_ISSUE_MAX_ID() view returns(uint256)
func (_Cpt *CptSession) CPTISSUEMAXID() (*big.Int, error) {
	return _Cpt.Contract.CPTISSUEMAXID(&_Cpt.CallOpts)
}

// CPTISSUEMAXID is a free data retrieval call binding the contract method 0x0d7aad03.
//
// Solidity: function CPT_ISSUE_MAX_ID() view returns(uint256)
func (_Cpt *CptCallerSession) CPTISSUEMAXID() (*big.Int, error) {
	return _Cpt.Contract.CPTISSUEMAXID(&_Cpt.CallOpts)
}

// CPTISSUESTARTID is a free data retrieval call binding the contract method 0xb776755b.
//
// Solidity: function CPT_ISSUE_START_ID() view returns(uint256)
func (_Cpt *CptCaller) CPTISSUESTARTID(opts *bind.CallOpts) (*big.Int, error) {
	var out []interface{}
	err := _Cpt.contract.Call(opts, &out, "CPT_ISSUE_START_ID")

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// CPTISSUESTARTID is a free data retrieval call binding the contract method 0xb776755b.
//
// Solidity: function CPT_ISSUE_START_ID() view returns(uint256)
func (_Cpt *CptSession) CPTISSUESTARTID() (*big.Int, error) {
	return _Cpt.Contract.CPTISSUESTARTID(&_Cpt.CallOpts)
}

// CPTISSUESTARTID is a free data retrieval call binding the contract method 0xb776755b.
//
// Solidity: function CPT_ISSUE_START_ID() view returns(uint256)
func (_Cpt *CptCallerSession) CPTISSUESTARTID() (*big.Int, error) {
	return _Cpt.Contract.CPTISSUESTARTID(&_Cpt.CallOpts)
}

// GetCptCounts is a free data retrieval call binding the contract method 0x4cf5e2d5.
//
// Solidity: function getCptCounts() view returns(uint256)
func (_Cpt *CptCaller) GetCptCounts(opts *bind.CallOpts) (*big.Int, error) {
	var out []interface{}
	err := _Cpt.contract.Call(opts, &out, "getCptCounts")

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// GetCptCounts is a free data retrieval call binding the contract method 0x4cf5e2d5.
//
// Solidity: function getCptCounts() view returns(uint256)
func (_Cpt *CptSession) GetCptCounts() (*big.Int, error) {
	return _Cpt.Contract.GetCptCounts(&_Cpt.CallOpts)
}

// GetCptCounts is a free data retrieval call binding the contract method 0x4cf5e2d5.
//
// Solidity: function getCptCounts() view returns(uint256)
func (_Cpt *CptCallerSession) GetCptCounts() (*big.Int, error) {
	return _Cpt.Contract.GetCptCounts(&_Cpt.CallOpts)
}

// GetCptDynamicBytes32Array is a free data retrieval call binding the contract method 0x102b508d.
//
// Solidity: function getCptDynamicBytes32Array(uint256 cptId) view returns(bytes32[])
func (_Cpt *CptCaller) GetCptDynamicBytes32Array(opts *bind.CallOpts, cptId *big.Int) ([][32]byte, error) {
	var out []interface{}
	err := _Cpt.contract.Call(opts, &out, "getCptDynamicBytes32Array", cptId)

	if err != nil {
		return *new([][32]byte), err
	}

	out0 := *abi.ConvertType(out[0], new([][32]byte)).(*[][32]byte)

	return out0, err

}

// GetCptDynamicBytes32Array is a free data retrieval call binding the contract method 0x102b508d.
//
// Solidity: function getCptDynamicBytes32Array(uint256 cptId) view returns(bytes32[])
func (_Cpt *CptSession) GetCptDynamicBytes32Array(cptId *big.Int) ([][32]byte, error) {
	return _Cpt.Contract.GetCptDynamicBytes32Array(&_Cpt.CallOpts, cptId)
}

// GetCptDynamicBytes32Array is a free data retrieval call binding the contract method 0x102b508d.
//
// Solidity: function getCptDynamicBytes32Array(uint256 cptId) view returns(bytes32[])
func (_Cpt *CptCallerSession) GetCptDynamicBytes32Array(cptId *big.Int) ([][32]byte, error) {
	return _Cpt.Contract.GetCptDynamicBytes32Array(&_Cpt.CallOpts, cptId)
}

// GetCptDynamicIntArray is a free data retrieval call binding the contract method 0x672ddcf0.
//
// Solidity: function getCptDynamicIntArray(uint256 cptId) view returns(int256[])
func (_Cpt *CptCaller) GetCptDynamicIntArray(opts *bind.CallOpts, cptId *big.Int) ([]*big.Int, error) {
	var out []interface{}
	err := _Cpt.contract.Call(opts, &out, "getCptDynamicIntArray", cptId)

	if err != nil {
		return *new([]*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new([]*big.Int)).(*[]*big.Int)

	return out0, err

}

// GetCptDynamicIntArray is a free data retrieval call binding the contract method 0x672ddcf0.
//
// Solidity: function getCptDynamicIntArray(uint256 cptId) view returns(int256[])
func (_Cpt *CptSession) GetCptDynamicIntArray(cptId *big.Int) ([]*big.Int, error) {
	return _Cpt.Contract.GetCptDynamicIntArray(&_Cpt.CallOpts, cptId)
}

// GetCptDynamicIntArray is a free data retrieval call binding the contract method 0x672ddcf0.
//
// Solidity: function getCptDynamicIntArray(uint256 cptId) view returns(int256[])
func (_Cpt *CptCallerSession) GetCptDynamicIntArray(cptId *big.Int) ([]*big.Int, error) {
	return _Cpt.Contract.GetCptDynamicIntArray(&_Cpt.CallOpts, cptId)
}

// GetCptDynamicJsonSchemaArray is a free data retrieval call binding the contract method 0xb4af7090.
//
// Solidity: function getCptDynamicJsonSchemaArray(uint256 cptId) view returns(bytes32[])
func (_Cpt *CptCaller) GetCptDynamicJsonSchemaArray(opts *bind.CallOpts, cptId *big.Int) ([][32]byte, error) {
	var out []interface{}
	err := _Cpt.contract.Call(opts, &out, "getCptDynamicJsonSchemaArray", cptId)

	if err != nil {
		return *new([][32]byte), err
	}

	out0 := *abi.ConvertType(out[0], new([][32]byte)).(*[][32]byte)

	return out0, err

}

// GetCptDynamicJsonSchemaArray is a free data retrieval call binding the contract method 0xb4af7090.
//
// Solidity: function getCptDynamicJsonSchemaArray(uint256 cptId) view returns(bytes32[])
func (_Cpt *CptSession) GetCptDynamicJsonSchemaArray(cptId *big.Int) ([][32]byte, error) {
	return _Cpt.Contract.GetCptDynamicJsonSchemaArray(&_Cpt.CallOpts, cptId)
}

// GetCptDynamicJsonSchemaArray is a free data retrieval call binding the contract method 0xb4af7090.
//
// Solidity: function getCptDynamicJsonSchemaArray(uint256 cptId) view returns(bytes32[])
func (_Cpt *CptCallerSession) GetCptDynamicJsonSchemaArray(cptId *big.Int) ([][32]byte, error) {
	return _Cpt.Contract.GetCptDynamicJsonSchemaArray(&_Cpt.CallOpts, cptId)
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
// Solidity: function allocateCptId() returns(uint256 cptId, bool success)
func (_Cpt *CptTransactor) AllocateCptId(opts *bind.TransactOpts) (*types.Transaction, error) {
	return _Cpt.contract.Transact(opts, "allocateCptId")
}

// AllocateCptId is a paid mutator transaction binding the contract method 0x744d6436.
//
// Solidity: function allocateCptId() returns(uint256 cptId, bool success)
func (_Cpt *CptSession) AllocateCptId() (*types.Transaction, error) {
	return _Cpt.Contract.AllocateCptId(&_Cpt.TransactOpts)
}

// AllocateCptId is a paid mutator transaction binding the contract method 0x744d6436.
//
// Solidity: function allocateCptId() returns(uint256 cptId, bool success)
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
