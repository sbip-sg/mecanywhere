package com.meca.did.protocol.request;

import io.swagger.annotations.ApiModelProperty;
import lombok.Data;

import java.util.Map;

@Data
public class VerifyCredentialRequest {
    @ApiModelProperty(name = "credential", value = "Credential to be verified", required = true,
            example = "{\n"
                    + "    \"context\": \"https://www.w3.org/2018/credentials/v1\",\n"
                    + "    \"id\": \"ae559160-c1bb-4f15-845e-af7d7912e07b\",\n"
                    + "    \"issuer\": \"did:meca:0xfd340b5a30de452ae4a14dd1b92a7006868a29c8\",\n"
                    + "    \"issuanceDate\": 1644379660,\n"
                    + "    \"expirationDate\": 4797979660,\n"
                    + "    \"claim\": {\n"
                    + "      \"gender\": \"M\",\n"
                    + "      \"name\": \"Chai\",\n"
                    + "      \"DID\": \"did:meca:0x0fa21fd3d11d2cd5e6cdef2c7cd6531a25a5964f\"\n"
                    + "    },\n"
                    + "    \"proof\": {\n"
                    + "      \"creator\": \"did:meca:0xfd340b5a30de452ae4a14dd1b92a7006868a29c8\",\n"
                    + "      \"signature\": \"G1r9auOBUNK6qa/vnWsSdpBg5UW4bXc2nAnbRTRI/kxFHv8w4S5VYUx6cyQ3YxEnErbWMhsvOfA83kiQ/bH5A8A=\",\n"
                    + "      \"created\": \"1578467662\",\n"
                    + "      \"type\": \"Secp256k1\"\n"
                    + "    },\n"
                    + "    \"signature\": \"G1r9auOBUNK6qa/vnWsSdpBg5UW4bXc2nAnbRTRI/kxFHv8w4S5VYUx6cyQ3YxEnErbWMhsvOfA83kiQ/bH5A8A=\",\n"
                    + "    \"hash\": \"0x804c18e44b71e18339a8481d83fb3cbf89ac27e7a883025b95a4635385f8680e\",\n"
                    + "    \"proofType\": \"Secp256k1\",\n"
                    + "    \"signatureThumbprint\": \"{\\\"claim\\\":\\\"age0x8b953cbb84328003779eb1ef176ef07f7dd0ae3d4a8e408de53d15a36466c86egender0xe61d9a3d3848fb2cdd9a2ab61e2f21a10ea431275aed628a0557f9dee697c37aname0xd437888f8f49572399b4a94fe4ca3adc1404e4bc0e4e0de11bcdc525071279c7\\\",\\\"context\\\":\\\"https://www.w3.org/2018/credentials/v1\\\",\\\"expirationDate\\\":4732067662,\\\"id\\\":\\\"ae559160-c1bb-4f15-845e-af7d7912e07b\\\",\\\"issuanceDate\\\":1578467662,\\\"issuer\\\":\\\"did:meca:0xfd340b5a30de452ae4a14dd1b92a7006868a29c8\\\",\\\"proof\\\":{\\\"created\\\":\\\"1578467662\\\",\\\"creator\\\":\\\"did:meca:0xfd340b5a30de452ae4a14dd1b92a7006868a29c8\\\",\\\"signature\\\":\\\"G1r9auOBUNK6qa/vnWsSdpBg5UW4bXc2nAnbRTRI/kxFHv8w4S5VYUx6cyQ3YxEnErbWMhsvOfA83kiQ/bH5A8A=\\\",\\\"type\\\":\\\"Secp256k1\\\"}}\"\n"
                    + "}")
    private Map<String, Object> credential;
}
