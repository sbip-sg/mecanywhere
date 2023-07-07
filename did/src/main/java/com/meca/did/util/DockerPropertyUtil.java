package com.meca.did.util;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.env.Environment;

public class DockerPropertyUtil extends PropertyUtils {
    @Autowired
    private Environment env;

    @Override
    public String getProperty(String key) {
        return env.getProperty(key);
    }

    @Override
    public String getProperty(String key, String defaultValue) {
        return env.getProperty(key, defaultValue);
    }
}
