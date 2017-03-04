package com.autocognite.pvt.unitee.testobject.lib.fixture;

import com.autocognite.pvt.arjuna.enums.TestClassFixtureType;

public class TestClassFixtures implements TestFixtures {
	private Fixture setUpClassFixture = null;
	private Fixture tearDownClassFixture = null;
	private Fixture setUpClassInstanceFixture = null;
	private Fixture tearDownClassInstanceFixture = null;
	private Fixture setUpClassFragmentFixture = null;
	private Fixture tearDownClassFragmentFixture = null;
	private Fixture setUpMethodFixture = null;
	private Fixture tearDownMethodFixture = null;
	private Fixture setUpMethodInstanceFixture = null;
	private Fixture tearDownMethodInstanceFixture = null;
	private Fixture setUpTestFixture = null;
	private Fixture tearDownTestFixture = null;
	
	public TestClassFixtures(
			Fixture setUpClassFixture,
			Fixture tearDownClassFixture,
			Fixture setUpClassInstanceFixture,
			Fixture tearDownClassInstanceFixture,
			Fixture setUpClassFragmentFixture,
			Fixture tearDownClassFragmentFixture,
			Fixture setUpMethodFixture,
			Fixture tearDownMethodFixture,
			Fixture setUpMethodInstanceFixture,
			Fixture tearDownMethodInstanceFixture,
			Fixture setUpTestFixture,
			Fixture tearDownTestFixture
			){
		
		this.setSetUpClassFixture(setUpClassFixture);
		this.setTearDownClassFixture(tearDownClassFixture);
		
		this.setSetUpClassInstanceFixture(setUpClassInstanceFixture);
		this.setTearDownClassInstanceFixture(tearDownClassInstanceFixture);
		
		this.setSetUpClassFragmentFixture(setUpClassFragmentFixture);
		this.setTearDownClassFragmentFixture(tearDownClassFragmentFixture);
		
		this.setSetUpMethodFixture(setUpMethodFixture);
		this.setTearDownMethodFixture(tearDownMethodFixture);
		
		this.setSetUpMethodInstanceFixture(setUpMethodInstanceFixture);
		this.setTearDownMethodInstanceFixture(tearDownMethodInstanceFixture);
		
		this.setSetUpTestFixture(setUpTestFixture);
		this.setTearDownTestFixture(tearDownTestFixture);
	}
	
	public Fixture getSetUpClassFixture() {
		return setUpClassFixture;
	}
	
	private void setSetUpClassFixture(Fixture fixture) {
		this.setUpClassFixture = fixture;
	}
	
	public Fixture getTearDownClassFixture() {
		return tearDownClassFixture;
	}
	
	private void setTearDownClassFixture(Fixture fixture) {
		this.tearDownClassFixture = fixture;
	}
	
	public Fixture getSetUpClassInstanceFixture() {
		return setUpClassInstanceFixture;
	}
	
	private void setSetUpClassInstanceFixture(Fixture fixture) {
		this.setUpClassInstanceFixture = fixture;
	}
	
	public Fixture getTearDownClassInstanceInstanceFixture() {
		return tearDownClassInstanceFixture;
	}
	
	private void setTearDownClassInstanceFixture(Fixture fixture) {
		this.tearDownClassInstanceFixture = fixture;
	}

	public Fixture getSetUpClassFragmentFixture() {
		return setUpClassFragmentFixture;
	}
	
	private void setSetUpClassFragmentFixture(Fixture fixture) {
		this.setUpClassFragmentFixture = fixture;
	}
	
	public Fixture getTearDownClassFragmentFixture() {
		return tearDownClassFragmentFixture;
	}
	
	private void setTearDownClassFragmentFixture(Fixture fixture) {
		this.tearDownClassFragmentFixture = fixture;
	}
	
	public Fixture getSetUpMethodFixture() {
		return setUpMethodFixture;
	}
	
	private void setSetUpMethodFixture(Fixture fixture) {
		this.setUpMethodFixture = fixture;
	}
	
	public Fixture getTearDownMethodFixture() {
		return tearDownMethodFixture;
	}
	
	private void setTearDownMethodFixture(Fixture fixture) {
		this.tearDownMethodFixture = fixture;
	}
	
	public Fixture getSetUpMethodInstanceFixture() {
		return setUpMethodInstanceFixture;
	}
	
	private void setSetUpMethodInstanceFixture(Fixture fixture) {
		this.setUpMethodInstanceFixture = fixture;
	}
	
	public Fixture getTearDownMethodInstanceFixture() {
		return tearDownMethodInstanceFixture;
	}
	
	private void setTearDownMethodInstanceFixture(Fixture fixture) {
		this.tearDownMethodInstanceFixture = fixture;
	}

	public Fixture getSetUpTestFixture() {
		return setUpTestFixture;
	}
	
	private void setSetUpTestFixture(Fixture fixture) {
		this.setUpTestFixture = fixture;
	}
	
	public Fixture getTearDownTestFixture() {
		return tearDownTestFixture;
	}
	
	private void setTearDownTestFixture(Fixture fixture) {
		this.tearDownTestFixture = fixture;
	}
	
	public Fixture _getFixture(TestClassFixtureType type) throws Exception {
		switch(type){
		case SETUP_CLASS: return this.getSetUpClassFixture();
		case SETUP_CLASS_INSTANCE: return this.getSetUpClassInstanceFixture();
		case SETUP_CLASS_FRAGMENT: return this.getSetUpClassFragmentFixture();
		case SETUP_METHOD: return this.getSetUpMethodFixture();
		case SETUP_METHOD_INSTANCE: return this.getSetUpMethodInstanceFixture();
		case SETUP_TEST: return this.getSetUpTestFixture();
		case TEARDOWN_TEST: return this.getTearDownTestFixture();
		case TEARDOWN_METHOD_INSTANCE: return this.getTearDownMethodInstanceFixture();
		case TEARDOWN_METHOD: return this.getTearDownMethodFixture();
		case TEARDOWN_CLASS_FRAGMENT: return this.getTearDownClassFragmentFixture();
		case TEARDOWN_CLASS_INSTANCE: return this.getTearDownClassInstanceInstanceFixture();
		case TEARDOWN_CLASS: return this.getTearDownClassFixture();
		}
		return null;
	}
	
	public Fixture getFixture(TestClassFixtureType type) throws Exception {
		Fixture fixture = this._getFixture(type);
		if (fixture != null){
			return fixture.clone();
		} else {
			return null;
		}
	}

	@Override
	public String getFixtureName(TestClassFixtureType type) throws Exception {
		Fixture fixture = this._getFixture(type);
		if (fixture != null){
			return fixture.getName();
		} else {
			return "NOT_SET";
		}
	}
}
