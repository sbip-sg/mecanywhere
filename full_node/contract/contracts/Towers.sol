// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract Towers {
    struct Tower {
        // personal
        string did;
        string ip;
        uint256 stake; // todo

        // settings
        uint256 bandwidth;
        uint256 fee;

        // variables
        string[] hosts;
        string[] taskQueue;
        uint256 throughput;
    }

    mapping(string => uint) private towDidToIndex;
    Tower[] private towers;

    constructor() {
        delete towers;
        Tower memory dummy;
        towers.push(dummy);
    }

    function initialize() public {
        delete towers;
        Tower memory dummy;
        towers.push(dummy);
    }

    function getAllTowers() public view returns (Tower[] memory) {
        return towers;
    }

    function registerTower(string memory did, string memory ip, uint256 bandwidth, uint256 fee) public {
        require(towDidToIndex[did] == 0, "Tower already exists");
        Tower memory tower;
        tower.did = did;
        tower.ip = ip;
        tower.bandwidth = bandwidth;
        tower.fee = fee;
        towers.push(tower);
        towDidToIndex[did] = towers.length - 1;
    }

    function deregisterTower(string memory did) public {
        require(towDidToIndex[did] != 0, "Tower does not exist");
        towDidToIndex[towers[towers.length - 1].did] = towDidToIndex[did];
        towers[towDidToIndex[did]] = towers[towers.length - 1];
        towers.pop();
        delete towDidToIndex[did];
    }

    function addHost(string memory did, string memory host) public {
        require(towDidToIndex[did] != 0, "Tower does not exist");
        // TODO: check host on host contract
        towers[towDidToIndex[did]].hosts.push(host);
    }

    function removeHost(string memory did, string memory host) public {
        require(towDidToIndex[did] != 0, "Tower does not exist");
        uint index = towDidToIndex[did];
        uint hostsLength = towers[index].hosts.length;
        for (uint i = 0; i < hostsLength; i++) {
            if (keccak256(abi.encodePacked(towers[index].hosts[i])) == keccak256(abi.encodePacked(host))) {
                towers[index].hosts[i] = towers[index].hosts[hostsLength - 1];
                towers[index].hosts.pop();
                break;
            }
        }
    }

    function queueTask(string memory did, string memory task, uint256 ioSizeLimit) public {
        require(towDidToIndex[did] != 0, "Tower does not exist");
        uint256 combinedThroughput = towers[towDidToIndex[did]].throughput + ioSizeLimit;
        require(combinedThroughput <= towers[towDidToIndex[did]].bandwidth, "Bandwidth exceeded");
        towers[towDidToIndex[did]].taskQueue.push(task);
        towers[towDidToIndex[did]].throughput = combinedThroughput;
    }

    function dequeueTask(string memory did, string memory task) public {
        require(towDidToIndex[did] != 0, "Tower does not exist");
        uint index = towDidToIndex[did];
        uint tasksLength = towers[index].taskQueue.length;
        for (uint i = 0; i < tasksLength; i++) {
            if (keccak256(abi.encodePacked(towers[index].taskQueue[i])) == keccak256(abi.encodePacked(task))) {
                towers[index].taskQueue[i] = towers[index].taskQueue[tasksLength - 1];
                towers[index].taskQueue.pop();
                break;
            }
        }
        towers[index].throughput -= 1; // todo: get ioSizeLimit from task contract
    }
}
