package com.meca.did.util;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.util.Properties;
import java.util.Set;

public class PropertyUtils {
    private static final Logger logger = LoggerFactory.getLogger(PropertyUtils.class);
    private static final String ENV_FILE = ".env";
    private static Properties prop = new Properties();

    static {
        load();
    }

    /**
     * load properties from specific config file.
     *
     * @param filePath properties config file.
     */
    private static synchronized void loadProperties(String filePath) {

        try {
            InputStream in = PropertyUtils.class.getClassLoader().getResourceAsStream(filePath);
            BufferedReader br = new BufferedReader(new InputStreamReader(in));
            prop.load(br);
            br.close();
            in.close();
            logger.info("loadProps finish...");
        } catch (IOException e) {
            logger.error("loadProps error", e);
        }
    }

    /**
     * get property value by specific key.
     *
     * @param key property key
     * @return value of the key
     */
    public static String getProperty(String key) {
        if (null == prop) {
            load();
        }
        return prop.getProperty(key);
    }

    /**
     * get property value by specific key.
     *
     * @param key          property keys
     * @param defaultValue default value
     * @return value of the key
     */
    public static String getProperty(String key, String defaultValue) {
        return prop.getProperty(key, defaultValue);
    }

    /**
     * get the all key from Properties.
     *
     * @return value of the key Set
     */
    public static Set<Object> getAllPropertyKey() {
        return prop.keySet();
    }

    /**
     * load the properties.
     */
    private static void load() {
        loadProperties(ENV_FILE);
    }

    /**
     * reload the properties.
     */
    public static void reload() {
        load();
    }
}
