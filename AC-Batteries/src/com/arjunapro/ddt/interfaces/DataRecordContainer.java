package com.arjunapro.ddt.interfaces;

import java.util.ArrayList;
import java.util.Iterator;

public interface DataRecordContainer {

	void setHeaders(String[] names);

	void add(DataRecord record);

	void add(Object[] record);

	void addAll(Object[][] records);

	DataRecord get(int index);

	ArrayList<DataRecord> getAll();

	Iterator<DataRecord> iterator();

}