package com.meca.did.protocol.inf;

import com.meca.did.exception.DataTypeCastException;

public interface RawSerializer extends JsonSerializer {

    public default String toRawData() throws DataTypeCastException {
        return JsonSerializer.super.toJson();
    }
}
