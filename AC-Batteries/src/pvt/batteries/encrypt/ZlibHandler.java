package pvt.batteries.encrypt;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.zip.DataFormatException;
import java.util.zip.Deflater;
import java.util.zip.Inflater;

public class ZlibHandler {
	private static int decompressFactor = 3;
	
	public static ZipArray compress (String toCompress){
		byte[] result = new byte[toCompress.length()*2];
		Deflater deflater = new Deflater();
		byte[] bytes = toCompress.getBytes();
		deflater.setInput(bytes);
		deflater.finish();
		 ByteArrayOutputStream bos = new ByteArrayOutputStream(bytes.length);
		 while(!deflater.finished())
		 {
			 int bytesCompressed = deflater.deflate(result);
			 bos.write(result,0,bytesCompressed);
		 }
		  try
         {
                 bos.close();
         }
         catch(IOException ioe)
         {
       	  	ioe.printStackTrace();
         }
		return new ZipArray(bos.toByteArray(), bos.size());
	}
	
	public static String decompress (byte[] decrypted){
		ByteArrayOutputStream baos = new ByteArrayOutputStream(decrypted.length);
		try {
			Inflater decompresser = new Inflater();
			decompresser.setInput(decrypted, 0, decrypted.length);
			byte[] buff = new byte[decrypted.length* ZlibHandler.decompressFactor];

			while(!decompresser.finished())
			{
				int count = decompresser.inflate(buff);
				baos.write(buff, 0, count);
			}
			baos.close();
			decompresser.end();
			
		} catch (DataFormatException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return new String(baos.toByteArray());
	}	
}
