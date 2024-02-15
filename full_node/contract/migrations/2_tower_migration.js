const Contract = artifacts.require("TowerContract");

module.exports = function (deployer) {
    deployer.deploy(Contract);
};
