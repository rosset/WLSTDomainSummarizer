# Prototype Script to perform WLST online collection of managed server config MBeans
# The script retrieves a selection of config and runtime MBeans values. The values are printed as part of a HTML file which is built dynamically by this script.
# Author: Daniel Mortimer
# Proactive Support Delivery
# Date: 7th May 2013
# Version 001

#IMPORTS

# import types;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import os;
import string;
from java.lang import *
from java.util import Date


# START OF FUNCTIONS

# function to help locate whether MBean directory exists. 
# This does not perform a global search. It just checks whether a given MBean directory exists at the level the script is currently in 
def findMBean(v_pattern):
        # get a listing of everything in the current directory
	mydirs = ls(returnMap='true');
 
        v_compile_pattern = java.util.regex.Pattern.compile(v_pattern);
	
	found = 'Nope not here';
        
	for mydir in mydirs:
		x = java.lang.String(mydir);
		v_matched = v_compile_pattern.matcher(x);
		if v_matched.find():
			found = 'true';
                 
        return found;

# function to strip the Bean Value which is returned as tuple (list). 
# We only want to return and print the target name and type

		
def stripMBeanValue (v_mbeanvalue,v_type):
	
	v_check_value = str(v_mbeanvalue);
	v_strippedValue01 = String.replace(v_check_value,'[MBeanServerInvocationHandler]','');
	v_strippedValue02 = String.replace(v_strippedValue01,'com.bea:Name=','');
	#v_strippedValue03 = "Strip Function Failed";
	
	if v_type == 'Cluster':
		v_strippedValue = String.replace(v_strippedValue02,',Type=Cluster','');
	
	if v_type == 'Machine':
		v_strippedValue = String.replace(v_strippedValue02,',Type=Machine','');
		
	if v_type == 'JDBC_Server':
		v_strippedValue03 = String.replace(v_strippedValue02,'Location=','');
		v_strippedValue04 = String.replace(v_strippedValue03,',Type=ServerRuntime','');
		v_strippedValue05 = String.replace(v_strippedValue04,',',' ');
		v_strippedValue = v_strippedValue05.split();
		# Pick v_strippedValue[1]	
	
	if v_type == 'JDBC_DataSource':
		
		v_strippedValue03 = String.replace(v_strippedValue02,'com.bea:ServerRuntime=','');
		v_strippedValue04 = String.replace(v_strippedValue03,'Name=','');
		v_strippedValue05 = String.replace(v_strippedValue04,',Type=JDBCDataSourceRuntime','');
		v_strippedValue06 = String.replace(v_strippedValue05,',',' ');
		v_strippedValue = v_strippedValue06.split();	
		# Pick v_strippedValue[1]	
		
	if v_type == 'HealthCheck':
		
		v_strippedValue03 = String.replace(v_strippedValue02,'Component:ServerRuntime,State:','');
		v_strippedValue04 = String.replace(v_strippedValue03,'MBean:','');
		v_strippedValue05 = String.replace(v_strippedValue04,'Component:','');
		v_strippedValue06 = String.replace(v_strippedValue05,'null','');
		v_strippedValue07 = String.replace(v_strippedValue06,'State:','');
		v_strippedValue08 = String.replace(v_strippedValue07,'ReasonCode:[]','');
		v_strippedValue09 = String.replace(v_strippedValue08,',',' ');
		v_strippedValue = v_strippedValue09.split();
		
	if v_type == 'Target':
		
		v_strippedValue03 = String.replace(v_strippedValue02,'array(weblogic.management.configuration.TargetMBean,','');
		v_strippedValue04 = String.replace(v_strippedValue03,'[[MBeanServerInvocationHandler]','');
		v_strippedValue05 = String.replace(v_strippedValue04,'com.bea:Name=','');
		v_strippedValue06 = String.replace(v_strippedValue05,'array(javax.management.ObjectName,[','');
		v_strippedValue07 = String.replace(v_strippedValue06,'Type=','');
		v_strippedValue08 = String.replace(v_strippedValue07,'])','');
		v_strippedValue09 = String.replace(v_strippedValue08,',',' ');
		v_strippedValue = v_strippedValue09.split();
		
	if v_type == 'JMSStore':
	
		v_strippedValue03 = String.replace(v_strippedValue02,'com.bea:Name=','');
		v_strippedValue04 = String.replace(v_strippedValue03,'Type=','');
		v_strippedValue05 = String.replace(v_strippedValue04,',',' ');
		v_strippedValue = v_strippedValue05.split();
		
	if v_type == 'ThreadPool':
	
		v_strippedValue03 = String.replace(v_strippedValue02,'Component:threadpool,State:','');
		v_strippedValue04 = String.replace(v_strippedValue03,'Component:null,State:','');
		v_strippedValue05 = String.replace(v_strippedValue04,',MBean:ThreadPoolRuntime','');
		v_strippedValue = String.replace(v_strippedValue05,'MBean:null,','');
		#v_strippedValue05 = String.replace(v_strippedValue04,',',' ');
		#v_strippedValue = v_strippedValue05.split();
		
	if v_type == 'AppHealth':

		v_strippedValue03 = String.replace(v_strippedValue02,'Component:null,State:','');
		v_strippedValue04 = String.replace(v_strippedValue03,'MBean:null,','');
		v_strippedValue05 = String.replace(v_strippedValue04,',',' ');
		v_strippedValue = v_strippedValue05.split();
					
	
	return v_strippedValue;		

# END OF FUNCTIONS

# START OF SCRIPT

#Some WLST commands throw output to stdout
#For a cleaner user experience we redirect that stuff to log.
#Only print commands will display to the console - print >>f commands are redirecting to the HTML output file


redirect('wlstonlinedomainsummarizer.log', 'false');


v_domainHome = os.environ["DOMAIN_HOME"];
v_outputFilePath = os.environ["WLST_OUTPUT_PATH"];
v_outputFile = os.environ["WLST_OUTPUT_FILE"];


#Start in Domain Config to get some top level domain information
domainConfig();


# OPEN the output HTML file and start to write to it

f = open(v_outputFilePath  + v_outputFile, 'w');

# BUILD the HTML, header includes javascript and css to enable table styling and sorting

print >>f, "<html>"

print >>f, "<head>"

print >>f, "<script src=\"spry.js\"></script>"
print >>f, "<script type=\"text/javascript\" src=\"jquery-ui.js\"></script>"
print >>f,"<link href=\"WLSTSummarizer.css\" type=\"text/css\" rel=\"stylesheet\">"


print >>f, "</head>"

print >>f, "<body>"


print >>f, "<div id=\"divContainer\">"
print >>f, "<h1 class=\"headline3\">Introduction</h1>"
print >>f, "<p>This is the output from a WLST script run in <u><strong>ONLINE mode</strong></u>. The script retrieves a selection of configuration and runtime MBean values. It is intended to provide a high level summary of a given WebLogic domain.</p>"
print >>f, "<p>Note: Make sure the spry.js, jquery-ui.js and WLSTSummarizer.css are located in same local directory as this HTML file"
print >>f, "</p>"
print >>f, "</div>"
print >>f, "<p></p>"


print >>f, "<div id=\"divContainer\">"
print >>f, "<p></p>"
print >>f, "<div id=\"TabbedPanels001\" class=\"TabbedPanels\">"
print >>f,  "<ul class=\"TabbedPanelsTabGroup\">"
print >>f, "<li class=\"TabbedPanelsTab\" tabindex=\"0\">Domain</li>"
print >>f,  "<li class=\"TabbedPanelsTab\" tabindex=\"0\">Servers, Clusters and Machines</li>"
print >>f,  "<li class=\"TabbedPanelsTab\" tabindex=\"0\">Application Runtime</li>"
print >>f,	"<li class=\"TabbedPanelsTab\" tabindex=\"0\">JDBC</li>"
print >>f, "<li class=\"TabbedPanelsTab\" tabindex=\"0\">JMS</li></ul>"
print >>f, "<div class=\"TabbedPanelsContentGroup\">"	
print >>f, "<div class=\"TabbedPanelsContent\">"

