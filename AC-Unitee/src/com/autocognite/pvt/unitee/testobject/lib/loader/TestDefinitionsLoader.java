package com.autocognite.pvt.unitee.testobject.lib.loader;

import com.autocognite.pvt.batteries.discoverer.DiscoveredFile;

public interface TestDefinitionsLoader {

	void setTestDir(String testDir) throws Exception;

	void load(DiscoveredFile f);

	void validateDependencies() throws Exception;

}