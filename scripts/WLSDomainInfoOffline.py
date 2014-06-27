# Prototype Script to perform WLST offline collection of managed server config MBeans
# The script retrieves a selection of config MBeans values. The values are printed as part of a HTML file which is built dynamically by this script.
# Author: Daniel Mortimer
# Proactive Support Delivery
# Date: 7th May 2013
# Version 007

#IMPORTS

# import types;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import os;
import string;

# START OF FUNCTIONS

# function to help locate whether MBean directory exists. 
# This does not perform a global search. It just checks whether a given MBean directory exists at the level the script is currently in 
def findMBean(v_pattern):
        # get a listing of everything in the current directory
	mydirs = ls(returnMap='true');
 
        v_compile_pattern = java.util.regex.Pattern.compile(v_pattern);
	
	found = 'false';
        
	for mydir in mydirs:
		x = java.lang.String(mydir);
		v_matched = v_compile_pattern.matcher(x);
		if v_matched.find():
			found = 'true';
                 
        return found;

# function to strip the Bean Value which is returned as tuple (list). 
# We only want to return and print the target name and type
def stripMBeanValue (v_mbeanvalue):
	
	v_check_value = str(v_mbeanvalue);
	v_strippedValue01 = String.replace(v_check_value,'Proxy for ','');
	v_strippedValue02 = String.replace(v_strippedValue01,'Name=','');
	v_strippedValue03 = String.replace(v_strippedValue02,'Type=','');
	v_strippedValue04 = String.replace(v_strippedValue03,':',' ');
	v_strippedValue = v_strippedValue04.split();
	return v_strippedValue;

# END OF FUNCTIONS

# START OF SCRIPT

# Collect and Store Domain Home, Output Directory and Output File Name

v_domainHome = os.environ["DOMAIN_HOME"];

if v_domainHome == '':
	v_domainHome = raw_input('Enter DOMAIN_HOME, specify full path: ');

if os.path.isdir(v_domainHome) == false:
 	raise Exception ('Invalid Domain Home. The path does not exist.')


#Some WLST commands throw output to stdout
#For a cleaner user experience we redirect that stuff to log in the online py file
#Unfortunately redirect function is not supported when WLST is in offline mode :-(
# e.g redirect('wlstonlinedomainsummarizer.log', 'false'); will not work

# Read in the Domain Configuration

readDomain(v_domainHome);

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


# Some blurb

print >>f, "<div id=\"divContainer\">"
print >>f, "<h1 class=\"headline3\">Introduction</h1>"
print >>f, "<p>This is the output from a WLST script run in <u><strong>offline mode</strong></u>. The script retrieves a selection of configuration MBean values. It is intended to provide a high level summary of a given WebLogic domain.</p>"
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
#print >>f,  "<li class=\"TabbedPanelsTab\" tabindex=\"0\">Application Runtime</li>"
print >>f,	"<li class=\"TabbedPanelsTab\" tabindex=\"0\">JDBC</li>"
print >>f, "<li class=\"TabbedPanelsTab\" tabindex=\"0\">JMS</li></ul>"
print >>f, "<div class=\"TabbedPanelsContentGroup\">"	
print >>f, "<div class=\"TabbedPanelsContent\">"



# From Top of Domain MBean Tree, obtain some high level domain attributes.

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

print >>f, "<div class=\"TabbedPanelsContent\">"


print >>f, "<h3 class=\"headline1\">All Servers</h3>"
print >>f, "<p>"
print >>f, "</p>"


cd ('Server');
myservers = ls(returnMap='true');


print >>f, "<table id=\"my_Server1_Table\" border=\"1\" class=\"formatHTML5\">"
print >>f, "<thead align=\"left\">"
print >>f, "<tr>"
print >>f, "<th rowspan=2>Server Name</th>"
print >>f, "<th rowspan=2>Cluster</th>"
print >>f, "<th rowspan=2>Machine</th>"
print >>f, "<th colspan=3>Default Network Info</th>"
print >>f, "<th colspan=4>Custom Network Channel</th>"
print >>f, "<th colspan=2>ClassPath Info</th>"
print >>f, "</tr>"
print >>f, "<tr>"

print >>f, "<th>Listen Address</th>"
print >>f, "<th>Listen Port</th>"
print >>f, "<th>SSL Listen Port</th>"

print >>f, "<th>Name</th>"
print >>f, "<th>Listen Address</th>"
print >>f, "<th>Protocol</th>"
print >>f, "<th>Listen Port</th>"

