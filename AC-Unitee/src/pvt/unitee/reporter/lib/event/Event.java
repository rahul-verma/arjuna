package pvt.unitee.reporter.lib.event;

import java.util.List;

import com.google.gson.JsonObject;

import pvt.unitee.enums.EventAttribute;

public class Event {
	private EventProperties props = null;
	
	public Event(EventProperties props) throws Exception{
		this.props = props;
	}
	
	public EventProperties infoProps() throws Exception {
		return this.props;
	}

	public void setText(String text) {
		this.props.setText(text);
	}

	public void setComponent(String component) {
		this.props.setComponent(component);
	}
	
	public List<String> infoPropStrings(List<EventAttribute> props) throws Exception {
		return this.infoProps().strings(props);
	}
	
	public JsonObject asJsonObject() throws Exception{
		EventSerializer serializer = new EventSerializer();
		return serializer.process(this);
	}
	
}