# From Top of Domain MBean Tree, obtain some high level domain attributes.

print "++++++++++++++++++++++++++"
print "Obtaining Domain Top Level Information"
print "++++++++++++++++++++++++++"

print >>f, "<h3 class=\"headline1\">Top Level Information</h3>"
print >>f, "<p>"
print >>f, "</p>"

print >>f, "<table id=\"my_TopLevelDomain_Table\" border=\"1\" class=\"formatHTML5\">"
print >>f, "<thead align=\"left\">"
print >>f, "<tr>"
print >>f, "<th>Domain Name</th>"
print >>f, "<th>Version</th>"
print >>f, "<th>Production Mode Enabled?</th>"
print >>f, "<th>Console Enabled?</th>"
print >>f, "<th>Console Context Path</th>"
print >>f, "</tr>"
print >>f,"</thead>"
print >>f, "<tbody>"

v_DomainName = get('Name');
v_DomainVersion = get('DomainVersion');
v_DomainHome = get('RootDirectory');

v_ProductionModeEnabled = get('ProductionModeEnabled');

if v_ProductionModeEnabled == 0:
	v_ProductionModeEnabled = 'False';
else:
	v_ProductionModeEnabled = 'True';

v_ConsoleEnabled = get('ConsoleEnabled');

if v_ConsoleEnabled == 0:
	v_ConsoleEnabled = 'False';
else:
	v_ConsoleEnabled = 'True';

v_ConsoleContextPath = get('ConsoleContextPath');

print >>f, "<td>"
print >>f, v_DomainName;
print >>f, "</td>"

print >>f, "<td>"
print >>f, v_DomainVersion;
print >>f, "</td>"

print >>f, "<td>"
print >>f, v_ProductionModeEnabled;
print >>f, "</td>"

print >>f, "<td>"
print >>f, v_ConsoleEnabled;
print >>f, "</td>"

print >>f, "<td>"
print >>f, v_ConsoleContextPath;
print >>f, "</td>"


print >>f, "</tbody></table>"
print >>f, "<p></p>"

print >>f, "</div>"

# CHANGE to the Server MBean tree, loop through the servers printing a selection of MBean values

print ""
print "++++++++++++++++++++++++++"
print "Obtaining managed servers configuration information"
print "++++++++++++++++++++++++++"
print ""

print >>f, "<div class=\"TabbedPanelsContent\">"


print >>f, "<h3 class=\"headline1\">All Servers</h3>"
print >>f, "<p>"
print >>f, "</p>"



print >>f, "<table id=\"my_Server1_Table\" border=\"1\" class=\"formatHTML5\">"
print >>f, "<thead align=\"left\">"
print >>f, "<tr>"
print >>f, "<th rowspan=2>Server Name</th>"
print >>f, "<th rowspan=2>Status</th>"
print >>f, "<th rowspan=2>Health State</th>"
print >>f, "<th rowspan=2>Cluster</th>"
print >>f, "<th rowspan=2>Machine</th>"
print >>f, "<th colspan=3>Default Network Info</th>"
print >>f, "<th colspan=4>Custom Network Channel</th>"
print >>f, "</tr>"
print >>f, "<tr>"

print >>f, "<th>Listen Address</th>"
print >>f, "<th>Listen Port</th>"
print >>f, "<th>SSL Listen Port</th>"

print >>f, "<th>Name</th>"
print >>f, "<th>Listen Address</th>"
print >>f, "<th>Protocol</th>"
print >>f, "<th>Listen Port</th>"

print >>f,"</tr>"
print >>f,"</thead>"
print >>f, "<tbody>"


# Here is where we loop through the servers in the tree,
# Note: we do not store the MBean values in an array, for simplicity we print the MBean value as soon as we have retrieved it

domainRuntime();

cd('ServerLifeCycleRuntimes');
myservers=ls(returnMap='true');
#cd ('../Servers')


