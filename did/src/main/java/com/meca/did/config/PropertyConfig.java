package com.meca.did.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.meca.did.util.DevPropertyUtil;
import com.meca.did.util.DockerPropertyUtil;
import com.meca.did.util.PropertyUtils;

@Configuration
public class PropertyConfig {
    @Value("${did.is.development}")
    private Boolean isDevelopment;

    @Bean
    public PropertyUtils propertyUtils() {
        if (isDevelopment) {
            return new DevPropertyUtil();
        } else {
            return new DockerPropertyUtil();
        }
    }
}
