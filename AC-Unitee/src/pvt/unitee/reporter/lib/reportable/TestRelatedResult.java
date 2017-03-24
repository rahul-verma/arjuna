package pvt.unitee.reporter.lib.reportable;

import java.util.List;
import java.util.Map;

import com.arjunapro.testauto.enums.TestAttribute;
import com.arjunapro.testauto.enums.TestObjectAttribute;
import com.arjunapro.testauto.interfaces.StringKeyValueContainer;
import com.arjunapro.testauto.interfaces.TestObjectProperties;
import com.arjunapro.testauto.interfaces.TestProperties;
import com.arjunapro.testauto.interfaces.TestVariables;

public class TestRelatedResult {
	private TestVariables testVars = null;
	
	public TestRelatedResult(TestVariables testVars) throws Exception{
		this.testVars = testVars;
	}
	
	public TestVariables testVars() throws Exception {
		return this.testVars;
	}
	
	public TestObjectProperties objectProps() throws Exception {
		return this.testVars.object();
	}
	
	public TestProperties testProps() throws Exception {
		return this.testVars.test();
	}
	
	public StringKeyValueContainer customProps() throws Exception {
		return this.testVars.utp();
	}
	
	public StringKeyValueContainer utv() throws Exception {
		return this.testVars.utv();
	}

	public void setTestVariables(TestVariables testVars) {
		this.testVars = testVars;
	}
	
	public List<String> objectPropStrings(List<TestObjectAttribute> props) throws Exception {
		return this.objectProps().strings(props);
	}
	
	public Map<String,String> objectPropStrItems(List<TestObjectAttribute> props) throws Exception {
		return this.objectProps().strItems(props);
	}
	
	public List<String> testPropStrings(List<TestAttribute> props) throws Exception {
		return this.testProps().strings(props);
	}
	
	public Map<String,String> testPropStrItems(List<TestAttribute> props) throws Exception {
		return this.testProps().strItems(props);
	}	
	
	public List<String> customPropStrings(List<String> props) throws Exception {
		return this.customProps().strings(props);
	}
	
	public Map<String,String> customPropStrItems(List<String> props) throws Exception {
		return this.customProps().strItems(props);
	}
}