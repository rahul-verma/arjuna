package com.arjunapro.ddt.datarecord;

import pvt.batteries.ddt.datarecord.BaseDataRecordContainer;

public class ListDataRecordContainer extends BaseDataRecordContainer {

	@Override
	public void setHeaders(String[] names) throws Exception {
		throw new Exception("Not supported for List Data Record Container.");
	}
}
