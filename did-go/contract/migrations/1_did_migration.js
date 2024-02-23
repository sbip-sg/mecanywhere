const DidContract = artifacts.require("DIDContract");

module.exports = function (deployer) {
    deployer.deploy(DidContract);
};
