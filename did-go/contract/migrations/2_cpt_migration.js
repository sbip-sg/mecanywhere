const CptContract = artifacts.require("CptContract");

module.exports = function (deployer) {
    deployer.deploy(CptContract);
};
