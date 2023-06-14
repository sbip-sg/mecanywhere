package com.meca.did.protocol.base;

import com.meca.did.util.DataToolUtils;
import com.meca.did.exception.DataTypeCastException;
import com.meca.did.protocol.inf.JsonSerializer;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;

@Data
@EqualsAndHashCode(callSuper = true)
public class DIDDocument extends DIDBaseInfo implements JsonSerializer {

    private static final Logger logger = LoggerFactory.getLogger(DIDDocument.class);

    /**
     *  the serialVersionUID.
     */
    private static final long serialVersionUID = 411522771907189878L;

    /**
     * Required: The updated.
     */
    private Long updated;

    /**
     * Required: The public key list.
     */
    private List<PublicKeyProperty> publicKey = new ArrayList<>();

    /**
     * Required: The authentication list.
     */
    private List<AuthenticationProperty> authentication = new ArrayList<>();

    /**
     * Required: The service list.
     */
    private List<ServiceProperty> service = new ArrayList<>();

    @Override
    public String toJson() {
        return DataToolUtils.addTagFromToJson(DataToolUtils.serialize(this));
    }

    /**
     * create DIDDocument with JSON String.
     * @param DIDDocumentJson the DIDDocument JSON String
     * @return DIDDocument
     */
    public static DIDDocument fromJson(String DIDDocumentJson) throws DataTypeCastException {
        if (StringUtils.isBlank(DIDDocumentJson)) {
            logger.error("create DIDDocument with JSON String failed, "
                    + "the DIDDocument JSON String is null");
            throw new DataTypeCastException("the DIDDocument JSON String is null.");
        }
        String didDocumentString = DIDDocumentJson;
        if (DataToolUtils.isValidFromToJson(DIDDocumentJson)) {
            didDocumentString = DataToolUtils.removeTagFromToJson(DIDDocumentJson);
        }
        return DataToolUtils.deserialize(didDocumentString, DIDDocument.class);
    }
}
