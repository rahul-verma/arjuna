package com.autocognite.pvt.unitee.testobject.lib.fixture;

import java.lang.reflect.Method;

import com.autocognite.pvt.arjuna.enums.TestClassFixtureType;

public class StaticFixture extends BaseTestClassFixture {
	
	public StaticFixture(Class<?> container, TestClassFixtureType fType, Method m) {
		super(container, fType, m);
	}

	public void executeFixture() throws Exception {
		this.getMethod().invoke(this.getTestClass());
	}
	
	public StaticFixture clone(){
		StaticFixture sFixture = new StaticFixture(this.getTestClass(), this.getType(), this.getMethod());
		sFixture.setTestContainerInstance(null);
		return sFixture;
	}
}
