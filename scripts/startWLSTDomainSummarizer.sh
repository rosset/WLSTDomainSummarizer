#!/bin/sh

#Change the environment variables below to suit your target environment
#The WLST_OUTPUT_PATH and WLST_OUTPUT_FILE environment variables in this script 
#determine the output directory and file of the script
#The WLST_OUTPUT_PATH directory value must have a trailing slash. If there is no trailing slash 
#script will error and not continue.

#my configuration
export domain_name=medrec
WL_HOME=/oracle/product/Middleware/11g/wlserver_10.3
DOMAIN_HOME=/oracle/product/Middleware/11g/wlserver_10.3/samples/domains/$domain_name; export DOMAIN_HOME
WLST_OUTPUT_PATH=/oracle/scripts/WLSTDomainSummarizer/output/; export WLST_OUTPUT_PATH
WLST_OUTPUT_FILE=WLST_MBean_Config_Summary_domain_$domain_name.html; export WLST_OUTPUT_FILE

${WL_HOME}/common/bin/wlst.sh StartDomainSummarizer.py
