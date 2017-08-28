package pvt.unitee.reporter.lib;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import org.apache.log4j.Logger;

import arjunasdk.config.RunConfig;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.enums.TestResultType;
import pvt.unitee.reporter.lib.issue.Issue;
import pvt.unitee.reporter.lib.test.TestResult;
import pvt.unitee.testobject.lib.loader.group.Group;
import unitee.interfaces.TestObjectProperties;

public class GroupState {
	private Logger logger = RunConfig.logger();
	
	private Group group = null;
	private SummaryResult groupSummary = new SummaryResult();
	private Map<String,SummaryResult> testClassResultMap = new HashMap<String,SummaryResult>();
	private Map<String,HashMap<String,SummaryResult>> methodResultMap = new HashMap<String,HashMap<String,SummaryResult>>();

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
	
	public GroupState(Group group){
		this.group = group;
	}
	
	public synchronized void update(TestResult reportable) throws Exception{
		this.update(reportable.objectProps(), reportable);
	}
	
	private void update(TestObjectProperties objectProps, TestResult reportable) throws Exception{
		if (ArjunaInternal.groupStateUpdateInfo){
			logger.debug(String.format("Update group state with Test result for group: %s", group.getID()));
			logger.debug("Execution State: Test Method Name: " + objectProps.qualifiedName());
			logger.debug("Execution State: Test Result: " + reportable.resultProps().result());
		}
		TestResultType resultType = reportable.resultProps().result();
		int issueId = reportable.resultProps().issueId();
		updateTestCreatorState(objectProps.parentQualifiedName(), objectProps.name(), resultType, issueId);
		updateTestClassState(objectProps.parentQualifiedName(), resultType, issueId);
		updateGroupState(objectProps.sessionName(), resultType);			
	}	
	
	private void updateTestCreatorState(String containerName, String methodName, TestResultType type, int issueId){
		if (ArjunaInternal.groupStateUpdateInfo){
			logger.debug("Execution State: Test Creator: Name: " + methodName);
			logger.debug("Execution State: Test Creator: Type: " + type);
		}
		if  (!methodResultMap.containsKey(containerName)){
			methodResultMap.put(containerName, new HashMap<String, SummaryResult>());
		}
		
		if (!methodResultMap.get(containerName).containsKey(methodName)){
			methodResultMap.get(containerName).put(methodName, new SummaryResult());
		}

		methodResultMap.get(containerName).get(methodName).incrementCount(type);	
		
		if ((type == TestResultType.FAIL) || (type == TestResultType.ERROR) || (type == TestResultType.EXCLUDED)){
			addCreatorIssue(containerName + "." + methodName, issueId);
		}
	}
	
	private void updateTestClassState(String name, TestResultType type, int issueId){
		if (ArjunaInternal.groupStateUpdateInfo){
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
	
	private void updateGroupState(String bucketName, TestResultType type){
		groupSummary.incrementCount(type);
		ArjunaInternal.getGlobalState().updateState(type);
	}
	
	private void addCreatorIssue(String methodName, int issueId){
		if (!this.methodsWithIssues.contains(methodName)){
			this.methodsWithIssues.add(methodName);
			this.methodIssueMap.put(methodName, issueId);
			ArjunaInternal.getGlobalState().addCreatorIssue(methodName, issueId);
		}		
	}
	
	private void addContainerIssue(String containerName, int issueId){
		if (!this.classesWithIssues.contains(containerName)){
			this.classesWithIssues.add(containerName);
			this.classIssueMap.put(containerName, issueId);
			ArjunaInternal.getGlobalState().addContainerIssue(containerName, issueId);
		}	
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
	
}
