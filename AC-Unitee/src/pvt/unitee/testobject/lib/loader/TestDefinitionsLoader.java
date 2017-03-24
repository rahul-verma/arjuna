package pvt.unitee.testobject.lib.loader;

import pvt.batteries.discoverer.DiscoveredFile;

public interface TestDefinitionsLoader {

	void setTestDir(String testDir) throws Exception;

	void load(DiscoveredFile f);

	void validateDependencies() throws Exception;

}