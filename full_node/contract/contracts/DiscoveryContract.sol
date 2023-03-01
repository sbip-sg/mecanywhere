pragma solidity >=0.4.22 <0.9.0;

pragma experimental ABIEncoderV2;

contract DiscoveryContract {
    mapping(string => uint256) private ipAddressToTimestamp;
    string[] private ipAddressList;

    function setIpAddressTimestamp(string memory ipAddress, uint256 timestamp)
        public
    {
        if (ipAddressToTimestamp[ipAddress] == 0) {
            ipAddressList.push(ipAddress);
        }
        ipAddressToTimestamp[ipAddress] = timestamp;
    }

    function getIpAddressTimestamp(string memory ipAddress)
        public
        view
        returns (uint256)
    {
        return ipAddressToTimestamp[ipAddress];
    }

    function getAllIpAddressTimestamps()
        public
        view
        returns (string[] memory, uint256[] memory)
    {
        uint256 length = ipAddressList.length;
        string[] memory trimmedIpAddressList = new string[](length);
        uint256[] memory timestampList = new uint256[](length);

        for (uint256 i = 0; i < length; i++) {
            trimmedIpAddressList[i] = ipAddressList[i];
            timestampList[i] = ipAddressToTimestamp[ipAddressList[i]];
        }

        return (trimmedIpAddressList, timestampList);
    }

    function removeIpAddress(string memory ipAddress) public {
        if (ipAddressToTimestamp[ipAddress] != 0) {
            delete ipAddressToTimestamp[ipAddress];
            for (uint256 i = 0; i < ipAddressList.length; i++) {
                if (
                    keccak256(abi.encodePacked(ipAddressList[i])) ==
                    keccak256(abi.encodePacked(ipAddress))
                ) {
                    delete ipAddressList[i];
                    break;
                }
            }
        }
    }
}
