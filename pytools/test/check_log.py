CO = [
    "Log file initialised",
    "Python version:",
    "Testing common.msg_box",
    "Testing common.string.get_duration",
]

TO = [
    "Log file initialised",
    "Python version:",
    "[toolParseXML] parse_xml: start",
    " * lines processed in * ms. * lines processed in total.",
    "Parse dictionary generated (82 lines processed)",
    "2 lines written in * ms. 2 lines written in total.",
    "[toolParseXML] parse_xml: end (3 lines written in * ms)",
    "[dq] file_match: start",
    "[dq] file_match: end",
    "[toolSplit] split_file: start",
    "[toolSplit] split_file: end",
    "[toolDup] find_dup: start",
    "Examples of duplicates (limited to *):",
    "List of duplicates saved in ",
    "[toolDup] find_dup: end",
    "[toolFilter] filter: start",
    " * lines read in * ms. * lines read in total (* lines written in output list).",
    "[toolFilter] filter: end (* ms)",
    "[toolShuf] shuffle_csv: start",
    "[toolShuf] shuffle_csv: end",
    "[toolBF] read_big_file: start",
    "EOF reached. 2 901 lines read.",
    "A05IANDR;290078031;07394934787868",
    "e (TEST = True)",
    "[toolBF] read_big_file: end",
    "[toolBF] search_big_file: start",
    "Searching string '22173227102607' in file *...",
    "String found in line no. 45 of list no. 19 (global line no. 1 845) in col 20!",
    "Current list written in *",
    "[toolBF] search_big_file: end (* ms)",
    "[dq] sort_file: start (*)",
    "Generating first list to be sorted...",
    "Output file * successfully generated (2 897 lines written, 4 duplicates removed).",
    "4 key duplicates found. List written in *",
    "[dq] sort_file: end (* ms)",
]

DQ = [
    "Log file initialised (",
    "Python version:",
    "Error: the input file * must have a header",
    "Make sure the first elements of the first two lines are of different lengths",
    "Error: files * and * don't have the same header. Input files must have the same header.",
    "Warning: 4 different lines with the same research key were identified",
    "File comparison may not work correctly. Here are your options:",
    "c (TEST_PROMPT_DK = True)",
    "List of key duplicates written in file",
    "run_dq job initialised. Input files * and * are going to be sorted and compared.",
    "* lines read in * ms. * lines read in total.",
    "* lines read in * ms. * lines read in total and * lines written in the output file.",
    "Maximum number of lines reached (* lines) for list no. 1, sorting...",
    "Current list sorted. Generating temporary file no. 1...",
    "Temporary file successfully generated, input file reading goes on...",
    "Filling buffer array - Iteration no. *",
    "Emptying buffer array in output file (and removing dupes)...",
    "Deleting temporary file no. 2",
    "Output file * successfully generated (25 lines written, 4 duplicates removed).",
    "Examples of duplicates (limited to *):",
    "Input file has more than * lines. It will be splitted in * files (max file nb set to *). Continue? (y/n)",
    "y (TEST_PROMPT_SPLIT = True)",
    "Splitted file no. 1 (*) successfully generated",
    "[dq] run_dq: start",
    "[dq] sort_file: start (*)",
    "[dq] sort_file: end (* ms)",
    "[dq] compare_files: start",
    "[dq] compare_files: end (* ms)",
    "[dq] run_dq: end (* ms)",
    "[dq] file_match: start",
    "Deep comparison of '*' and '*'...",
    "[dq] file_match: end",
    "[toolSplit] split_file: start",
    "[toolSplit] split_file: end",
]

