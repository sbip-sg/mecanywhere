package com.meca.did.contract;

import lombok.Data;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.web3j.crypto.Credentials;
import org.web3j.protocol.Web3j;
import org.web3j.protocol.http.HttpService;
import org.web3j.tx.gas.ContractGasProvider;
import org.web3j.tx.gas.StaticGasProvider;

import com.meca.did.util.PropertyUtils;

import java.math.BigInteger;

@Data
@Configuration
public class ContractConfig {
    private static final Logger logger = LoggerFactory.getLogger(ContractConfig.class);

    @Autowired
    private PropertyUtils propertyUtils;

    @Value("${did.is.development}")
    private Boolean isDevelopment;

    @Value("${did.contract.url}")
    private String url;

    @Value("${did.contract.address}")
    private String dIDContractAddress;

    @Value("${did.contract.binary}")
    private String dIDContractBinary;

    @Value("${cpt.contract.address}")
    private String cptContractAddress;

    @Value("${cpt.contract.binary}")
    private String cptContractBinary;

    @Value("${did.gas.price}")
    private Long gasPrice;

    @Value("${did.gas.limit}")
    private Long gasLimit;

    @Value("${wallet.private.key:}")
    private String walletPrivateKey;

    @Bean
    public Web3j web3j() {
        return Web3j.build(new HttpService(url));
    }

    @Bean
    public Credentials credentials() {
        if (isDevelopment) {
            walletPrivateKey = propertyUtils.getProperty("WALLET_PRIVATE_KEY");
        }
        return Credentials.create(walletPrivateKey);
    }

    @Bean
    public ContractGasProvider contractGasProvider() {
        return new StaticGasProvider(
                BigInteger.valueOf(gasPrice),
                BigInteger.valueOf(gasLimit)
        );
    }
}
