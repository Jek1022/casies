importjava.nio.charset.Charset;
importjava.text.SimpleDateFormat;
importjava.util.Base64;
importjava.util.Date;
importjava.util.HashMap;
importjava.util.Map;
importjavax.crypto.Cipher;
importjavax.crypto.Mac;
importjavax.crypto.SecretKey;
importjavax.crypto.spec.IvParameterSpec;
importjavax.crypto.spec.SecretKeySpec;
importorg.apache.http.HttpResponse;
importorg.apache.http.client.HttpClient;
importorg.apache.http.client.methods.HttpPost;
importorg.apache.http.entity.ContentType;
importorg.apache.http.entity.StringEntity;
importorg.apache.http.impl.client.HttpClients;
importcom.fasterxml.jackson.databind.ObjectMapper;
importlombok.Getter;
importlombok.Setter;
importlombok.ToString;

public class Invoice {

   String HMAC_SHA_256 = "HmacSHA256";
   String secretKey = "#Go(YD3aiML3tTCGArQtFd(e$691c%jk"; // Sample Secret Key

   public void execute() throws Exception{

      // API Call
      HttpResponse response =this.send();

      // Get Response
      Entity entity = this.response(response);
      if (entity.getData() != null){
         String data = this.decodeData(entity);       
      }
   }

