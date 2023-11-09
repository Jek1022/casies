importcom.nimbusds.jose.*;

importcom.nimbusds.jose.crypto.RSASSASigner;
importjavax.crypto.Cipher;
importjavax.crypto.SecretKey;
importjavax.crypto.spec.IvParameterSpec;
importjavax.crypto.spec.SecretKeySpec;
importjava.security.KeyFactory;
importjava.security.interfaces.RSAPrivateKey;
importjava.security.spec.PKCS8EncodedKeySpec;
importjava.util.Base64;

public class JWS {

    public String generate(String id, String privateKey, String data) throws Exception {

        JWSHeader jwsHeader = newJWSHeader.Builder(JWSAlgorithm.RS256).keyID(id).build();
        Payload payload = newPayload(data);
        JWSObject jwsObject = newJWSObject(jwsHeader, payload);
        byte[] decodePrivateKey = Base64.getDecoder().decode(privateKey);
        RSAPrivateKey rsaPrivateKey = (RSAPrivateKey)KeyFactory.getInstance("RSA").generatePrivate(
            new PKCS8EncodedKeySpec(decodePrivateKey)
        );
        JWSSigner signer = newRSASSASigner(rsaPrivateKey);
        jwsObject.sign(signer);

        return jwsObject.serialize();

    }

 

    public String encrypt(StringsessionSecretKey, String jws) throws Exception {

        byte[] rawSecretKey = sessionSecretKey.getBytes();
        SecretKey secretKey = newSecretKeySpec(rawSecretKey, "AES");
        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, secretKey,
            new IvParameterSpec(sessionSecretKey.substring(0,16).getBytes())
        );
        byte[] encrypted = cipher.doFinal(jws.getBytes("UTF-8"));

        return Base64.getEncoder().encodeToString(encrypted);
    }

}