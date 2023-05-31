package com.meca.did.command;

import com.meca.did.util.DataToolUtils;

public class EncryptCommand {
    public static void main(String[] args) throws Exception {
        String data = "Test data";
        String publicKey = "10602037121808842313668323030516760731382935999091919099994486542091530276379890028012616862347706348958138289944509535670170838575215973441081046279498783";
        String privateKey = "109749059563353407780004371376912062700691932434018017772536499834726837571867";

        System.out.println("Data: " + data);

        byte[] encrypted = DataToolUtils.encrypt(data, publicKey);
        System.out.println("Encrypted: " + encrypted);

        byte[] decrypted = DataToolUtils.decrypt(encrypted, privateKey);
        System.out.println("Decrypted: " + new String(decrypted));
    }
}