for myserver in myservers:
	
	x_server = java.lang.String(myserver);
	
	
	cd(x_server);
	
	
	v_ServerState = cmo.getState();
	
	if v_ServerState != "SHUTDOWN" :
		cd ('../../ServerRuntimes')
		cd(x_server);
		v_ServerHealthState = cmo.getHealthState();
		v_ServerHealthState = stripMBeanValue(v_ServerHealthState, 'HealthCheck')[0];
		cd ('../../ServerLifeCycleRuntimes');
		cd(x_server);
	else:
		v_ServerHealthState = "n/a";	
	
	#Change to config tree to get some config info
	serverConfig();
	
	
	
	cd ('Servers');
	cd(x_server);
	
	
	v_Cluster = cmo.getCluster();
	v_Cluster = stripMBeanValue(v_Cluster, 'Cluster');
		
	v_ListenAddress = cmo.getListenAddress();
	
	if v_ListenAddress == '':
		v_ListenAddress = "All Local Addresses";
	
	v_ListenPort = cmo.getListenPort();
	
	v_Machine = cmo.getMachine();
	v_Machine = stripMBeanValue(v_Machine,'Machine');
	
	
	cd ('SSL');
	cd(x_server);
	
	v_SSL_enabled = get('Enabled');
	
	#v_check_SSLexists = findMBean('SSL');
	#v_check_CustomNetwork = findMBean('NetworkAccessPoint');
	

	# Check to see if the Server has a SSL MBean Branch .. if yes we will try to find the SSL Listen Port	
	if v_SSL_enabled == 1:
		v_SSL_ListenPort = get('ListenPort');
	else:
		v_SSL_ListenPort = "SSL not enabled";
			
	
	# We are still in serverConfig();
	cd ('../../NetworkAccessPoints');
	customNetChannels = ls(returnMap='true');
	v_no_of_netchannels = len(customNetChannels);
	
	
	if v_no_of_netchannels > 0:
		
	
	
		
		# Set a flag to help determine whether we print sub rows if there are multiple channels
		v_count03 = 'false';
			
		print >>f, "<tr>";
		print >>f, "<td rowspan=";
		print >>f, v_no_of_netchannels;
		print >>f, ">";
		print >>f, x_server;
		print >>f, "</td>";
			
		
		# Loop through the Custom Network channels and retrieve some MBean values	
		for customNetChannel in customNetChannels:
			v_CustomNetworkName = java.lang.String(customNetChannel);
			cd (v_CustomNetworkName);
			v_CustomNetworkAddress = get('ListenAddress');
			v_CustomNetworkPort = get('ListenPort');
			v_CustomProtocol = get('Protocol');
			
			if v_count03 == 'true':
				
				print >>f, "<tr>";
				print >>f, "<td>";
				print >>f, v_CustomNetworkName;
				print >>f, "</td>";
				print >>f, "<td>";
				print >>f, v_CustomNetworkAddress;
				print >>f, "</td>";
				print >>f, "<td>";
				print >>f, v_CustomProtocol;
				print >>f, "</td>";
				print >>f, "<td>";
				print >>f, v_CustomNetworkPort;
				print >>f, "</td>";
				print >>f, "</tr>";
				# Back to NetworkAccessPoints
				cd ('../');
			else:	
				
				print >>f, "<td rowspan=";
				print >>f, v_no_of_netchannels;
				print >>f, ">";
				
				if v_ServerState == 'RUNNING':
					print >>f, "<span style=\"color:green\">";
					print >>f, v_ServerState;
					print >>f, "</span>";
					print >>f, "</td>";
				
				if v_ServerState == 'FAILED':
					print >>f, "<strong><span style=\"color:red\">";
					print >>f, v_ServerState;
					print >>f, "</span></strong>";
					print >>f, "</td>";
				
				if v_ServerState == 'SHUTDOWN':
					print >>f, v_ServerState;
					print >>f, "</td>";
				
				
				if v_ServerState == 'ADMIN' or v_ServerState == 'STANDBY' or v_ServerState == 'RESUMING' or  v_ServerState == 'FORCE_SUSPENDING' or  v_ServerState == 'SUSPENDING' or  v_ServerState == 'SHUTTING DOWN':
					print >>f, "<strong><span style=\"color:orange\">"
					print >>f, v_ServerState;
					print >>f, "</span></strong>"
					print >>f, "</td>"
				
					
				
				print >>f, "</td>"
				print >>f, "<td rowspan=";
				print >>f, v_no_of_netchannels;
				print >>f, ">";
				print >>f, v_ServerHealthState;
				print >>f, "</td>"
				
				
				print >>f, "<td rowspan=";
				print >>f, v_no_of_netchannels;
				print >>f, ">";
				print >>f, v_Cluster;
				print >>f, "</td>"
					
				print >>f, "<td rowspan=";
				print >>f, v_no_of_netchannels;
				print >>f, ">";
				print >>f, v_Machine;
				print >>f, "</td>"
				
				print >>f, "<td rowspan=";
				print >>f, v_no_of_netchannels;
				print >>f, ">";
				print >>f, v_ListenAddress;
				print >>f, "</td>"
				

					
				print >>f, "<td rowspan=";
				print >>f, v_no_of_netchannels;
				print >>f, ">";
				print >>f, v_ListenPort;
				print >>f, "</td>"
				
				print >>f, "<td rowspan=";
				print >>f, v_no_of_netchannels;
				print >>f, ">";
				print >>f, v_SSL_ListenPort;
				print >>f, "</td>"
					
				print >>f, "<td>"
				print >>f, v_CustomNetworkName;
				print >>f, "</td>"
				
				print >>f, "<td>"
				print >>f, v_CustomNetworkAddress;
				print >>f, "</td>"
				
				print >>f, "<td>"
				print >>f, v_CustomProtocol;
				print >>f, "</td>"
				
				print >>f, "<td>"
				print >>f, v_CustomNetworkPort;
				print >>f, "</td>"
					
				
				print >>f, "</tr>"
				
				
				v_count03 = 'true';
				# Back to NetworkAccessPoints
				cd ('../');
		
		
		
		cd ('../../');
		
 		
	
	# If no custom network channels are found we print the entire row with null values for the custom network channel
	else:
		v_CustomNetworkName = "None";
		v_CustomNetworkAddress = "n/a";
		v_CustomNetworkPort = "n/a";
		v_CustomProtocol = "n/a";
		
		print >>f, "<tr>"
		print >>f, "<td>"
		print >>f, x_server;
		print >>f, "</td>"
		
		print >>f, "<td>"
		
		if v_ServerState == 'RUNNING':
			print >>f, "<span style=\"color:green\">";
			print >>f, v_ServerState;
			print >>f, "</span>";
			print >>f, "</td>";
			
		if v_ServerState == 'FAILED':
			print >>f, "<strong><span style=\"color:red\">";
			print >>f, v_ServerState;
			print >>f, "</span></strong>";
			print >>f, "</td>";
				
		if v_ServerState == 'SHUTDOWN':
			print >>f, v_ServerState;
			print >>f, "</td>";
				
				
		if v_ServerState == 'ADMIN' or v_ServerState == 'STANDBY' or v_ServerState == 'RESUMING' or  v_ServerState == 'FORCE_SUSPENDING' or  v_ServerState == 'SUSPENDING' or  v_ServerState == 'SHUTTING DOWN':
			print >>f, "<strong><span style=\"color:orange\">"
			print >>f, v_ServerState;
			print >>f, "</span></strong>"
			print >>f, "</td>"
		
		
		
		
		print >>f, "<td>"
		print >>f, v_ServerHealthState;
		print >>f, "</td>"
		

			
		print >>f, "<td>"
		print >>f, v_Cluster;
		print >>f, "</td>"
		
		print >>f, "<td>"
		print >>f, v_Machine;
		print >>f, "</td>"
		
		print >>f, "<td>"
		print >>f, v_ListenAddress;
		print >>f, "</td>"
		
		print >>f, "<td>"
		print >>f, v_ListenPort;
		print >>f, "</td>"
		
		print >>f, "<td>"
		print >>f, v_SSL_ListenPort;
		print >>f, "</td>"
		
		print >>f, "<td>"
		print >>f, v_CustomNetworkName;
		print >>f, "</td>"
		
		print >>f, "<td>"
		print >>f, v_CustomNetworkAddress;
		print >>f, "</td>"
		
		print >>f, "<td>"
		print >>f, v_CustomProtocol;
		print >>f, "</td>"
		
		print >>f, "<td>"
		print >>f, v_CustomNetworkPort;
		print >>f, "</td>"
		
		
		print >>f, "</tr>"
		
		cd ('../../');
		
	
	
	
	
	domainRuntime();
	cd('../');
	

print >>f, "</tbody></table>"
print >>f, "<p></p>"

# Return to MBean Tree Root
cd ('..');




# We will now print some runtime MBean values for those servers in the domain which are running

print ""
print "++++++++++++++++++++++++++"
print "Obtaining runtime data from any managed servers which are not shutdown"
print "++++++++++++++++++++++++++"
print ""


cd ('ServerRuntimes')
myservers=ls(returnMap='true');

print >>f, "<h3 class=\"headline1\">Running Servers</h3>"
print >>f, "<p>"
print >>f, "</p>"

print >>f, "<table id=\"my_Server2_Table\" border=\"1\" class=\"formatHTML5\">"
print >>f, "<thead align=\"left\">"
print >>f, "<tr>"
print >>f, "<th rowspan=2>Name</th>"
print >>f, "<th colspan=6>JVM Runtime</th>"
print >>f, "<th colspan=3>Thread Pool</th>"
print >>f, "</tr>"

print >>f, "<tr>"
print >>f, "<th>Heap Free (Mb)</th>"
print >>f, "<th>Heap Free (%)</th>"
print >>f, "<th>Heap Size Current (Mb)</th>"
print >>f, "<th>Heap Size Max (Mb)</th>"
print >>f, "<th>Java Vendor</th>"
print >>f, "<th>Java Version</th>"

print >>f, "<th>Thread Pool Health State</th>"
print >>f, "<th>Completed Requests</th>"
print >>f, "<th>Throughput</th>"
print >>f,"</tr>"

print >>f,"</thead>"
print >>f, "<tbody>"


for myserver in myservers:
	x_server = java.lang.String(myserver);
	cd (x_server);
	
	#Collect Server State
	v_ServerHealthState = cmo.getHealthState();
	v_ServerHealthState = stripMBeanValue(v_ServerHealthState, 'HealthCheck')[0];
	
	
	#Collect JVM Information
	cd ('JVMRuntime');
	cd (x_server);
	
	v_HeapFreeCurrent = int(cmo.getHeapFreeCurrent())/(1024*1024);
	v_HeapFreePercent = cmo.getHeapFreePercent();
	v_HeapSizeCurrent = int(cmo.getHeapSizeCurrent())/(1024*1024);
	v_HeapSizeMax = int(cmo.getHeapSizeMax())/(1024*1024);
	v_JavaVendor = cmo.getJavaVendor();
	v_JavaVersion= cmo.getJavaVersion();
	
	
	#Collect Thread Pool Information
	cd ('../../ThreadPoolRuntime/ThreadPoolRuntime');
	
	v_HogThread = cmo.getHoggingThreadCount();
	v_PoolHealthState = cmo.getHealthState();
	
	v_PoolHealthState = stripMBeanValue(v_PoolHealthState, 'ThreadPool');
	v_CompletedThreadRequests = cmo.getCompletedRequestCount();
	v_PoolThroughput = cmo.getThroughput();
	
	#If Server health state is "FAILED" or we see 1 or more thread hogs in the JVM
	#We will produce a more detailed table, and attempt capture a threaddump for the effected server

	if v_ServerHealthState == 'FAILED' or v_HogThread > 0:
		v_CaptureMoreThreadInfo = 'true';
	else:
		v_CaptureMoreThreadInfo = 'false';	
	
	
	#Back to root of Server Runtimes
	cd ('../../../');
	
	
	print >>f, "<tr>"
	print >>f, "<td>"
	print >>f, x_server;
	print >>f, "</td>"
	
	print >>f, "<td>";
	print >>f, v_HeapFreeCurrent;
	print >>f, "Mb"
	print >>f, "</td>";
	
	print >>f, "<td>";
	print >>f, v_HeapFreePercent;
	print >>f, "%"
	print >>f, "</td>";
	
	print >>f, "<td>";
	print >>f, v_HeapSizeCurrent;
	print >>f, "Mb"
	print >>f, "</td>";
	
	print >>f, "<td>";
	print >>f, v_HeapSizeMax;
	print >>f, "Mb"
	print >>f, "</td>";
	
	print >>f, "<td>";
	print >>f, v_JavaVendor;
	print >>f, "</td>";
	
	print >>f, "<td>";
	print >>f, v_JavaVersion;
	print >>f, "</td>";
	
	print >>f, "<td>";
	print >>f, v_PoolHealthState;
	print >>f, "</td>";
	
	print >>f, "<td>";
	print >>f, v_CompletedThreadRequests;
	print >>f, "</td>";
	
	print >>f, "<td>";
	print >>f, v_PoolThroughput;
	print >>f, "</td>";
	
	
	print >>f, "</tr>";
		
