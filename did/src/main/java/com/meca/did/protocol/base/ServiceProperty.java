package com.meca.did.protocol.base;

import lombok.Data;

@Data
public class ServiceProperty {

    /**
     * Required: The type.
     */
    private String type;

    /**
     * Required: The service endpoint.
     */
    private String serviceEndpoint;
}
