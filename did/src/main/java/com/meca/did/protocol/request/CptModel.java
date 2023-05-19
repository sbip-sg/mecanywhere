package com.meca.did.protocol.request;

import io.swagger.annotations.ApiModelProperty;

import java.util.Map;

public class CptModel {

    @ApiModelProperty(name = "publisher", value = "did", required = true,
            example = "did:meca:0xfd340b5a30de452ae4a14dd1b92a7006868a29c8")
    private String publisher;

    @ApiModelProperty(name = "claim", value = "CPT", required = true,
            example = "{\n"
                    + "    \"title\": \"cpt\",\n"
                    + "    \"description\": \"this is cpt\",\n"
                    + "    \"properties\" : {\n"
                    + "        \"name\": {\n"
                    + "            \"type\": \"string\",\n"
                    + "            \"description\": \"the name of certificate owner\"\n"
                    + "        },\n"
                    + "        \"gender\": {\n"
                    + "            \"enum\": [\"F\", \"M\"],\n"
                    + "            \"type\": \"string\",\n"
                    + "            \"description\": \"the gender of certificate owner\"\n"
                    + "        },\n"
                    + "        \"age\": {\n"
                    + "            \"type\": \"number\",\n"
                    + "            \"description\": \"the age of certificate owner\"\n"
                    + "        }\n"
                    + "    },\n"
                    + "    \"required\": [\"name\", \"age\"]\n"
                    + "}")
    private Map<String, Object> claim;

    public String getPublisher() {
        return publisher;
    }

    public void setPublisher(String publisher) {
        this.publisher = publisher;
    }

    public Map<String, Object> getClaim() {
        return claim;
    }

    public void setClaim(Map<String, Object> claim) {
        this.claim = claim;
    }
}
