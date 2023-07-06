package com.meca.did.util;

import com.meca.did.constant.*;
import com.meca.did.exception.DataTypeCastException;
import com.meca.did.protocol.base.DIDDocument;
import com.meca.did.protocol.base.PublicKeyProperty;
import com.meca.did.protocol.request.CptMapArgs;
import com.meca.did.protocol.response.RsvSignature;
import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.PropertyAccessor;
import com.fasterxml.jackson.core.JsonGenerationException;
import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.*;
import com.fasterxml.jackson.databind.json.JsonMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.fasterxml.jackson.databind.type.TypeFactory;
import com.github.fge.jackson.JsonLoader;
import com.github.fge.jsonschema.core.report.ProcessingMessage;
import com.github.fge.jsonschema.core.report.ProcessingReport;
import com.github.fge.jsonschema.main.JsonSchema;
import com.github.fge.jsonschema.main.JsonSchemaFactory;
import org.apache.commons.lang3.RandomStringUtils;
import org.apache.commons.lang3.StringUtils;
import org.apache.commons.lang3.math.NumberUtils;
import org.bouncycastle.crypto.params.ECDomainParameters;
import org.bouncycastle.crypto.params.ECPublicKeyParameters;
import org.bouncycastle.jcajce.provider.asymmetric.ec.BCECPrivateKey;
import org.bouncycastle.jcajce.provider.asymmetric.ec.BCECPublicKey;
import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.bouncycastle.math.ec.custom.sec.SecP256K1Curve;
import org.bouncycastle.math.ec.custom.sec.SecP256K1Point;
import org.bouncycastle.util.encoders.Base64;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.web3j.abi.datatypes.generated.Bytes32;
import org.web3j.abi.datatypes.generated.Uint8;
import org.web3j.crypto.ECKeyPair;
import org.web3j.crypto.Hash;
import org.web3j.crypto.Sign;
import org.web3j.crypto.Sign.SignatureData;
import org.web3j.utils.Numeric;

import javax.crypto.Cipher;
import java.io.*;
import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.security.Security;
import java.security.spec.ECPrivateKeySpec;
import java.util.*;

public class DataToolUtils {
    private static final Logger logger = LoggerFactory.getLogger(DataToolUtils.class);

    private static final String SEPARATOR_CHAR = "-";
    //private static ObjectMapper objectMapper = new ObjectMapper();

    /**
     * default salt length.
     */
    private static final String DEFAULT_SALT_LENGTH = "5";

    private static final int SERIALIZED_SIGNATUREDATA_LENGTH = 65;

    private static final int radix = 10;

    private static final String TO_JSON = "toJson";

    private static final String FROM_JSON = "fromJson";

    private static final String KEY_CREATED = "created";

    private static final String KEY_ISSUANCEDATE = "issuanceDate";

    private static final String KEY_EXPIRATIONDATE = "expirationDate";

    private static final String KEY_CLAIM = "claim";

    private static final String KEY_FROM_TOJSON = "$from";

    private static final List<String> CONVERT_UTC_LONG_KEYLIST = new ArrayList<>();

    private static final ObjectMapper OBJECT_MAPPER;

    //private static final ObjectWriter OBJECT_WRITER;
    //private static final ObjectReader OBJECT_READER;
    private static final ObjectWriter OBJECT_WRITER_UN_PRETTY_PRINTER;

    static {
        OBJECT_MAPPER = JsonMapper.builder()
            // sort by letter
            .configure(MapperFeature.SORT_PROPERTIES_ALPHABETICALLY, true)
            // when map is serialization, sort by key
            .configure(SerializationFeature.ORDER_MAP_ENTRIES_BY_KEYS, true)
            // ignore mismatched fields
            .configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false)
            .enable(DeserializationFeature.ACCEPT_SINGLE_VALUE_AS_ARRAY)
            // use field for serialize and deSerialize
            .visibility(PropertyAccessor.SETTER, JsonAutoDetect.Visibility.NONE)
            .visibility(PropertyAccessor.GETTER, JsonAutoDetect.Visibility.NONE)
            .visibility(PropertyAccessor.FIELD, JsonAutoDetect.Visibility.ANY)
            .build();

        OBJECT_WRITER_UN_PRETTY_PRINTER = OBJECT_MAPPER.writer();

        CONVERT_UTC_LONG_KEYLIST.add(KEY_CREATED);
        CONVERT_UTC_LONG_KEYLIST.add(KEY_ISSUANCEDATE);
        CONVERT_UTC_LONG_KEYLIST.add(KEY_EXPIRATIONDATE);

        //OBJECT_WRITER = OBJECT_MAPPER.writer().withDefaultPrettyPrinter();
        //OBJECT_READER = OBJECT_MAPPER.reader();
        // if provider is not present, add it

