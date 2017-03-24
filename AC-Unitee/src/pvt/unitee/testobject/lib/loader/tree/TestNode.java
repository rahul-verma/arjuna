package pvt.unitee.testobject.lib.loader.tree;

import java.util.List;

import pvt.unitee.testobject.lib.definitions.JavaTestMethodDefinition;

public interface TestNode {
	boolean isDummy();

	public void addEdge(TestNode node);

	public List<TestNode> getEdges();

	public JavaTestMethodDefinition getCreatorDefinition();

	public String getName();

}
