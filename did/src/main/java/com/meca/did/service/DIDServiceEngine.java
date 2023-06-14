package com.meca.did.service;

import com.meca.did.protocol.base.DIDDocument;
import com.meca.did.protocol.base.DIDPojo;
import com.meca.did.protocol.response.ResponseData;

import java.util.List;

public interface DIDServiceEngine {
    /**
     * call DID contract to create a new DID.
     *
     * @param DIDAddress identity on blockchain
     * @param publicKey public key of the identity
     * @return result
     */
    ResponseData<Boolean> createDID(
            String DIDAddress,
            String publicKey
    );

    /**
     * write attribute to blockchain.
     *
     * @param DIDAddress identity on blockchain
     * @param attributeKey the key of the attribute
     * @param value the value of the attribute
     * @return result
     */
    ResponseData<Boolean> setAttribute(
            String DIDAddress,
            String attributeKey,
            String value
    );

    /**
     * check if the DID exists on blockchain.
     *
     * @param DID the DID of the entity
     * @return result
     */
    ResponseData<Boolean> DIDExists(String DID);

    /**
     * get DID document from blockchain.
     *
     * @param DID the entity's DID
     * @return DID document
     */
    ResponseData<DIDDocument> getDIDDocument(String DID);

    /**
     * query data according to block height, index location and search direction.
     *
     * @param blockNumber the query blockNumber
     * @param pageSize the page size
     * @param indexInBlock the beginning (including) of the current block
     * @param direction search direction: true means forward search, false means backward search
     * @return return the didPojo List
     * @throws Exception unknown exception
     */
    ResponseData<List<DIDPojo>> getDIDList(
            Integer blockNumber,
            Integer pageSize,
            Integer indexInBlock,
            boolean direction
    ) throws Exception;

    /**
     * get total DID
     *
     * @return total DID
     */
    ResponseData<Integer> getDIDCount();
}
