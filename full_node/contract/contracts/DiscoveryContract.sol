// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

pragma experimental ABIEncoderV2;

contract DiscoveryContract {
    uint256 public EXPIRY_DURATION;

    struct User {
        string did;
        string poDid;
        uint256 index;
        bool isUser;
        uint256 timestamp;
        uint256 latency;
        string queue;
    }

    mapping(string => User) private didToUser;
    User[] private users;
    uint256 private userCount = 0;

    constructor(uint256 expiryDuration) {
        EXPIRY_DURATION = expiryDuration;
    }

    function setUser(string memory did, string memory poDid, uint256 timestamp, uint256 latency) public {
        if (didToUser[did].isUser) {
            uint256 index = didToUser[did].index;
            users[index].poDid = poDid;
            users[index].timestamp = timestamp;
            users[index].latency = latency;
            return;
        }
        User memory newUser = User(did, poDid, userCount, true, timestamp, latency, did);
        users.push(newUser);
        didToUser[did] = newUser;
        userCount = userCount + 1;
    }

    function lazyRemoveExpiredUsers(uint256 currentTimestamp) public {
        while (userCount > 0 && currentTimestamp - users[0].timestamp > EXPIRY_DURATION) {
            removeUser(users[0].did);
        }
    }

    function getUser(string memory did) public view returns (User memory) {
        if (didToUser[did].isUser) {
          return didToUser[did];
        }
        return User("", "", 0, false, 0, 0, "");
    }

    function getFirstUser() public view returns (User memory) {
        if (userCount == 0) {
            return User("", "", 0, false, 0, 0, "");
        }
        return users[0];
    }

    function getUserCount() public view returns (uint256) {
        return userCount;
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
        require(didToUser[did].isUser, "Id does not exist");
        uint256 indexToRemove = didToUser[did].index;
        User memory lastUser = users[userCount - 1];
        lastUser.index = indexToRemove;
        didToUser[lastUser.did] = lastUser;
        users[indexToRemove] = lastUser;
        userCount = userCount - 1;
        users.pop();
        delete didToUser[did];
    }

    function removeUsers(string[] memory dids) public {
        for (uint256 i = 0; i < dids.length; i++) {
            removeUser(dids[i]);
        }
    }
}
