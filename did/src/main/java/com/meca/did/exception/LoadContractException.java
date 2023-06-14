package com.meca.did.exception;

import com.meca.did.constant.ErrorCode;

public class LoadContractException extends DIDBaseException {

    public LoadContractException(Throwable cause) {
        super(ErrorCode.LOAD_CONTRACT_FAILED.getCodeDesc(), cause);
    }

    public LoadContractException() {
        super(ErrorCode.LOAD_CONTRACT_FAILED.getCodeDesc());
    }

    @Override
    public ErrorCode getErrorCode() {
        return ErrorCode.LOAD_CONTRACT_FAILED;
    }
}