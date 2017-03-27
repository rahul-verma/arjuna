package pvt.license;

import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;

import org.apache.commons.io.IOUtils;

import pvt.unitee.config.ArjunaSingleton;

public class LicenseChecker {

	private byte[] extractBytes() throws IOException {
		return IOUtils.toByteArray((InputStream) ArjunaSingleton.class.getResource("/pvt/arjunapro/img/ArjunaFavicon.png").getContent());
	}
}
