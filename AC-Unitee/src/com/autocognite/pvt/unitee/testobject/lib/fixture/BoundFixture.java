package com.autocognite.pvt.unitee.testobject.lib.fixture;

import java.lang.reflect.Method;

import com.autocognite.pvt.arjuna.enums.TestClassFixtureType;
import com.autocognite.pvt.arjuna.enums.TestResultCode;

public class BoundFixture extends BaseTestClassFixture {
	
	public BoundFixture(Class<?> class1, TestClassFixtureType fType, Method m) {
		super(class1, fType, m);
	}

	public void executeFixture() throws Exception {
		this.getMethod().invoke(this.getTestClassInstance().getUserTestContainerObject());
	}
	
	public BoundFixture clone(){
		BoundFixture boundFixture = new BoundFixture(this.getTestClass(), this.getType(), this.getMethod());
		boundFixture.setTestContainerInstance(null);
		return boundFixture;
	}

}
