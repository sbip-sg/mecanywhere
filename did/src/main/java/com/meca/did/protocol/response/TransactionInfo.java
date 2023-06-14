package com.meca.did.protocol.response;

import lombok.Data;
import org.web3j.protocol.core.methods.response.TransactionReceipt;

import java.math.BigInteger;

@Data
public class TransactionInfo {
    /**
     * The block number.
     */
    private BigInteger blockNumber;

    /**
     * The transaction hash value.
     */
    private String transactionHash;

    /**
     * The transaction index.
     */
    private BigInteger transactionIndex;

    /**
     * Constructor from a transactionReceipt.
     *
     * @param receipt the transaction receipt
     */
    public TransactionInfo(TransactionReceipt receipt) {
        if (receipt != null) {
            this.blockNumber = receipt.getBlockNumber();
            this.transactionHash = receipt.getTransactionHash();
            this.transactionIndex = receipt.getTransactionIndex();
        }
    }

    /**
     * Constructor.
     *
     * @param blockNumber blockNumber
     * @param transactionHash transactionHash
     * @param transactionIndex transactionIndex
     */
    public TransactionInfo(BigInteger blockNumber,
                           String transactionHash,
                           BigInteger transactionIndex) {
        this.blockNumber = blockNumber;
        this.transactionHash = transactionHash;
        this.transactionIndex = transactionIndex;
    }
}
