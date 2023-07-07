package com.meca.did.util;

import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;

@Configuration
public class PrivateKeyUtil {

    private static final Logger logger = LoggerFactory.getLogger(PrivateKeyUtil.class);

    @Autowired
    private PropertyUtils propertyUtils;

    /**
     * get the private key by DID.
     *
     * @param path the path
     * @param DID the DID
     * @return returns the private key
     */
    public String getPrivateKeyByDID(String DID) {

        if (null == DID) {
            logger.error("DID is null");
            return StringUtils.EMPTY;
        }

        // get the third paragraph of DID.
        String fileName = DID.substring(DID.lastIndexOf(":") + 1);

        return propertyUtils.getProperty(fileName.substring(2));
    }
}
