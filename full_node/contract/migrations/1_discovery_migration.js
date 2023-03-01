const DiscoveryContract = artifacts.require("DiscoveryContract");

module.exports = function (deployer) {
    deployer.deploy(DiscoveryContract);
};
