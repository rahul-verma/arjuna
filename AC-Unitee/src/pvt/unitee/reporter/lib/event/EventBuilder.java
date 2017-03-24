package pvt.unitee.reporter.lib.event;

import pvt.arjunapro.enums.EventAttribute;
import pvt.batteries.utils.ExceptionBatteries;
import pvt.batteries.value.BooleanValue;
import pvt.batteries.value.StringValue;

public class EventBuilder {
	private EventProperties props = new EventProperties();

	public EventBuilder activity(String activity) throws Exception {
		this.props.add(EventAttribute.TEXT, new StringValue(activity));
		return this;
	}	
	
	public EventBuilder component(String component) throws Exception {
		this.props.add(EventAttribute.COMPONENT, new StringValue(component));
		return this;
	}
	
	public EventBuilder suceedeed(boolean flag) throws Exception {
		this.props.add(EventAttribute.SUCCESS, new BooleanValue(flag));
		return this;
	}
	
	public EventBuilder remarks(String remarks) throws Exception {
		this.props.add(EventAttribute.EXC_TRACE, new StringValue(remarks));
		return this;
	}

	public EventBuilder message(String msg) throws Exception {
		this.props.add(EventAttribute.EXC_MSG, new StringValue(msg));
		return this;
	}	

	public EventBuilder trace(String trace) throws Exception {
		this.props.add(EventAttribute.EXC_TRACE, new StringValue(trace));
		return this;
	}
	
	public EventBuilder thread(String thread) throws Exception {
		this.props.add(EventAttribute.EXC_TRACE, new StringValue(thread));
		return this;
	}
	
	public EventBuilder exception(Throwable e) throws Exception {
		this.message(e.getMessage());
		this.trace(ExceptionBatteries.getStackTraceAsString(e));
		return this;
	}
	
	public EventBuilder props(EventProperties props){
		this.props = props;
		return this;
	}

	public Event build() throws Exception {
		return new Event(this.props);
	}
}
