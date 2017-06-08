package pvt.unitee.core.lib.dependency;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.enums.DependencyCondition;
import pvt.unitee.enums.DependencyTarget;
import pvt.unitee.reporter.lib.IssueId;

public class DependencyHandler implements Cloneable{
	private DependencyTarget dType = null;
	private DependencyCondition dCondition = null; // Not used as of now.
	private Set<String> targets = new HashSet<String>();
	
	public DependencyHandler(){
		this.setType(DependencyTarget.NONE);
		this.setCondition(DependencyCondition.NONE);
	}
	
	public DependencyHandler(DependencyTarget dType, DependencyCondition dCondition){
		this.setType(dType);
		this.setCondition(dCondition);
	}
	
	public void add(String qualifiedName){
		this.targets.add(qualifiedName);
	}
	
	public void setTargets(Set<String> names){
		this.targets = names;
	}
	
	public void setTargets(List<String> names){
		this.targets = new HashSet<String>();
		this.targets.addAll(names);
	}
	
	public synchronized boolean isMet(IssueId outId){
		if ((this.targets == null) || (this.targets .size() == 0)){
			return true;
		}
		switch(this.getType()){
		case TEST_METHODS:
			return ArjunaInternal.getCentralExecState().didTestCreatorsSucceed(this.targets, outId);
		case TEST_CLASSES:
			return ArjunaInternal.getCentralExecState().didTestContainersSucceed(this.targets, outId);
		}
		return true;
	}
	
	public DependencyHandler clone(){
		DependencyHandler dep = new DependencyHandler();
		dep.setType(this.dType);
		dep.setCondition(this.dCondition);
		dep.setTargets(this.targets);
		return dep;
	}

	public DependencyCondition getCondition() {
		return dCondition;
	}

	public void setCondition(DependencyCondition dCondition) {
		this.dCondition = dCondition;
	}

	private DependencyTarget getType() {
		return dType;
	}

	public void setType(DependencyTarget dType) {
		this.dType = dType;
	}
	
}
