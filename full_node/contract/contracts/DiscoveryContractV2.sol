// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract DiscoveryContractV2 {
    struct Host {
        // personal
        string did;
        uint256 stake; // todo

        // settings
        uint256 blockQueueTimeout; // remove

        // variables
        uint256[] taskComputationPrice;
        string[] activeTasks;
        string[] taskQueue;
    }

    mapping(string => uint) private hidToIndex;
    Host[] private hosts;

    constructor() {
        delete hosts;
        Host memory dummy;
        hosts.push(dummy);
    }

    function initialize() public {
        delete hosts;
        Host memory dummy;
        hosts.push(dummy);
    }

    function getAllHosts() public view returns (Host[] memory) {
        return hosts;
    }

    function registerHost(string memory did, uint256 blockQueueTimeout) public {
        require(hidToIndex[did] == 0, "Host already exists");
        Host memory host;
        host.did = did;
        host.blockQueueTimeout = blockQueueTimeout;
        hosts.push(host);
        hidToIndex[did] = hosts.length - 1;
    }

    function deregisterHost(string memory did) public {
        require(hidToIndex[did] != 0, "Host does not exist");
        hidToIndex[hosts[hosts.length - 1].did] = hidToIndex[did];
        hosts[hidToIndex[did]] = hosts[hosts.length - 1];
        hosts.pop();
        delete hidToIndex[did];
    }

    function activateTask(string memory did, string memory task, uint256 price) public {
        require(hidToIndex[did] != 0, "Host does not exist");
        // TODO: check task in task contract
        hosts[hidToIndex[did]].activeTasks.push(task);
        hosts[hidToIndex[did]].taskComputationPrice.push(price);
    }

    function deactivateTask(string memory did, string memory task) public {
        require(hidToIndex[did] != 0, "Host does not exist");
        uint index = hidToIndex[did];
        uint tasksLength = hosts[index].activeTasks.length;
        for (uint i = 0; i < tasksLength; i++) {
            if (keccak256(abi.encodePacked(hosts[index].activeTasks[i])) == keccak256(abi.encodePacked(task))) {
                hosts[index].activeTasks[i] = hosts[index].activeTasks[tasksLength - 1];
                hosts[index].activeTasks.pop();
                hosts[index].taskComputationPrice[i] = hosts[index].taskComputationPrice[tasksLength - 1];
                hosts[index].taskComputationPrice.pop();
                break;
            }
        }
    }

    function queueTask(string memory did, string memory task) public {
        require(hidToIndex[did] != 0, "Host does not exist");
        // TODO: check task in active tasks
        hosts[hidToIndex[did]].taskQueue.push(task);
    }

    function dequeueTask(string memory did, string memory task) public {
        require(hidToIndex[did] != 0, "Host does not exist");
        uint index = hidToIndex[did];
        uint tasksLength = hosts[index].taskQueue.length;
        for (uint i = 0; i < tasksLength; i++) {
            if (keccak256(abi.encodePacked(hosts[index].taskQueue[i])) == keccak256(abi.encodePacked(task))) {
                hosts[index].taskQueue[i] = hosts[index].taskQueue[tasksLength - 1];
                hosts[index].taskQueue.pop();
                break;
            }
        }
    }
}
