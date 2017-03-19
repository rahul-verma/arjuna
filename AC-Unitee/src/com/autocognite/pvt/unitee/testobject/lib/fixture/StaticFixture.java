package com.autocognite.pvt.unitee.testobject.lib.fixture;

import java.lang.reflect.Method;

import com.autocognite.pvt.arjuna.enums.TestClassFixtureType;

public class StaticFixture extends BaseTestClassFixture {
	
	public StaticFixture(Class<?> container, TestClassFixtureType fType, Method m) {
		super(container, fType, m);
	}

	public void executeFixture() throws Exception {
		switch(this.getSignatureType()){
		case NO_ARG:
			this.getMethod().invoke(this.getTestClass());
			break;
		case SINGLEARG_TESTVARS:
			this.getMethod().invoke(this.getTestClass(), this.getTestObject().getTestVariables());
			break;
		}
	}
	
	public StaticFixture clone(){
		StaticFixture sFixture = new StaticFixture(this.getTestClass(), this.getType(), this.getMethod());
		sFixture.setSignatureType(this.getSignatureType());
		sFixture.setTestContainerInstance(null);
		return sFixture;
	}
}
