def merge_arrays(ar1, ar2):

    if not len(ar1) == len(ar2):
        s = "The two arrays must be of same length to be merged"
        raise Exception(s)

    out = []
    for i, row in enumerate(ar1):
        out.append(row + ar2[i])
    return out


def sub_array(ar, col, value_list=[]):

    index_list = []
    for i, row in enumerate(ar):
        if row[col] in value_list:
            index_list.append(i)

    out = [ar[i] for i in index_list]
    return out


def get_array_elt(ar, id, col, col_id=0):

    id_list = extract_one_col(ar, col_id)
    if id in id_list:
        i = id_list.index(id)
    else:
        return ''
    elt = ar[i][col]
    return elt


def extract_cols(ar, col_id_list):

    out = []
    for row in ar:
        cur = [row[j] for j in col_id_list]
        out.append(cur)
    return out


def extract_one_col(ar, col_id):

    out = [row[col_id] for row in ar]
    return out
