import partools.utils as u

from . import gl


def read_file(in_file):

    if gl.LINE_PER_LINE:
        line = in_file.readline()
    else:
        line = in_file.read(gl.BUFFER_SIZE)
    gl.c_main += 1

    return line


def check_counter(in_file):

    if gl.c_read % gl.N_READ == 0:
        if gl.TEST:
            u.log_print(gl.s_prompt)
            u.log_print('e (TEST = True)')
            command = 'e'
        else:
            command = u.log_input(gl.s_prompt)
        u.log_print()
        if command == '':
            return True
        if command == 'q':
            return False
        if command == 'e':
            goto_eof(in_file)
        if command[0].isdigit():
            skip(command, in_file)

    return True


def goto_eof(in_file):

    cur_list = []
    line = read_file(in_file)
    cur_list.append(line)
    while line != "":
        line = read_file(in_file)
        cur_list.append(line.strip("\n"))
        if len(cur_list) > gl.N_READ + 1:
            del cur_list[0]

    u.log_array(cur_list)
    bn = u.big_number(gl.c_main - 1)
    if gl.LINE_PER_LINE:
        s = f"EOF reached. {bn} lines read."
    else:
        s = f"EOF reached. {bn} buffers of {gl.BUFFER_SIZE} characters read."
    u.log(s)


def skip(nb, in_file):
    i = 0
    while i < int(nb):
        i += 1
        read_file(in_file)


def fill_cur_list(in_file):

    gl.c_list += 1
    gl.cur_list = []
    gl.c_cur_row = 0
    s = f"Generating temporary list no. {gl.c_list}..."
    u.log(s, 1)

    while gl.c_cur_row < gl.MAX_LIST_SIZE:
        gl.c_cur_row += 1
        if gl.LINE_PER_LINE:
            line = get_line_lpl(in_file)
        else:
            line = get_line_buf(in_file)
        if gl.EOF:
            return
        gl.cur_list.append(line)
    u.log("Temporary list generated", 1)


def get_line_lpl(in_file):

    line = in_file.readline()
    if line == '':
        gl.EOF = True
        return
    return line


def get_line_buf(in_file):
    # For the buffer, end of previous line is taken to
    # guarantee the integrity of searched string

    line = in_file.read(gl.BUFFER_SIZE)
    if gl.c_cur_row > 1:
        prev_line = gl.cur_list[gl.c_cur_row - 2].strip('\n')
        end_prev_line = prev_line[-len(gl.LOOK_FOR):]
        line = end_prev_line + line
    if line == '':
        gl.EOF = True
        return
    return line + '\n'


def search_cur_list():

    s = f"Temp list no. {gl.c_list} search"
    u.log(s, 1)
    i = 0
    for elt in gl.cur_list:
        i += 1
        gl.c_main += 1
        j = elt.find(gl.LOOK_FOR)
        if j != -1:
            found_msg(i, j)
            gl.FOUND = True
            return True
    bn = u.big_number(gl.c_main)
    s = (f"Temp list no. {gl.c_list} search over, string not found"
         f" ({bn} lines read in total)")
    u.log(s, 1)
    return False


def found_msg(i, j):

    gl.c_row = i
    bni = u.big_number(i)
    bn = u.big_number(gl.c_main)
    if gl.LINE_PER_LINE:
        s = (f"String found in line no. {bni} of list no. {gl.c_list}"
             f" (global line no. {bn}) in col {j + 1}!")
    else:
        s = (f"String found in buffer no. {bn}"
             f" (buffer list no. {gl.c_list}) in col {j + 1}!")
    u.log(s)
