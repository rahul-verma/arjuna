package pvt.batteries.ddt.datarecord;

import com.arjunapro.ddt.interfaces.DataSource;

public abstract class BaseDataSource implements DataSource {
	private String name = null;
	private boolean ended = false;

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}
	
	public void terminate(){
		this.ended = true;
	}
	
	@Override
	public boolean isTerminated(){
		return this.ended;
	}
	
	@Override
	public void validate() throws Exception {
		// TODO Auto-generated method stub
		
	}
}
