package com.meca.did.exception;

import com.meca.did.constant.ErrorCode;

public class PrivateKeyIllegalException extends DIDBaseException {

    public PrivateKeyIllegalException(Throwable cause) {
        super(ErrorCode.DID_PRIVATEKEY_INVALID.getCodeDesc(), cause);
    }

    public PrivateKeyIllegalException() {
        super(ErrorCode.DID_PRIVATEKEY_INVALID.getCodeDesc());
    }

    @Override
    public ErrorCode getErrorCode() {
        return ErrorCode.DID_PRIVATEKEY_INVALID;
    }
}
