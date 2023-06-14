package com.meca.did.util;

import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.annotation.Configuration;

@Configuration
public class PrivateKeyUtil {

    private static final Logger logger = LoggerFactory.getLogger(PrivateKeyUtil.class);

    public static final String KEY_DIR = "./keys/";

    /**
     * this method stores DID private key information by file and stores
     * private key information by itself in actual scene.
     *
     * @param path save path
     * @param DID the DID
     * @param privateKey the private key
     * @return returns saved results
     */
    public static boolean savePrivateKey(String path, String DID, String privateKey) {

        try {
            if (null == DID) {
                logger.error("DID is null");
                return false;
            }

            // get the third paragraph of DID.
            String fileName = DID.substring(DID.lastIndexOf(":") + 1);

            // check whether the path exists or not, then create the path and return.
            String checkPath = FileUtil.checkDir(path);
            String filePath = checkPath + fileName;

            logger.info("save private key into file, DID={}, filePath={}", DID, filePath);

            // save the private key information as the file name for the third paragraph of DID.
            FileUtil.saveFile(filePath, privateKey);
            return true;
        } catch (Exception e) {
            logger.error("savePrivateKey error", e);
        }
        return false;
    }

    /**
     * get the private key by DID.
     *
     * @param path the path
     * @param DID the DID
     * @return returns the private key
     */
    public static String getPrivateKeyByDID(String path, String DID) {

        if (null == DID) {
            logger.error("DID is null");
            return StringUtils.EMPTY;
        }

        // get the third paragraph of DID.
        String fileName = DID.substring(DID.lastIndexOf(":") + 1);

        // check whether the path exists or not, then create the path and return.
        String checkPath = FileUtil.checkDir(path);
        String filePath = checkPath + fileName;

        logger.info("get private key from file, DID={}, filePath={}", DID, filePath);

        // get private key information from a file according to the third paragraph of DID.
        return FileUtil.getDataByPath(filePath);
    }
}
