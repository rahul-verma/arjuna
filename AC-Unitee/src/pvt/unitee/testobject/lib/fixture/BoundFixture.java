package pvt.unitee.testobject.lib.fixture;

import java.lang.reflect.Method;

import pvt.unitee.enums.TestClassFixtureType;

public class BoundFixture extends BaseTestClassFixture {
	
	public BoundFixture(Class<?> class1, TestClassFixtureType fType, Method m) {
		super(class1, fType, m);
	}

	public void executeFixture() throws Exception {
		switch(this.getSignatureType()){
		case NO_ARG:
			this.getMethod().invoke(this.getTestClassInstance().getUserTestContainerObject());
			break;
		case SINGLEARG_TESTVARS:
			this.getMethod().invoke(this.getTestClassInstance().getUserTestContainerObject(), this.getTestObject().getTestVariables());
			break;
		}
	}
	
	public BoundFixture clone(){
		BoundFixture boundFixture = new BoundFixture(this.getTestClass(), this.getType(), this.getMethod());
		boundFixture.setSignatureType(this.getSignatureType());
		boundFixture.setTestContainerInstance(null);
		return boundFixture;
	}

}
