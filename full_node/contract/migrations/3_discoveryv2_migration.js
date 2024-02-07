const contract = artifacts.require("DiscoveryContractV2");

module.exports = function (deployer) {
    deployer.deploy(contract);
};
