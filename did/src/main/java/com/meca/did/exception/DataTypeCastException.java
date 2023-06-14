package com.meca.did.exception;

import com.meca.did.constant.ErrorCode;

@SuppressWarnings("serial")
public class DataTypeCastException extends DIDBaseException {

    /**
     * constructor.
     *
     * @param cause Throwable
     */
    public DataTypeCastException(Throwable cause) {
        super(ErrorCode.DATA_TYPE_CASE_ERROR.getCodeDesc(), cause);
    }

    /**
     * constructor.
     *
     * @param message message
     */
    public DataTypeCastException(String message) {
        super(message);
    }

    /**
     * get associated error code.
     */
    public ErrorCode getErrorCode() {
        return ErrorCode.DATA_TYPE_CASE_ERROR;
    }
}