        if (Security.getProvider(BouncyCastleProvider.PROVIDER_NAME) == null) {
            // insert at specific position
            Security.insertProviderAt(new BouncyCastleProvider(), 1);
        }
    }

    /**
     * add tag which the json string is converted by toJson().
     *
     * @param json jsonString
     * @return result
     */
    public static String addTagFromToJson(String json) {
        JsonNode jsonObject;
        try {
            jsonObject = loadJsonObject(json);
            if (!jsonObject.has(KEY_FROM_TOJSON)) {
                ((ObjectNode) jsonObject).put(KEY_FROM_TOJSON, TO_JSON);
            }
        } catch (IOException e) {
            logger.error("addTagFromToJson fail." + e);
            return json;
        }
        return jsonObject.toString();
    }

    /**
     * remove tag which the json string is converted by toJson().
     *
     * @param json jsonString
     * @return result
     */
    public static String removeTagFromToJson(String json) {
        JsonNode jsonObject;
        try {
            jsonObject = loadJsonObject(json);
            if (jsonObject.has(KEY_FROM_TOJSON)) {
                ((ObjectNode) jsonObject).remove(KEY_FROM_TOJSON);
            }
        } catch (IOException e) {
            logger.error("removeTag fail." + e);
            return json;
        }
        return jsonObject.toString();
    }

    /**
     * Load Json Object. Can be used to return both Json Data and Json Schema.
     *
     * @param jsonString the json string
     * @return JsonNode
     * @throws IOException Signals that an I/O exception has occurred.
     */
    public static JsonNode loadJsonObject(String jsonString) throws IOException {
        return JsonLoader.fromString(jsonString);
    }

    /**
     * valid the json string is converted by toJson().
     *
     * @param json jsonString
     * @return result
     */
    public static boolean isValidFromToJson(String json) {
        if (StringUtils.isBlank(json)) {
            logger.error("input json param is null.");
            return false;
        }
        JsonNode jsonObject = null;
        try {
            jsonObject = loadJsonObject(json);
        } catch (IOException e) {
            logger.error("convert jsonString to JSONObject failed." + e);
            return false;
        }
        return jsonObject.has(KEY_FROM_TOJSON);
    }

    /**
     * serialize a class instance to Json String.
     *
     * @param object the class instance to serialize
     * @param <T>    the type of the element
     * @return JSON String
     */
    public static <T> String serialize(T object) {
        Writer write = new StringWriter();
        try {
            OBJECT_MAPPER.writeValue(write, object);
        } catch (JsonGenerationException e) {
            logger.error("JsonGenerationException when serialize object to json", e);
        } catch (JsonMappingException e) {
            logger.error("JsonMappingException when serialize object to json", e);
        } catch (IOException e) {
            logger.error("IOException when serialize object to json", e);
        }
        return write.toString();
    }

    /**
     * deserialize a JSON String to an class instance.
     *
     * @param json  json string
     * @param clazz Class.class
     * @param <T>   the type of the element
     * @return class instance
     */
    public static <T> T deserialize(String json, Class<T> clazz) throws DataTypeCastException {
        Object object = null;
        try {
            if (isValidFromToJson(json)) {
                logger.error("this jsonString is converted by toJson(), "
                        + "please use fromJson() to deserialize it");
                throw new DataTypeCastException("deserialize json to Object error");
            }
            object = OBJECT_MAPPER.readValue(json, TypeFactory.rawClass(clazz));
        } catch (JsonParseException e) {
            logger.error("JsonParseException when deserialize json to object", e);
            throw new DataTypeCastException(e);
        } catch (JsonMappingException e) {
            logger.error("JsonMappingException when deserialize json to object", e);
            throw new DataTypeCastException(e);
        } catch (IOException e) {
            logger.error("IOException when deserialize json to object", e);
            throw new DataTypeCastException(e);
        }
        return (T) object;
    }

    /**
     * Checks if is valid base 64 string.
     *
     * @param string the string
     * @return true, if is valid base 64 string
     */
    public static boolean isValidBase64String(String string) {
        return org.apache.commons.codec.binary.Base64.isBase64(string);
    }

    /**
     * Convert a POJO to Map.
     *
     * @param object POJO
     * @return Map
     * @throws Exception IOException
     */
    public static Map<String, Object> objToMap(Object object) throws Exception {
        JsonNode jsonNode = OBJECT_MAPPER.readTree(serialize(object));
        return (HashMap<String, Object>) OBJECT_MAPPER.convertValue(jsonNode, HashMap.class);
    }

    /**
     * Convert a MAP to POJO.
     *
     * @param map   the input data
     * @param <T>   the type of the element
     * @param clazz the output class type
     * @return object in T type
     * @throws Exception IOException
     */
    public static <T> T mapToObj(Map<String, Object> map, Class<T> clazz) throws Exception {
        final T pojo = (T) OBJECT_MAPPER.convertValue(map, clazz);
        return pojo;
    }

    /**
     * convert UTC Date to timestamp of Json string.
     *
     * @param jsonString presentationJson
     * @return presentationJson after convert
     */
    public static String convertUtcToTimestamp(String jsonString) throws DataTypeCastException {
        String utcToTimestampString;
        try {
            utcToTimestampString = dealNodeOfConvertUtcAndLong(
                    loadJsonObject(jsonString),
                    CONVERT_UTC_LONG_KEYLIST,
                    FROM_JSON
            ).toString();
        } catch (IOException e) {
            logger.error("replaceJsonObj exception.", e);
            throw new DataTypeCastException(e);
        }
        return utcToTimestampString;
    }

    private static JsonNode dealNodeOfConvertUtcAndLong(
            JsonNode jsonObj,
            List<String> list,
            String type) {
        if (jsonObj.isObject()) {
            return dealObjectOfConvertUtcAndLong((ObjectNode) jsonObj, list, type);
        } else if (jsonObj.isArray()) {
            return dealArrayOfConvertUtcAndLong((ArrayNode) jsonObj, list, type);
        } else {
            return jsonObj;
        }
    }

    private static JsonNode dealObjectOfConvertUtcAndLong(
            ObjectNode jsonObj,
            List<String> list,
            String type) {
        ObjectNode resJson = OBJECT_MAPPER.createObjectNode();
        jsonObj.fields().forEachRemaining(entry -> {
            String key = entry.getKey();
            JsonNode obj = entry.getValue();
            if (obj.isObject()) {
                //JSONObject
                if (key.equals(KEY_CLAIM)) {
                    resJson.set(key, obj);
                } else {
                    resJson.set(key, dealObjectOfConvertUtcAndLong((ObjectNode) obj, list, type));
                }
            } else if (obj.isArray()) {
                //JSONArray
                resJson.set(key, dealArrayOfConvertUtcAndLong((ArrayNode) obj, list, type));
            } else {
                if (list.contains(key)) {
                    if (TO_JSON.equals(type)) {
                        if (isValidLongString(obj.asText())) {
                            resJson.put(
                                    key,
                                    DateUtils.convertNoMillisecondTimestampToUtc(
                                            Long.parseLong(obj.asText())));
                        } else {
                            resJson.set(key, obj);
                        }
                    } else {
                        if (DateUtils.isValidDateString(obj.asText())) {
                            resJson.put(
                                    key,
                                    DateUtils.convertUtcDateToNoMillisecondTime(obj.asText()));
                        } else {
                            resJson.set(key, obj);
                        }
                    }
                } else {
                    resJson.set(key, obj);
                }
            }
        });
        return resJson;
    }

    private static JsonNode dealArrayOfConvertUtcAndLong(
            ArrayNode jsonArr,
            List<String> list,
            String type) {
        ArrayNode resJson = OBJECT_MAPPER.createArrayNode();
        for (int i = 0; i < jsonArr.size(); i++) {
            JsonNode jsonObj = jsonArr.get(i);
            if (jsonObj.isObject()) {
                resJson.add(dealObjectOfConvertUtcAndLong((ObjectNode) jsonObj, list, type));
            } else if (jsonObj.isArray()) {
                resJson.add(dealArrayOfConvertUtcAndLong((ArrayNode) jsonObj, list, type));
            } else {
                resJson.add(jsonObj);
            }
        }
        return resJson;
    }

    /**
     * valid string is a long type.
     *
     * @param str string
     * @return result
     */
    public static boolean isValidLongString(String str) {
        if (StringUtils.isBlank(str)) {
            return false;
        }

        long result = 0;
        int i = 0;
        int len = str.length();
        long limit = -Long.MAX_VALUE;
        long multmin;
        int digit;

        char firstChar = str.charAt(0);
        if (firstChar <= '0') {
            return false;
        }
        multmin = limit / radix;
        while (i < len) {
            digit = Character.digit(str.charAt(i++), radix);
            if (digit < 0) {
                return false;
            }
            if (result < multmin) {
                return false;
            }
            result *= radix;
            if (result < limit + digit) {
                return false;
            }
            result -= digit;
        }
        return true;
    }

    /**
     * convert timestamp to UTC of json string.
     *
     * @param jsonString json string
     * @return timestampToUtcString
     */
    public static String convertTimestampToUtc(String jsonString) throws DataTypeCastException {
        String timestampToUtcString;
        try {
            timestampToUtcString = dealNodeOfConvertUtcAndLong(
                    loadJsonObject(jsonString),
                    CONVERT_UTC_LONG_KEYLIST,
                    TO_JSON
            ).toString();
        } catch (IOException e) {
            logger.error("replaceJsonObj exception.", e);
            throw new DataTypeCastException(e);
        }
        return timestampToUtcString;
    }

    /**
     * Convert a Map to compact Json output, with keys ordered. Use Jackson JsonNode toString() to
     * ensure key order and compact output.
     *
     * @param map input map
     * @return JsonString
     * @throws Exception IOException
     */
    public static String mapToCompactJson(Map<String, Object> map) throws Exception {
        return OBJECT_MAPPER.readTree(serialize(map)).toString();
    }

    /**
     * Keccak-256 hash function.
     *
     * @param utfString the utfString
     * @return hash value as hex encoded string
     */
    public static String sha3(String utfString) {
        return Numeric.toHexString(sha3(utfString.getBytes(StandardCharsets.UTF_8)));
    }

    /**
     * Sha 3.
     *
     * @param input the input
     * @return the byte[]
     */
    public static byte[] sha3(byte[] input) {
        return Hash.sha3(input, 0, input.length);
    }

    /**
     * 对象深度复制(对象必须是实现了Serializable接口).
     *
     * @param obj pojo
     * @param <T> the type of the element
     * @return Object clonedObj
     */
    @SuppressWarnings("unchecked")
    public static <T extends Serializable> T clone(T obj) {
        T clonedObj = null;
        try {
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            ObjectOutputStream oos = new ObjectOutputStream(baos);
            oos.writeObject(obj);
            oos.close();

            ByteArrayInputStream bais = new ByteArrayInputStream(baos.toByteArray());
            ObjectInputStream ois = new ObjectInputStream(bais);
            clonedObj = (T) ois.readObject();
            ois.close();
        } catch (Exception e) {
            logger.error("clone object has error.", e);
        }
        return clonedObj;
    }

    /**
     * Secp256k1 sign.
     *
     * @param rawData    original raw data
     * @param privateKey private key in BigInteger format
     * @return base64 string for signature value
     */
    public static String secp256k1Sign(String rawData, BigInteger privateKey) {
        Sign.SignatureData sigData = secp256k1SignToSignature(rawData, privateKey);
        return secp256k1SigBase64Serialization(sigData);
    }


    /**
     * Secp256k1 sign to Signature.
     *
     * @param rawData    original raw data
     * @param privateKey private key in BigInteger format
     * @return SignatureData for signature value
     */
    public static SignatureData secp256k1SignToSignature(String rawData, BigInteger privateKey) {
        //TODO might cause a bug
        ECKeyPair keyPair = ECKeyPair.create(privateKey);
        return secp256k1SignToSignature(rawData, keyPair);
    }

    /**
     * Secp256k1 sign to Signature.
     *
     * @param rawData original raw data
     * @param keyPair keyPair
     * @return SignatureData for signature value
     */
    public static Sign.SignatureData secp256k1SignToSignature(String rawData, ECKeyPair keyPair) {
        return Sign.signMessage(rawData.getBytes(), keyPair);
    }

    /**
     * Serialize secp256k1 signature into base64 encoded, in R, S, V (0, 1) format.
     *
     * @param sigData secp256k1 signature (v = 0,1)
     * @return base64 string
     */
    public static String secp256k1SigBase64Serialization(
            Sign.SignatureData sigData) {
        byte[] sigBytes = new byte[65];
        sigBytes[64] = sigData.getV()[0];
        System.arraycopy(sigData.getR(), 0, sigBytes, 0, 32);
        System.arraycopy(sigData.getS(), 0, sigBytes, 32, 32);
        return new String(base64Encode(sigBytes), StandardCharsets.UTF_8);
    }

    /**
     * Base 64 encode.
     *
     * @param nonBase64Bytes the non base 64 bytes
     * @return the byte[]
     */
    public static byte[] base64Encode(byte[] nonBase64Bytes) {
        return Base64.encode(nonBase64Bytes);
    }


    /**
     * generate random string.
     *
     * @return random string
     */
    public static String getRandomSalt() {

        String length = DEFAULT_SALT_LENGTH;
        int saltLength = Integer.valueOf(length);
        String salt = RandomStringUtils.random(saltLength, true, true);
        return salt;
    }

    /**
     * Object to Json String.
     *
     * @param obj Object
     * @return String
     */
    public static String objToJsonStrWithNoPretty(Object obj) throws DataTypeCastException {

        try {
            return OBJECT_WRITER_UN_PRETTY_PRINTER.writeValueAsString(obj);
        } catch (JsonProcessingException e) {
            throw new DataTypeCastException(e);
        }
    }

    /**
     * Verify a secp256k1 signature (base64).
     *
     * @param rawData        the rawData to be verified
     * @param signature      the Signature Data in secp256k1 style
     * @param DIDDocument    the DIDDocument to be extracted
     * @param DIDPublicKeyId the DID public key ID
     * @return true if yes, false otherwise with exact error codes
     */
    public static ErrorCode verifySecp256k1SignatureFromDID(
            String rawData,
            String signature,
            DIDDocument DIDDocument,
            String DIDPublicKeyId) {
        List<String> publicKeysListToVerify = new ArrayList<String>();

        try {
            secp256k1SigBase64Deserialization(signature);
        } catch (Exception e) {
            logger.error(e.getMessage());
            return ErrorCode.CREDENTIAL_SIGNATURE_BROKEN;
        }

        // Traverse public key list indexed Authentication key list

        for (PublicKeyProperty publicKeyProperty : DIDDocument.getPublicKey()) {
            if (publicKeyProperty.getRevoked()) {
                continue;
            }
            publicKeysListToVerify.add(publicKeyProperty.getPublicKey());
        }
        String foundMatchingPubKeyId = StringUtils.EMPTY;
        try {
            boolean result = false;
            for (String publicKeyItem : publicKeysListToVerify) {
                if (StringUtils.isNotEmpty(publicKeyItem)) {
                    boolean currentResult = verifySecp256k1Signature(
                            rawData, signature, new BigInteger(publicKeyItem));
                    result = currentResult || result;
                    if (currentResult) {
                        for (PublicKeyProperty pkp : DIDDocument.getPublicKey()) {
                            if (pkp.getRevoked()) {
                                continue;
                            }
                            if (pkp.getPublicKey().equalsIgnoreCase(publicKeyItem)) {
                                foundMatchingPubKeyId = pkp.getId();
                            }
                        }
                        break;
                    }
                }
            }
            if (!result) {
                return ErrorCode.CREDENTIAL_VERIFY_FAIL;
            }
        } catch (Exception e) {
            logger.error("some exceptions occurred in signature verification", e);
            return ErrorCode.CREDENTIAL_EXCEPTION_VERIFYSIGNATURE;
        }
        if (NumberUtils.isDigits(DIDPublicKeyId)) {
            DIDPublicKeyId = DIDDocument.getId() + "#keys-" + Integer.valueOf(DIDPublicKeyId);
        }
        if (!StringUtils.isEmpty(DIDPublicKeyId)
                && !foundMatchingPubKeyId.equalsIgnoreCase(DIDPublicKeyId)) {
            return ErrorCode.CREDENTIAL_VERIFY_SUCCEEDED_WITH_WRONG_PUBLIC_KEY_ID;
        }
        return ErrorCode.SUCCESS;
    }

    /**
     * De-Serialize secp256k1 signature base64 encoded string, in R, S, V (0, 1) format.
     *
     * @param signature signature base64 string
     * @return secp256k1 signature (v = 0,1)
     */
    public static Sign.SignatureData secp256k1SigBase64Deserialization(String signature) {
        byte[] sigBytes = base64Decode(signature.getBytes(StandardCharsets.UTF_8));
        byte[] r = new byte[32];
        byte[] s = new byte[32];
        System.arraycopy(sigBytes, 0, r, 0, 32);
        System.arraycopy(sigBytes, 32, s, 0, 32);
        byte v;
        if (sigBytes.length == 65) {
            v = sigBytes[64];
        } else if (sigBytes.length == 64) {
            v = 28;
        } else {
            throw new RuntimeException("Invalid signature length");
        }
        return new Sign.SignatureData(v, r, s);
    }

    /**
     * De-Serialize secp256k1 signature base64 encoded string, in R, S, V (0, 1) format.
     *
     * @param signature signature base64 string
     * @param publicKey publicKey
     * @return secp256k1 signature (v = 0,1)
     */
    public static Sign.SignatureData secp256k1SigBase64Deserialization(
            String signature,
            BigInteger publicKey) {
        byte[] sigBytes = base64Decode(signature.getBytes(StandardCharsets.UTF_8));
        byte[] r = new byte[32];
        byte[] s = new byte[32];
        System.arraycopy(sigBytes, 0, r, 0, 32);
        System.arraycopy(sigBytes, 32, s, 0, 32);

//        might cuase a bug
        return new Sign.SignatureData(sigBytes[64], r, s);
    }

    /**
     * The Base64 encode/decode class.
     *
     * @param base64Bytes the base 64 bytes
     * @return the byte[]
     */
    public static byte[] base64Decode(byte[] base64Bytes) {
        return Base64.decode(base64Bytes);
    }

    /**
     * Verify secp256k1 signature.
     *
     * @param rawData         original raw data
     * @param signatureBase64 signature base64 string
     * @param publicKey       in BigInteger format
     * @return return boolean result, true is success and false is fail
     */
    public static boolean verifySecp256k1Signature(
            String rawData,
            String signatureBase64,
            BigInteger publicKey
    ) {
        try {
            if (rawData == null) {
                return false;
            }
            Sign.SignatureData sigData =
                    secp256k1SigBase64Deserialization(signatureBase64);
            byte[] hashBytes = Hash.sha3(rawData.getBytes(StandardCharsets.UTF_8));
            BigInteger k = Sign.signedMessageHashToKey(hashBytes, sigData);
            logger.info(String.valueOf(publicKey.equals(k)));
            return publicKey.equals(k);
        } catch (Exception e) {
            logger.error("Error occurred during secp256k1 sig verification: {}", e);
            return false;
        }
    }

    /**
     * string to byte.
     *
     * @param value stringData
     * @return byte[]
     */
    public static byte[] stringToByteArray(String value) {
        if (StringUtils.isBlank(value)) {
            return new byte[1];
        }
        return value.getBytes(StandardCharsets.UTF_8);
    }

    /**
     * string to byte32.
     *
     * @param value stringData
     * @return byte[]
     */
    public static byte[] stringToByte32Array(String value) {
        if (StringUtils.isBlank(value)) {
            return new byte[32];
        }

        byte[] bytes = value.getBytes(StandardCharsets.UTF_8);
        byte[] newBytes = new byte[32];

        System.arraycopy(bytes, 0, newBytes, 0, bytes.length);
        return newBytes;
    }

    /**
     * Obtain the PublicKey from given PrivateKey.
     *
     * @param privateKey the private key
     * @return publicKey
     */
    public static BigInteger publicKeyFromPrivate(BigInteger privateKey) {
        return Sign.publicKeyFromPrivate(privateKey);
    }

    /**
     * Obtain the public keypair from given PrivateKey.
     *
     * @param privateKey the private key
     * @return public keypair
     */
    public static ECKeyPair createKeyPairFromPrivate(BigInteger privateKey) {
        try {
            ECKeyPair keyPair = ECKeyPair.create(privateKey);
            return keyPair;
        } catch (Exception e) {
            logger.error("create keypair of ECDSA failed, error msg:" + e.getMessage());
            return null;
        }
    }

    /**
     * Get the UUID and remove the '-'.
     *
     * @return return the UUID of the length is 32
     */
    public static String getUuId32() {
        return UUID.randomUUID().toString().replaceAll(SEPARATOR_CHAR, StringUtils.EMPTY);
    }

    /**
     * eecrypt the data.
     *
     * @param data the data to encrypt
     * @param publicKey public key
     * @return decrypt data
     * @throws Exception encrypt exception
     */
    public static byte[] encrypt(String data, String publicKey)
            throws Exception {
        // Encrypt data.
        Cipher cipher = Cipher.getInstance("ECIES", "BC");
        cipher.init(Cipher.ENCRYPT_MODE, createBCECPublicKey(new BigInteger(publicKey)), ECCParams.IES_PARAMS);
//        cipher.init(Cipher.ENCRYPT_MODE, createBCECPublicKey(new BigInteger(publicKey)), new IESParameterSpec(null, null, 64));

        return cipher.doFinal(data.getBytes());
    }


    /**
     * decrypt the data.
     *
     * @param data the data to decrypt
     * @param privateKey private key
     * @return original data
     * @throws Exception decrypt exception
     */
    public static byte[] decrypt(byte[] data, String privateKey) throws Exception {

        Cipher cipher = Cipher.getInstance("ECIES", "BC");
        cipher.init(Cipher.DECRYPT_MODE, createBCECPrivateKey(new BigInteger(privateKey)), ECCParams.IES_PARAMS);

        return cipher.doFinal(data);
    }

    private static BCECPublicKey createBCECPublicKey(BigInteger publicKey) {
        // Handle public key.
//        might need to change size to constant/config file
        String publicKeyValue =
                Numeric.toHexStringNoPrefixZeroPadded(publicKey, 64 << 1);
        String prePublicKeyStr = publicKeyValue.substring(0, 64);
        String postPublicKeyStr = publicKeyValue.substring(64);
        SecP256K1Curve secP256K1Curve = new SecP256K1Curve();
        SecP256K1Point secP256K1Point =
                (SecP256K1Point)
                        secP256K1Curve.createPoint(
                                new BigInteger(prePublicKeyStr, 16),
                                new BigInteger(postPublicKeyStr, 16));
        SecP256K1Point secP256K1PointG =
                (SecP256K1Point)
                        secP256K1Curve.createPoint(ECCParams.POINTG_PRE, ECCParams.POINTG_POST);

        ECDomainParameters domainParameters =
                new ECDomainParameters(secP256K1Curve, secP256K1PointG, ECCParams.FACTOR_N);
        ECPublicKeyParameters publicKeyParameters =
                new ECPublicKeyParameters(secP256K1Point, domainParameters);

        BCECPublicKey bcecPublicKey =
                new BCECPublicKey(
                        "ECDSA",
                        publicKeyParameters,
                        ECCParams.ecNamedCurveSpec,
                        BouncyCastleProvider.CONFIGURATION);

        return bcecPublicKey;
    }

    /**
     * create BCECPrivateKey from privateKey
     *
     * @param privateKey
     * @return
     */
    private static BCECPrivateKey createBCECPrivateKey(BigInteger privateKey) {
        // Handle secret key
        ECPrivateKeySpec secretKeySpec =
                new ECPrivateKeySpec(privateKey, ECCParams.ecNamedCurveSpec);
        BCECPrivateKey bcecPrivateKey =
                new BCECPrivateKey("ECDSA", secretKeySpec, BouncyCastleProvider.CONFIGURATION);
        return bcecPrivateKey;
    }

    /**
     * verify public key format
     *
     * @param publicKey the public key in string format
     * @return return whether the format is correct
     */
    public static ErrorCode verifyPublicKeyFormat(String publicKey) {
        byte[] bytes = new BigInteger(publicKey).toByteArray();
        if (StringUtils.isBlank(publicKey)) {
            return ErrorCode.ILLEGAL_INPUT;
        } else if (bytes.length < 64) {
            return ErrorCode.DID_PUBLIC_KEY_LENGTH_INVALID;
        } else if (bytes.length >= 65) {
            if (bytes.length == 65) {
                if (bytes[0] == 0x04) {
                    return ErrorCode.DID_PUBLIC_KEY_PREFIX_INVALID;
                } else if (bytes[0] == 0x00) {
                    // it is still ok, if the length is 65 and the first byte is 0x00
                    return ErrorCode.SUCCESS;
                }
            }
            return ErrorCode.DID_PUBLIC_KEY_LENGTH_INVALID;
        }
        return ErrorCode.SUCCESS;
    }

    /**
     * validate Cpt Json Schema validity .
     *
     * @param cptJsonSchema the cpt json schema
     * @return true, if is cpt json schema valid
     * @throws IOException Signals that an I/O exception has occurred.
     */
    public static boolean isCptJsonSchemaValid(String cptJsonSchema) throws IOException {
        return StringUtils.isNotEmpty(cptJsonSchema)
                && isValidJsonSchema(cptJsonSchema)
                && cptJsonSchema.length() <= DIDConstant.JSON_SCHEMA_MAX_LENGTH;
    }

    /**
     * Validate Json Schema format validity.
     *
     * @param jsonSchema the json schema
     * @return true if yes, false otherwise
     * @throws IOException Signals that an I/O exception has occurred.
     */
    public static boolean isValidJsonSchema(String jsonSchema) throws IOException {
        return JsonSchemaFactory
                .byDefault()
                .getSyntaxValidator()
                .schemaIsValid(loadJsonObject(jsonSchema));
    }

    /**
     * create new cpt json schema.
     *
     * @param args Map
     * @return String
     */
    public static String cptSchemaToString(CptMapArgs args) {

        Map<String, Object> cptJsonSchema = args.getCptJsonSchema();
        Map<String, Object> cptJsonSchemaNew = new HashMap<String, Object>();
        cptJsonSchemaNew.put(JsonSchemaConstant.SCHEMA_KEY, JsonSchemaConstant.SCHEMA_VALUE);
        cptJsonSchemaNew.put(JsonSchemaConstant.TYPE_KEY, JsonSchemaConstant.DATA_TYPE_OBJECT);
        cptJsonSchemaNew.putAll(cptJsonSchema);
        String cptType = args.getCptType().getName();
        cptJsonSchemaNew.put(CredentialConstant.CPT_TYPE_KEY, cptType);
        return DataToolUtils.serialize(cptJsonSchemaNew);
    }

    /**
     * Convert SignatureData to blockchain-ready RSV format.
     *
     * @param signatureData the signature data
     * @return rsvSignature the rsv signature structure
     */
        public static RsvSignature convertSignatureDataToRsv(
                SignatureData signatureData) {
        Uint8 v = intToUnt8(signatureData.getV()[0]);
        Bytes32 r = bytesArrayToBytes32(signatureData.getR());
        Bytes32 s = bytesArrayToBytes32(signatureData.getS());
        RsvSignature rsvSignature = new RsvSignature();
        rsvSignature.setV(v);
        rsvSignature.setR(r);
        rsvSignature.setS(s);
        return rsvSignature;
    }

    /**
     * Int to unt 8.
     *
     * @param value the value
     * @return the uint 8
     */
    public static Uint8 intToUnt8(int value) {
        return new Uint8(value);
    }

    /**
     * Bytes array to bytes 32.
     *
     * @param byteValue the byte value
     * @return the bytes 32
     */
    public static Bytes32 bytesArrayToBytes32(byte[] byteValue) {

        byte[] byteValueLen32 = new byte[32];
        System.arraycopy(byteValue, 0, byteValueLen32, 0, byteValue.length);
        return new Bytes32(byteValueLen32);
    }


    /**
     * convert list to BigInteger list.
     *
     * @param list BigInteger list
     * @param size size
     * @return result
     */
    public static List<BigInteger> listToListBigInteger(List<BigInteger> list, int size) {
        List<BigInteger> bigIntegerList = new ArrayList<>();
        for (BigInteger bs : list) {
            bigIntegerList.add(bs);
        }

        List<BigInteger> addList = new ArrayList<>();
        if (bigIntegerList.size() < size) {
            for (int i = 0; i < size - bigIntegerList.size(); i++) {
                addList.add(BigInteger.ZERO);
            }
            bigIntegerList.addAll(addList);
        }
        return bigIntegerList;
    }

    /**
     * Get the current timestamp as the param "created". May be called elsewhere.
     *
     * @param length length
     * @return the StaticArray
     */
    public static List<BigInteger> getParamCreatedList(int length) {
        long created = DateUtils.getNoMillisecondTimeStamp();
        List<BigInteger> createdList = new ArrayList<>();
        createdList.add(BigInteger.ZERO);
        createdList.add(BigInteger.valueOf(created));
        return createdList;
    }


    /**
     * convert bytesArrayList to Bytes32ArrayList.
     *
     * @param list byte size
     * @param size size
     * @return result
     */
    public static List<byte[]> bytesArrayListToBytes32ArrayList(List<byte[]> list, int size) {

        List<byte[]> bytesList = new ArrayList<>();
        if (list.isEmpty()) {
            for (int i = 0; i < size; i++) {
                bytesList.add(new byte[32]);
            }
            return bytesList;
        }

        for (byte[] bytes : list) {
            if (bytes.length <= DIDConstant.MAX_AUTHORITY_ISSUER_NAME_LENGTH) {
                byte[] newBytes = new byte[32];
                System.arraycopy(bytes, 0, newBytes, 0, bytes.length);
                bytesList.add(newBytes);
            }
        }

        if (bytesList.size() < size) {
            List<byte[]> addList = new ArrayList<>();
            for (int i = 0; i < size - bytesList.size(); i++) {
                addList.add(new byte[32]);
            }
            bytesList.addAll(addList);
        }
        return bytesList;
    }

    /**
     * string to byte32List.
     *
     * @param data stringData
     * @param size size of byte32List
     * @return data
     */
    public static List<byte[]> stringToByte32ArrayList(String data, int size) {
        List<byte[]> byteList = new ArrayList<>();

        if (StringUtils.isBlank(data)) {
            for (int i = 0; i < size; i++) {
                byteList.add(new byte[32]);
            }
            return byteList;
        }

        byte[] dataBytes = data.getBytes(StandardCharsets.UTF_8);

        if (dataBytes.length <= DIDConstant.MAX_AUTHORITY_ISSUER_NAME_LENGTH) {
            byte[] newBytes = new byte[32];
            System.arraycopy(dataBytes, 0, newBytes, 0, dataBytes.length);
            byteList.add(newBytes);
        } else {
            byteList = splitBytes(dataBytes, size);
        }

        if (byteList.size() < size) {
            List<byte[]> addList = new ArrayList<>();
            for (int i = 0; i < size - byteList.size(); i++) {
                addList.add(new byte[32]);
            }
            byteList.addAll(addList);
        }
        return byteList;
    }

    private static synchronized List<byte[]> splitBytes(byte[] bytes, int size) {
        List<byte[]> byteList = new ArrayList<>();
        double splitLength =
                Double.parseDouble(DIDConstant.MAX_AUTHORITY_ISSUER_NAME_LENGTH + "");
        int arrayLength = (int) Math.ceil(bytes.length / splitLength);
        byte[] result = new byte[arrayLength];

        int from = 0;
        int to = 0;

        for (int i = 0; i < arrayLength; i++) {
            from = (int) (i * splitLength);
            to = (int) (from + splitLength);

            if (to > bytes.length) {
                to = bytes.length;
            }

            result = Arrays.copyOfRange(bytes, from, to);
            if (result.length < size) {
                byte[] newBytes = new byte[32];
                System.arraycopy(result, 0, newBytes, 0, result.length);
                byteList.add(newBytes);
            } else {
                byteList.add(result);
            }
        }
        return byteList;
    }

    /**
     * Validate Json Data versus Json Schema.
     *
     * @param jsonData the json data
     * @param jsonSchema the json schema
     * @return empty if yes, not empty otherwise
     * @throws Exception the exception
     */
    public static ProcessingReport checkJsonVersusSchema(String jsonData, String jsonSchema)
            throws Exception {
        JsonNode jsonDataNode = loadJsonObject(jsonData);
        JsonNode jsonSchemaNode = loadJsonObject(jsonSchema);
        JsonSchema schema = JsonSchemaFactory.byDefault().getJsonSchema(jsonSchemaNode);
        ProcessingReport report = schema.validate(jsonDataNode);
        if (report.isSuccess()) {
            logger.info(report.toString());
        } else {
            Iterator<ProcessingMessage> it = report.iterator();
            StringBuffer errorMsg = new StringBuffer();
            while (it.hasNext()) {
                errorMsg.append(it.next().getMessage());
            }
            logger.error("Json schema validator failed, error: {}", errorMsg.toString());
        }
        return report;
    }


    /**
     * convert byte32List to String.
     *
     * @param bytesList list
     * @param size size
     * @return reuslt
     */
    public static synchronized String byte32ListToString(List<byte[]> bytesList, int size) {
        if (bytesList.isEmpty()) {
            return "";
        }

        int zeroCount = 0;
        for (int i = 0; i < bytesList.size(); i++) {
            for (int j = 0; j < bytesList.get(i).length; j++) {
                if (bytesList.get(i)[j] == 0) {
                    zeroCount++;
                }
            }
        }

        if (DIDConstant.MAX_AUTHORITY_ISSUER_NAME_LENGTH * size - zeroCount == 0) {
            return "";
        }

        byte[] newByte = new byte[DIDConstant.MAX_AUTHORITY_ISSUER_NAME_LENGTH * size - zeroCount];
        int index = 0;
        for (int i = 0; i < bytesList.size(); i++) {
            for (int j = 0; j < bytesList.get(i).length; j++) {
                if (bytesList.get(i)[j] != 0) {
                    newByte[index] = bytesList.get(i)[j];
                    index++;
                }
            }
        }

        return (new String(newByte)).toString();
    }

    /**
     * The De-Serialization class of Signatures accepting raw values of v, r, and s. Note: due to
     * the non 1:1 mapping between default encoded Java String and Byte Array, all the parameters
     * derived from Byte Array should either be STILL IN Byte Array or Base-64.
     *
     * @param v the v
     * @param r the r
     * @param s the s
     * @return the sign. signature data
     */
    public static Sign.SignatureData rawSignatureDeserialization(int v, byte[] r, byte[] s) {
        byte valueByte = (byte) v;
        return new Sign.SignatureData(valueByte, r, s);
    }

    /**
     * The Serialization class of Signatures. This is simply a concatenation of bytes of the v, r,
     * and s. Ethereum uses a similar approach with a wrapping from Base64.
     * https://www.programcreek.com/java-api-examples/index.php?source_dir=redPandaj-master/src/org/redPandaLib/crypt/ECKey.java
     * uses a DER-formatted serialization, but it does not entail the v tag, henceforth is more
     * complex and computation hungry.
     *
     * @param signatureData the signature data
     * @return the byte[]
     */
    public static byte[] simpleSignatureSerialization(Sign.SignatureData signatureData) {
        byte[] serializedSignatureData = new byte[65];
        serializedSignatureData[0] = signatureData.getV()[0];
        System.arraycopy(signatureData.getR(), 0, serializedSignatureData, 1, 32);
        System.arraycopy(signatureData.getS(), 0, serializedSignatureData, 33, 32);
        return serializedSignatureData;
    }
}
