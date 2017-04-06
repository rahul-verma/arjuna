package com.arjunapro.ddt.datarecord;

import pvt.batteries.ddt.datarecord.BaseDataRecordContainer;

public class MapDataRecordContainer extends BaseDataRecordContainer {
	
	@Override
	public void validate() throws Exception {
		if ((this.getHeaders() == null) || (this.getHeaders().length == 0)){
			throw new Exception("You can not use a Map Data Record container without defining appropriate headers.");
		}
	}
}
