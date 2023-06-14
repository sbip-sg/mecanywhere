const DIDContract = artifacts.require('DIDContract');

contract('DIDContract', (accounts) => {
  let didContract;

  before(async () => {
    didContract = await DIDContract.deployed();
  });

  it('should create a DID and check identity existence', async () => {
    const identity = accounts[0];
    let exists = await didContract.identityExists(identity);
    assert.equal(exists, false, 'Identity should not exist.');
    
    const auth = web3.utils.utf8ToHex('authentication');
    const created = web3.utils.utf8ToHex('created');
    const updated = 1;
    const initialFirstBlockNum = await didContract.getFirstBlockNum();

    const tx = await didContract.createDID(identity, auth, created, updated);
    assert(tx.receipt.status, true, 'Transaction should succeed.');

    const latestBlock = await didContract.getLatestRelatedBlock(identity);
    assert.equal(latestBlock.toNumber(), tx.receipt.blockNumber, 'Latest related block should match transaction block number.');

    const firstBlockNum = await didContract.getFirstBlockNum();
    assert.equal(firstBlockNum.toNumber(), initialFirstBlockNum.toNumber(), 'First block number should match initial first block number.');

    const latestBlockNum = await didContract.getLatestBlockNum();
    assert.equal(latestBlockNum.toNumber(), tx.receipt.blockNumber, 'Latest block number should match transaction block number.');

    const didCount = await didContract.getDIDCount();
    assert.equal(didCount.toNumber(), 1, 'DID count should be 1.');

    exists = await didContract.identityExists(identity);
    assert.equal(exists, true, 'Identity should exist.');
  });

  it('should set an attribute', async () => {
    const identity = accounts[0];
    const key = web3.utils.utf8ToHex('attribute');
    const value = web3.utils.utf8ToHex('value');
    const updated = 2;

    const tx = await didContract.setAttribute(identity, key, value, updated);
    assert(tx.receipt.status, true, 'Transaction should succeed.');

    const latestBlock = await didContract.getLatestRelatedBlock(identity);
    assert.equal(latestBlock.toNumber(), tx.receipt.blockNumber, 'Latest related block should match transaction block number.');
  });

  it('should check if an identity exists', async () => {
    const identity = accounts[0];
    const exists = await didContract.identityExists(identity);
    assert.equal(exists, true, 'Identity should exist.');
  });
});
