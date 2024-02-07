// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract D3 {
    uint public constant MIN_STAKE = 1 ether;

    struct Task {
        string tid;
        uint256 blockTimeout;
        uint256 ioSizeLimit;
        string exampleInput;
        string exampleOutput;
        uint256 price;
        address ownerWallet;
        bool active;
    }

    struct Tower {
        // personal
        address addr;
        string ip;
        uint256 stake;

        // settings
        uint256 bandwidth;
        uint256 fee;
        bool active;

        // variables
        uint256 throughput;
    }

    struct Host {
        // personal
        address addr;
        uint256 stake;

        // settings
        uint256 blockQueueTimeout; // unused
        bool active;
    }

    mapping(string => uint256) private tidToIndex;
    Task[] private tasks;

    mapping(address => uint) private towerToIndex;
    Tower[] private towers;
    mapping(address => address[]) private towerToHosts;
    mapping(address => string[]) private towerToTaskQueue;

    mapping(address => uint) private hostToIndex;
    Host[] private hosts;
    mapping(address => uint256[]) private hostToTaskComputationPrice;
    mapping(address => string[]) private hostToActiveTasks;
    mapping(address => string[]) private hostToTaskQueue;

    event RequestPostedByClient(address tower, address host, string task);
    // event InputSentToTower(address tower, address host, string task);
    event InputReceivedOnTower(address tower, address host, string task);
    // event InputSentToHost(address tower, address host, string task);
    event InputReceivedOnHost(address tower, address host, string task);
    // event OutputSentToTower(address tower, address host, string task);
    event OutputReceivedOnTower(address tower, address host, string task);
    // event OutputSentToClient(address tower, address host, string task);
    event OutputReceivedOnClient(address tower, address host, string task);

    constructor() {
        delete tasks;
        Task memory dummy;
        tasks.push(dummy);
        delete towers;
        Tower memory dummy2;
        towers.push(dummy2);
        delete hosts;
        Host memory dummy3;
        hosts.push(dummy3);
    }

    function initialize() public {
        delete tasks;
        Task memory dummy;
        tasks.push(dummy);
        delete towers;
        Tower memory dummy2;
        towers.push(dummy2);
        delete hosts;
        Host memory dummy3;
        hosts.push(dummy3);
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

    function getActiveTowers() public view returns (Tower[] memory) {
        Tower[] memory activeTowers;
        uint activeTowersLength = 0;
        for (uint i = 0; i < towers.length; i++) {
            if (towers[i].active) {
                activeTowers[activeTowersLength] = towers[i];
                activeTowersLength++;
            }
        }
        return activeTowers;
    }

    // sent by tower
    function addTower(string memory ip, uint256 bandwidth, uint256 fee) public payable {
        require(msg.value >= MIN_STAKE, "Insufficient funds");
        Tower memory tower;
        tower.addr = msg.sender;
        tower.ip = ip;
        tower.bandwidth = bandwidth;
        tower.fee = fee;
        tower.stake = msg.value;
        tower.active = true;
        towers.push(tower);
        towerToIndex[msg.sender] = towers.length - 1;
    }

    // sent by tower
    function removeTower() public {
        address addr = msg.sender;
        require(towerToIndex[addr] != 0, "Tower does not exist");
        towers[towerToIndex[addr]].active = false;
        delete towerToHosts[addr];
        delete towerToTaskQueue[addr];
    }

    // sent by host
    function addHost(address tower, uint256 blockQueueTimeout) public payable {
        address hostAddr = msg.sender;
        require(towerToIndex[tower] != 0, "Tower does not exist");
        require(towers[towerToIndex[tower]].active, "Tower not active");
        require(msg.value >= MIN_STAKE, "Insufficient funds");

        towerToHosts[tower].push(hostAddr);
        
        Host memory host;
        host.addr = hostAddr;
        host.blockQueueTimeout = blockQueueTimeout;
        host.stake = msg.value;
        hosts.push(host);
        hostToIndex[hostAddr] = hosts.length - 1;
    }

    // sent by host
    function removeHost(address towerAddr) public {
        address hostAddr = msg.sender;
        require(towerToIndex[towerAddr] != 0, "Tower does not exist");
        require(hostToIndex[hostAddr] != 0, "Host does not exist");
        require(towers[towerToIndex[towerAddr]].active, "Tower not active");
        require(hosts[hostToIndex[msg.sender]].active, "Host not active");
        uint hostsLength = towerToHosts[towerAddr].length;
        bool found = false;
        for (uint i = 0; i < hostsLength; i++) {
            if (keccak256(abi.encodePacked(towerToHosts[towerAddr][i])) == keccak256(abi.encodePacked(hostAddr))) {
                towerToHosts[towerAddr][i] = towerToHosts[towerAddr][hostsLength - 1];
                towerToHosts[towerAddr].pop();
                found = true;
                break;
            }
        }
        require(found, "Host does not exist in tower");
        
        hosts[hostToIndex[hostAddr]].active = false;
        delete hostToTaskComputationPrice[hostAddr];
        delete hostToActiveTasks[hostAddr];
        delete hostToTaskQueue[hostAddr];
    }

    function calculateTotalPrice(address towerAddr, address hostAddr, string memory task) public view returns (uint256) {
        require(towerToIndex[towerAddr] != 0, "Tower does not exist");
        require(tidToIndex[task] != 0, "Task does not exist");
        require(hostToIndex[msg.sender] != 0, "Host does not exist");
        for (uint i = 0; i < hostToActiveTasks[hostAddr].length; i++) {
            if (keccak256(abi.encodePacked(hostToActiveTasks[hostAddr][i])) == keccak256(abi.encodePacked(task))) {
                uint256 totalPrice = tasks[tidToIndex[task]].price + hostToTaskComputationPrice[hostAddr][i] + towers[towerToIndex[towerAddr]].fee;
                return totalPrice;
            }
        }
        require(false, "Task does not exist in host");
    }

    // sent by client
    function queueTask(address towerAddr, string memory task, address hostAddr) public payable {
        require(towerToIndex[towerAddr] != 0, "Tower does not exist");
        require(tidToIndex[task] != 0, "Task does not exist");
        require(hostToIndex[msg.sender] != 0, "Host does not exist");
        require(towers[towerToIndex[towerAddr]].active, "Tower not active");
        require(tasks[tidToIndex[task]].active, "Task not active");
        require(hosts[hostToIndex[msg.sender]].active, "Host not active");
        uint256 combinedThroughput = towers[towerToIndex[towerAddr]].throughput + tasks[tidToIndex[task]].ioSizeLimit;
        require(combinedThroughput <= towers[towerToIndex[towerAddr]].bandwidth, "Bandwidth exceeded");
        require(msg.value >= calculateTotalPrice(towerAddr, hostAddr, task), "Insufficient funds");

        bool found = false;
        for (uint i = 0; i < hostToActiveTasks[hostAddr].length; i++) {
            if (keccak256(abi.encodePacked(hostToActiveTasks[hostAddr][i])) == keccak256(abi.encodePacked(task))) {
                found = true;
                break;
            }
        }
        require(found, "Task does not exist in host");
        
        towerToTaskQueue[towerAddr].push(task);
        towers[towerToIndex[towerAddr]].throughput = combinedThroughput;
        hostToTaskQueue[hostAddr].push(task);

        emit RequestPostedByClient(towerAddr, hostAddr, task);
    }

    // sent by tower
    function dequeueTask(string memory task, address hostAddr) public {
        address towerAddr = msg.sender;
        require(towerToIndex[towerAddr] != 0, "Tower does not exist");
        require(tidToIndex[task] != 0, "Task does not exist");
        require(hostToIndex[msg.sender] != 0, "Host does not exist");
        uint tasksLength = towerToTaskQueue[towerAddr].length;
        bool found = false;
        for (uint i = 0; i < tasksLength; i++) {
            if (keccak256(abi.encodePacked(towerToTaskQueue[towerAddr][i])) == keccak256(abi.encodePacked(task))) {
                towerToTaskQueue[towerAddr][i] = towerToTaskQueue[towerAddr][tasksLength - 1];
                towerToTaskQueue[towerAddr].pop();
                found = true;
                break;
            }
        }
        require(found, "Task does not exist in tower");
        
        towers[towerToIndex[towerAddr]].throughput -= tasks[tidToIndex[task]].ioSizeLimit;
        tasksLength = hostToTaskQueue[hostAddr].length;
        for (uint i = 0; i < tasksLength; i++) {
            if (keccak256(abi.encodePacked(hostToTaskQueue[hostAddr][i])) == keccak256(abi.encodePacked(task))) {
                hostToTaskQueue[hostAddr][i] = hostToTaskQueue[hostAddr][tasksLength - 1];
                hostToTaskQueue[hostAddr].pop();
                break;
            }
        }

        emit InputReceivedOnTower(towerAddr, hostAddr, task);
    }
    
    function getActiveHosts() public view returns (Host[] memory) {
        Host[] memory activeHosts;
        uint activeHostsLength = 0;
        for (uint i = 0; i < hosts.length; i++) {
            if (hosts[i].active) {
                activeHosts[activeHostsLength] = hosts[i];
                activeHostsLength++;
            }
        }
        return activeHosts;
    }

    // sent by host
    function activateTask(string memory task, uint256 price) public {
        address hostAddr = msg.sender;
        require(tidToIndex[task] != 0, "Task does not exist");
        require(hostToIndex[msg.sender] != 0, "Host does not exist");
        require(tasks[tidToIndex[task]].active, "Task not active");
        require(hosts[hostToIndex[msg.sender]].active, "Host not active");
        hostToActiveTasks[hostAddr].push(task);
        hostToTaskComputationPrice[hostAddr].push(price);
    }

    // sent by host
    function deactivateTask(string memory task) public {
        address hostAddr = msg.sender;
        require(tidToIndex[task] != 0, "Task does not exist");
        require(hostToIndex[msg.sender] != 0, "Host does not exist");
        require(tasks[tidToIndex[task]].active, "Task not active");
        require(hosts[hostToIndex[msg.sender]].active, "Host not active");
        uint tasksLength = hostToActiveTasks[hostAddr].length;
        for (uint i = 0; i < tasksLength; i++) {
            if (keccak256(abi.encodePacked(hostToActiveTasks[hostAddr][i])) == keccak256(abi.encodePacked(task))) {
                hostToActiveTasks[hostAddr][i] = hostToActiveTasks[hostAddr][tasksLength - 1];
                hostToActiveTasks[hostAddr].pop();
                hostToTaskComputationPrice[hostAddr][i] = hostToTaskComputationPrice[hostAddr][tasksLength - 1];
                hostToTaskComputationPrice[hostAddr].pop();
                break;
            }
        }
    }

    // sent by host
    function inputReceivedOnHost(address towerAddr, string memory task) public {
        require(towerToIndex[towerAddr] != 0, "Tower does not exist");
        require(tidToIndex[task] != 0, "Task does not exist");
        require(hostToIndex[msg.sender] != 0, "Host does not exist");
        require(towers[towerToIndex[towerAddr]].active, "Tower not active");
        require(tasks[tidToIndex[task]].active, "Task not active");
        require(hosts[hostToIndex[msg.sender]].active, "Host not active");
        emit InputReceivedOnHost(towerAddr, msg.sender, task);
    }

    // sent by tower
    function outputReceivedOnTower(address hostAddr, string memory task) public {
        require(towerToIndex[msg.sender] != 0, "Tower does not exist");
        require(tidToIndex[task] != 0, "Task does not exist");
        require(hostToIndex[hostAddr] != 0, "Host does not exist");
        require(towers[towerToIndex[msg.sender]].active, "Tower not active");
        emit OutputReceivedOnTower(msg.sender, hostAddr, task);
        for (uint i = 0; i < hostToActiveTasks[hostAddr].length; i++) {
            if (keccak256(abi.encodePacked(hostToActiveTasks[hostAddr][i])) == keccak256(abi.encodePacked(task))) {
                (bool success, ) = payable(hosts[hostToIndex[hostAddr]].addr).call{value: hostToTaskComputationPrice[hostAddr][i]}("");
                require(success, "Failed to pay");
                break;
            }
        }
    }

    // sent by client
    function outputReceivedOnClient(address towerAddr, address hostAddr, string memory task) public {
        require(towerToIndex[msg.sender] != 0, "Tower does not exist");
        require(tidToIndex[task] != 0, "Task does not exist");
        require(hostToIndex[hostAddr] != 0, "Host does not exist");
        emit OutputReceivedOnClient(towerAddr, hostAddr, task);
        (bool paidTaskOwner, ) = payable(tasks[tidToIndex[task]].ownerWallet).call{value: tasks[tidToIndex[task]].price}("");
        require(paidTaskOwner, "Failed to pay task owner");
        (bool paidTower, ) = payable(towers[towerToIndex[towerAddr]].addr).call{value: towers[towerToIndex[towerAddr]].fee}("");
        require(paidTower, "Failed to pay tower");
    }
}