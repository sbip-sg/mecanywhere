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
	ABI: "[{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"retCode\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"int256\",\"name\":\"cptVersion\",\"type\":\"int256\"}],\"name\":\"RegisterCptRetLog\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"retCode\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"int256\",\"name\":\"cptVersion\",\"type\":\"int256\"}],\"name\":\"UpdateCptRetLog\",\"type\":\"event\"},{\"inputs\":[],\"name\":\"AUTHORITY_ISSUER_START_ID\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"NONE_AUTHORITY_ISSUER_START_ID\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"}],\"name\":\"getCptBytes32Array\",\"outputs\":[{\"internalType\":\"bytes32[8]\",\"name\":\"bytes32Array\",\"type\":\"bytes32[8]\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"},{\"internalType\":\"address\",\"name\":\"dataStorageAddress\",\"type\":\"address\"}],\"name\":\"getCptDynamicBytes32Array\",\"outputs\":[{\"internalType\":\"bytes32[]\",\"name\":\"\",\"type\":\"bytes32[]\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"},{\"internalType\":\"address\",\"name\":\"dataStorageAddress\",\"type\":\"address\"}],\"name\":\"getCptDynamicIntArray\",\"outputs\":[{\"internalType\":\"int256[]\",\"name\":\"\",\"type\":\"int256[]\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"},{\"internalType\":\"address\",\"name\":\"dataStorageAddress\",\"type\":\"address\"}],\"name\":\"getCptDynamicJsonSchemaArray\",\"outputs\":[{\"internalType\":\"bytes32[]\",\"name\":\"\",\"type\":\"bytes32[]\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"getCptId\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"index\",\"type\":\"uint256\"}],\"name\":\"getCptIdFromIndex\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"startPos\",\"type\":\"uint256\"},{\"internalType\":\"uint256\",\"name\":\"num\",\"type\":\"uint256\"}],\"name\":\"getCptIdList\",\"outputs\":[{\"internalType\":\"uint256[]\",\"name\":\"\",\"type\":\"uint256[]\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"}],\"name\":\"getCptIntArray\",\"outputs\":[{\"internalType\":\"int256[8]\",\"name\":\"intArray\",\"type\":\"int256[8]\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"}],\"name\":\"getCptJsonSchemaArray\",\"outputs\":[{\"internalType\":\"bytes32[32]\",\"name\":\"jsonSchemaArray\",\"type\":\"bytes32[32]\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"}],\"name\":\"getCptPublisher\",\"outputs\":[{\"internalType\":\"address\",\"name\":\"publisher\",\"type\":\"address\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"}],\"name\":\"getCptSignature\",\"outputs\":[{\"internalType\":\"uint8\",\"name\":\"v\",\"type\":\"uint8\"},{\"internalType\":\"bytes32\",\"name\":\"r\",\"type\":\"bytes32\"},{\"internalType\":\"bytes32\",\"name\":\"s\",\"type\":\"bytes32\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"getDatasetLength\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"getTotalCptId\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"}],\"name\":\"isCptExist\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"\",\"type\":\"bool\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"},{\"internalType\":\"address\",\"name\":\"cptPublisher\",\"type\":\"address\"},{\"internalType\":\"int256[8]\",\"name\":\"cptIntArray\",\"type\":\"int256[8]\"},{\"internalType\":\"bytes32[8]\",\"name\":\"cptBytes32Array\",\"type\":\"bytes32[8]\"},{\"internalType\":\"bytes32[32]\",\"name\":\"cptJsonSchemaArray\",\"type\":\"bytes32[32]\"},{\"internalType\":\"uint8\",\"name\":\"cptV\",\"type\":\"uint8\"},{\"internalType\":\"bytes32\",\"name\":\"cptR\",\"type\":\"bytes32\"},{\"internalType\":\"bytes32\",\"name\":\"cptS\",\"type\":\"bytes32\"}],\"name\":\"putCpt\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"\",\"type\":\"bool\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"}],\"name\":\"queryCpt\",\"outputs\":[{\"internalType\":\"address\",\"name\":\"publisher\",\"type\":\"address\"},{\"internalType\":\"int256[]\",\"name\":\"intArray\",\"type\":\"int256[]\"},{\"internalType\":\"bytes32[]\",\"name\":\"bytes32Array\",\"type\":\"bytes32[]\"},{\"internalType\":\"bytes32[]\",\"name\":\"jsonSchemaArray\",\"type\":\"bytes32[]\"},{\"internalType\":\"uint8\",\"name\":\"v\",\"type\":\"uint8\"},{\"internalType\":\"bytes32\",\"name\":\"r\",\"type\":\"bytes32\"},{\"internalType\":\"bytes32\",\"name\":\"s\",\"type\":\"bytes32\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"publisher\",\"type\":\"address\"},{\"internalType\":\"int256[8]\",\"name\":\"intArray\",\"type\":\"int256[8]\"},{\"internalType\":\"bytes32[8]\",\"name\":\"bytes32Array\",\"type\":\"bytes32[8]\"},{\"internalType\":\"bytes32[32]\",\"name\":\"jsonSchemaArray\",\"type\":\"bytes32[32]\"},{\"internalType\":\"uint8\",\"name\":\"v\",\"type\":\"uint8\"},{\"internalType\":\"bytes32\",\"name\":\"r\",\"type\":\"bytes32\"},{\"internalType\":\"bytes32\",\"name\":\"s\",\"type\":\"bytes32\"}],\"name\":\"registerCpt\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"\",\"type\":\"bool\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"cptId\",\"type\":\"uint256\"},{\"internalType\":\"address\",\"name\":\"publisher\",\"type\":\"address\"},{\"internalType\":\"int256[8]\",\"name\":\"intArray\",\"type\":\"int256[8]\"},{\"internalType\":\"bytes32[8]\",\"name\":\"bytes32Array\",\"type\":\"bytes32[8]\"},{\"internalType\":\"bytes32[32]\",\"name\":\"jsonSchemaArray\",\"type\":\"bytes32[32]\"},{\"internalType\":\"uint8\",\"name\":\"v\",\"type\":\"uint8\"},{\"internalType\":\"bytes32\",\"name\":\"r\",\"type\":\"bytes32\"},{\"internalType\":\"bytes32\",\"name\":\"s\",\"type\":\"bytes32\"}],\"name\":\"updateCpt\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"\",\"type\":\"bool\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"}]",
	Bin: "0x60806040526103e85f55621e848060015534801561001b575f80fd5b5061247c806100295f395ff3fe608060405234801561000f575f80fd5b5060043610610129575f3560e01c806366d6a90b116100ab578063d4eb8a421161006f578063d4eb8a42146103bb578063d6edb44e146103eb578063e083a3ad1461041b578063e5741ff314610439578063e5a34e6e1461046b57610129565b806366d6a90b146102dd5780636da223b71461030d5780636fce6bb31461033d578063a07bd9b51461035b578063d2a3b53d1461038b57610129565b80633d29ba2b116100f25780633d29ba2b146101f957806347b42f88146102175780635ca35abf1461024757806362238a791461027d578063628e526f146102ad57610129565b806227baa41461012d5780631e040fc71461015d57806323b746f11461018d5780632984fcc8146101bd5780632c0abe1d146101db575b5f80fd5b610147600480360381019061014291906116db565b61049b565b60405161015491906117b4565b60405180910390f35b610177600480360381019061017291906117ce565b610635565b60405161018491906118c3565b60405180910390f35b6101a760048036038101906101a291906116db565b61076b565b6040516101b49190611991565b60405180910390f35b6101c5610905565b6040516101d291906119ba565b60405180910390f35b6101e3610913565b6040516101f091906119ba565b60405180910390f35b61020161091a565b60405161020e91906119ba565b60405180910390f35b610231600480360381019061022c9190611d51565b610963565b60405161023e9190611e0e565b60405180910390f35b610261600480360381019061025c91906116db565b6109a2565b6040516102749796959493929190611f76565b60405180910390f35b61029760048036038101906102929190611ff8565b6109ef565b6040516102a49190612036565b60405180910390f35b6102c760048036038101906102c291906116db565b610aa5565b6040516102d491906120d5565b60405180910390f35b6102f760048036038101906102f291906120ef565b610c3f565b6040516103049190611e0e565b60405180910390f35b610327600480360381019061032291906116db565b610c80565b60405161033491906121a5565b60405180910390f35b610345610e12565b60405161035291906119ba565b60405180910390f35b610375600480360381019061037091906116db565b610e18565b60405161038291906119ba565b60405180910390f35b6103a560048036038101906103a091906120ef565b610e3d565b6040516103b29190611e0e565b60405180910390f35b6103d560048036038101906103d091906116db565b610fb0565b6040516103e29190611e0e565b60405180910390f35b61040560048036038101906104009190611ff8565b610fef565b6040516104129190612036565b60405180910390f35b6104236110a5565b60405161043091906119ba565b60405180910390f35b610453600480360381019061044e91906116db565b6110b1565b604051610462939291906121be565b60405180910390f35b61048560048036038101906104809190611ff8565b611261565b60405161049291906121f3565b60405180910390f35b6104a361153c565b5f60025f8481526020019081526020015f206040518060a00160405290815f82015f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200160018201600880602002604051908101604052809291908260088015610550576020028201915b81548152602001906001019080831161053c575b5050505050815260200160098201600880602002604051908101604052809291908260088015610595576020028201915b815481526020019060010190808311610581575b50505050508152602001601182016020806020026040519081016040528092919082602080156105da576020028201915b8154815260200190600101908083116105c6575b50505050508152602001603182016040518060600160405290815f82015f9054906101000a900460ff1660ff1660ff168152602001600182015481526020016002820154815250508152505090508060400151915050919050565b60605f6106406110a5565b90505f8482101561069e57600167ffffffffffffffff81111561066657610665611a41565b5b6040519080825280602002602001820160405280156106945781602001602082028036833780820191505090505b5092505050610765565b83856106aa9190612240565b82116106c35784826106bc9190612273565b90506106c7565b8390505b5f8167ffffffffffffffff8111156106e2576106e1611a41565b5b6040519080825280602002602001820160405280156107105781602001602082028036833780820191505090505b5090505f5b8281101561075d57610731818861072c9190612240565b610e18565b828281518110610744576107436122a6565b5b6020026020010181815250508080600101915050610715565b508093505050505b92915050565b61077361155f565b5f60025f8481526020019081526020015f206040518060a00160405290815f82015f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200160018201600880602002604051908101604052809291908260088015610820576020028201915b81548152602001906001019080831161080c575b5050505050815260200160098201600880602002604051908101604052809291908260088015610865576020028201915b815481526020019060010190808311610851575b50505050508152602001601182016020806020026040519081016040528092919082602080156108aa576020028201915b815481526020019060010190808311610896575b50505050508152602001603182016040518060600160405290815f82015f9054906101000a900460ff1660ff1660ff168152602001600182015481526020016002820154815250508152505090508060200151915050919050565b5f61090e6110a5565b905090565b621e848081565b5f5b610927600154610fb0565b156109485760015f81548092919061093e906122d3565b919050555061091c565b60015f81548092919061095a906122d3565b91905055905090565b5f6109958888888888888860045f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff16611317565b9050979650505050505050565b5f60608060605f805f6109d68860045f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff166113a3565b9650965096509650965096509650919395979092949650565b60605f6109fb84610aa5565b90505f602067ffffffffffffffff811115610a1957610a18611a41565b5b604051908082528060200260200182016040528015610a475781602001602082028036833780820191505090505b5090505f5b6020811015610a9957828160208110610a6857610a676122a6565b5b6020020151828281518110610a8057610a7f6122a6565b5b6020026020010181815250508080600101915050610a4c565b50809250505092915050565b610aad611582565b5f60025f8481526020019081526020015f206040518060a00160405290815f82015f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200160018201600880602002604051908101604052809291908260088015610b5a576020028201915b815481526020019060010190808311610b46575b5050505050815260200160098201600880602002604051908101604052809291908260088015610b9f576020028201915b815481526020019060010190808311610b8b575b5050505050815260200160118201602080602002604051908101604052809291908260208015610be4576020028201915b815481526020019060010190808311610bd0575b50505050508152602001603182016040518060600160405290815f82015f9054906101000a900460ff1660ff1660ff168152602001600182015481526020016002820154815250508152505090508060600151915050919050565b5f610c72898989898989898960045f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff166113fc565b905098975050505050505050565b5f8060025f8481526020019081526020015f206040518060a00160405290815f82015f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200160018201600880602002604051908101604052809291908260088015610d2e576020028201915b815481526020019060010190808311610d1a575b5050505050815260200160098201600880602002604051908101604052809291908260088015610d73576020028201915b815481526020019060010190808311610d5f575b5050505050815260200160118201602080602002604051908101604052809291908260208015610db8576020028201915b815481526020019060010190808311610da4575b50505050508152602001603182016040518060600160405290815f82015f9054906101000a900460ff1660ff1660ff16815260200160018201548152602001600282015481525050815250509050805f0151915050919050565b6103e881565b5f60038281548110610e2d57610e2c6122a6565b5b905f5260205f2001549050919050565b5f8060405180606001604052808660ff1681526020018581526020018481525090506040518060a001604052808a73ffffffffffffffffffffffffffffffffffffffff1681526020018981526020018881526020018781526020018281525060025f8c81526020019081526020015f205f820151815f015f6101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550602082015181600101906008610f089291906115a5565b50604082015181600901906008610f209291906115e5565b50606082015181601101906020610f38929190611625565b506080820151816031015f820151815f015f6101000a81548160ff021916908360ff1602179055506020820151816001015560408201518160020155505090505060038a908060018154018082558091505060019003905f5260205f20015f9091909190915055600191505098975050505050505050565b5f80610fbb8361076b565b90505f815f60088110610fd157610fd06122a6565b5b602002015114610fe5576001915050610fea565b5f9150505b919050565b60605f610ffb8461049b565b90505f600867ffffffffffffffff81111561101957611018611a41565b5b6040519080825280602002602001820160405280156110475781602001602082028036833780820191505090505b5090505f5b600881101561109957828160088110611068576110676122a6565b5b60200201518282815181106110805761107f6122a6565b5b602002602001018181525050808060010191505061104c565b50809250505092915050565b5f600380549050905090565b5f805f8060025f8681526020019081526020015f206040518060a00160405290815f82015f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200160018201600880602002604051908101604052809291908260088015611161576020028201915b81548152602001906001019080831161114d575b50505050508152602001600982016008806020026040519081016040528092919082600880156111a6576020028201915b815481526020019060010190808311611192575b50505050508152602001601182016020806020026040519081016040528092919082602080156111eb576020028201915b8154815260200190600101908083116111d7575b50505050508152602001603182016040518060600160405290815f82015f9054906101000a900460ff1660ff1660ff1681526020016001820154815260200160028201548152505081525050905080608001515f0151935080608001516020015192508060800151604001519150509193909250565b60605f61126d8461076b565b90505f600867ffffffffffffffff81111561128b5761128a611a41565b5b6040519080825280602002602001820160405280156112b95781602001602082028036833780820191505090505b5090505f5b600881101561130b578281600881106112da576112d96122a6565b5b60200201518282815181106112f2576112f16122a6565b5b60200260200101818152505080806001019150506112be565b50809250505092915050565b5f8061132161091a565b90505f60019050808a5f6008811061133c5761133b6122a6565b5b602002018181525050611355828c8c8c8c8c8c8c610e3d565b507fa17f6f29c43d53fdf8a8d5fc788d118621cdca690e8ee29962c3e2fbe70d5eb35f83836040516113899392919061236b565b60405180910390a160019250505098975050505050505050565b5f60608060605f805f6113b589610c80565b96506113c18989611261565b95506113cd8989610fef565b94506113d989896109ef565b93506113e4896110b1565b80935081945082955050505092959891949750929550565b5f6114068a610fb0565b156114ed575f6114158b61076b565b90505f6001825f6008811061142d5761142c6122a6565b5b602002015161143c91906123a0565b9050808a5f60088110611452576114516122a6565b5b6020020181815250505f826001600881106114705761146f6122a6565b5b60200201519050808b60016008811061148c5761148b6122a6565b5b6020020181815250506114a58d8d8d8d8d8d8d8d610e3d565b507f2614d1ec3482cc2505bf211c39bee96c28940521311ec70c9ebf14d3896fd1965f8e846040516114d99392919061236b565b60405180910390a16001935050505061152f565b7f2614d1ec3482cc2505bf211c39bee96c28940521311ec70c9ebf14d3896fd1966207a24d5f8060405161152393929190612411565b60405180910390a15f90505b9998505050505050505050565b604051806101000160405280600890602082028036833780820191505090505090565b604051806101000160405280600890602082028036833780820191505090505090565b604051806104000160405280602090602082028036833780820191505090505090565b82600881019282156115d4579160200282015b828111156115d35782518255916020019190600101906115b8565b5b5090506115e19190611665565b5090565b8260088101928215611614579160200282015b828111156116135782518255916020019190600101906115f8565b5b5090506116219190611680565b5090565b8260208101928215611654579160200282015b82811115611653578251825591602001919060010190611638565b5b5090506116619190611680565b5090565b5b8082111561167c575f815f905550600101611666565b5090565b5b80821115611697575f815f905550600101611681565b5090565b5f604051905090565b5f80fd5b5f819050919050565b6116ba816116a8565b81146116c4575f80fd5b50565b5f813590506116d5816116b1565b92915050565b5f602082840312156116f0576116ef6116a4565b5b5f6116fd848285016116c7565b91505092915050565b5f60089050919050565b5f81905092915050565b5f819050919050565b5f819050919050565b61173581611723565b82525050565b5f611746838361172c565b60208301905092915050565b5f602082019050919050565b61176781611706565b6117718184611710565b925061177c8261171a565b805f5b838110156117ac578151611793878261173b565b965061179e83611752565b92505060018101905061177f565b505050505050565b5f610100820190506117c85f83018461175e565b92915050565b5f80604083850312156117e4576117e36116a4565b5b5f6117f1858286016116c7565b9250506020611802858286016116c7565b9150509250929050565b5f81519050919050565b5f82825260208201905092915050565b5f819050602082019050919050565b61183e816116a8565b82525050565b5f61184f8383611835565b60208301905092915050565b5f602082019050919050565b5f6118718261180c565b61187b8185611816565b935061188683611826565b805f5b838110156118b657815161189d8882611844565b97506118a88361185b565b925050600181019050611889565b5085935050505092915050565b5f6020820190508181035f8301526118db8184611867565b905092915050565b5f60089050919050565b5f81905092915050565b5f819050919050565b5f819050919050565b61191281611900565b82525050565b5f6119238383611909565b60208301905092915050565b5f602082019050919050565b611944816118e3565b61194e81846118ed565b9250611959826118f7565b805f5b838110156119895781516119708782611918565b965061197b8361192f565b92505060018101905061195c565b505050505050565b5f610100820190506119a55f83018461193b565b92915050565b6119b4816116a8565b82525050565b5f6020820190506119cd5f8301846119ab565b92915050565b5f73ffffffffffffffffffffffffffffffffffffffff82169050919050565b5f6119fc826119d3565b9050919050565b611a0c816119f2565b8114611a16575f80fd5b50565b5f81359050611a2781611a03565b92915050565b5f80fd5b5f601f19601f8301169050919050565b7f4e487b71000000000000000000000000000000000000000000000000000000005f52604160045260245ffd5b611a7782611a31565b810181811067ffffffffffffffff82111715611a9657611a95611a41565b5b80604052505050565b5f611aa861169b565b9050611ab48282611a6e565b919050565b5f67ffffffffffffffff821115611ad357611ad2611a41565b5b602082029050919050565b5f80fd5b611aeb81611900565b8114611af5575f80fd5b50565b5f81359050611b0681611ae2565b92915050565b5f611b1e611b1984611ab9565b611a9f565b90508060208402830185811115611b3857611b37611ade565b5b835b81811015611b615780611b4d8882611af8565b845260208401935050602081019050611b3a565b5050509392505050565b5f82601f830112611b7f57611b7e611a2d565b5b6008611b8c848285611b0c565b91505092915050565b5f67ffffffffffffffff821115611baf57611bae611a41565b5b602082029050919050565b611bc381611723565b8114611bcd575f80fd5b50565b5f81359050611bde81611bba565b92915050565b5f611bf6611bf184611b95565b611a9f565b90508060208402830185811115611c1057611c0f611ade565b5b835b81811015611c395780611c258882611bd0565b845260208401935050602081019050611c12565b5050509392505050565b5f82601f830112611c5757611c56611a2d565b5b6008611c64848285611be4565b91505092915050565b5f67ffffffffffffffff821115611c8757611c86611a41565b5b602082029050919050565b5f611ca4611c9f84611c6d565b611a9f565b90508060208402830185811115611cbe57611cbd611ade565b5b835b81811015611ce75780611cd38882611bd0565b845260208401935050602081019050611cc0565b5050509392505050565b5f82601f830112611d0557611d04611a2d565b5b6020611d12848285611c92565b91505092915050565b5f60ff82169050919050565b611d3081611d1b565b8114611d3a575f80fd5b50565b5f81359050611d4b81611d27565b92915050565b5f805f805f805f610680888a031215611d6d57611d6c6116a4565b5b5f611d7a8a828b01611a19565b9750506020611d8b8a828b01611b6b565b965050610120611d9d8a828b01611c43565b955050610220611daf8a828b01611cf1565b945050610620611dc18a828b01611d3d565b935050610640611dd38a828b01611bd0565b925050610660611de58a828b01611bd0565b91505092959891949750929550565b5f8115159050919050565b611e0881611df4565b82525050565b5f602082019050611e215f830184611dff565b92915050565b611e30816119f2565b82525050565b5f81519050919050565b5f82825260208201905092915050565b5f819050602082019050919050565b5f602082019050919050565b5f611e7582611e36565b611e7f8185611e40565b9350611e8a83611e50565b805f5b83811015611eba578151611ea18882611918565b9750611eac83611e5f565b925050600181019050611e8d565b5085935050505092915050565b5f81519050919050565b5f82825260208201905092915050565b5f819050602082019050919050565b5f602082019050919050565b5f611f0682611ec7565b611f108185611ed1565b9350611f1b83611ee1565b805f5b83811015611f4b578151611f32888261173b565b9750611f3d83611ef0565b925050600181019050611f1e565b5085935050505092915050565b611f6181611d1b565b82525050565b611f7081611723565b82525050565b5f60e082019050611f895f83018a611e27565b8181036020830152611f9b8189611e6b565b90508181036040830152611faf8188611efc565b90508181036060830152611fc38187611efc565b9050611fd26080830186611f58565b611fdf60a0830185611f67565b611fec60c0830184611f67565b98975050505050505050565b5f806040838503121561200e5761200d6116a4565b5b5f61201b858286016116c7565b925050602061202c85828601611a19565b9150509250929050565b5f6020820190508181035f83015261204e8184611efc565b905092915050565b5f60209050919050565b5f81905092915050565b5f819050919050565b5f602082019050919050565b61208881612056565b6120928184612060565b925061209d8261206a565b805f5b838110156120cd5781516120b4878261173b565b96506120bf83612073565b9250506001810190506120a0565b505050505050565b5f610400820190506120e95f83018461207f565b92915050565b5f805f805f805f806106a0898b03121561210c5761210b6116a4565b5b5f6121198b828c016116c7565b985050602061212a8b828c01611a19565b975050604061213b8b828c01611b6b565b96505061014061214d8b828c01611c43565b95505061024061215f8b828c01611cf1565b9450506106406121718b828c01611d3d565b9350506106606121838b828c01611bd0565b9250506106806121958b828c01611bd0565b9150509295985092959890939650565b5f6020820190506121b85f830184611e27565b92915050565b5f6060820190506121d15f830186611f58565b6121de6020830185611f67565b6121eb6040830184611f67565b949350505050565b5f6020820190508181035f83015261220b8184611e6b565b905092915050565b7f4e487b71000000000000000000000000000000000000000000000000000000005f52601160045260245ffd5b5f61224a826116a8565b9150612255836116a8565b925082820190508082111561226d5761226c612213565b5b92915050565b5f61227d826116a8565b9150612288836116a8565b92508282039050818111156122a05761229f612213565b5b92915050565b7f4e487b71000000000000000000000000000000000000000000000000000000005f52603260045260245ffd5b5f6122dd826116a8565b91507fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff820361230f5761230e612213565b5b600182019050919050565b5f819050919050565b5f819050919050565b5f61234661234161233c8461231a565b612323565b6116a8565b9050919050565b6123568161232c565b82525050565b61236581611900565b82525050565b5f60608201905061237e5f83018661234d565b61238b60208301856119ab565b612398604083018461235c565b949350505050565b5f6123aa82611900565b91506123b583611900565b92508282019050828112155f8312168382125f8412151617156123db576123da612213565b5b92915050565b5f6123fb6123f66123f18461231a565b612323565b611900565b9050919050565b61240b816123e1565b82525050565b5f6060820190506124245f8301866119ab565b612431602083018561234d565b61243e6040830184612402565b94935050505056fea264697066735822122013097a7d2d1ab965bce61a7419728e01b28a51048acbe834189fa10d912396c064736f6c63430008180033",
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

