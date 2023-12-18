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

        uint256 cpu;
        uint256 mem;

        string queue;
    }

    mapping(string => User) private didToUser;
    User[] private users;
    uint256 private userCount = 0;

    constructor(uint256 expiryDuration) {
        EXPIRY_DURATION = expiryDuration;
    }

    function setUser(string memory did, string memory poDid, uint256 timestamp, uint256 cpu, uint256 mem) public {
        if (didToUser[did].isUser) {
            User memory user = didToUser[did];
            user.poDid = poDid;
            user.timestamp = timestamp;
            user.cpu = cpu;
            user.mem = mem;
            users[user.index] = user;
            didToUser[did] = user;
            return;
        }
        User memory newUser = User(did, poDid, userCount, true, timestamp, cpu, mem, did);
        users.push(newUser);
        didToUser[did] = newUser;
        userCount = userCount + 1;
    }

    function updateTimestamp(string memory did, uint256 timestamp) public {
        require(didToUser[did].isUser, "Id does not exist");
        User memory user = didToUser[did];
        user.timestamp = timestamp;
        users[user.index] = user;
        didToUser[did] = user;
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
        return User("", "", 0, false, 0, 0, 0, "");
    }

    function getAvailableUser(uint256 cpu, uint256 mem) public view returns (User memory) {
        for (uint256 i = 0; i < userCount; i++) {
            if (users[i].cpu >= cpu && users[i].mem >= mem) {
                return users[i];
            }
        }
        return User("", "", 0, false, 0, 0, 0, "");
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

    function addResource(string memory did, uint256 cpu, uint256 mem) public {
        require(didToUser[did].isUser, "Id does not exist");
        User memory user = didToUser[did];
        user.cpu = user.cpu + cpu;
        user.mem = user.mem + mem;
        users[user.index] = user;
        didToUser[did] = user;
    }

    function subtractResource(string memory did, uint256 cpu, uint256 mem) public {
        require(didToUser[did].isUser, "Id does not exist");
        User memory user = didToUser[did];
        user.cpu = user.cpu - cpu;
        user.mem = user.mem - mem;
        users[user.index] = user;
        didToUser[did] = user;
    }
}
