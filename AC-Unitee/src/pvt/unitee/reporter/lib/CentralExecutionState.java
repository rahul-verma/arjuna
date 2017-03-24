package pvt.unitee.reporter.lib;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import org.apache.log4j.Logger;

import com.arjunapro.pvt.ArjunaInternal;
import com.arjunapro.testauto.config.RunConfig;
import com.arjunapro.testauto.interfaces.TestObjectProperties;

import pvt.arjunapro.enums.TestResultType;
import pvt.unitee.reporter.lib.issue.Issue;
import pvt.unitee.reporter.lib.test.TestResult;

public class CentralExecutionState {
	private Logger logger = RunConfig.logger();
	//private SummaryResult overallResultMap = new SummaryResult("Overall Results");
	private HashMap<String,SummaryResult> bucketResultMap = new HashMap<String,SummaryResult>();
	private HashMap<String,SummaryResult> testClassResultMap = new HashMap<String,SummaryResult>();
	private HashMap<String,SummaryResult> methodResultMap = new HashMap<String,SummaryResult>();
	private int currentIssueCounter = 0;

	/*
	 * For LookUp - Classes
	 */
	// Because of Fail/Error or dependency not met
	private Set<String> classesWithIssues = new HashSet<String>();
	private Map<String,Integer> classIssueMap = new HashMap<String,Integer>();

	/*
	 * For LookUp - Methods
	 */
	// Because of Fail/Error or dependency not met
	private Set<String> methodsWithIssues = new HashSet<String>();
	private Map<String,Integer> methodIssueMap = new HashMap<String,Integer>();

	/*
	 * For Results Capturing
	 */
	private HashMap<String,ThreadState> threadStates = new HashMap<String,ThreadState>();
	
	public ThreadState getCurrentThreadState(){
		return this.threadStates.get(Thread.currentThread().getName());
	}
	
	public synchronized void update(TestResult reportable) throws Exception{
		this.update(reportable.objectProps(), reportable);
	}
	
	public synchronized void update(Issue reportable) throws Exception{
		switch (reportable.objectProps().objectType()){
		case TEST_CLASS:
			addContainerIssue(reportable.objectProps().qualifiedName(), reportable.resultProps().id());
			break;
		case TEST_CLASS_INSTANCE:
			addContainerIssue(reportable.objectProps().qualifiedName(), reportable.resultProps().id());
			break;
		case TEST_CLASS_FRAGMENT:
			addContainerIssue(reportable.objectProps().qualifiedName(), reportable.resultProps().id());
			break;
		case TEST_METHOD:
			addCreatorIssue(reportable.objectProps().qualifiedName(), reportable.resultProps().id());
			addContainerIssue(reportable.objectProps().parentQualifiedName(), reportable.resultProps().id());
			break;
		case TEST_METHOD_INSTANCE:
			addCreatorIssue(reportable.objectProps().qualifiedName(), reportable.resultProps().id());
			addContainerIssue(reportable.objectProps().parentQualifiedName(), reportable.resultProps().id());
			break;
		case TEST:
			addCreatorIssue(reportable.objectProps().qualifiedName(), reportable.resultProps().id());
			addContainerIssue(reportable.objectProps().parentQualifiedName(), reportable.resultProps().id());
			break;
		}
	}

	public synchronized boolean wasTestMethodSuccessful(String methodName) {
		return !this.methodsWithIssues.contains(methodName);
	}
	
	public synchronized boolean didTestCreatorsSucceed(Set<String> targets, IssueId outId) {
		if (ArjunaInternal.logDependencyMetInfo){
			logger.debug("Checking success for these test creator dependencies: " + targets);
			logger.debug(this.methodIssueMap.keySet());
		}
		
		for (String target: targets){
			if (this.methodsWithIssues.contains(target)){
				outId.ID = this.methodIssueMap.get(target);
				return false;
			}
		}
		return true;
	}
	
	public synchronized boolean didTestContainersSucceed(Set<String> targets, IssueId outId) {
		if (ArjunaInternal.logDependencyMetInfo){
		logger.debug("Checking success for these test container dependencies: " + targets);
		}
		for (String target: targets){
			if (ArjunaInternal.logDependencyMetInfo){
				logger.debug("Checking for test container dependency: " + target);
			}
			if (this.classesWithIssues.contains(target)){
				if (ArjunaInternal.logDependencyMetInfo){
					logger.debug("Has Issues");
				}
				outId.ID = this.classIssueMap.get(target);
				return false;
			}
		}
		if (ArjunaInternal.logDependencyMetInfo){
			logger.debug("Container dependencies met.");
		}
		return true;
	}	
	
	private void addCreatorIssue(String methodName, int issueId){
		if (!this.methodsWithIssues.contains(methodName)){
			this.methodsWithIssues.add(methodName);
			this.methodIssueMap.put(methodName, issueId);
		}		
	}
	
	private void updateTestCreatorState(String methodName, TestResultType type, int issueId){
		if (ArjunaInternal.centralStateUpdateInfo){
			logger.debug("Execution State: Test Creator: Name: " + methodName);
			logger.debug("Execution State: Test Creator: Type: " + type);
		}
		if  (!methodResultMap.containsKey(methodName)){
			methodResultMap.put(methodName, new SummaryResult());
		}

		methodResultMap.get(methodName).incrementCount(type);	
		
		if ((type == TestResultType.FAIL) || (type == TestResultType.ERROR) || (type == TestResultType.EXCLUDED)){
			addCreatorIssue(methodName, issueId);
		}
	}
	
	private void addContainerIssue(String containerName, int issueId){
		if (!this.classesWithIssues.contains(containerName)){
			this.classesWithIssues.add(containerName);
			this.classIssueMap.put(containerName, issueId);
		}	
	}
	
	private void updateTestClassState(String name, TestResultType type, int issueId){
		if (ArjunaInternal.displayReportProcessingInfo){
			logger.debug(String.format("Updating Test Container State as %s for %s", type, name));
		}
		if  (!testClassResultMap.containsKey(name)){
			testClassResultMap.put(name, new SummaryResult());
		}

		testClassResultMap.get(name).incrementCount(type);	
		
		if ((type == TestResultType.FAIL) || (type == TestResultType.ERROR) || (type == TestResultType.EXCLUDED)){
			addContainerIssue(name, issueId);
		}
	}
	
	private void updateSessionState(String bucketName, TestResultType type){
		if  (!bucketResultMap.containsKey(bucketName)){
			bucketResultMap.put(bucketName, new SummaryResult());
		}		

		bucketResultMap.get(bucketName).incrementCount(type);
	}
	
	private void update(TestObjectProperties objectProps, TestResult reportable) throws Exception{
		if (ArjunaInternal.centralStateUpdateInfo){
			logger.debug("Update central state with Test result");
			logger.debug("Execution State: Test Method Name: " + objectProps.qualifiedName());
			logger.debug("Execution State: Test Result: " + reportable.resultProps().result());
		}
		TestResultType resultType = reportable.resultProps().result();
		int issueId = reportable.resultProps().issueId();
		switch(objectProps.objectType()){
		case TEST:
			updateTestCreatorState(objectProps.qualifiedName(), resultType, issueId);
			updateTestClassState(objectProps.parentQualifiedName(), resultType, issueId);
			updateSessionState(objectProps.sessionName(), resultType);			
			break;	
		}
	}

	public synchronized void registerThread(String name) {
		this.threadStates.put(name, new ThreadState());
	}

	public void deregisterThread(String tName) {
		this.threadStates.remove(tName);
	}
	
	public synchronized int getIssueId(){
		return ++currentIssueCounter;
	}
}