print >>f, "</tbody></table>"
print >>f, "<p></p>"
	
	
	
# Show more thread pool info if Health State is not ok
if v_CaptureMoreThreadInfo == 'true':

	
	#cd ('ServerRuntimes')
	myproblemservers=ls(returnMap='true');
	
	

	print >>f, "<h4 class=\"headline1\">More Thread Pool Information</h4>"
	print >>f, "<p>"
	print >>f, "</p>"

	print >>f, "<table id=\"my_Server3_Table\" border=\"1\" class=\"formatHTML5\">"
	print >>f, "<thead align=\"left\">"
	print >>f, "<tr>"
	print >>f, "<th rowspan=2>Server Name</th>"
	print >>f, "<th colspan=9>Thread Pool Details</th>"
	print >>f, "</tr>"

	print >>f, "<tr>"

	print >>f, "<th>Thread Runtime Health State</th>"
	print >>f, "<th>Total Threads</th>"
	print >>f, "<th>Idle Threads</th>"
	print >>f, "<th>Hogging Threads</th>"
	print >>f, "<th>Pending Threads</th>"
	print >>f, "<th>Thread Pool</th>"
	print >>f, "<th>Thread Dumps </br><i>(Taken 15 seconds apart)</i></th>"
	print >>f,"</tr>"

	print >>f,"</thead>"
	print >>f, "<tbody>"

	
	for myproblemserver in myproblemservers:
		x_problemserver = java.lang.String(myproblemserver);
		cd (x_problemserver);
		
		v_ServerHealthState = cmo.getHealthState();
		v_ServerHealthState = stripMBeanValue(v_ServerHealthState, 'HealthCheck')[0];
		
		
		if v_ServerHealthState != 'HEALTH_OK':
			
			
			print ""
			print "++++++++++++++++++++++++++"
			print "Server Health State is flagged as not OK."
			print "Obtaining three JVM thread dumps (15 second intervals) from the problem server"
			print "++++++++++++++++++++++++++"
			print ""
			
			
			
			
			cd ('ThreadPoolRuntime');
			cd ('ThreadPoolRuntime');
			v_PoolHealthState = cmo.getHealthState();
			v_PoolHealthState = stripMBeanValue(v_PoolHealthState, 'ThreadPool');
			v_CompletedThreadRequests = cmo.getCompletedRequestCount();
			v_TotalThreads = cmo.getExecuteThreadTotalCount();
			v_idleThreads = cmo.getExecuteThreadIdleCount();
			v_pendingThreads = cmo.getPendingUserRequestCount();
			v_ThreadPoolQueue = cmo.getQueueLength();
			v_HogThread = cmo.getHoggingThreadCount();
			v_PoolThroughput = cmo.getThroughput();
			
			
			counter = 0;
			sleepTime = 15000;
			threadNumber = 3;
			d= Date();

			for counter in range(threadNumber):
				currentFile = 'ThreadDump_%s_%s_%s.dmp' % (myproblemserver, d.time,counter);
				threadDump(writeToFile='true', fileName=currentFile,serverName=myproblemserver);
				currentFileRead = open(currentFile, 'r');
				currentFileRead.close();
				Thread.sleep(sleepTime);
				
				if counter == 0:
					v_ThreadDumpFile0 = currentFile;
					
				if counter == 1:
					v_ThreadDumpFile1 = currentFile;	
					
				if counter == 1:
					v_ThreadDumpFile2 = currentFile;		
				
					
			
		
			print >>f, "<tr>"
			print >>f, "<td>"
			print >>f, x_problemserver;
			print >>f, "</td>"
			
			print >>f, "<td>";
			print >>f, v_PoolHealthState;
			print >>f, "</td>";
			
			
			print >>f, "<td>";
			print >>f, v_TotalThreads;
			print >>f, "</td>";
			
			print >>f, "<td>";
			print >>f, v_idleThreads;
			print >>f, "</td>";
			
			print >>f, "<td>";
			print >>f, v_HogThread;
			print >>f, "</td>";
			
			print >>f, "<td>";
			print >>f, v_pendingThreads;
			print >>f, "</td>";
			
			print >>f, "<td>";
			print >>f, v_ThreadPoolQueue;
			print >>f, "</td>";
			
			print >>f, "<td>";
			print >>f, "<a href=\"file:///";
			print >>f, v_outputFilePath;
			print >>f, v_ThreadDumpFile0;
			print >>f, "\" target=\"_blank\">First Thread Dump File</a></br>";
			print >>f, "<a href=\"file:///";
			print >>f, v_outputFilePath;
			print >>f, v_ThreadDumpFile1;
			print >>f, "\" target=\"_blank\">Second Thread Dump File</a></br>";
			print >>f, "<a href=\"file:///";
			print >>f, v_outputFilePath;
			print >>f, v_ThreadDumpFile2;
			print >>f, "\" target=\"_blank\">Third Thread Dump File</a></br></br>";
			print >>f, "If the links do not work, go manually check the output directory.";
			print >>f, "</td>";
			
			
			print >>f, "</tr>";
			
			# Go back to ServerRuntimes
			cd ('../../../');
		else:
			# Go back to ServerRuntimes
			cd ('../');
		
		
		
			

				
	print >>f, "</tbody></table>"
print >>f, "<p></p>"	

	

# CHANGE to the Cluster MBean tree, loop through the clusters printing a selection of MBean values





print >>f, "<h3 class=\"headline1\">Clusters</h3>"
print >>f, "<p>"
print >>f, "</p>"


# Initialize Server in Cluster list
v_build_server_in_cluster_list = [];

# Check if Cluster MBean Directory exists

serverConfig();
v_didyoufindit = 'Dummy Value';
v_didyoufindit = findMBean('Clusters');


