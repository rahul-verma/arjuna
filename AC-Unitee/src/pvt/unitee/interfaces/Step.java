package pvt.unitee.interfaces;

public interface Step {

	String getPurpose();

	void setPurpose(String purpose);

	String getBenchmark();

	void setBenchmark(String benchmark);

	String getActualObservation();

	void setActualObservation(String actual);
	
	String getText();

	void setText(String assertion);

	void setFailure();

	void setError();

	String getExceptionMessage();

	void evaluate() throws Exception;

	void setExceptionMessage(String message);
}
