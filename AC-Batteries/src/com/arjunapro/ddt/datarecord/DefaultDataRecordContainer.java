/*******************************************************************************
 * Copyright 2015-16 AutoCognite Testing Research Pvt Ltd
 * 
 * Website: www.AutoCognite.com
 * Email: support [at] autocognite.com
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *   http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 ******************************************************************************/
package com.arjunapro.ddt.datarecord;

import java.util.ArrayList;
import java.util.Iterator;

import com.arjunapro.ddt.interfaces.DataRecord;
import com.arjunapro.ddt.interfaces.DataRecordContainer;

import pvt.arjunapro.enums.DataRecordOrder;

public class DefaultDataRecordContainer implements DataRecordContainer {
	private DataRecordOrder order = DataRecordOrder.ORDERED;
	private ArrayList<DataRecord> queue = new ArrayList<DataRecord>();
	private String[] headers = null;

	public DefaultDataRecordContainer(DataRecordOrder order) {
		this.order = order;
	}

	public DefaultDataRecordContainer() {
		this(DataRecordOrder.ORDERED);
	}

	public DefaultDataRecordContainer(Object[][] records) {
		this.addAll(records);
	}

	/* (non-Javadoc)
	 * @see com.autocognite.arjuna.bases.DataRecordContainer#setHeaders(java.lang.String[])
	 */
	@Override
	public void setHeaders(String[] names) {
		this.headers = names;
	}

	/* (non-Javadoc)
	 * @see com.autocognite.arjuna.bases.DataRecordContainer#add(com.autocognite.arjuna.interfaces.DataRecord)
	 */
	@Override
	public void add(DataRecord record) {
		this.queue.add(record);
	}

	/* (non-Javadoc)
	 * @see com.autocognite.arjuna.bases.DataRecordContainer#add(java.lang.Object[])
	 */
	@Override
	public void add(Object[] record) {
		if (this.headers == null) {
			this.queue.add(new DefaultDataRecord(record));
		} else {
			this.queue.add(new DefaultDataRecord(headers, record));
		}
	}

	/* (non-Javadoc)
	 * @see com.autocognite.arjuna.bases.DataRecordContainer#addAll(java.lang.Object[][])
	 */
	@Override
	public void addAll(Object[][] records) {
		if (this.headers == null) {
			for (Object[] record : records) {
				this.queue.add(new DefaultDataRecord(record));
			}
		} else {
			for (Object[] record : records) {
				this.queue.add(new DefaultDataRecord(headers, record));
			}
		}
	}

	/* (non-Javadoc)
	 * @see com.autocognite.arjuna.bases.DataRecordContainer#get(int)
	 */
	@Override
	public DataRecord get(int index) {
		return this.queue.get(index);
	}

	/* (non-Javadoc)
	 * @see com.autocognite.arjuna.bases.DataRecordContainer#getAll()
	 */
	@Override
	public ArrayList<DataRecord> getAll() {
		return queue;
	}

	/* (non-Javadoc)
	 * @see com.autocognite.arjuna.bases.DataRecordContainer#iterator()
	 */
	@Override
	public Iterator<DataRecord> iterator() {
		return queue.iterator();
	}

}
