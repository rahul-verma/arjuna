package pvt.batteries.webserver;

import java.util.ArrayList;
import java.util.List;

import org.eclipse.jetty.server.Handler;
import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.server.handler.ContextHandlerCollection;
import org.eclipse.jetty.servlet.DefaultServlet;
import org.eclipse.jetty.servlet.ServletContextHandler;

public abstract class BaseWebServer implements ArjunaWebServer {
	private List<Handler> handlers = new ArrayList<Handler>();
	private Server server = null;
	
	public BaseWebServer(int port) throws Exception{
		this.setServer(new Server(port));
		ServletContextHandler context = new ServletContextHandler(ServletContextHandler.SESSIONS);
		context.setContextPath("/static/root");
		context.setResourceBase(BaseWebServer.class.getClassLoader().getResource("com/arjunapro/pvt/resources").toExternalForm());
		context.addServlet(DefaultServlet.class, "/");
		this.handlers.addAll(this.getHandlers());
		this.registerHandlers(handlers);
	}
	
//	private void addHandler(ServletContextHandler handler) throws Exception{
//		handlers.add(handler);
//	}
	
	protected abstract List<Handler> getHandlers() throws Exception;
	
	private void registerHandlers(List<Handler> handlers){
		 ContextHandlerCollection contexts=new ContextHandlerCollection();
		 contexts.setHandlers(handlers.toArray(new Handler[handlers.size()]));
		 server.setHandler(contexts);		
	}
	
	public void launch() throws Exception {
        server.start();
        server.join();
	}

	private Server getServer() {
		return server;
	}

	private void setServer(Server server) {
		this.server = server;
	}
}
