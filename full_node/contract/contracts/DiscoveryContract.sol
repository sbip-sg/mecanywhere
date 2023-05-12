// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

pragma experimental ABIEncoderV2;

contract DiscoveryContract {
    uint256 public EXPIRY_DURATION;

    struct User {
        string did;
        uint256 timestamp;
        uint256 latency;
        string queue;
    }

    mapping(string => uint256) private didToIndex;
    User[] private users;
    uint256 private userCount = 0;

    constructor(uint256 expiryDuration) {
        EXPIRY_DURATION = expiryDuration;
    }

    function setUser(string memory did, uint256 timestamp, uint256 latency) public {
        if (didToIndex[did] != 0) {
            users[didToIndex[did]].timestamp = timestamp;
            users[didToIndex[did]].latency = latency;
            return;
        }
        didToIndex[did] = userCount;
        users.push(User(did, timestamp, latency, did));
        userCount = users.length + 1;
    }

    function lazyRemoveExpiredUsers(uint256 currentTimestamp) public {
        uint256 i = 0;
        while (i < userCount) {
            i++;
            if (currentTimestamp - users[i].timestamp > EXPIRY_DURATION) {
                removeUser(users[i].did);
            } else {
                break;
            }
        }
    }

    function getFirstUserQueue() public view returns (string memory) {
        if (userCount == 0) {
            return "";
        }
        return users[0].queue;
    }

    function getAllDidToTimestamps()
        public
        view
        returns (string[] memory, uint256[] memory)
    {
        uint256[] memory timestamps = new uint256[](userCount);
        string[] memory dids = new string[](userCount);
        for (uint i = 0; i < userCount; i++) {
            timestamps[i] = users[i].timestamp;
            dids[i] = users[i].did;
        }
        return (dids, timestamps);
    }

    function removeUser(string memory did) public {
        require(didToIndex[did] != 0, "Id does not exist");
        uint256 indexToRemove = didToIndex[did];
        uint256 lastIndex = userCount - 1;
        User memory lastUser = users[lastIndex];
        users[indexToRemove] = lastUser;
        didToIndex[lastUser.did] = indexToRemove;
        userCount = userCount - 1;
        delete users[lastIndex];
        delete didToIndex[did];
    }

    function removeUsers(string[] memory dids) public {
        for (uint256 i = 0; i < dids.length; i++) {
            removeUser(dids[i]);
        }
    }
}
