package com.meca.did.util;

import com.meca.did.constant.DIDConstant;
import com.meca.did.protocol.base.DIDPrivateKey;
import org.apache.commons.lang3.StringUtils;
import org.apache.commons.lang3.math.NumberUtils;
import org.web3j.crypto.ECKeyPair;
import org.web3j.crypto.Keys;
import org.web3j.crypto.WalletUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.math.BigInteger;
import java.util.regex.Pattern;

public class DIDUtils {

    private static final Logger logger = LoggerFactory.getLogger(DIDUtils.class);

    /**
     * Convert a DID to an account address.
     *
     * @param DID the DID
     * @return DID related address, empty if input DID is illegal
     */
    public static String convertDIDToAddress(String DID) {
        if (StringUtils.isEmpty(DID) || !StringUtils.contains(DID, DIDConstant.DID_PREFIX)) {
            return StringUtils.EMPTY;
        }
        String[] DIDFields = StringUtils.splitByWholeSeparator(DID, DIDConstant.DID_SEPARATOR);
        return DIDFields[DIDFields.length - 1];
    }

    /**
     * Convert an account address to DID.
     *
     * @param address the address
     * @return a related DID, or empty string if the input is illegal.
     */
    public static String convertAddressToDID(String address) {
        if (StringUtils.isEmpty(address)) {
            return StringUtils.EMPTY;
        }
        return buildDIDByAddress(address);
    }

    /**
     * Convert a public key to a DID.
     *
     * @param publicKey the public key
     * @return DID
     */
    public static String convertPublicKeyToDID(String publicKey) {
        try {
            String address = Keys.getAddress(new BigInteger(publicKey));
            return buildDIDByAddress(address);
        } catch (Exception e) {
            logger.error("convert publicKey to DID error.", e);
            return StringUtils.EMPTY;
        }
    }

    private static String buildDIDByAddress(String address) {
        StringBuffer DID = new StringBuffer();
        DID.append(DIDConstant.DID_PREFIX);
        if (!StringUtils.contains(address, DIDConstant.HEX_PREFIX)) {
            DID.append(DIDConstant.HEX_PREFIX);
        }
        DID.append(address);
        return DID.toString();
    }

    /**
     * check if private key is empty.
     *
     * @param DIDPrivateKey the DID private key
     * @return true if the private key is not empty, false otherwise.
     */
    public static boolean isPrivateKeyValid(DIDPrivateKey DIDPrivateKey) {
        return (null != DIDPrivateKey && StringUtils.isNotEmpty(DIDPrivateKey.getPrivateKey())
                && NumberUtils.isDigits(DIDPrivateKey.getPrivateKey())
                && new BigInteger(DIDPrivateKey.getPrivateKey()).compareTo(BigInteger.ZERO) > 0);
    }

    /**
     * Check if the input DID is legal or not.
     *
     * @param DID the DID
     * @return true if the DID is legal, false otherwise.
     */
    public static boolean isDIDValid(String DID) {
        return StringUtils.isNotEmpty(DID)
                && StringUtils.startsWith(DID, DIDConstant.DID_PREFIX)
                && isValidAddress(convertDIDToAddress(DID));
    }

    /**
     * check if the given string is a valid address.
     *
     * @param addr given string
     * @return true if yes, false otherwise.
     */
    public static boolean isValidAddress(String addr) {
        if (StringUtils.isEmpty(addr)
                || !Pattern.compile(DIDConstant.ADDRESS_PATTERN).matcher(addr).matches()) {
            return false;
        }
        try {
            return WalletUtils.isValidAddress(addr);
        } catch (Exception e) {
            return false;
        }
    }

    /**
     * check if the public key matchs the private key.
     *
     * @param privateKey the DID private key
     * @param publicKey the DID publicKey key
     * @return true if the private and publicKey key is match, false otherwise.
     */
    public static boolean isKeypairMatch(String privateKey, String publicKey) {
        ECKeyPair keyPair = DataToolUtils.createKeyPairFromPrivate(new BigInteger(privateKey));
        return StringUtils.equals(String.valueOf(keyPair.getPublicKey()), publicKey);
    }

    /**
     * Check private key length.
     *
     * @param privateKey private key string in decimal
     * @return true if OK, false otherwise
     */
    public static boolean isPrivateKeyLengthValid(String privateKey) {
        if (StringUtils.isBlank(privateKey)) {
            return false;
        }
        DIDPrivateKey DIDPrivateKey = new DIDPrivateKey();
        DIDPrivateKey.setPrivateKey(privateKey);
        try {
            BigInteger privKeyBig = new BigInteger(privateKey, 10);
            BigInteger maxPrivKeyValue = new BigInteger(
                    "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141", 16);
            return (privKeyBig.compareTo(maxPrivKeyValue) <= 0);
        } catch (Exception e) {
            return false;
        }
    }

    /**
     * check the dID is match the private key.
     *
     * @param privateKey the private key
     * @param dID the dID
     * @return true if match, false mismatch
     */
    public static boolean validatePrivateKeyDIDMatches(DIDPrivateKey privateKey, String dID) {
        boolean isMatch = false;

        try {
            BigInteger publicKey = DataToolUtils
                    .publicKeyFromPrivate(new BigInteger(privateKey.getPrivateKey()));
            String address1 = "0x" + Keys.getAddress(publicKey);
            String address2 = DIDUtils.convertDIDToAddress(dID);
            if (address1.equals(address2)) {
                isMatch = true;
            }
        } catch (Exception e) {
            logger.error("Validate private key We Id matches failed. Error message :" + e);
            return isMatch;
        }

        return isMatch;
    }
}