package com.autocognite.pvt.unitee.testobject.lib.loader.session;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.pvt.batteries.value.DefaultStringKeyValueContainer;
import com.autocognite.pvt.unitee.core.lib.exception.SessionNodesFinishedException;

public abstract class BaseSession implements Session {
	private static Logger logger = RunConfig.getCentralLogger();
	private List<SessionNode> nodesQueue = new ArrayList<SessionNode>(); 
	private Iterator<SessionNode> iter = null;
	private int testMethodCount = 0;
	private String name = null;
	private DefaultStringKeyValueContainer udvars = new DefaultStringKeyValueContainer();
	
	public BaseSession(String name){
		this.name = name;
	}
	
	public void load() throws Exception{
		logger.debug(String.format("Session %s - Loading", this.getName()));
		BaseSessionNode beginNode = new BaseSessionNode(this, 1, "mbnode", "mbgroup");
		nodesQueue.add(0, beginNode);
		BaseSessionNode endNode = new BaseSessionNode(this, nodesQueue.size() + 1, "mlnode", "mlgroup");
		endNode.setName("mlnode");
		nodesQueue.add(endNode);
		logger.debug(String.format("%s: Loading nodes", this.getName()));
		for (SessionNode node: this.nodesQueue){
			logger.debug("Session Node: " + node.getName());
			node.load();
			this.testMethodCount += node.getTestMethodCount();
		}
		iter = nodesQueue.iterator();
	}
	
	public void addNode(BaseSessionNode node){
		this.nodesQueue.add(node);
	}
	
	@Override
	public int getTestMethodCount() {
		return this.testMethodCount;
	}

	@Override
	public SessionNode next() throws Exception {
		if (iter.hasNext()){
			return iter.next();
		} else {
			throw new SessionNodesFinishedException();
		}
	}
	
	public String getName() {
		return this.name;
	}
	
	@Override
	public void setUDVs(DefaultStringKeyValueContainer udvs){
		udvars = udvs;
	}
	
	@Override 	
	public DefaultStringKeyValueContainer getUDV(){
		return this.udvars;
	}
}