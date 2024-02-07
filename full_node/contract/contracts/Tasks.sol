// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract Tasks {
    struct Task {
        string tid;
        uint256 blockTimeout;
        uint256 ioSizeLimit;
        string exampleInput;
        string exampleOutput;
        uint256 price;
        string ownerAddr;
    }

    mapping(string => uint256) private tidToIndex;
    Task[] private tasks;

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

    function getAllTasks() public view returns (Task[] memory) {
        return tasks;
    }

    function listTask(
        string memory tid,
        uint256 blockTimeout,
        uint256 ioSizeLimit,
        string memory exampleInput,
        string memory exampleOutput,
        uint256 price,
        string memory ownerAddr
    ) public {
        require(tidToIndex[tid] == 0, "Task already exists");
        Task memory task;
        task.tid = tid;
        task.blockTimeout = blockTimeout;
        task.ioSizeLimit = ioSizeLimit;
        task.exampleInput = exampleInput;
        task.exampleOutput = exampleOutput;
        task.price = price;
        task.ownerAddr = ownerAddr;
        tasks.push(task);
        tidToIndex[tid] = tasks.length - 1;
    }

    function unlistTask(string memory tid) public {
        require(tidToIndex[tid] != 0, "Task does not exist");
        tidToIndex[tasks[tasks.length - 1].tid] = tidToIndex[tid];
        tasks[tidToIndex[tid]] = tasks[tasks.length - 1];
        tasks.pop();
        delete tidToIndex[tid];
    }
}