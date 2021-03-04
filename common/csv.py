from common import g


def get_csv_fields_dict(in_dir):
    fields = {}
    with open(in_dir, 'r', encoding='utf-8') as in_file:
        header = in_file.readline()

    line_list = csv_to_list(header)
    for i, elt in enumerate(line_list):
        fields[elt] = i

    return fields


def load_csv(in_dir):
    g.counters["csv_read"] = 0
    out_list = []
    with open(in_dir, 'r', encoding='utf-8') as in_file:
        for line in in_file:
            line_list = csv_to_list(line)
            out_list.append(line_list)
            g.counters["csv_read"] += 1

    return out_list


def csv_to_list(line_in):
    return line_in.strip('\n').split(g.CSV_SEPARATOR)


def save_csv(array_in, out_file_dir, att='w'):
    with open(out_file_dir, att, encoding='utf-8') as out_file:
        for row in array_in:
            write_csv_line(row, out_file)


def write_csv_line(row, out_file):
    if isinstance(row, str):
        line_out = row
    else:
        line_out = g.CSV_SEPARATOR.join(row)
    line_out += '\n'
    out_file.write(line_out)


def csv_clean(s):
    out = s.replace('\r', '')
    out = out.replace('\n', '')
    out = out.replace(g.CSV_SEPARATOR, '')
    return out
