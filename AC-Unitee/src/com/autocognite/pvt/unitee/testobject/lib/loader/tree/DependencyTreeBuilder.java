package com.autocognite.pvt.unitee.testobject.lib.loader.tree;

import java.lang.annotation.Annotation;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.annotations.ClassDependency;
import com.autocognite.arjuna.annotations.MethodDependency;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.batteries.config.Batteries;
import com.autocognite.pvt.unitee.core.lib.annotate.None;
import com.autocognite.pvt.unitee.testobject.lib.definitions.JavaTestClassDefinition;
import com.autocognite.pvt.unitee.testobject.lib.definitions.JavaTestMethodDefinition;
import com.autocognite.pvt.unitee.testobject.lib.definitions.TestDefinitionsDB;

public class DependencyTreeBuilder {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	TestNode baseNode = null;
	Set<String> allFilteredMethods = new HashSet<String>();
	HashMap<String, TestMethodNode> allNodesMap = new HashMap<String, TestMethodNode>();
	
	ArrayList<TestNode> resolved = new ArrayList<TestNode>();
	Set<TestNode> resolvedSet = new HashSet<TestNode>();
	ArrayList<TestNode> unresolved = new ArrayList<TestNode>();
	Set<TestNode> unResolvedSet = new HashSet<TestNode>();
	
	public DependencyTreeBuilder(){
		this.baseNode = new NonTestNode("Dummy");
	}
	
	private void addSingleMethodDependencyEdge(String dependentMethodQualifiedName, String dependencyMethodQualifiedName){	
		if (ArjunaInternal.displayDependencyDefInfo){
			logger.debug("Dependent: " + dependentMethodQualifiedName);
			logger.debug("Dependency: " + dependencyMethodQualifiedName);
			logger.debug(String.format("Adding dependency edge %s for: %s", dependencyMethodQualifiedName, dependentMethodQualifiedName));
		}
		allNodesMap.get(dependentMethodQualifiedName).addEdge(allNodesMap.get(dependencyMethodQualifiedName));
	}
	
	private List<String> addDependencyEdgesForClassesDependency(JavaTestMethodDefinition dependentMethodDef, String dependentMethodQualifiedName, ClassDependency depAnn) throws Exception{
		List<String> processedClassDeps = new ArrayList<String>();
		for (Class<?> dependencyClass: depAnn.testClasses()){
			JavaTestClassDefinition depClassDef = DependencyUtils.getClassDefForDependencyClass(dependentMethodQualifiedName, dependencyClass);
			if (depClassDef == null){
				continue;
			}
			
			processedClassDeps.add(dependencyClass.getName());
			for(String dependencyMethodName: depClassDef.getTestMethodQueue()){
				addSingleMethodDependencyEdge(dependentMethodQualifiedName, dependencyClass.getName() + "." + dependencyMethodName);
			}
		}
		return processedClassDeps;
	}

	private List<String> addDependencyEdgesForMethodDependency(JavaTestMethodDefinition dependentMethodDef, String dependentMethodQualifiedName, MethodDependency depAnn, List<String> dependencyMethodNames) throws Exception{
		List<String> processedDepMethodNames =  new ArrayList<String>();
//		Dependency dep = new Dependency(DependencyType.TEST_METHODS, DependencyCondition.NO_ISSUES);
		
		Class<?> containerClass = depAnn.containerClass();
		JavaTestClassDefinition depClassDef = null;
		if (containerClass == None.class){
			containerClass = dependentMethodDef.getClassDefinition().getUserTestClass();
			depClassDef = dependentMethodDef.getClassDefinition();
		} else {
			depClassDef = DependencyUtils.getClassDefForDependencyClass(dependentMethodQualifiedName, containerClass);
		}
		
		if (depClassDef == null){
			return processedDepMethodNames;
		}
		
		DependencyUtils.validateDependencyMethodNames(dependentMethodQualifiedName, depClassDef, dependencyMethodNames);

		for (String dependencyMethodName: dependencyMethodNames){
			String dependencyMethodQualifiedName = containerClass.getName() + "." + dependencyMethodName;
			if (ArjunaInternal.displayDefProcessingInfo){
				logger.debug("Adding: " + dependencyMethodQualifiedName);
			}
			addSingleMethodDependencyEdge(dependentMethodQualifiedName, dependencyMethodQualifiedName);
			processedDepMethodNames.add(dependencyMethodQualifiedName);
		}

		return processedDepMethodNames;
	}

