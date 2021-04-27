# PyTools

This package contains a bunch of Python tools I have developped and used as a Support / Test Engenieer.
You can mainly use them for:

- Performing multithread SQL queries on an Oracle DB (sql)
- Performing multithread SQL queries on a given perimeter on an Oracle DB (reqlist)
- Comparing and sorting potentially big files (dq)
- Reading and searching potentially big files (toolBF)
- Parsing potentially big XML files (toolParseXML)
- Searching and removing duplicates (toolDup)
- Filtering potentially big file with flexible conditions (toolFilter)
- Splitting potentially big files (toolSplit)
- Sending mails (mail)

## Quickstart

Dowload code, extract zip and run `pip install -e .` at the root.

You'll find examples of use and descriptions of the different available packages and functions in the _quickstart_ folder.
If you want to use the cx*Oracle dependant packages (sql and reqlist), you'll need an [Oracle instant client](https://www.oracle.com/uk/database/technologies/instant-client/downloads.html) whose directory you can set in the conf.py* file.

## Good to know

### The common package

The pytools package includes a _common_ package which provides generic functions used by other the packages. As you may find usefull to use some of them for your own code, I recommend you to check out the list of those functions in pytools/common/\_\_init\_\_.py. Here are a few examples:

- `save_list`: saves a list into a text file
- `load_txt`: loads a text file into a string or a list
- `get_file_list`: returns the list of the files in a folder
- `like`: behaves as the LIKE of SQL (you can match strings with joker character '\*')
- `big_number`: converts a potentially big number into a lisible string. For example 10000000 becomes '10 000 000'
- `get_duration_string`: outputs a string representing the time elapsed since the input start_time. For example '3 minutes and 20 seconds'.

### Logging with the common package

If you want the `log` function to actually fill a log file, you have to use `init_log()` before using it, otherwise it will just print out the log info in the console.

The `step_log` function

### The PT folder

### The conf.py file

### The common package

### The global variable file gl.py

### Main package functions input

### The step_log function

### Recovery functionnality