if v_didyoufindit == 'true':
	
	print ""
	print "++++++++++++++++++++++++++"
	print "Obtaining cluster configuration information"
	print "++++++++++++++++++++++++++"
	print ""
	
	cd ('Clusters');
	myclusters = ls(returnMap='true');
	
	print >>f, "<table id=\"my_Cluster_table\" border=\"1\" class=\"formatHTML5\">"
	print >>f, "<thead align=\"left\">"
	print >>f, "<tr>"
	print >>f, "<th>Cluster Name</th>"
	print >>f, "<th>Servers in Cluster</th>"
	print >>f, "<th>Cluster Address</th>"
	print >>f, "<th>Cluster Messaging Mode</th>"
	print >>f, "<th>Multicast Address</th>"
	print >>f, "<th>Multicast Port</th>"
	print >>f, "<th>WebLogicPluginEnabled</th>"
	print >>f, "</tr>"
	print >>f,"</thead>"
	print >>f, "<tbody>"
	
	for mycluster in myclusters:
		
		v_build_server_in_cluster_list = [];
		x_cluster = java.lang.String(mycluster);
		
		
		cd(x_cluster);
		
		v_ClusterMessagingMode = get('ClusterMessagingMode');
		v_WebLogicPluginEnabled = get('WeblogicPluginEnabled');
		v_ClusterAddress = get('ClusterAddress');
		v_MulticastAddress = get('MulticastAddress');
		v_MulticastPort = get('MulticastPort');
		
		# Now let's get the server names in the cluster
		cd ('Servers');
		myservers = ls(returnMap='true');
		v_no_of_servers = len(myservers);
		
		
		# Back to the Cluster tree again
		
		cd ('../../');
		
		# Initialize loop count flag	
		v_count01 = '';
		
		# We need to know length of cluster list to set the HTML rowspan value
		
		
		
		print >>f, "<tr>";
		print >>f, "<td rowspan=";
		print >>f, v_no_of_servers;
		print >>f, ">";
		print >>f, x_cluster;
		print >>f, "</td>";
		

		if v_no_of_servers == 0:
			print >>f, "<td>";
			print >>f, "None";
			print >>f, "</td>";
				
			print >>f, "<td>";
			print >>f, v_ClusterAddress;
			print >>f, "</td>";
		
			print >>f, "<td>";
			print >>f, v_ClusterMessagingMode;
			print >>f, "</td>";
		
			print >>f, "<td>";
			print >>f, v_MulticastAddress;
			print >>f, "</td>";
		
			print >>f, "<td>";
			print >>f, v_MulticastPort;
			print >>f, "</td>";
		
			print >>f, "<td>";
			print >>f, v_WebLogicPluginEnabled;
			print >>f, "</td>";
		
			print >>f, "</tr>";
		else:	
			for value in myservers:
				if v_count01 == 'true':
					print >>f, "<tr>";
					print >>f, "<td>";
					print >>f, value;
					print >>f, "</td>";
					print >>f, "</tr>";
				else:	
					print >>f, "<td>";
					print >>f, value;
					print >>f, "</td>";
				
					print >>f, "<td rowspan=";
					print >>f, v_no_of_servers;
					print >>f, ">";
					print >>f, v_ClusterAddress;
					print >>f, "</td>"
		
					print >>f, "<td rowspan=";
					print >>f, v_no_of_servers;
					print >>f, ">";
					print >>f, v_ClusterMessagingMode;
					print >>f, "</td>"
		
					print >>f, "<td rowspan=";
					print >>f, v_no_of_servers;
					print >>f, ">";
					print >>f, v_MulticastAddress;
					print >>f, "</td>"
		
					print >>f, "<td rowspan=";
					print >>f, v_no_of_servers;
					print >>f, ">";
					print >>f, v_MulticastPort;
					print >>f, "</td>"
		
					print >>f, "<td rowspan=";
					print >>f, v_no_of_servers;
					print >>f, ">";
					print >>f, v_WebLogicPluginEnabled;
					print >>f, "</td>"
		
					print >>f, "</tr>"	
					v_count01 = 'true';
		
		
	print >>f, "</tbody></table>"
	print >>f, "<p></p>"
	v_didyoufindit = '';
	# Return to MBean Tree Root
	cd ('..');
	
else:
	print >>f, "<p>No Clusters are configured in this domain</p>";
	v_didyoufindit = '';
	# Return to MBean Tree Root
	cd ('..');
	

# CHANGE to the serverConfig Machines MBean tree, loop through the Machines Resources printing a selection of MBean values




print >>f, "<h3 class=\"headline1\">Machines (NodeManager)</h3>"
print >>f, "<p>"
print >>f, "</p>"

v_didyoufindit = findMBean('Machines');

if v_didyoufindit == 'true':
	
	print ""
	print "++++++++++++++++++++++++++"
	print "Obtaining NodeManager (machine) information"
	print "++++++++++++++++++++++++++"
	print ""
	
	cd ('Machines')
	mymachines = ls(returnMap='true');
	
	print >>f, "<table id=\"my_Machine_table\" border=\"1\" class=\"formatHTML5\">"
	print >>f, "<thead align=\"left\">"
	print >>f, "<tr>"
	print >>f, "<th>Machine Name</th>"
	print >>f, "<th>Listen Address</th>"
	print >>f, "<th>Listen Port</th>"
	print >>f, "<th>NodeManager Protocol</th>"
	print >>f, "<th>NodeManager Status</th>"
	print >>f, "</tr>"
	print >>f,"</thead>"
	print >>f, "<tbody>"

	for mymachine in mymachines:
		x_machine = java.lang.String(mymachine);
		print >>f, "<tr>"
		print >>f, "<td>"
		print >>f, x_machine;
		print >>f, "</td>"
		
		cd (x_machine);
		
		
		# Some machines do not have a Node Manager association and therefore no Node Manager MBean tree to traverse
		# Need to check for this
		
		v_check_path01 = findMBean('NodeManager');
		
		
		if v_check_path01 == 'true':
			cd ('NodeManager');
			
			#Some setups have a different path to the NM ListenAddress and ListenPort
			#Need to check for this
			v_check_path02 = findMBean('NodeManager');
			
			if v_check_path02 == 'true':
				cd ('NodeManager');
			else:
				cd (x_machine);

			v_MachineListenAddress = get('ListenAddress');
			v_MachineListenPort = get('ListenPort');
			v_NMType = get('NMType');
			
			#We need to guard against the possibility that nmConnect to a NodeManager hangs
			#Unfortunately, there does not appear to be a method for timing out or programmatically breaking out of a nmConnect attempt
			#To work-around we give the user the option whether or not to attempt a test connection
			#If they choose "yes", we provide a warning / instruction as to what to do in the event the nmConnect hangs
			
			print "";
			v_attemptNMConnect = raw_input('Test connection to NodeManager? (Y/N) [' + str(v_MachineListenAddress) + ':' + str(v_MachineListenPort) + '] :/> ').lower();
			print "";
			
			if v_attemptNMConnect == 'y':
				
				print "";
				print "+++++++++++++++++++++++++++++++++++";
				print "Attempting nmConnect to [" + str(v_MachineListenAddress) + ":" + str(v_MachineListenPort)+"]";
				print "";
				print "The connection should only take a few seconds returning a success or failure.";
				print "If the connection attempt hangs, manually kill the WLST session.";
				print "Then run the script again and at the prompt";
				print "refuse the offer to attempt a connection to this nodemanager";
				print "+++++++++++++++++++++++++++++++++++";
				print "";
				
				try:
					#We pass the username, password which was captured in the StartDomainSummarizer.py
					nmConnect(username, password,v_MachineListenAddress,v_MachineListenPort,v_DomainName,v_DomainHome,v_NMType);
					v_nmConnected = 'RUNNING';
					nmDisconnect();
					v_attemptNMConnect = 'null';
				except:

					print "";
					print "Attempted connection failed";
					v_nmConnected = 'nmConnect failed';
					v_attemptNMConnect = 'null';
			
			else:
				print "";
				print "Test connection not attempted"
				v_nmConnected = 'Test connection not attempted';
				v_attemptNMConnect = 'null';	
			
		
			print >>f, "<td>"
			print >>f, v_MachineListenAddress;
			print >>f, "</td>";
			print >>f, "<td>";
			print >>f, v_MachineListenPort;
			print >>f, "</td>";
			print >>f, "<td>";
			print >>f, v_NMType;
			print >>f, "</td>";
			print >>f, "<td>";
			print >>f, v_nmConnected;
			print >>f, "</td>";
			print >>f, "</tr>";
				
			cd ('../../../');
		else:
			print >>f, "<td>";
			print >>f, "Not Available (No NodeManager associated with this machine)";
			print >>f, "</td>";
			print >>f, "<td>";
			print >>f, "Not Available (No NodeManager associated with this machine)";
			print >>f, "</td>";
			print >>f, "<td>";
			print >>f, "Not Available (No NodeManager associated with this machine)";
			print >>f, "</td>";
			print >>f, "<td>";
			print >>f, "Not Available (No NodeManager associated with this machine)";
			print >>f, "</td>";
			print >>f, "</tr>";
			
			cd ('../');
		
		
	print >>f, "</tbody></table>"
	print >>f, "<p></p>"
	v_didyoufindit = '';