// GetCptBytes32Array is a free data retrieval call binding the contract method 0x0027baa4.
//
// Solidity: function getCptBytes32Array(uint256 cptId) view returns(bytes32[8] bytes32Array)
func (_Cpt *CptCaller) GetCptBytes32Array(opts *bind.CallOpts, cptId *big.Int) ([8][32]byte, error) {
	var out []interface{}
	err := _Cpt.contract.Call(opts, &out, "getCptBytes32Array", cptId)

	if err != nil {
		return *new([8][32]byte), err
	}

	out0 := *abi.ConvertType(out[0], new([8][32]byte)).(*[8][32]byte)

	return out0, err

}

// GetCptBytes32Array is a free data retrieval call binding the contract method 0x0027baa4.
//
// Solidity: function getCptBytes32Array(uint256 cptId) view returns(bytes32[8] bytes32Array)
func (_Cpt *CptSession) GetCptBytes32Array(cptId *big.Int) ([8][32]byte, error) {
	return _Cpt.Contract.GetCptBytes32Array(&_Cpt.CallOpts, cptId)
}

// GetCptBytes32Array is a free data retrieval call binding the contract method 0x0027baa4.
//
// Solidity: function getCptBytes32Array(uint256 cptId) view returns(bytes32[8] bytes32Array)
func (_Cpt *CptCallerSession) GetCptBytes32Array(cptId *big.Int) ([8][32]byte, error) {
	return _Cpt.Contract.GetCptBytes32Array(&_Cpt.CallOpts, cptId)
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

// GetCptJsonSchemaArray is a free data retrieval call binding the contract method 0x628e526f.
//
// Solidity: function getCptJsonSchemaArray(uint256 cptId) view returns(bytes32[32] jsonSchemaArray)
func (_Cpt *CptCaller) GetCptJsonSchemaArray(opts *bind.CallOpts, cptId *big.Int) ([32][32]byte, error) {
	var out []interface{}
	err := _Cpt.contract.Call(opts, &out, "getCptJsonSchemaArray", cptId)

	if err != nil {
		return *new([32][32]byte), err
	}

	out0 := *abi.ConvertType(out[0], new([32][32]byte)).(*[32][32]byte)

	return out0, err

}

// GetCptJsonSchemaArray is a free data retrieval call binding the contract method 0x628e526f.
//
// Solidity: function getCptJsonSchemaArray(uint256 cptId) view returns(bytes32[32] jsonSchemaArray)
func (_Cpt *CptSession) GetCptJsonSchemaArray(cptId *big.Int) ([32][32]byte, error) {
	return _Cpt.Contract.GetCptJsonSchemaArray(&_Cpt.CallOpts, cptId)
}

// GetCptJsonSchemaArray is a free data retrieval call binding the contract method 0x628e526f.
//
// Solidity: function getCptJsonSchemaArray(uint256 cptId) view returns(bytes32[32] jsonSchemaArray)
func (_Cpt *CptCallerSession) GetCptJsonSchemaArray(cptId *big.Int) ([32][32]byte, error) {
	return _Cpt.Contract.GetCptJsonSchemaArray(&_Cpt.CallOpts, cptId)
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

// GetCptId is a paid mutator transaction binding the contract method 0x3d29ba2b.
//
// Solidity: function getCptId() returns(uint256 cptId)
func (_Cpt *CptTransactor) GetCptId(opts *bind.TransactOpts) (*types.Transaction, error) {
	return _Cpt.contract.Transact(opts, "getCptId")
}

// GetCptId is a paid mutator transaction binding the contract method 0x3d29ba2b.
//
// Solidity: function getCptId() returns(uint256 cptId)
func (_Cpt *CptSession) GetCptId() (*types.Transaction, error) {
	return _Cpt.Contract.GetCptId(&_Cpt.TransactOpts)
}

// GetCptId is a paid mutator transaction binding the contract method 0x3d29ba2b.
//
// Solidity: function getCptId() returns(uint256 cptId)
func (_Cpt *CptTransactorSession) GetCptId() (*types.Transaction, error) {
	return _Cpt.Contract.GetCptId(&_Cpt.TransactOpts)
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