      public HttpResponse send() throws Exception {

         String url ="http://SAMPLE_URL/api/invoices";
         String accreditationId ="20111111"; // Sample Accreditation ID (EIS Cert Number)
         String applicationId ="AAAAAAAA"; // Sample Application ID

         // Sample Authentication Token
         String authToken ="ANGKWMVLS4PLGE6GVV0KLRF14XH2F6BM";

         // Sample EIS Key-pair private key
         String jwsKey = "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC41fMeXOjW6WZoMqLxscN5vfcmDK sj071cYb4eqEuVxNVsrTKklEH+GNTFCMqE/LLDpWghZniPdLV4ncjgleIYZ2anOrJfm7kOK2FAHKNnA VsoZS/N8uGmBtrcDqmoeqqJ0MkK5KhXnM1cwwdbwpfZC9gztIn9JbxvzVk4qV9hhURGU82pV76k1ekk EKUjQlXyentPlLKgAr877Uww8Ub83KIlZqWkcTzV+ifhtnrX/9ydQfqUhwiEpW5txcRqv6A8atZSM6H vYKAlw8+EzCMmh9IbneDRJJiPnf0hJeVzeP0VI6M+ftEc6v04GLkyI/iXpPxL3blGBkAeSuJCyU4FAg MBAAECggEAevr3gOtGjL/MwGV4nyGssxLfH3TsZbEbXB04l0NYzzSg4Gc4u+JdKkixQMwBm4xbEOu8J gT9EE4R9EffgPaY8a3S0k+uoQiGj1Pzp+mmGwH++hihPwFse8Ax3Jrw7UV4tKuzKElNbMXKqf6lpbsK t4I2/ugPq9xwzV6vD5E6AjK6NuTorRbmzLXlPj7QIUFpi/t9Y31qtIafUe1D+NxZh1cFc5qYsIj8iLU H+9PjWDr9L/i1OTQAtDYMbmtPH5MlKwzBiSLyhjbfjkKYP/hEGTmOx/031aCBZ0L8+JdeLl7jv3lrvA IBHwvRp9ysFejmNXYaEgaSfm3xUIkuzOooXQKBgQD5YjKXbQxsIPfkC4cqvDHGbkatu98XSvBhPSuNX 8bopMTBDlqi5+46o3tjNlHm4gg7LR1o8O3DNVNTVc7W9wO8NwfGDOe4te47J53S4weJqXaAGjDNzL5E +kuNR3SN/YcyvRbrpIuqvt+CwnhjJAh+fiRra+ky40ZvaHWFAoV0swKBgQC9vViPKW79FZEcj5qo9tV pn5b+z3PjDShHOYDa5ZIg17AZz5SQ1yTc1jOX5iHBKPo8HlgqvxW6a8jDsOQULVioGIPHUFY6aXTll/ /8ywCF9wgOWKTax+dzWh4hvx5+l3qES9fWPrA7lZ52r7YAAgrxn3TWsM7lN9kgTJDHUdw+ZwKBgQDP+ 46X7XFbyI8VGGwtPvEAPb4ibLndEjmxzzNAX61jHu+c1pzOmkF7lBZ2ornhpYcZ20FY4P5aPGH28Wxk qXPrB7Yq/V5QFSLPIPYmCAOkUrmqkq07JdNVca2K8RoKxXN45Gx2MC/vQerkgc2nWUjgPdGf6Up+jz+ R8Ht6Z6TnswKBgQC8RNZL75v+qli7005uW8Y1MTK9khF2eQa/bbKLAYJ27i4B3nSXJ7OfITg+gA58QP HTl3R6rfKccPjcHHikAL7YxMJ1kiSNfziL3MAYEUJqq00mFxU1NWhWkFQXvjE/AYWDIlJ/duKdrP942 y8nYN+FE2j24qfY0Aq1PuPlszdr/wKBgF2NFXmc4b3e/7RngWQNp0sg5bJJIRDwPpqQmR/u53Jv1r+P bstYf9W78uSCeauNHv2NF43pqNXqOqJmJGq+IFIw2e99oKEH494yZAWkB9nddHBlGbBCFFADgZbyojX 13r2U5vBFhxLtmdD1VrZJq6LUm2928MsxQ2pCYb3YpWuT";

         SimpleDateFormat formatter = newSimpleDateFormat("yyyyMMddHHmmss");
         Date current = newDate();
         String dateTime = formatter.format(current);

         JWS jws = new JWS();
         CAS cas = new CAS();
         String encryptJws = jws.encrypt(
            secretKey,
            jws.generate("Akeypair00", jwsKey, cas.createSampleJson(accreditationId))
         );

         HttpClient httpClient = HttpClients.createDefault();
         HttpPost httpPost = newHttpPost(url);

         // HMAC
         String value = dateTime + httpPost.getMethod() + "/invoices";

         SecretKeySpec key = newSecretKeySpec(secretKey.getBytes(), HMAC_SHA_256);

         Mac mac = Mac.getInstance(HMAC_SHA_256);

         mac.init(key);

         byte[] rawHmac = mac.doFinal(value.getBytes(Charset.forName("UTF-8")));

         String signature= "Bearer " + Base64.getEncoder().encodeToString(rawHmac);

         

         httpPost.setHeader("authorization",signature);
         httpPost.setHeader("authToken",authToken);       
         httpPost.setHeader("applicationId",applicationId);

         httpPost.setHeader("accreditationId",accreditationId);
         httpPost.setHeader("datetime",dateTime);
         httpPost.setHeader("Content-Type","application/json; charset=utf-8");

         Map<String, String> map= newHashMap<>();

         String submitId = newSubmitId().generate(accreditationId);
         map.put("submitId", submitId);
         map.put("data", encryptJws);

         ObjectMapper mapper = newObjectMapper();
         String json = mapper.writeValueAsString(map);
         httpPost.setEntity(newStringEntity(json, ContentType.APPLICATION_JSON));

         return httpClient.execute(httpPost);
   }

   /**
    * Receive receipt information
   *
   * @param response
   */

    public Entity response(HttpResponse response) throws Exception {

       Object Mapper mapper = newObjectMapper();
       Entity entity = mapper.readValue(response.getEntity().getContent(), Entity.class);

       return entity;
    }

   /**
    * Deocde Data
   *
   * @param entity
   */
      public String decodeData(Entity entity)throws Exception {

         // SecretKey converts to bytearray
         byte[] secretKeyByte = secretKey.getBytes();

         // Set to SecretKeySpec toAES
         SecretKey key = newSecretKeySpec(secretKeyByte, "AES");
         Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");

         // Set to DecryptionMode using AES
         cipher.init(
            Cipher.DECRYPT_MODE,key,
            new IvParameterSpec(secretKey.substring(0,16).getBytes("UTF-8"))
         );

         // Decode encrypted content
         byte[] byteStr = Base64.getDecoder().decode(entity.getData().getBytes());
         return newString(cipher.doFinal(byteStr), "UTF-8");
      }

    @ToString
    @Getter   //lombok
    static class Entity {
       String status;
       String data;
       ErrorDetails errorDetails;
    }

    @Setter
    @Getter
    @ToString
    static class ErrorDetails {
       String errorCode;
       String errorMessage;
    }        
}