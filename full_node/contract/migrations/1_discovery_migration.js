const DiscoveryContract = artifacts.require("DiscoveryContract");
const fullNodeConfig = require("../../config.json");

module.exports = function (deployer) {
    deployer.deploy(DiscoveryContract, fullNodeConfig.full_node.host_expiry_duration_sec);
};
