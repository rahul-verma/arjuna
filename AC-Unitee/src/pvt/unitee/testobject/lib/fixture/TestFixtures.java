package pvt.unitee.testobject.lib.fixture;

import pvt.unitee.enums.TestClassFixtureType;

public interface TestFixtures {

	Fixture getSetUpTestFixture();

	Fixture getFixture(TestClassFixtureType fixtureType) throws Exception;

	String getFixtureName(TestClassFixtureType setupClass) throws Exception;

}