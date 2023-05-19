package com.meca.did.protocol.response;

import com.meca.did.constant.ErrorCode;
import lombok.Data;

@Data
public class ResponseData<T> {
    private T result;

    /**
     * The error code.
     */
    private Integer errorCode;

    /**
     * The error message.
     */
    private String errorMessage;

    /**
     * The blockchain transaction info. Note that this transaction only becomes valid (not null nor
     * blank) when a successful transaction is sent to chain with a block generated.
     */
    private TransactionInfo transactionInfo = null;

    /**
     * The blockchain transaction info. Note that this transaction only becomes valid (not null nor
     * blank) when a successful transaction is sent to chain with a block generated.
     */
//    private TransactionInfo transactionInfo = null;

    public ResponseData() {
        this.setErrorCode(ErrorCode.SUCCESS);
    }

    /**
     * Instantiates a new response data. Transaction info is left null to avoid unnecessary boxing.
     *
     * @param result the result
     * @param errorCode the return code
     */
    public ResponseData(T result, ErrorCode errorCode) {
        this.result = result;
        if (errorCode != null) {
            this.errorCode = errorCode.getCode();
            this.errorMessage = errorCode.getCodeDesc();
        }
    }

    /**
     * Instantiates a new response data with transaction info.
     *
     * @param result the result
     * @param errorCode the return code
     * @param transactionInfo transactionInfo
     */
    public ResponseData(T result, ErrorCode errorCode, TransactionInfo transactionInfo) {
        this.result = result;
        if (errorCode != null) {
            this.errorCode = errorCode.getCode();
            this.errorMessage = errorCode.getCodeDesc();
        }
        if (transactionInfo != null) {
            this.transactionInfo = transactionInfo;
        }
    }

    /**
     * set a ErrorCode type errorCode.
     *
     * @param errorCode the errorCode
     */
    public void setErrorCode(ErrorCode errorCode) {
        if (errorCode != null) {
            this.errorCode = errorCode.getCode();
            this.errorMessage = errorCode.getCodeDesc();
        }
    }

    /**
     * Instantiates a new Response data based on the error code and error message.
     *
     * @param result the result
     * @param errorCode code number
     * @param errorMessage errorMessage
     */
    public ResponseData(T result, Integer errorCode, String errorMessage) {
        this.result = result;
        this.errorCode = errorCode;
        this.errorMessage = errorMessage;
    }
}