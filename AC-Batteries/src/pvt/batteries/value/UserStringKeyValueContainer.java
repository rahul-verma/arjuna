package pvt.batteries.value;

import arjunasdk.console.Console;
import arjunasdk.exceptions.StringKeyValueContainerLookUpException;
import arjunasdk.interfaces.Value;

public class UserStringKeyValueContainer extends DefaultStringKeyValueContainer{

	public UserStringKeyValueContainer clone() {
		UserStringKeyValueContainer map = new UserStringKeyValueContainer();
		try {
			map.cloneAdd(this.items());
		} catch (Exception e) {
			Console.displayExceptionBlock(e);
		}
		return map;
	}
	
	@Override
	protected Value getValueForNonExistentKey(String key) throws Exception {
		throw new StringKeyValueContainerLookUpException(key);
	}

	@Override
	protected String getStrValueForNonExistentKey(String key) throws Exception {
		throw new StringKeyValueContainerLookUpException(key);
	}

}
