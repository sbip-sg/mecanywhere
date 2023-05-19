package com.meca.did.protocol.base;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.ToString;

@Data
@EqualsAndHashCode(callSuper = true)
@ToString(callSuper = true)
public class DIDPojo extends DIDBaseInfo {

    /**
     * the blockNum for the DID.
     */
    private Integer currentBlockNum;

    /**
     * the index for the blockNum.
     */
    private Integer index;

    /**
     * the previous blockNum.
     */
    private Integer previousBlockNum;
}
