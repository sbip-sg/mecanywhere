pragma solidity >=0.4.22 <0.9.0;

contract DIDContract {
    mapping(address => uint) changed;

    uint firstBlockNum;

    uint lastBlockNum;

    uint didCount = 0;

    mapping(uint => uint) blockAfterLink;

    modifier onlyOwner(address identity, address actor) {
        require(actor == identity);
        _;
    }

    bytes32 private constant DID_KEY_CREATED = "created";
    bytes32 private constant DID_KEY_AUTHENTICATION = "pubKey";

    constructor() public {
        firstBlockNum = block.number;
        lastBlockNum = firstBlockNum;
    }

    event DIDAttributeChanged(
        address indexed identity,
        bytes32 key,
        bytes value,
        uint previousBlock,
        int updated
    );

    event DIDHistoryEvent(
        address indexed identity,
        uint previousBlock,
        int created
    );

    function getLatestRelatedBlock(
        address identity
    ) public view returns (uint) {
        return changed[identity];
    }

    function getFirstBlockNum() public view returns (uint) {
        return firstBlockNum;
    }

    function getLatestBlockNum() public view returns (uint) {
        return lastBlockNum;
    }

    function getNextBlockNumByBlockNum(
        uint currentBlockNum
    ) public view returns (uint) {
        return blockAfterLink[currentBlockNum];
    }

    function getDIDCount() public view returns (uint) {
        return didCount;
    }

    function createDID(
        address identity,
        bytes memory auth,
        bytes memory created,
        int updated
    ) public //        onlyOwner(identity, msg.sender)
    {
        emit DIDAttributeChanged(
            identity,
            DID_KEY_CREATED,
            created,
            changed[identity],
            updated
        );
        emit DIDAttributeChanged(
            identity,
            DID_KEY_AUTHENTICATION,
            auth,
            changed[identity],
            updated
        );
        changed[identity] = block.number;
        if (block.number > lastBlockNum) {
            blockAfterLink[lastBlockNum] = block.number;
        }
        emit DIDHistoryEvent(identity, lastBlockNum, updated);
        if (block.number > lastBlockNum) {
            lastBlockNum = block.number;
        }
        didCount++;
    }

    function setAttribute(
        address identity,
        bytes32 key,
        bytes memory value,
        int updated
    ) public //        onlyOwner(identity, msg.sender)
    {
        emit DIDAttributeChanged(
            identity,
            key,
            value,
            changed[identity],
            updated
        );
        changed[identity] = block.number;
    }

    function identityExists(address identity) public view returns (bool) {
        if (address(0x0) != identity && 0 != changed[identity]) {
            return true;
        }
        return false;
    }
}
