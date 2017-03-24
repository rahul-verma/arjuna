package pvt.unitee.reporter.lib.step;

import java.util.List;

import com.google.gson.JsonObject;

import pvt.arjunapro.enums.StepResultAttribute;

public class StepResult {
	private StepResultProperties resultProps =  null;
	
	public StepResult(
			StepResultProperties resultProps) throws Exception{
		this.resultProps = resultProps;
	}

	public StepResultProperties resultProps(){
		return this.resultProps;
	}
	
	public List<String> resultPropStrings(List<StepResultAttribute> props) throws Exception {
		return this.resultProps().strings(props);
	}
	
	public JsonObject asJsonObject() throws Exception{
		StepResultSerializer serializer = new StepResultSerializer();
		return serializer.process(this);
	}

	public void setIssueId(int issueId) {
		this.resultProps.setIssueId(issueId);
	}

	public int issueId() throws Exception {
		return this.resultProps.issueId();
	}
}