package com.autocognite.pvt.unitee.testobject.lib.loader.session;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import com.autocognite.batteries.console.Console;
import com.autocognite.batteries.value.StringKeyValueContainer;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.batteries.config.Batteries;
import com.autocognite.pvt.batteries.hocon.HoconReader;
import com.autocognite.pvt.batteries.hocon.HoconStringReader;
import com.autocognite.pvt.unitee.core.lib.exception.SubTestsFinishedException;
import com.autocognite.pvt.unitee.testobject.lib.loader.group.Group;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

public class BaseSessionNode implements SessionNode{
	private List<SessionSubNode> groupNodes = new ArrayList<SessionSubNode>();
	private int testMethodCount = 0;
	private int groupThreads = 1;
	private String name = null;
	private int id;
	private Iterator<SessionSubNode> iter = null;
	private Session session = null;
	private StringKeyValueContainer udvars = new StringKeyValueContainer();
	
	private BaseSessionNode(Session session, int id) throws Exception{
		this.session = session;
		this.id = id;		
		this.name = String.format("node%d", id);
		this.udvars.cloneAdd(session.getUDV().items());
	}
	
	public BaseSessionNode(Session session, int id, String groupName) throws Exception{
		this(session, id);
		this.addGroupNode(groupName);
	}
	
	public BaseSessionNode(Session session, int id, String nodeName, String groupName) throws Exception{
		this(session, id);
		this.addGroupNode(groupName);
	}
	
	public BaseSessionNode(Session session, int id, JsonObject nodeObj) throws Exception{
		this(session, id);
		
		try{
			JsonObject udv = nodeObj.getAsJsonObject("udv");
			HoconReader udvReader = new HoconStringReader(udv.toString());
			udvReader.process();
			this.udvars.add(udvReader.getProperties());
		} catch (ClassCastException e){
			this.errorUdvNotObject();
		} catch (NullPointerException e){
			// do nothing
		}
		
		String nodeName = null;
		try{ 
			nodeName = nodeObj.getAsJsonPrimitive("name").getAsString();
		} catch (ClassCastException e){
			this.existAsNameIsNotString();
		} catch (NullPointerException e){
			nodeName = String.format("node%d", id);
		}
		
		this.setName(nodeName);
		
		int groupThreads = 1;
		try{ 
			groupThreads = nodeObj.getAsJsonPrimitive("groupThreads").getAsInt();
		} catch (NumberFormatException e){
			this.existAsGroupThreadsIsNotInt();
		} catch (ClassCastException e){
			this.existAsGroupThreadsIsNotInt();
		} catch (NullPointerException e){
			// Do nothing. Default is 1
		}

		JsonArray groupsArray = null;
		try{
			groupsArray = nodeObj.getAsJsonArray("groups");
		} catch (ClassCastException e){
			exitAsAttrNotAnArray("node in nodes array", "groups");
		}
		if (groupsArray == null){
			exitAsAttrIsNull("node in nodes array", "groups");		
		}
		if (groupsArray.size() == 0){
			exitAsAttrIsEmptyArray("node in nodes array", "groups");			
		}
		
		for (JsonElement groupElement: groupsArray){
			JsonObject groupObj = null;
			String groupName = null;
			try{
				groupObj = groupElement.getAsJsonObject();
				this.addGroupNode(groupObj);
			} catch (Exception e){
				try{
					groupName =  groupElement.getAsString();
					this.addGroupNode(groupName);
				} catch (Exception f){
					existAsInvalidGroupNodeSupplied();
				}
			}
		}
		
		this.setGroupThreadCount(groupThreads);
	}
	
	private void errorUdvNotObject(){
			Console.displayError(
					String.format(
							">>udv<< attribute in session node definition should be a JSON object. Fix session template file: >>%s<<",
							session.getSessionFilePath()
					));			
			Console.displayError("Exiting...");
			System.exit(1);			
	}
		
	private void existAsNameIsNotString(){
		Console.displayError(
				String.format(
						">>name<< attribute in session node definition should be a string. Fix session template file: >>%s<<",
						session.getSessionFilePath()
				));			
		Console.displayError("Exiting...");
		System.exit(1);			
	}
	
	private void existAsGroupThreadsIsNotInt(){
		Console.displayError(
				String.format(
						">>groupThreads<< attribute in session node definition can only be an Integer. Fix session template file: >>%s<<",
						session.getSessionFilePath()
				));			
		Console.displayError("Exiting...");
		System.exit(1);			
	}
	
	private void existAsInvalidGroupNodeSupplied(){
		Console.displayError(
				String.format(
						">>groupNodes<< attribute can only contain a queue of either group names or group node json object.Fix session template file: >>%s<<",
						session.getSessionFilePath()
				));			
		Console.displayError("Exiting...");
		System.exit(1);			
	}
	
	private void exitAsAttrNotAnArray(String subjectName, String attr){
		Console.displayError(
				String.format(
						"A %s must define >>%s<< as an array. Fix session template file: >>%s<<",
						subjectName,
						attr,
						session.getSessionFilePath()
				));			
		Console.displayError("Exiting...");
		System.exit(1);			
	}
	
	private void exitAsAttrIsNull(String subjectName, String attr){
		Console.displayError(
				String.format(
						"A %s must have a >>%s<< attribute. Fix session template file: >>%s<<",
						subjectName,
						attr,
						session.getSessionFilePath()
				));			
		Console.displayError("Exiting...");
		System.exit(1);			
	}
	
	private void exitAsAttrIsEmptyArray(String subjectName, String attr){
		Console.displayError(
				String.format(
						"A %s must have non-empty >>%s<< array. Fix session template file: >>%s<<",
						subjectName,
						attr,
						session.getSessionFilePath()
				));			
		Console.displayError("Exiting...");
		System.exit(1);			
	}
	
	public void load() throws Exception{
		for (SessionSubNode groupNode: this.groupNodes){
			groupNode.load();
			this.testMethodCount += groupNode.getTestMethodCount();
		}
		
		iter = this.groupNodes.iterator();
	}
	
	public void addGroupNode(Group group) throws Exception {
		this.groupNodes.add(new BaseSessionSubNode(this, this.groupNodes.size() + 1, group));
	}
	
	public void addGroupNode(String groupName) throws Exception {
		this.groupNodes.add(new BaseSessionSubNode(this, this.groupNodes.size() + 1, groupName));
	}
	
	public void addGroupNode(JsonObject groupJsonObj) throws Exception {
		this.groupNodes.add(new BaseSessionSubNode(this, this.groupNodes.size() + 1, groupJsonObj));
	}

	@Override
	public int getTestMethodCount() {
		return this.testMethodCount;
	}

	public void setGroupThreadCount(int count) {
		this.groupThreads = count;
	} 

	@Override
	public String getName() {
		return this.name;
	}
	
	@Override
	public void setName(String name) {
		this.name = name;
	}

	@Override
	public int getGroupThreadCount() {
		return this.groupThreads;
	}

	@Override
	public SessionSubNode next() throws Exception {
		if (this.iter.hasNext()){
			return this.iter.next();
		} else {
			throw new SubTestsFinishedException();
		}
	}

	@Override
	public int getId() {
		return this.id;
	}

	@Override
	public Session getSession() {
		return this.session;
	}

	@Override
	public StringKeyValueContainer getUDV() {
		return this.udvars;
	} 
}
