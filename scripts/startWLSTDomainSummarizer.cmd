@ECHO ON

@REM Change the environment variables below to suit your target environment
@REM The WLST_OUTPUT_PATH and WLST_OUTPUT_FILE environment variables in this script 
@REM determine the output directory and file of the script
@REM The WLST_OUTPUT_PATH directory value must have a trailing slash. If there is no trailing slash 
@REM script will error and not continue.


SETLOCAL

set WL_HOME=D:\product\FMW11g\wlserver_10.3
set DOMAIN_HOME=D:\product\FMW11g\user_projects\domains\MyDomain
set WLST_OUTPUT_PATH=D:\WLSTDomainSummarizer\output\
set WLST_OUTPUT_FILE=WLST_Domain_Summary_Via_MBeans.html

call "%WL_HOME%\common\bin\wlst.cmd" StartDomainSummarizer.py



pause

ENDLOCAL