package com.autocognite.pvt.unitee.reporter.lib.writer.json;

import java.io.File;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.text.SimpleDateFormat;
import java.util.Date;

import org.apache.commons.io.FileUtils;

import com.autocognite.batteries.util.FileSystemBatteries;
import com.autocognite.pvt.batteries.filehandler.FileWriter;
import com.autocognite.pvt.unitee.reporter.lib.DefaultObserver;

public abstract class JsonResultWriter<T> extends DefaultObserver<T>{
	private String reportDir = null;
	
	public JsonResultWriter(String reportDir) throws Exception{
		super();
		this.reportDir = FileSystemBatteries.getCanonicalPath(reportDir);
		FileUtils.forceMkdir(new File(reportDir));
	}
	
	protected void update(String reportName, String jsonString) throws Exception {
		String rPath = FileSystemBatteries.getCanonicalPath(reportDir + "/" + reportName);
		FileWriter writer = new FileWriter(rPath);
		writer.write(jsonString);
		writer.close();
	}
	
	protected String createFileID(String inStr) throws NoSuchAlgorithmException{

        MessageDigest md = MessageDigest.getInstance("MD5");
        md.update(inStr.getBytes());

        byte byteData[] = md.digest();

        //convert the byte to hex format method 1
        StringBuffer sb = new StringBuffer();
        sb.append(new SimpleDateFormat("yyyy.MM.dd.HH.mm.ss.SSS").format(new Date()));
        for (int i = 0; i < byteData.length; i++) {
         sb.append(Integer.toString((byteData[i] & 0xff) + 0x100, 16).substring(1));
        }	
 
        return sb.toString();
	}
}