print >>f, "<th>JavaCompilerPreClassPath</th>"
print >>f, "<th>JavaCompilerPostClassPath</th>"
print >>f,"</tr>"
print >>f,"</thead>"
print >>f, "<tbody>"


# Here is where we loop through the servers in the tree,
# Note: we do not store the MBean values in an array, for simplicity we print the MBean value as soon as we have retrieved it

for myserver in myservers:
	
	
	x_server = java.lang.String(myserver);
	
	cd(x_server);
	
	v_Cluster = get('Cluster');
	v_Cluster = stripMBeanValue(v_Cluster);
		
	v_ListenAddress = get('ListenAddress');
	v_ListenPort = get('ListenPort');
	
	v_Machine = get('Machine');
	v_Machine = stripMBeanValue(v_Machine);
	
	v_JavaCompilerPreClassPath = get('JavaCompilerPreClassPath');
	v_JavaCompilerPostClassPath = get('JavaCompilerPostClassPath');
	
	v_check_SSLexists = findMBean('SSL');
	v_check_CustomNetwork = findMBean('NetworkAccessPoint');
	

	# Check to see if the Server has a SSL MBean Branch .. if yes we will try to find the SSL Listen Port	
	if v_check_SSLexists == 'true':
		cd ('SSL');
		cd ('NO_NAME_0');
		
		try:
			v_SSL_ListenPort = get('ListenPort');
		except:
			
			# The exception will still display to standard out, which may cause alarm
			# So adding this message telling the user the exception is expected and can be ignored
			v_SSL_ListenPort = "null";
			print "IGNORE this exception";	
		
		v_check_SSLexists = '';
		# v_SSL_ListenPort = get('ListenPort');
		cd ('../../');
	else:
		v_SSL_ListenPort = "SSL not enabled";
			
	# Check to see if the Server has a NetAccessPoint branch .. if yes we will try to find custom network channel information
	if v_check_CustomNetwork == 'true':
		
		cd ('NetworkAccessPoint');
		customNetChannels = ls(returnMap='true');
		
		# Obtain the number of custom network channels configured against a server
		# We need this value to set the rowspan HTML attribute
		v_no_of_netchannels = len(customNetChannels);
		
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
				# Back to NetworkAccessPoint
				cd ('../');
			else:	
				
				print >>f, "<td rowspan=";
				print >>f, v_no_of_netchannels;
				print >>f, ">";
				print >>f, v_Cluster[0];
				print >>f, "</td>"
					
				print >>f, "<td rowspan=";
				print >>f, v_no_of_netchannels;
				print >>f, ">";
				print >>f, v_Machine[0];
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
					
				print >>f, "<td rowspan=";
				print >>f, v_no_of_netchannels;
				print >>f, ">";
				print >>f, v_JavaCompilerPreClassPath;
				print >>f, "</td>"
					
				print >>f, "<td rowspan=";
				print >>f, v_no_of_netchannels;
				print >>f, ">";
				print >>f, v_JavaCompilerPostClassPath;
				print >>f, "</td>"
				
				print >>f, "</tr>"
				
				
				v_count03 = 'true';
				# Back to NetworkAccessPoint
				cd ('../');
		
		#Back to Server/Servername		
		cd ('../');	
	
	
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
		print >>f, v_Cluster[0];
		print >>f, "</td>"
		
		print >>f, "<td>"
		print >>f, v_Machine[0];
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
		print >>f, "<td>"
		
		print >>f, v_JavaCompilerPreClassPath;
		print >>f, "</td>"
		
		print >>f, "<td>"
		print >>f, v_JavaCompilerPostClassPath;
		print >>f, "</td>"
		
		print >>f, "</tr>"
	
	#Back to Servers		
	v_check_CustomNetwork = 'false';
	cd ('../');

print >>f, "</tbody></table>"
print >>f, "<p></p>"

# Return to MBean Tree Root
cd ('..');



# CHANGE to the Cluster MBean tree, loop through the clusters printing a selection of MBean values


print >>f, "<h3 class=\"headline1\">Clusters</h3>"
print >>f, "<p>"
print >>f, "</p>"


# Initialize Server in Cluster list
v_build_server_in_cluster_list = [];

# Check if Cluster MBean Directory exists

v_didyoufindit = 'Dummy Value';
v_didyoufindit = findMBean('Cluster');


