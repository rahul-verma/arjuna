package pvt.batteries.encrypt;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

import pvt.batteries.utils.ExceptionBatteries;

public class BlowFishHandler {
	private byte[] encKey = null;
	//new byte [] {'T','h','i','s', 'i','s','a','t','e','s','t','e','d','k','e','y'};

	public BlowFishHandler (byte[] encKey){
		this.encKey = encKey;
	}

	public byte[] encrypt(ZipArray compressed) throws Exception {
		try {
			// create a key
			SecretKeySpec secretkeySpec = new SecretKeySpec(this.encKey,"BlowFish");

			// create a cipher based upon Blowfish
			Cipher cipher = Cipher.getInstance("Blowfish");
			// initialize cipher to with secret key
			cipher.init(Cipher.ENCRYPT_MODE, secretkeySpec);

			byte[] encrypted = cipher.doFinal(compressed.byteArray, 0, compressed.length);
			return encrypted;

		}
		catch (Exception e) {
			ExceptionBatteries.getStackTraceAsString(e);
			throw e;
		}
	}
	
	public byte[] decrypt(byte[] decoded) throws Exception {
		try {
			// create a key
			SecretKeySpec secretkeySpec = new SecretKeySpec(this.encKey,"BlowFish");

			// create a cipher based upon Blowfish
			Cipher cipher = Cipher.getInstance("Blowfish");
			// initialize cipher to with secret key
			cipher.init(Cipher.DECRYPT_MODE, secretkeySpec);

			byte[] decrypted = cipher.doFinal(decoded);
			return decrypted;

		}
		catch (Exception e) {
			ExceptionBatteries.getStackTraceAsString(e);
			throw e;
		}
	}	
}

