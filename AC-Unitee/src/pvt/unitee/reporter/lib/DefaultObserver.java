package pvt.unitee.reporter.lib;

import pvt.unitee.interfaces.InternalReportableObserver;

public abstract class DefaultObserver<T> implements InternalReportableObserver<T>{

	@Override
	public void initUpdate() throws Exception {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void endUpdate() throws Exception {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void setUp() throws Exception {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void tearDown() throws Exception {
		// TODO Auto-generated method stub
		
	}

	public abstract void update(T reportable) throws Exception;

}