if v_didyoufindit == 'true':
	cd ('Cluster');
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
		v_WebLogicPluginEnabled = get('WebLogicPluginEnabled');
		v_ClusterAddress = get('ClusterAddress');
		v_MulticastAddress = get('MulticastAddress');
		v_MulticastPort = get('MulticastPort');
		
		# Now let's get the server names in the cluster
		cd ('../../');
		cd ('Server');
		
		
		
		for myserver in myservers:
			x_server = java.lang.String(myserver);
			# print x_server;
			cd(x_server);
			v_Cluster = get('Cluster');
			v_Cluster = stripMBeanValue(v_Cluster);
			v_check_cluster_value = java.lang.String(v_Cluster[0]);
			
			if v_check_cluster_value == x_cluster:
				v_build_server_in_cluster_list.append(x_server);
				# print v_build_server_in_cluster_list;
			cd ('../');	
		
		
		# Back to the Cluster tree again
		
		cd ('../');
		cd ('Cluster');
		
		# Initialize loop count flag	
		v_count01 = '';
		
		# We need to know length of cluster list to set the HTML rowspan value
		v_no_of_servers = len(v_build_server_in_cluster_list);
		
		
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
			for value in v_build_server_in_cluster_list:
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
	

# CHANGE to the Machines MBean tree, loop through the Machines Resources printing a selection of MBean values

print >>f, "<h3 class=\"headline1\">Machines (NodeManager)</h3>"
print >>f, "<p>"
print >>f, "</p>"

v_didyoufindit = findMBean('AnyMachine');

if v_didyoufindit == 'true':
	cd ('Machines')
	mymachines = ls(returnMap='true');
	
	print >>f, "<table id=\"my_Machine_table\" border=\"1\" class=\"formatHTML5\">"
	print >>f, "<thead align=\"left\">"
	print >>f, "<tr>"
	print >>f, "<th>Machine Name</th>"
	print >>f, "<th>Listen Address</th>"
	print >>f, "<th>Listen Port</th>"
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
		
			print >>f, "<td>"
			print >>f, v_MachineListenAddress;
			print >>f, "</td>";
			print >>f, "<td>";
			print >>f, v_MachineListenPort;
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
			print >>f, "</tr>";
			
			cd ('../');
		
		
	print >>f, "</tbody></table>"
	print >>f, "<p></p>"
	v_didyoufindit = '';

else:
	print >>f, "<p>No Machines are configured within this domain.</p>";
	v_didyoufindit = '';

# Return to MBean Tree Root
cd ('../');



print >>f, "</div>"


# CHANGE to the JDBC MBean tree, loop through the JDBC Resources printing a selection of MBean values

print >>f, "<div class=\"TabbedPanelsContent\">"

print >>f, "<h3 class=\"headline1\">JDBC System Resources</h3>"
print >>f, "<p>"
print >>f, "</p>"

# Check if JDBC System Resource MBean Directory exists



v_didyoufindit = findMBean('JDBCSystemResource');

#Initializing variables which are use to flag whether data source is Multi and if yes, to collect data
v_MultiSourceFlag = 'false';
v_isMultiLink = 'false';