else:
	print >>f, "<p>No Machines are configured within this domain.</p>";
	v_didyoufindit = '';

# Return to serverConfig MBean Tree Root
cd ('../');

print >>f, "</div>"

# CHANGE to the Application Runtime MBean tree, get applications runtime info by server

print ""
print "++++++++++++++++++++++++++"
print "Obtaining application runtime information (per managed server)"
print "++++++++++++++++++++++++++"
print ""


print >>f, "<div class=\"TabbedPanelsContent\">"

domainRuntime();
cd ('../');
cd ('ServerRuntimes');
myservers=ls(returnMap='true');



print >>f, "<h3 class=\"headline1\">Application Runtime Information</h3>"
print >>f, "<p>"
print >>f, "</p>"

print >>f, "<table id=\"my_AppRuntime_table\" border=\"1\" class=\"formatHTML5\">"
print >>f, "<thead align=\"left\">"
print >>f, "<tr>"
print >>f, "<th>Server</th>"
print >>f, "<th>App Name</th>"
print >>f, "<th>Health State</th>"
print >>f, "</tr>"
print >>f,"</thead>"
print >>f, "<tbody>"




for myserver in myservers:
	
	x_server = java.lang.String(myserver);
	cd (x_server);
	
	
	#Collect App Information
	cd ('ApplicationRuntimes');
	
	myapps = ls(returnMap='true');
	
	v_no_of_apps = len(myapps);
	
	print >>f, "<tr>";
	print >>f, "<td";
	print >>f, "rowspan=";
	print >>f, v_no_of_apps;
	print >>f, ">";
	print >>f, x_server;
	print >>f, "</td>";
			
	
	v_count06 = 'false';
	
	for myapp in myapps:
	
		cd (myapp);
		v_getAppName = cmo.getName();
		v_AppHealthState = cmo.getHealthState();
		v_AppHealthState = stripMBeanValue(v_AppHealthState, 'AppHealth');
		
		if v_count06 == 'true':
			print >>f, "<tr>";
			print >>f, "<td>";
			print >>f, v_getAppName;
			print >>f, "</td>";
			print >>f, "<td>";
			print >>f, v_AppHealthState;
			print >>f, "</td>";
			print >>f, "</tr>";
		else:	
			print >>f, "<td>";
			print >>f, v_getAppName;
			print >>f, "</td>";
			print >>f, "<td>";
			print >>f, v_AppHealthState;
			print >>f, "</td>";
				
			print >>f, "</tr>";
			v_count06 = 'true';
		#Back to pick up next app
		cd ('../')
	
	#Back to pick up next server			
	cd ('../../')
	
print >>f, "</tbody></table>"
print >>f, "<p></p>"	
	
	
# Return to serverConfig MBean Tree Root
serverConfig();
#cd ('../');



print >>f, "</div>"
print >>f, "<div class=\"TabbedPanelsContent\">"


print >>f, "<h3 class=\"headline1\">JDBC System Resources - Configuration</h3>"
print >>f, "<p>"
print >>f, "</p>"

# Check if JDBC System Resource MBean Directory exists



v_didyoufindit = findMBean('JDBCSystemResources');

if v_didyoufindit == 'true':

	print ""
	print "++++++++++++++++++++++++++"
	print "Obtaining System JDBC Resource configuration information"
	print "++++++++++++++++++++++++++"
	print ""



	cd ('JDBCSystemResources');
	myjdbcresources = ls(returnMap='true');
	v_MultiSourceFlag = 'false';
	
	
	
	print >>f, "<table id=\"my_JDBC_table\" border=\"1\" class=\"formatHTML5\">"
	print >>f, "<thead align=\"left\">"
	print >>f, "<tr>"
	print >>f, "<th rowspan=2>JDBC Data Source Name</th>"
	print >>f, "<th rowspan=2>Type</th>"
	print >>f, "<th colspan=2>Target(s)</th>"
	print >>f, "<th rowspan=2>Driver Name</th>"
	print >>f, "<th rowspan=2>Global Transactions Protocol</th>"
	print >>f, "<th rowspan=2>User</th>"
	print >>f, "<th rowspan=2>JDBC URL</th>"
	print >>f, "</tr>"
	print >>f, "<tr>"
	print >>f, "<th>Name</th>"
	print >>f,  "<th>Type</th>"
	print >>f, "</tr>"
	print >>f,"</thead>"
	print >>f, "<tbody>"
	
	
	for myjdbcresource in myjdbcresources:
		x_jdbc = java.lang.String(myjdbcresource);
		
		# Change to the JDBC Resource
		cd(x_jdbc);
		
		# If a resource has no targets, the get will fail with an error, so we need to code for this scenario 
		try:
			v_any_targets = '';
			v_jdbc_target = get('Targets');
			v_no_of_targets = len(v_jdbc_target);
					
		except:
			
			v_no_of_targets = 0;
			
			# The exception will still display to standard out, which may cause alarm
			# So adding this message telling the user the exception is expected and can be ignored
			print "IGNORE this exception";	
		
			
		
		
		# Get the other attribute values
		cd ('JDBCResource')
		cd (x_jdbc);
		cd ('JDBCDriverParams');
		cd (x_jdbc);
		
		v_JDBCType = 'Generic';
		
		v_DriverName = get('DriverName');
		v_JDBC_URL = get('Url');
		
		# Get username attribute from datasource Properties
		# JDBCDriverParams/'+dsName+'/Properties/'+dsName+'/Properties/user') then get('Value') to recovery the username
		cd ('Properties');
		cd (x_jdbc);
		cd ('Properties');
		cd ('user');

		v_User = get('Value');
		
		cd ('../../../../../../');
		
		cd ('JDBCDataSourceParams');
		cd (x_jdbc);
		
		v_GlobalTransactionsProtocol = get('GlobalTransactionsProtocol');
		v_DataSourceList = get('DataSourceList');
		
		#Checking to see if this is Gridlink Data Source Type. If OneNodeList returns a value then we can assume yes it is
		cd ('../../JDBCOracleParams');
		cd (x_jdbc);
		v_OnsNodeList = get('OnsNodeList'); 
		
		
		# If the Data Source is Multi, set the Type to Multi. Driver Name and URL are not applicable
		# as a multi data source is like a cluster i.e it consists of multi generic data sources
		if str(v_DriverName) == 'None':
			
			v_JDBCType = 'Multi';
			v_DriverName = 'n/a';
			v_JDBC_URL = 'n/a';
			v_User = 'n/a';
			v_GlobalTransactionsProtocol = 'n/a';
			v_MultiSourceFlag = 'true';
		else:
			v_DataSourceList = 'n/a';	
		
		
		
		if str(v_OnsNodeList)  != 'None':
			v_JDBCType = 'GridLink';
			v_OnsNodeList = '';
		
		
		cd ('../../../../../');
		
		
		
		
		
		if v_JDBCType != 'Multi':
		
			# Now we are ready to print the HTML, setting rowspan
			print >>f, "<tr>";
			print >>f, "<td";
			print >>f, "rowspan=";
			print >>f, v_no_of_targets;
			print >>f, ">";
			print >>f, x_jdbc;
			print >>f, "</td>";
			print >>f, "<td";
			print >>f, "rowspan=";
			print >>f, v_no_of_targets;
			print >>f, ">";
			print >>f, v_JDBCType;
			print >>f, "</td>";
		
		
		
			if v_no_of_targets > 0:
			
				v_count02 = 'false';
			
				for value in v_jdbc_target:
					value = stripMBeanValue(value, 'Target');
					if v_count02 == 'true':
						print >>f, "<tr>";
						print >>f, "<td>";
						print >>f, value[0];
						print >>f, "</td>";
						print >>f, "<td>";
						print >>f, value[1];
						print >>f, "</td>";
						print >>f, "</tr>";
					else:	
						print >>f, "<td>";
						print >>f, value[0];
						print >>f, "</td>";
						print >>f, "<td>";
						print >>f, value[1];
						print >>f, "</td>";
						
					
						print >>f, "<td";
						print >>f, "rowspan=";
						print >>f, v_no_of_targets;
						print >>f, ">";
						print >>f, v_DriverName;
						print >>f, "</td>";
					
						print >>f, "<td";
						print >>f, "rowspan=";
						print >>f, v_no_of_targets;
						print >>f, ">";
						print >>f, v_GlobalTransactionsProtocol;
						print >>f, "</td>";
					
						print >>f, "<td";
						print >>f, "rowspan=";
						print >>f, v_no_of_targets;
						print >>f, ">";
						print >>f, v_User;
						print >>f, "</td>";
					
						print >>f, "<td";
						print >>f, "rowspan=";
						print >>f, v_no_of_targets;
						print >>f, ">";
						print >>f, v_JDBC_URL;
						print >>f, "</td>";
				
						print >>f, "</tr>";
						v_count02 = 'true';
			else:
				v_any_targets = 'None';
				print >>f, "<td>";
				print >>f, 	v_any_targets;
				print >>f, "</td>";
				
				print >>f, "<td>";
				print >>f, 	"n/a";
				print >>f, "</td>";
				
				
				print >>f, "<td>";
				print >>f, v_DriverName;
				print >>f, "</td>";
					
				print >>f, "<td>";
				print >>f, v_GlobalTransactionsProtocol;
				print >>f, "</td>";
					
				print >>f, "<td>";
				print >>f, v_User;
				print >>f, "</td>";
					
				print >>f, "<td>";
				print >>f, v_JDBC_URL;
				print >>f, "</td>";
				
				print >>f, "</tr>";
		
	

	print >>f, "</tbody></table>"
	print >>f, "<p></p>"		
	
	
	v_didyoufindit = '';
	# Return to MBean Tree Root
	cd ('..');

