package com.autocognite.pvt.batteries.value;

import java.util.List;

import com.autocognite.batteries.value.DataWrapper;

public abstract class AbstractDataWrapper implements DataWrapper {
	@Override
	public boolean asBoolean() throws Exception {
		throw new Exception(String.format("Not supported for %s", this.getClass().getSimpleName()));
	}

	@Override
	public Number asNumber() throws Exception {
		throw new Exception(String.format("Not supported for %s", this.getClass().getSimpleName()));
	}

	@Override
	public int asInt() throws Exception {
		throw new Exception(String.format("Not supported for %s", this.getClass().getSimpleName()));
	}

	@Override
	public long asLong() throws Exception {
		throw new Exception(String.format("Not supported for %s", this.getClass().getSimpleName()));
	}

	@Override
	public double asDouble() throws Exception {
		throw new Exception(String.format("Not supported for %s", this.getClass().getSimpleName()));
	}

	@Override
	public float asFloat() throws Exception {
		throw new Exception(String.format("Not supported for %s", this.getClass().getSimpleName()));
	}

	@Override
	public <T extends Enum<T>> T asEnum(Class<T> enumClass) throws Exception {
		throw new Exception(String.format("Not supported for %s", this.getClass().getSimpleName()));
	}

	@Override
	public <T extends Enum<T>> List<T> asEnumList(Class<T> klass) throws Exception {
		throw new Exception(String.format("Not supported for %s", this.getClass().getSimpleName()));
	}

	@Override
	public List<Number> asNumberList() throws Exception {
		throw new Exception(String.format("Not supported for %s", this.getClass().getSimpleName()));
	}

	@Override
	public List<Integer> asIntList() throws Exception {
		throw new Exception(String.format("Not supported for %s", this.getClass().getSimpleName()));
	}

	@Override
	public List<String> asStringList() throws Exception {
		throw new Exception(String.format("Not supported for %s", this.getClass().getSimpleName()));
	}

	public List<?> asList() throws Exception {
		throw new Exception(String.format("Not supported for %s", this.getClass().getSimpleName()));
	}

}

//test
