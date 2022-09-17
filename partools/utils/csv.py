SEPARATOR = ';'


def get_csv_fields_dict(in_path):
    """Returns a dictionary whose keys are the csv fields of the 'in_path' file
    and elements are the columns index.
    """
    from . import header

    fields = {}
    line_list = header.get_header(in_path, True)
    for i, elt in enumerate(line_list):
        fields[elt] = i

    return fields


def load_csv(in_path):
    """Loads a csv file and returns a list whose elements correspond to the
    lines of the 'in_path' file.
    Each element is also a list whose elements correspond to the csv fields.
    """

    out_list = []
    with open(in_path, 'r', encoding='utf-8') as in_file:
        for line in in_file:
            line_list = csv_to_list(line)
            out_list.append(line_list)

    return out_list


def csv_to_list(line_in):
    """Converts a csv line to a list using SEPARATOR as separator"""

    return line_in.strip('\n').split(SEPARATOR)


def save_csv(array_in, out_path, mode='w'):
    """Saves a list to a csv file

    - mode: mode for the open methode.
    """

    with open(out_path, mode, encoding='utf-8') as out_file:
        for row in array_in:
            write_csv_line(row, out_file)


def write_csv_line(row, out_file):
    """Writes a line to a csv file

    - row: can be either a list of the csv fields or a csv string
    """

    if isinstance(row, str):
        line_out = row
    else:
        line_out = SEPARATOR.join(row)
    line_out += '\n'
    out_file.write(line_out)


def csv_clean(s):
    """Cleans a csv field by removing csv separators and new line characters"""

    out = s.replace('\r', '')
    out = out.replace('\n', '')
    out = out.replace(SEPARATOR, '')
    return out
