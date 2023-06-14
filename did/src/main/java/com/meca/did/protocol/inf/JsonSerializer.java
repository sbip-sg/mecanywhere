package com.meca.did.protocol.inf;

import com.meca.did.exception.DataTypeCastException;
import com.meca.did.util.DataToolUtils;

import java.io.Serializable;

public interface JsonSerializer extends Serializable {

    public default String toJson() throws DataTypeCastException {
        return DataToolUtils.serialize(this);
    }
}
