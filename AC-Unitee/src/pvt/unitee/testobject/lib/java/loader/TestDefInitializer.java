package pvt.unitee.testobject.lib.java.loader;

import pvt.batteries.discoverer.DiscoveredFile;

public interface TestDefInitializer {

	void init(String testDir) throws Exception;

	void handle(DiscoveredFile f);

	void load();

}