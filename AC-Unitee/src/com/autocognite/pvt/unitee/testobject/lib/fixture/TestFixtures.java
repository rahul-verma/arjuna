package com.autocognite.pvt.unitee.testobject.lib.fixture;

import com.autocognite.pvt.arjuna.enums.TestClassFixtureType;

public interface TestFixtures {

	Fixture getSetUpTestFixture();

	Fixture getFixture(TestClassFixtureType fixtureType) throws Exception;

	String getFixtureName(TestClassFixtureType setupClass) throws Exception;

}