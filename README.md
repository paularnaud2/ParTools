# PyTools

This package contains a bunch of Python tools I have developped and used as a Support / Test Engenieer.
You can mainly use them for:

- Performing multithreaded SQL queries on Oracle DB (sql)
- Performing multithreaded SQL queries on a given perimeter on Oracle DB (reqlist)
- Comparing and sorting potentially big files (dq)
- Reading and searching potentially big files (toolBF)
- Parsing potentially big XML files (toolParseXML)
- Searching and removing duplicates (toolDup)
- Filtering potentially big file with flexible conditions (toolFilter)
- Splitting potentially big files (toolSplit)
- Sending mails (mail)

## Quickstart

Extract zip and run: ``pip install -e .`` at the root.  

You'll find examples of use and descriptions of the different available packages and functions in the *run* folder.
If you want to use the cx-Oracle dependant packages (sql and reqlist), you'll need an [Oracle instant client](https://www.oracle.com/uk/database/technologies/instant-client/downloads.html) whose path you can set in the *conf/_conf_main.py* file.
