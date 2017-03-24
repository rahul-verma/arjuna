package pvt.batteries.networker.lib.http;

public class AcHttpRequests {
	
	public static AcHttpRequester createDefaultRequester(){
		return new AcHttpRequesterBuilder().build();
	}
	
	public static AcHttpRequesterBuilder createCustomRequester(){
		return new AcHttpRequesterBuilder();
	}
}
