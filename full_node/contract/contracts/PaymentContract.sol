// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract PaymentContract {
    // Records for payments that are due to our wallet
    struct DueRecord {
        uint256 nonce;
        string did;
        address source;
        uint256 amount;
    }

    mapping(uint256 => DueRecord) private nonceToDueRecord;

    function getDue(uint256 nonce) public view returns (DueRecord memory) {
        return nonceToDueRecord[nonce];
    }
    
    function setDue(uint256 nonce, string memory did, address source, uint256 amount) public {
        nonceToDueRecord[nonce] = DueRecord(nonce, did, source, amount);
    }

    function removeDue(uint256 nonce) public {
        delete nonceToDueRecord[nonce];
    }

    mapping(string => uint256) private didToBalance;

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
