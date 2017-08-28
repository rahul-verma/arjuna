package pvt.unitee.reporter.lib;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import org.apache.log4j.Logger;

import arjunasdk.config.RunConfig;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.enums.TestResultType;
import pvt.unitee.testobject.lib.loader.group.Group;

public class GlobalState {
	private Logger logger = RunConfig.logger();
	private SummaryResult overallSummary = new SummaryResult();
	
	/*
	 * For Results Capturing
	 */
	private Map<String,ThreadState> threadStates = new HashMap<String,ThreadState>();
	
	// Group States
	private Map<String,GroupState> groupStateMap = new HashMap<String,GroupState>();
	
	// Issue id is globally maintained across all groups in session
	// Need to think about multi-session distributed testing scenario
	// May be the issue id should be a string: runid-session-issuenumber
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
	
	public ThreadState getCurrentThreadState(){
		return this.threadStates.get(Thread.currentThread().getName());
	}
	
	public ThreadState getThreadState(String parentTestThreadName) {
		return this.threadStates.get(parentTestThreadName);
	}

	public synchronized void registerThread(String name) {
		this.threadStates.put(name, new ThreadState());
	}

	public synchronized void deregisterThread(String tName) {
		this.threadStates.remove(tName);
	}
	
	public synchronized int getIssueId(){
		return ++currentIssueCounter;
	}
	
	public synchronized void registerGroupState(Group group) {
		this.groupStateMap.put(group.getID(), new GroupState(group));
	}	

	public GroupState getGroupState(String groupID) {
		return groupStateMap.get(groupID);
	}
	
	public synchronized void updateState(TestResultType type) {
		overallSummary.incrementCount(type);
	}
	
	public synchronized void addCreatorIssue(String methodName, int issueId){
		if (!this.methodsWithIssues.contains(methodName)){
			this.methodsWithIssues.add(methodName);
			this.methodIssueMap.put(methodName, issueId);
		}		
	}
	
	public synchronized void addContainerIssue(String containerName, int issueId){
		if (!this.classesWithIssues.contains(containerName)){
			this.classesWithIssues.add(containerName);
			this.classIssueMap.put(containerName, issueId);
		}	
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
