const crypto = require('crypto');
const CptContract = artifacts.require("CptContract");
const DIDContract = artifacts.require("DIDContract");

function getRandomNumber(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min);
}

function getRandomHex(length) {
    const bytes = Math.ceil(length / 2);
    const hex = crypto.randomBytes(bytes).toString('hex');
    return '0x' + hex.slice(0, length);
}

contract("CptContract", (accounts) => {
  let cptContract;
  let didContract;

  before(async () => {
    cptContract = await CptContract.deployed();
    didContract = await DIDContract.deployed();
  });

  it('should register a new CPT', async () => {
    // Set up test data
    const publisher = accounts[0];
    const intArray = Array.from({ length: 8 }, () => getRandomNumber(1, 10));
    const bytes32Array = Array.from({ length: 8 }, () => getRandomHex(64));
    const jsonSchemaArray = Array.from({ length: 32 }, () => getRandomHex(64));
    const v = getRandomNumber(0, 255);
    const r = getRandomHex(64);
    const s = getRandomHex(64);

    // Register CPT
    const result = await cptContract.registerCpt(
      publisher,
      intArray,
      bytes32Array,
      jsonSchemaArray,
      v,
      r,
      s
    );
    
    // Retrieve the registered CPT
    const cptId = result.logs[0].args.cptId.toNumber();
    const registeredCpt = await cptContract.queryCpt(cptId);

    // Assertions
    assert.equal(result.receipt.status, true, 'CPT registration failed');
    assert.equal(registeredCpt.publisher, publisher, 'Incorrect publisher');
    // assert.deepEqual(registeredCpt.intArray, intArray, 'Incorrect intArray');
    assert.deepEqual(registeredCpt.bytes32Array, bytes32Array, 'Incorrect bytes32Array');
    assert.deepEqual(registeredCpt.jsonSchemaArray, jsonSchemaArray, 'Incorrect jsonSchemaArray');
    assert.equal(registeredCpt.v, v, 'Incorrect signature v');
    assert.equal(registeredCpt.r, r, 'Incorrect signature r');
    assert.equal(registeredCpt.s, s, 'Incorrect signature s');
  });
  
  it('should update an existing CPT', async () => {
    // Set up test data
    const publisher = accounts[0];
    
    const auth = web3.utils.utf8ToHex('authentication');
    const created = web3.utils.utf8ToHex('created');
    const updated = 1;
    const tx = await didContract.createDID(publisher, auth, created, updated);
    assert(tx.receipt.status, true, 'Transaction should succeed.');

    const intArray = Array.from({ length: 8 }, () => getRandomNumber(1, 10));
    const bytes32Array = Array.from({ length: 8 }, () => getRandomHex(64));
    const jsonSchemaArray = Array.from({ length: 32 }, () => getRandomHex(64));
    const v = getRandomNumber(0, 255);
    const r = getRandomHex(64);
    const s = getRandomHex(64);

    // Register CPT
    const result = await cptContract.registerCpt(
        publisher,
        intArray,
        bytes32Array,
        jsonSchemaArray,
        v,
        r,
        s
    );

    // Retrieve the registered CPT
    const cptId = result.logs[0].args.cptId.toNumber();
    const registeredCpt = await cptContract.queryCpt(cptId);

    // Assertions
    assert.equal(result.receipt.status, true, 'CPT registration failed');
    assert.equal(registeredCpt.publisher, publisher, 'Incorrect publisher');
    // assert.deepEqual(registeredCpt.intArray, intArray, 'Incorrect intArray');
    assert.deepEqual(registeredCpt.bytes32Array, bytes32Array, 'Incorrect bytes32Array');
    assert.deepEqual(registeredCpt.jsonSchemaArray, jsonSchemaArray, 'Incorrect jsonSchemaArray');
    assert.equal(registeredCpt.v, v, 'Incorrect signature v');
    assert.equal(registeredCpt.r, r, 'Incorrect signature r');
    assert.equal(registeredCpt.s, s, 'Incorrect signature s');

    // Set up test data
    const newIntArray = Array.from({ length: 8 }, () => getRandomNumber(1, 10));
    const newBytes32Array = Array.from({ length: 8 }, () => getRandomHex(64));
    const newJsonSchemaArray = Array.from({ length: 32 }, () => getRandomHex(64));
    const newV = getRandomNumber(0, 255);
    const newR = getRandomHex(64);
    const newS = getRandomHex(64);
    
    // Update CPT
    const updateResult = await cptContract.updateCpt(
        cptId,
        publisher,
        newIntArray,
        newBytes32Array,
        newJsonSchemaArray,
        newV,
        newR,
        newS
    );

    // Retrieve the updated CPT
    const updatedCpt = await cptContract.queryCpt(cptId);

    // Assertions
    assert.equal(updateResult.receipt.status, true, 'CPT update failed');
    assert.equal(updatedCpt.publisher, publisher, 'Incorrect publisher');
    // assert.deepEqual(updatedCpt.intArray, newIntArray, 'Incorrect intArray');
    assert.deepEqual(updatedCpt.bytes32Array, newBytes32Array, 'Incorrect bytes32Array');
    assert.deepEqual(updatedCpt.jsonSchemaArray, newJsonSchemaArray, 'Incorrect jsonSchemaArray');
    assert.equal(updatedCpt.v, newV, 'Incorrect signature v');
    assert.equal(updatedCpt.r, newR, 'Incorrect signature r');
    assert.equal(updatedCpt.s, newS, 'Incorrect signature s');

    });
});
