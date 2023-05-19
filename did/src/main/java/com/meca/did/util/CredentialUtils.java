package com.meca.did.util;

import com.meca.did.constant.CredentialConstant;
import com.meca.did.constant.DIDConstant;

import java.util.regex.Pattern;

public class CredentialUtils {

    /**
     * Check whether the given String is a valid UUID.
     *
     * @param id the Credential id
     * @return true if yes, false otherwise
     */
    public static boolean isValidUuid(String id) {
        Pattern p = Pattern.compile(DIDConstant.UUID_PATTERN);
        return p.matcher(id).matches();
    }

    /**
     * Get default Credential Context String.
     *
     * @return Context value in String.
     */
    public static String getDefaultCredentialContext() {
        return CredentialConstant.DEFAULT_CREDENTIAL_CONTEXT;
    }
}