if v_didyoufindit == 'true':
	
	
	cd ('JDBCSystemResource');
	myjdbcresources = ls(returnMap='true');
	
	
	print >>f, "<table id=\"my_JDBC_table\" border=\"1\" class=\"formatHTML5\">"
	print >>f, "<thead align=\"left\">"
	print >>f, "<tr>"
	print >>f, "<th rowspan=2>Name</th>"
	print >>f, "<th rowspan=2>Type</th>"
	print >>f, "<th colspan=2>Target(s)</th>"
	print >>f, "<th rowspan=2>Driver Name</th>"
	print >>f, "<th rowspan=2>Global Transactions Protocol</th>"
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
		
		v_JDBC_Type = 'Generic';
		
		# Change to the JDBC Resource
		cd(x_jdbc);
		
		
		# If a resource has no targets, the get will fail with an error, so we need to code for this scenario 
		try:
			v_any_targets = '';
			v_jdbc_target = get('Target');
			
			# Even if the get fails, the variable is assigned a value of none, set the flag variable accordingly
			if v_jdbc_target == 'None':
				v_any_targets = 'None';
				v_no_of_targets = 1;
			else:	
				# If the get has succeeded then set flag accordingly and obtain length of array returned by the get
				# The array length will be used to determine the HTML rowspan value
				
				v_any_targets ='Use v_jdbc_target';
				v_no_of_targets = len(v_jdbc_target);
					
		except:
			
			# Setting flag and rowspan variable here as well .. belt and braces
			v_any_targets = 'None';
			v_no_of_targets = 1;
			
			# The exception will still display to standard out, which may cause alarm
			# So adding this message telling the user the exception is expected and can be ignored
			print "IGNORE this exception";	
		
		
		# Get the other attribute values
		cd ('JdbcResource');
		
		
		
		
		cd (x_jdbc);
		
		#If JDBCOracleParams is found we know this to be a Gridlink data source
		v_isGridLink = findMBean('JDBCOracleParams');
		
		#If JDBCDriverParams is not found then we know the Data Source must a multi source definition
		v_isMultiLink = findMBean('JDBCDriverParams');
		
		if v_isGridLink == 'true':
			v_JDBC_Type = 'Gridlink';
			
		if v_isMultiLink == 'false':
			v_JDBC_Type = 'Multi';
			v_MultiSourceFlag = 'true';	
		else:	
			
			ls();
			
			cd ('JDBCDriverParams');
			cd ('NO_NAME_0');		
			v_DriverName = get('DriverName');
			v_JDBC_URL = get('URL');
			cd ('../../');
		
		cd ('JDBCDataSourceParams');
		cd ('NO_NAME_0');
		
		v_GlobalTransactionsProtocol = get('GlobalTransactionsProtocol');
					
		cd ('../../../../../');
		
		
			
		if v_JDBC_Type != 'Multi':
			
		
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
			print >>f, v_JDBC_Type;
			print >>f, "</td>";
		
			# print >>f, "<td>";
			if v_any_targets == 'Use v_jdbc_target':
			
				v_count02 = 'false';
			
				for value in v_jdbc_target:
					value = stripMBeanValue(value);
					if v_count02 == 'true':
						print >>f, "<tr>";
						print >>f, "<td>";
						print >>f, value[0];
						print >>f, "</td>";
						print >>f, "<td>";
						print >>f, value[2];
						print >>f, "</td>";
						print >>f, "</tr>";
					else:	
						print >>f, "<td>";
						print >>f, value[0];
						print >>f, "</td>";
						print >>f, "<td>";
						print >>f, value[2];
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
						print >>f, v_JDBC_URL;
						print >>f, "</td>";
				
						print >>f, "</tr>";
						v_count02 = 'true';
			else:
				print >>f, "<td>";
				print >>f, 	"No targets";
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
				print >>f, v_JDBC_URL;
				print >>f, "</td>";
			
				print >>f, "</tr>";
		
		#print >>f, "</td>"
		
		
		
	

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
	
	print >>f, "<h3>Multi Data Sources</h3>"
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
	
	cd ('JDBCSystemResource');
	
	
	for myjdbcresource in myjdbcresources:
		x_jdbc = java.lang.String(myjdbcresource);
		
		
		
		cd (x_jdbc);
		cd('JdbcResource');
		cd (x_jdbc);
		cd('JDBCDataSourceParams/NO_NAME_0');
		
		v_DataSourceList00 = get('DataSourceList');
		
		
		# Return to MBean Tree Root
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

print >>f, "</div>"



# CHANGE to the JMS Server MBean tree, loop through the JMS Servers printing a selection of MBean values

print >>f, "<div class=\"TabbedPanelsContent\">"

print >>f, "<h3 class=\"headline1\">JMS Servers</h3>"
print >>f, "<p>"
print >>f, "</p>"

# Check if JMS Server MBean Directory exists

v_didyoufindit = findMBean('JMSServer');

if v_didyoufindit == 'true':
	cd ('JMSServer');
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
		v_jms_target = get('Target');
		
		print >>f, "<td>"
		
		# Some MBeans values are returned as an array or list. 
		# Therefore to display the array contents in a more friendly way, 
		# we loop through the array and print each content followed by a line break
		
		for value in v_jms_target:
			value = stripMBeanValue(value);
			print >>f, value[0];
			#print >>f, ",&nbsp"
			#print >>f, value[2];
			#print >>f, "</br>"
		print >>f, "</td>"
		
		v_PersistentStore = get('PersistentStore');
		v_PersistentStore = stripMBeanValue(v_PersistentStore);
		
		print >>f, "<td>"
		print >>f, v_PersistentStore[0];
		
		if v_PersistentStore[0] == 'None':
			print >>f, "&nbsp"
		else:
			print >>f, ",&nbsp"	
			print >>f, v_PersistentStore[2];
			
		print >>f, "</td>"
		print >>f, "</tr>"
		cd ('../');
		
	print >>f, "</tbody></table>"
	print >>f, "<p></p>"
	v_didyoufindit = '';

else:
	print >>f, "<p>No JMS Servers are configured within this domain.</p>";
	v_didyoufindit = '';

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

f.close();		
closeDomain();
exit();