else:
	print >>f, "<p>No JDBC Data Sources are configured within this domain.</p>";
	v_didyoufindit = '';
	# Return to MBean Tree Root
	cd ('..');


# Print out the Multi Data Sources if they exist

if v_MultiSourceFlag == 'true':
	
	print ""
	print "++++++++++++++++++++++++++"
	print "Obtaining System JDBC (Multi Source) configuration information"
	print "++++++++++++++++++++++++++"
	print ""
	
	cd ('JDBCSystemResources');
	
	print >>f, "<h4 class=\"headline1\">Multi Data Sources</h4>"
	print >>f, "<p>"
	print >>f, "</p>"
	
	print >>f, "<table id=\"my_JDBCMulti_table\" border=\"1\" class=\"formatHTML5\">"
	print >>f, "<thead align=\"left\">"
	print >>f, "<tr>"
	print >>f, "<th>JDBC Data Source Name</th>"
	print >>f, "<th>Contains</th>"
	print >>f, "</tr>"
	print >>f,"</thead>"
	print >>f, "<tbody>"

	for myjdbcresource in myjdbcresources:
		x_jdbc = java.lang.String(myjdbcresource);
		
		
		# Find Data Sources
		cd(x_jdbc);
		cd ('JDBCResource')
		cd (x_jdbc);
		cd ('JDBCDataSourceParams');
		cd (x_jdbc);
		
		v_DataSourceList00 = get('DataSourceList');
		
		# Return to JDBCSystemResources Tree Root
		cd ('../../../../../');
		
		if str(v_DataSourceList00) != 'None':
			
			#Data Sources List is returned as a comma delimited string. 
			#We need to turn it into a list if we want to print the data in sub rows
			v_DataSourceList01 = String.replace(v_DataSourceList00,',',' ');
			v_DataSourceList = v_DataSourceList01.split();
			v_no_of_datasources = len(v_DataSourceList);
			v_count05 = 'false';
			
			
			print >>f, "<tr>";
			print >>f, "<td";
			print >>f, "rowspan=";
			print >>f, v_no_of_datasources;
			print >>f, ">";
			print >>f, x_jdbc;
			print >>f, "</td>";
			
			
			for value in v_DataSourceList:
				if v_count05 == 'true':
					print >>f, "<tr>";
					print >>f, "<td>";
					print >>f, value;
					print >>f, "</td>";
					print >>f, "</tr>";
				else:	
					print >>f, "<td>";
					print >>f, value;
					print >>f, "</td>";
								
					print >>f, "</tr>";
					v_count05 = 'true';
		
	print >>f, "</tbody></table>"
	print >>f, "<p></p>"	
	
# Return to MBean Tree Root	
cd ('..');	
		

# Now if data sources are active get JDBC Runtime data

print >>f, "<h3 class=\"headline1\">JDBC Runtime Information</h3>"
print >>f, "<p>"
print >>f, "</p>"

		
servers = domainRuntimeService.getServerRuntimes();
v_JDBCRuntimeDataExists = 'false';

for server in servers:
	jdbcRuntime = server.getJDBCServiceRuntime();
	datasources = jdbcRuntime.getJDBCDataSourceRuntimeMBeans();
	
	
        v_no_of_datasources = len(datasources);
	
	if v_no_of_datasources > 0:
		v_JDBCRuntimeDataExists = 'true';


if v_JDBCRuntimeDataExists == 'true':
	
	
	print ""
	print "++++++++++++++++++++++++++"
	print "Obtaining System JDBC Resource runtime information"
	print "++++++++++++++++++++++++++"
	print ""
	
	
	
	print >>f, "<table id=\"my_JDBCRuntime_table\" border=\"1\" class=\"formatHTML5\">"
	print >>f, "<thead align=\"left\">"
	print >>f, "<tr>"
	print >>f, "<th rowspan=2>Server Name</th>"
	print >>f, "<th rowspan=2>JDBC Data Source Name</th>"
	print >>f, "<th rowspan=2>State</th>"
	print >>f, "<th colspan=4>Connections</th>"
	print >>f, "</tr>"
	print >>f, "<tr>"
	print >>f, "<th>Active</th>"
	print >>f,  "<th>Waiting</th>"
	print >>f,  "<th>Leaked</th>"
	print >>f,  "<th>Current Capacity</th>"
	print >>f, "</tr>"
	print >>f,"</thead>"
	print >>f, "<tbody>"


	for server in servers:
		jdbcRuntime = server.getJDBCServiceRuntime();
		datasources = jdbcRuntime.getJDBCDataSourceRuntimeMBeans();
		v_no_of_datasources = len(datasources);
		
		if v_no_of_datasources > 0:
			v_count04 = 'false';
			
			print >>f, "<tr>";
			print >>f, "<td rowspan=";
			print >>f, v_no_of_datasources;
			print >>f, ">";
			print >>f, stripMBeanValue(server, 'JDBC_Server')[1];
			print >>f, "</td>";
			
			
			for datasource in datasources:
				v_ActiveConnections = datasource.getActiveConnectionsCurrentCount();
				v_WaitingConnections = datasource.getWaitingForConnectionCurrentCount();
				v_JDBCSource_State = datasource.getState();
				v_LeakedConnectionCount = datasource.getLeakedConnectionCount()
				v_CurrCapacity = datasource.getCurrCapacity()
		
				if v_count04 =='true':
					print >>f, "<tr>";
					print >>f, "<td>";
					print >>f, stripMBeanValue(datasource, 'JDBC_DataSource')[1];
					print >>f, "</td>";
					
					print >>f, "<td>";
					print >>f, v_JDBCSource_State;
					print >>f, "</td>";
					
					print >>f, "<td>";
					print >>f, v_ActiveConnections;
					print >>f, "</td>";
					print >>f, "<td>";
					print >>f, v_WaitingConnections;
					print >>f, "</td>";
					
					print >>f, "<td>";
					print >>f, v_LeakedConnectionCount;
					print >>f, "</td>";
					
					print >>f, "<td>";
					print >>f, v_CurrCapacity;
					print >>f, "</td>";
					
					print >>f, "</tr>";
				else:
					print >>f, "<td>";
					print >>f, stripMBeanValue(datasource, 'JDBC_DataSource')[1];
					print >>f, "</td>"
					
					print >>f, "<td>";
					print >>f, v_JDBCSource_State;
					print >>f, "</td>";
			
					print >>f, "<td>";
					print >>f, v_ActiveConnections;
					print >>f, "</td>"
			
					print >>f, "<td>";
					print >>f, v_WaitingConnections;
					print >>f, "</td>"
					
					print >>f, "<td>";
					print >>f, v_LeakedConnectionCount;
					print >>f, "</td>";
					
					print >>f, "<td>";
					print >>f, v_CurrCapacity;
					print >>f, "</td>";
					
					print >>f, "</tr>";
					v_count04 ='true';
					
	
			
	print >>f, "</tbody></table>"
	print >>f, "<p></p>"		

