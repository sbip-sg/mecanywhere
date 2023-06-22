// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract PaymentContract {
    address private owner;
    mapping(string => uint256) private didToBalance;

    event PaymentReceived(string indexed did, uint256 amount);

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "You're not the smart contract owner!");
        _;
    }

    function pay(string memory fromDid) external payable {
        if (msg.value <= 0) {
            revert("Value must be positive.");
        }
        
        emit PaymentReceived(fromDid, msg.value);
        increaseBalance(fromDid, msg.value);
    }

    function withdraw(string memory toDid, address payable to, uint256 amount) public payable onlyOwner {
        if (didToBalance[toDid] < amount) {
            revert("Insufficient balance.");
        }

        decreaseBalance(toDid, amount);
        (bool sent, bytes memory data) = to.call{value: amount}("");
        if (!sent) {
            revert("Failed to send Ether");
        }
    }

    function getBalance(string memory did) public view returns (uint256) {
        return didToBalance[did];
    }
    
    function increaseBalance(string memory did, uint256 amount) public {
        didToBalance[did] += amount;
    }

    function decreaseBalance(string memory did, uint256 amount) public {
        didToBalance[did] -= amount;
    }
}