	public void processDependencies() throws Exception{
		if (ArjunaInternal.displayDefProcessingInfo){
			logger.debug("PROCESSING DEPENDENCIES");
		}
		
		for (String targetNodeName: this.allNodesMap.keySet()){
			if (ArjunaInternal.displayDefProcessingInfo){
				logger.debug(targetNodeName);
			}
			JavaTestMethodDefinition methodDef =  this.allNodesMap.get(targetNodeName).getCreatorDefinition();
			Method m = methodDef.getMethod();
			
			// Add parent dependencies
			if (ArjunaInternal.displayDefProcessingInfo){
				logger.debug(methodDef.getClassDefinition().getDependencyMethodNames());
			}
			for (String mName: methodDef.getClassDefinition().getDependencyMethodNames()){
				addSingleMethodDependencyEdge(methodDef.getQualifiedName(), mName);
			}
			
			for (String cName: methodDef.getClassDefinition().getDependencyClassNames()){
				if (ArjunaInternal.displayDefProcessingInfo){
					logger.debug("Parent's class dependency: " + cName);
				}
				for (String mName: TestDefinitionsDB.getContainerDefinition(cName).getTestMethodQueue()){
					if (ArjunaInternal.displayDefProcessingInfo){
						logger.debug(String.format("Parent's class dependency %s -> Method %s",cName, mName));
					}
					addSingleMethodDependencyEdge(methodDef.getQualifiedName(), cName + "." + mName);
				}
			}
			// Add self dependencies
			if (m.isAnnotationPresent(MethodDependency.class)){
				Annotation annotation = m.getAnnotation(MethodDependency.class);
				MethodDependency depAnn = (MethodDependency) annotation;
				List<String> processedDepMethodNames =  null;
				List<String> depMethodNames = Arrays.asList(DependencyUtils.getDependencyMethods(targetNodeName, depAnn));
				if (ArjunaInternal.displayDefProcessingInfo){
					logger.debug(String.format("Found dependencies for %s: %s", targetNodeName, depMethodNames));
				}

				if (depMethodNames.size() > 0){
					processedDepMethodNames = addDependencyEdgesForMethodDependency(methodDef, targetNodeName, depAnn, depMethodNames);
				}
				
				if (processedDepMethodNames != null){
					if (ArjunaInternal.displayDefProcessingInfo){
						logger.debug("Adding dependencies to Method Definition : " + processedDepMethodNames);
					}
					methodDef.addDependencyMethodNames(processedDepMethodNames);
				}
			}
			
			// Add self dependencies
			if (m.isAnnotationPresent(ClassDependency.class)){
				Annotation annotation = m.getAnnotation(ClassDependency.class);
				ClassDependency depAnn = (ClassDependency) annotation;
				List<String> processedClassDeps = null;
				Class<?>[] depClasses = DependencyUtils.getDependencyClasses(targetNodeName, depAnn);
				if (ArjunaInternal.displayDefProcessingInfo){
					logger.debug(String.format("Found class dependencies type annotation for %s: %s.", targetNodeName, Arrays.toString(depClasses)));
				}
				
				if (depClasses.length > 0){
					processedClassDeps = this.addDependencyEdgesForClassesDependency(methodDef, targetNodeName, depAnn);
				}
				
				if (processedClassDeps.size() != 0){
					if (ArjunaInternal.displayDefProcessingInfo){
						logger.debug("Adding Class dependencies to Method Definition : " + processedClassDeps);
					}
					methodDef.addDependencyClassNames(processedClassDeps);
				}					
			}

			this.baseNode.addEdge(allNodesMap.get(targetNodeName));
		}
		if (ArjunaInternal.displayDefProcessingInfo){
			logger.debug("Deps processed.");
		}
	}

	public void validate() throws Exception{
		this.resolveDeps(this.baseNode);
		if (ArjunaInternal.displayDefProcessingInfo){
			logger.debug("Dependency definitions are ok.");
		}
	}
	
	public void addFilteredCreator(String name){
		this.allFilteredMethods.add(name);
	}
	
	public boolean isCreatorFiltered(String name){
		return this.allFilteredMethods.contains(name);
	}

	public void createNode(String name, JavaTestMethodDefinition methodDef){
		TestMethodNode node = new TestMethodNode(methodDef.getQualifiedName(), methodDef);
		this.allNodesMap.put(methodDef.getQualifiedName(), node);
	}

	private void resolveDeps(TestNode node) throws Exception{
		unResolvedSet.add(node);
//		logger.debug("Now looping on node edges. #Edges =" + node.getEdges().size());
		if (node.getEdges().size() > 0){
			for (TestNode edge: node.getEdges()){
//				logger.debug("Check edge: " + edge.getName());
				if (edge == null) continue;
				if (!resolvedSet.contains(edge)){
					if (unResolvedSet.contains(edge)){
						throw new Exception (String.format("Circular reference: %s %s", node.getName(), edge.getName()));
					}
					resolveDeps(edge);
				}
			}
		}
		resolved.add(node);
		resolvedSet.add(node);
		unResolvedSet.remove(node);	
	}
	
	public synchronized DependencyTree getDepenencyTree(List<String> methodNames){
		Map<String, TestMethodNode> nodeMap = new HashMap<String,TestMethodNode>();
		if (ArjunaInternal.displayExecTreeLoadingInfo){
			logger.debug("Now creating execution tree");
			logger.debug("Creator List: " + methodNames);
			logger.debug("Creating Test Node clones");
		}
		
		for (String name: methodNames){
			if (ArjunaInternal.displayExecTreeLoadingInfo){
				logger.debug("Cloning: " + name);
			}			
			TestMethodNode sourceNode = this.allNodesMap.get(name);
			nodeMap.put(name, new TestMethodNode(sourceNode.getName(), sourceNode.getCreatorDefinition()));			
		}
		
		if (ArjunaInternal.displayExecTreeLoadingInfo){
			logger.debug(nodeMap);
		}	
		// Now add Edges for the methods in current group, ignore others
		if (ArjunaInternal.displayExecTreeLoadingInfo){
			logger.debug("Loading Edges");
		}	
		for (String name: methodNames){
			if (ArjunaInternal.displayExecTreeLoadingInfo){
				logger.debug(name);
			}			
			TestMethodNode targetNode = nodeMap.get(name);
			TestMethodNode sourceNode = this.allNodesMap.get(name);

			for (TestNode edge: sourceNode.getEdges()){
				if (ArjunaInternal.displayExecTreeLoadingInfo){
					logger.debug("Edge: " + edge);
				}
				if (edge == null) continue;
				if (nodeMap.containsKey(edge.getName())){
					TestMethodNode edgeNode = nodeMap.get(edge.getName());
					targetNode.addEdge(edgeNode);
				}
			}		
		}	
		
		return new DependencyTree(methodNames, nodeMap);
	}
}

