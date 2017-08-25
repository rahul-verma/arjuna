package pvt.unitee.reporter.lib.ignored;

import java.util.List;

import com.google.gson.JsonObject;

import pvt.unitee.enums.IgnoredTestAttribute;
import pvt.unitee.enums.IssueAttribute;
import pvt.unitee.reporter.lib.reportable.TestRelatedResult;
import unitee.interfaces.TestVariables;

public class IgnoredTest extends TestRelatedResult{
	IgnoredTestProperties resultProps = null;
	
	public IgnoredTest(
			IgnoredTestProperties resultProps,
			TestVariables testVars) throws Exception{
		super(testVars);
		this.resultProps = resultProps;
	}
	
	public IgnoredTestProperties resultProps(){
		return this.resultProps;
	}

	public List<String> resultPropStrings(List<IgnoredTestAttribute> props) throws Exception {
		return this.resultProps().strings(props);
	}
	
	public JsonObject asJsonObject() throws Exception{
		JsonObject obj =  new JsonObject();
		IgnoredTestSerializer serializer = new IgnoredTestSerializer();
		serializer.process(this, obj);
		return obj;
	}
}