else:
	print >>f, "There is no JDBC System Resource Runtime data available";
	print >>f, "<p>"
	print >>f, "</p>"




print >>f, "</div>"
print >>f, "<div class=\"TabbedPanelsContent\">"


# CHANGE to the JMS Server MBean tree, loop through the JMS Servers printing a selection of MBean values

print >>f, "<h3 class=\"headline1\">JMS Servers</h3>"
print >>f, "<p>"
print >>f, "</p>"

# Check if JMS Server MBean Directory exists

v_didyoufindit = findMBean('JMSServers');

if v_didyoufindit == 'true':
	
	print ""
	print "++++++++++++++++++++++++++"
	print "Obtaining JMS Server configuration information"
	print "++++++++++++++++++++++++++"
	print ""
	
	cd ('JMSServers');
	myjmsservers = ls(returnMap='true');
	
	print >>f, "<table id=\"my_JMS_table\" border=\"1\" class=\"formatHTML5\">"
	print >>f, "<thead align=\"left\">"
	print >>f, "<tr>"
	print >>f, "<th>JMS Server Name</th>"
	print >>f, "<th>Target</th>"
	print >>f, "<th>PersistentStore</th>"
	print >>f, "</tr>"
	print >>f,"</thead>"
	print >>f, "<tbody>"
	
	
	for myjmsserver in myjmsservers:
		x_jms = java.lang.String(myjmsserver);
		print >>f, "<tr>"
		print >>f, "<td>"
		print >>f, x_jms;
		print >>f, "</td>"
		cd(x_jms);
		v_jms_target = get('Targets');
		
		print >>f, "<td>"
		
		# Some MBeans values are returned as an array or list. 
		# Therefore to display the array contents in a more friendly way, 
		# we loop through the array and print each content followed by a line break
		
		for value in v_jms_target:
			value = stripMBeanValue(value, 'Target');
			print >>f, value[0];
			#print >>f, ",&nbsp"
			#print >>f, value[2];
			#print >>f, "</br>"
		print >>f, "</td>"
		
		v_PersistentStore = get('PersistentStore');
		v_PersistentStore = stripMBeanValue(v_PersistentStore, 'JMSStore');
		
		print >>f, "<td>"
		print >>f, v_PersistentStore[0];
		
		if str(v_PersistentStore[0]) == 'None':
			print >>f, "&nbsp"
		else:
			print >>f, ",&nbsp"	
			print >>f, v_PersistentStore[1];
			
		print >>f, "</td>"
		print >>f, "</tr>"
		cd ('../');
		
	print >>f, "</tbody></table>"
	print >>f, "<p></p>"
	v_didyoufindit = '';

else:
	print >>f, "<p>No JMS Servers are configured within this domain.</p>";
	v_didyoufindit = '';



# Get JMS Runtime data if it exists

print >>f, "<h3 class=\"headline1\">JMS Runtime Information</h3>"
print >>f, "<p>"
print >>f, "</p>"


servers = domainRuntimeService.getServerRuntimes();


v_JMSRuntimeDataExists = 'false';


for server in servers:
	jmsRuntime = server.getJMSRuntime();
        jmsServers = jmsRuntime.getJMSServers();
	
	v_no_of_jmsservers = len(jmsServers);
	
	x_server = server.getName();
	
	
	if v_no_of_jmsservers > 0:
		v_JMSRuntimeDataExists = 'true';
		
	
	if v_JMSRuntimeDataExists == 'true':
	
	
		print ""
		print "++++++++++++++++++++++++++"
		print "Obtaining JMS runtime information"
		print "++++++++++++++++++++++++++"
		print ""
		
		for jmsServer in jmsServers:
			
			x_jmsserver = jmsServer.getName();
			
			
			#print >>f, "<h3>"
			#print >>f, x_server;
			#print >>f, "</h3>"
			print >>f, "<h4>"
			print >>f, x_jmsserver;
			print >>f, "</h4>"
			print >>f, "<p>"
			print >>f, "</p>"
			
			
			destinations = jmsServer.getDestinations();
			
			if len(destinations) > 0:
			
			
				print >>f, "<table id=\"my_JMSRuntime_table\" border=\"1\" class=\"formatHTML5\">"
				print >>f, "<thead align=\"left\">"
				print >>f, "<tr>"
				print >>f, "<th rowspan=2>Destination</th>"
				print >>f, "<th rowspan=2>Type</th>"
				# print >>f, "<th rowspan=2>State</th>"
				print >>f, "<th colspan=4>Messages</th>"
				print >>f, "</tr>"
				print >>f, "<tr>"
				print >>f, "<th>Current Count</th>"
				print >>f,  "<th>High Count</th>"
				print >>f,  "<th>Pending Count</th>"
				print >>f,  "<th>Deleted Current Count</th>"
				print >>f, "</tr>"
				print >>f,"</thead>"
				print >>f, "<tbody>"
				
					
				for destination in destinations:
					
					x_destination = destination.getName();
					v_DestinationType = destination.getDestinationType();
					v_MessagesCurrentCount = destination.getMessagesCurrentCount();
					v_MessagesHighCount = destination.getMessagesHighCount();
					v_MessagesPendingCount = destination.getMessagesPendingCount();
					v_MessagesDeletedCurrentCount = destination.getMessagesDeletedCurrentCount();
					
					print >>f, "<tr>";
					
					print >>f, "<td>";
					print >>f, x_destination;
					print >>f, "</td>";
					
					print >>f, "<td>";
					print >>f, v_DestinationType;
					print >>f, "</td>";
					
					print >>f, "<td>";
					print >>f, v_MessagesCurrentCount;
					print >>f, "</td>";
					
					print >>f, "<td>";
					print >>f, v_MessagesHighCount;
					print >>f, "</td>";
					
					print >>f, "<td>";
					print >>f, v_MessagesPendingCount;
					print >>f, "</td>";
					
					print >>f, "<td>";
					print >>f, v_MessagesDeletedCurrentCount;
					print >>f, "</td>";
							
					print >>f, "</tr>";
					


				print >>f, "</tbody></table>"
				print >>f, "<p></p>"	
			else:
				print >>f, "There is no JMS Destination Runtime data available";
				print >>f, "<p>"
				print >>f, "</p>"	

	else:
		print >>f, "There is no JMS Server Runtime data available";
		print >>f, "<p>"
		print >>f, "</p>"





print >>f, "</div>"
print >>f, "</div>"
print >>f, "</div>"

# This piece of javascript enabled the Tabs to work
print >>f, "<script type=\"text/javascript\">"
print >>f, "var TabbedPanels001 = new Spry.Widget.TabbedPanels(\"TabbedPanels001\");"
print >>f, "</script>"

print >>f, "</body>"
print >>f, "</html>"

# CLOSE output file, program end

print ""
print "++++++++++++++++++++++++++"
print "Script end, closing output file, disconnect from Admin Server and exiting WLST session"
print "++++++++++++++++++++++++++"
print ""

f.close();
disconnect();
exit();



	


