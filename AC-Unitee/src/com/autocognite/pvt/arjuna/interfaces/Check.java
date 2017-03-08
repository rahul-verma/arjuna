package com.autocognite.pvt.arjuna.interfaces;

public interface Check {

	String getSourceMethodName();

	void setSourceMethodName(String methodName);

	String getSourceClassName();

	void setSourceClassName(String className);

	String getPurpose();

	void setPurpose(String purpose);

	String getBenchmark();

	void setBenchmark(String benchmark);

	String getActualObservation();

	void setActualObservation(String actual);

	String getText();

	void setText(String assertion);

	boolean passed();

	boolean failed();

	void setFailure();

	boolean erred();

	void setError();

	String getExceptionMessage();

	void evaluate() throws Exception;

	void setExceptionMessage(String message);

}