// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract Tasks {
    struct Task {
        string tid;
        // uint256 blockTimeout;
        uint256 ioSizeLimit;
        string exampleInput; //ipfs
        string exampleOutput; //ipfs
        uint256 price;
        address ownerWallet;
        // bool active;
        type;
    }

    mapping(string => uint256) public tidToIndex;
    Task[] public tasks;

    constructor() {
        delete tasks;
        Task memory dummy;
        tasks.push(dummy);
    }

    function initialize() public {
        delete tasks;
        Task memory dummy;
        tasks.push(dummy);
    }

    function getActiveTasks() public view returns (Task[] memory) {
        Task[] memory activeTasks;
        uint activeTasksLength = 0;
        for (uint i = 0; i < tasks.length; i++) {
            if (tasks[i].active) {
                activeTasks[activeTasksLength] = tasks[i];
                activeTasksLength++;
            }
        }
        return activeTasks;
    }

    // sent by task owner
    function listTask(
        string memory tid,
        uint256 blockTimeout,
        uint256 ioSizeLimit,
        string memory exampleInput,
        string memory exampleOutput,
        uint256 price
    ) public {
        Task memory task;
        task.tid = tid;
        task.blockTimeout = blockTimeout;
        task.ioSizeLimit = ioSizeLimit;
        task.exampleInput = exampleInput;
        task.exampleOutput = exampleOutput;
        task.price = price;
        task.active = true;
        task.ownerWallet = msg.sender;
        tasks.push(task);
        tidToIndex[tid] = tasks.length - 1;
    }

    function unlistTask(string memory tid) public {
        require(tidToIndex[tid] != 0, "Task does not exist");
        tasks[tidToIndex[tid]].active = false;
    }
}