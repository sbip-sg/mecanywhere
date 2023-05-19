package com.meca.did.exception;

import com.meca.did.constant.ErrorCode;

@SuppressWarnings("serial")
public class DIDBaseException extends RuntimeException {
    private ErrorCode errorCode = ErrorCode.BASE_ERROR;

    /**
     * constructor.
     *
     * @param msg exception message
     * @param cause exception object
     */
    public DIDBaseException(String msg, Throwable cause) {
        super(msg, cause);
    }

    /**
     * constructor.
     *
     * @param msg exception message
     */
    public DIDBaseException(String msg) {
        super(msg);
    }

    /**
     * constructor.
     *
     * @param errorCode the errorCode
     */
    public DIDBaseException(ErrorCode errorCode) {
        this(errorCode.getCode() + " - " + errorCode.getCodeDesc());
        this.errorCode = errorCode;
    }

    /**
     * get associated error code.
     *
     * @return ErrorCode
     */
    public ErrorCode getErrorCode() {
        return errorCode;
    }

    @Override
    public String toString() {
        String s = getClass().getName();
        StringBuilder builder = new StringBuilder();
        builder
                .append(s)
                .append(". Error code = ")
                .append(getErrorCode().getCode())
                .append(", Error message : ")
                .append(getMessage());
        return builder.toString();
    }
}
