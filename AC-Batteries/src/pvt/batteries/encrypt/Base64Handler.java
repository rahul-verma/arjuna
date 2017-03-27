package pvt.batteries.encrypt;

import org.apache.commons.codec.binary.Base64;

public class Base64Handler {
	public String encode(byte[] encrypted){
		return Base64.encodeBase64URLSafeString(encrypted);
	}
	
	public byte[] decode(String encoded){
		Base64 decoder = new Base64(true); //True make decoding url safe
		byte[] bArray = decoder.decode(encoded);
		return bArray;
	}
}