SQ = [
    "Log file initialised (",
    "Python version:",
    "Error: the input file * must have a header",
    "IUTD (Is Up To Date) check for DB",
    "Can't find IUTD check file",
    "Check file saved in",
    "IUTD check OK",
    "Warning: conf of DB '*' don't seem to be up to date:",
    "y (TEST_IUTD = True)",
    "The date found in the check file doesn't match the current date",
    "Error: the input file * must have a header",
    "Error: either gl.CNX_STR or gl.DB have to be defined",
    "Error: data base * doesn't seem to be defined. Pease check the CONF_ORACLE conf var.",
    "Error: data base * of environment * doesn't seem to be defined. Pease check the CONF_ORACLE conf var.",
    "Make sure the first elements of the first two lines are of different lengths",
    "Subprocess terminated (upload_interrupted)",
    "Injection running detected. Recover? (y/n)",
    "y (TEST_RECOVER = True)",
    "* lines written in * ms. * lines written in total.",
    "Examples of duplicates (limited to *):",
    "Executing query '01' (connection no. 2)...",
    "Query '02' executed (connection no. 3)",
    "Writing lines for query '00' (connection no. 1)...",
    "All lines written for query '01' (149 lines written, connection no. 2)",
    "TEST_RECOVER: Automatic stop (thread no. *)",
    "Range query detected. Base query:",
    "Work in progress detected. Recover? (y/n)",
    "y (TEST_RECOVER = True)",
    "Query list modified according previous work in progress. Recovering from query '*'",
    "lines written in * ms. * lines written in total for query '*' (connection no. *)",
    "Verifying duplicates on the first column of the output file...",
    "Resetting folders...",
    "Reset over",
    "Ranges to be queried: [",
    "Connecting to data base",
    "Connecting to data base * of environment",
    "Creating connection no.",
    "lines written in * ms. * lines written in total for query '06'.",
    "All lines written for query '09' (150 lines written)",
    "Executing query '09'",
    "Query '12' executed",
    "All threads are done",
    "Group by on output file...",
    "Group by over",
    "Cleaning DB...",
    "DROP TABLE TEST",
    "DB cleaned",
    "[sql] upload: start",
    "[sql] upload: end (* ms)",
    "[sql] execute: start",
    "[sql] execute: end (* ms)",
    "[sql] download: start",
    "[sql] download: end (* ms)",
    "[dq] file_match: start",
    "[dq] file_match: end",
    "[toolDup] find_dup: start",
    "[toolDup] find_dup: end",
]

RL = [
    "Log file initialised",
    "Python version:",
    "Error: right array is void",
    "Error: query must contain @@IN@@",
    "Executing query '01' (connection no. 1)...",
    "Query '01' executed (connection no. 1)",
    "Writing lines for query '01'...",
    "All lines written for query '01' (0 lines written, connection no. 1)",
    "Merging and deleting * temporary files...",
    "Data fetched from * (2 900 lines written)",
    "Error: the input file * must have a header",
    "Make sure the first elements of the first two lines are of different lengths",
    "TEST_RECOVER: Automatic stop (thread no. *)",
    "Work in progress detected. Recover? (y/n)",
    "y (TEST_RECOVER = True)",
    "Query list modified according previous work in progress. Recovering from query '*'",
    "Building query list to be input in sql.dowload...",
    "Query list built: 2 894 elements to be processed distributed in 15 groups (200 max per group). They will be processed in parallel by 3 connection pools.",
    "All threads are done",
    "Checking duplicates on the first column of the output file...",
    "Examples of duplicates (limited to *):",
    "Cleaning DB...",
    "DROP TABLE TEST",
    "DB cleaned",
    "[reqlist] left_join_files: start",
    "[reqlist] left_join_files: end (* ms)",
    "[dq] file_match: start",
    "[dq] file_match: end",
    "[sql] upload: start",
    "[sql] upload: end (*)",
    "[sql] execute: start",
    "[sql] execute: end (*)",
    "[reqlist] run_reqList: start",
    "[reqlist] run_reqList: end (*)",
    "[sql] download: start",
    "[sql] download: end (* ms)",
    "[toolDup] find_dup: start",
    "[toolDup] find_dup: end",
]
