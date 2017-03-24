package pvt.unitee.testobject.lib.loader.session;

import pvt.batteries.value.DefaultStringKeyValueContainer;

public interface SessionNode {

	int getTestMethodCount();

	void load() throws Exception;

	String getName();

	int getGroupThreadCount();

	SessionSubNode next() throws Exception;

	int getId();

	Session getSession();

	void setName(String name);

	DefaultStringKeyValueContainer getUTV();
}
