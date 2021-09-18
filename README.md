# ParTools
 
This package contains a bunch of Python tools I have developed and used as an IT Test / Support / Automation Engineer.  
You can mainly use them for:
 
- Performing multi threaded SQL queries on an Oracle DB (__sql__)
- Performing multi threaded SQL queries on a given perimeter on an Oracle DB (__rl__)
- Comparing and sorting potentially big files (__dq__)
- Reading and searching potentially big files (__tools.bf__)
- Parsing potentially big XML files (__tools.xml__)
- Searching and removing duplicates (__tools.dup__)
- Filtering potentially big files with flexible conditions (__tools.filter__)
- Splitting potentially big files (__tools.split__)
- Extracting doc string from Python code (__tools.extract_doc__)
- Sending mails with gmail, outlook or without authentication (__mail__)
- Simple logging or logging in loops (``log`` and ``step_log``), manipulating files and strings, running shell commands, generating threaded message boxes and many others (__utils__)
 
## Quickstart
  
    pip install partools
 
Then just run ``import partools`` (or run any partools function) with python to initialise the package.  
You should then see something like this in the console:
 
    ...
    Checkout the README.md on GitHub: https://github.com/paularnaud2/ParTools
    Get started here c:\Git\Test\venv\lib\site-packages\partools\quickstart
    Set up your conf here: c:\Git\Test\venv\lib\site-packages\partools\conf.py
    Happy scripting!
 
This gives you the links to the __quickstart__ folder where you'll find examples of use and descriptions of the different available packages and functions. You'll also find here the link to the __conf.py__ file (see below).
 
If you want to use the __cx_Oracle__ dependant packages (__sql__ and __rl__), you'll need an [Oracle instant client](https://www.oracle.com/uk/database/technologies/instant-client/downloads.html) whose directory you can set in the __conf.py__ file.
 
### The conf.py file
 
The __partools/conf.py__ file contains the __main user settings__ for the __partools__ package such as the path to the Oracle instant client (``ORACLE_CLIENT``). If needed, you can create a __PTconf.py__ file at the root. Attributes found in this file will overwrite default (found in __partools/conf.py__). Similarly, you can also create a __PTconf_perso.py__ file at the root that will take over PTconf.py. This can be useful if you __work on a shared repository__ but still want/need to have your own local configurations.
 
### The global variable files gl.py and main functions inputs
 
Each package has a __gl.py__ file which sets its __global variables and constants__. Each of these variables can be passed to the main package function (e.g. rl.reqlist for the rl package) and if so, overwrites the value defined in the __gl.py__ file. In that respect, __constants defined in the gl.py file can be seen as default input values__.

## The utils package
 
The __partools__ package includes a __utils__ package which provides generic functions used by the other packages. As you may want to use some of them for your own code, I recommend you to check out the list of those functions in __partools/utils/\_\_init\_\_.py__. Here are a few examples:
 
- `save_list`: saves a list into a text file
- `load_txt`: loads a text file into a string or a list
- `list_files`: returns the list of the files in a folder
- `like`: behaves as the LIKE of Oracle SQL (you can match strings with wildcard character '\*'). It returns a re.match object giving you access to the matched wildcards.  
Example: ``m = like('Hello World', 'He\*o w\*d')``, m.group(1) => 'll'
- `big_number`: converts a potentially big number into a lisible string. For example big_number(10000000) returns '10 000 000'.
- `get_duration_string`: outputs a string representing the time elapsed since the input ``start_time``. For example ``get_duration_string(0, end_time=200)`` returns '3 minutes and 20 seconds'.
- ``run_cmd``: runs a Windows shell command (__sTools__)
- ``run_sqlplus``: connects to sqlplus as sysdba and runs a sql script (__sTools__)
- ``msg_box``: opens a threaded message box containing the 'msg' input string. This can be used as a end-process notification (__sTools__)
 
### Logging with the utils package
 
If you want the `log` function to actually fill a log file, you have to run `init_log()` before using it, otherwise it will just print out the log info in the console.  
You can specify a ``log_format`` for the log timestamp which by default is ``'%H:%M:%S -'`` (conf.LOG_FORMAT setting). Here is what a default log line looks like:
 
    19:45:04 - This line has been generated by the partools.utils.log function
 
