# WLST Domain Summarizer Script
# This script launches either the WLST online or offline collection script depending on whether a connection can be made to the Admin Server
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

# START OF SCRIPT

# Collect and Store Domain Home, Output Directory and Output File Name

# The recommendation is to stick this script off from a wrapper os script e.g cmd (Windows) or .sh (Unix)		
v_domainHome = os.environ["DOMAIN_HOME"];
v_outputFilePath = os.environ["WLST_OUTPUT_PATH"];
v_outputFile = os.environ["WLST_OUTPUT_FILE"];


# Check the variable values to see if they are empty or valid. If yes, ask for values
# We could write something more sophisicated here, but it's a start

if v_domainHome == '':
	v_domainHome = raw_input('Enter DOMAIN_HOME, specify full path: ');
	
if v_outputFilePath== '':	
	v_outputFilePath = raw_input('Enter output directory, specify full path including final trailing slash: ');
if v_outputFile== '':	
	v_outputFile = raw_input('Enter output file name, specify .html as the file extension: ');

if os.path.isdir(v_domainHome) == false:
 	raise Exception ('Invalid Domain Home. The path does not exist. Check the start summarizer cmd or sh file.')

if os.path.isdir(v_outputFilePath) == false:
 	raise Exception ('Invalid Output Directory. The path does not exist')



v_chooseMode = raw_input('Is your domain Admin Server up and running and do you have the connection details? (Y /N ): ').lower();

if v_chooseMode == 'y':
		
	try:
		
		#We need to manually capture username / password details so later we can test a connection to the Node Manager
		URL = raw_input('Enter connection URL to Admin Server e.g t3://mymachine.acme.com:7001 : ');
		username = raw_input('Enter weblogic username: ');
		password = "".join(java.lang.System.console().readPassword("Enter weblogic username password %s", [prompt]));
		connect(username, password,URL);
	except:
		print "There has been a problem connecting to the Admin Server, running offline connection instead";
		execfile('WLSDomainInfoOffline.py');
		
	try:
		execfile('WLSDomainInfoOnline.py');
	except:
		print "There has been a problem running WLSDomainInfoOnline.py. Debug this script by running it standalone.";
		
else:
	print "Ok, no problem running an offline collection";
	execfile('WLSDomainInfoOffline.py');

exit();



	


