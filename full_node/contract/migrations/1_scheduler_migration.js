const Contract = artifacts.require("SchedulerContract");

module.exports = function (deployer) {
    deployer.deploy(Contract);
};