The `step_log` function allows you to log some information only when the input ``counter`` is a multiple of the input ``step``. Thus, `step_log` is to be used in loops to __track the progress of long processes__ such as reading or writing millions of lines in a file. The ``what`` input expects a description of what is being counted. It's default value is  ``'lines written'``.  
In order to correctly measure the elapsed time for the first log line, the ``step_log`` function has to be initialised by running ``init_sl_time()``.  
So for example, if you input ``step=500`` and don't input any ``what`` value, you should get something like this:
 
    19:45:04 - 500 lines written in 3 ms. 500 lines written in total.
    19:45:04 - 500 lines written in 2 ms. 1 000 lines written in total.
    19:45:04 - 500 lines written in 2 ms. 1 500 lines written in total.
 
Checkout the __utils_log.py__ file in __partools/quickstart__ for a simple example of use.
 
### The PT folder
 
When first used, the __utils__ package gets initialised by creating a __PT__ directory (which you can set in __conf.py__). It is intended to contain the __log files and the temporary files__ generated by the different ParTools's scripts. It also has __in__ and __out__ directories used by the __test__ package (and of course that you can also use for your own scripts using ParTools).
 
## The sql package
 
The __sql__ package provides you with three main functions:
- ``download``: executes multithreaded SELECT or COUNT queries (see partools/quickstart/sql_download.py)
- ``upload``: executes mass insert queries (see partools/quickstart/sql_upload.py)
- ``execute``: executes PL/SQL procedures or SQL scripts (see partools/quickstart/sql_execute.py)
 
The ``download`` function has three main cases of use:
- Writing the result of a simple SELECT/COUNT query in a csv file
- Processing a list of SELECT/COUNT queries in parallel
- Processing a range query ie. a variabilized query which is executed in parallel for a specified range of KEYs/IDs

Each of these cases is detailed in __partools/quickstart/sql_download.py__
 
## The rl package
 
The __rl__ package has two main functions:
- ``reqlist``: executes a multithreaded SELECT query on a perimeter given by a csv file. The SQL output can be joint to the input file (see partools/quickstart/reqlist.py)
- ``left_join_files``: performs a joint between two csv files. This function is used by reqlist to joint the SQL result to the input file.

## Sending emails
 
ParTools is provided with a __mail__ package allowing you to easily send HTML emails with Python. Three functions are available corresponding to different infrastructure/environment usages:
 
- ``gmail``: for personal computer/network use
- ``no_auth``: for business computer/network use (if an internal no authentication smtp server is available)
- ``outlook``: for business computer/network use (uses your Outlook application)
 
In order for the mail package to be working, you have to initialise a mail folder by running the 'init_mail' function. This will create a folder in the MAIL_DIR defined in 'conf.py' ('mails/' by default).
 
If you want to use the gmail or no_auth functions, you have to set a confidential.txt file. This file must be saved at the CFI_PATH defined in the partools/conf.py file (root by default) using the example provided in the initialised folder. 
 
The initialised folder contains the mail folders corresponding to the mail_name passed in the mail function. As you'll notice, it initially contains a 'test' folder, allowing you to quickly test the function and to provide you with an example of what a 'mail_name' folder is expected to contain. USER_GMAIL and PWD_GMAIL are only to be set if you use the ``gmail`` function.
 
So you'll see two files in the mails/test folder:
- template.html: the HTML template for the body of your mail. It can contain variables delimited by @@ (in the example @@NAME@@ and @@DATE@@) which are replaced using the ``var_dict`` passed in input.
- recipients.txt: the list of recipients here containing three fictitious recipients. For your test, it is advised to just let one line with your address.
 
You can also directly input a recipients list and a HTMLbody. In that case, setting the template.html and recipients.html is not needed. If you input a ``HTMLbody`` and a ``var_dict``, your ``HTMLbody`` input will be seen as a template whose variables will be replaced using the ``var_dict``.
 
For the no_auth function, you'll need to set the host in the conf file (``HOST_NO_AUTH``).
 
 
## Recover functionalities
 
``sql.download``, ``rl.reqlist`` and ``sql.execute`` have a __recovery functionality__. This means that if the process is unexpectedly stopped (e.g. because of network issues), then when relaunched, the script __automatically restarts from where it stopped__. When you run long processes (e.g. extracting millions of lines from a database), this can save you a significant amount of time if something goes wrong (especially when close to the end!).  
The reliability of these recovery mechanisms is ensured by automated tests using the ``multiprocessing`` library to simulate the unexpected process interruption.
 
Happy scripting!
 


