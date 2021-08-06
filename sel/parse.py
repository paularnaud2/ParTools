import lxml.html
import partools.utils as pt

from . import g


def get_elt(x_path):
    root = lxml.html.fromstring(g.source)
    elt = root.xpath(x_path)
    if elt:
        pt.log(f"Element found ({x_path})")
    else:
        pt.log(f"Element not found ({x_path})")

    return elt


def table(table_xpath, elt_path='td', use_idx=False):

    tbody = get_elt(table_xpath)
    rows = tbody[0].findall('tr')
    out = []
    counter = 0
    for row in rows:
        cols = row.findall(elt_path)
        if not cols:
            out.append([''])
            continue
        new_cols = []
        for elt in cols:
            if elt.text:
                new_cols.append(elt.text.strip())
            else:
                new_cols.append('')
        if counter == 0 and use_idx:
            idx = get_index(new_cols)
        if use_idx:
            new_cols = [new_cols[i] for i in idx]
        else:
            new_cols = [elt for elt in new_cols if elt]
        out.append(new_cols)
        counter + 1
    return out


def get_index(cols):

    idx = []
    for i, elt in enumerate(cols):
        if elt and elt[0].isalnum():
            idx.append(i)
    return idx


def text(txt):

    rows = txt.split('\n')
    rows = [elt.split('') for elt in rows]
    out = []
    for row in rows:
        cols = [elt for elt in row if elt]
        out.append(cols)
    return out


def split_array(ar):
    ars = []
    new_ar = ar
    while True:
        i_min, i_max = get_ar_boundaries(new_ar)
        if i_min == 0:
            break
        cur_ar = new_ar[i_min:i_max]
        ars.append(cur_ar)
        new_ar = new_ar[i_max:]
    return ars


def get_ar_boundaries(ar):

    i, i_min, i_max = 0, 0, 0
    for row in ar:
        if row and '---' in row[0]:
            i_min = i + 1
        if not row and i_min > 0:
            i_max = i
            return i_min, i_max
        i += 1
    i_max = i
    return i_min, i_max


def sub_list(list_in, elt1, elt2='', offset1=0, offset2=0):

    i1 = list_in.index(elt1) + offset1
    if elt2:
        i2 = list_in.index(elt2) - offset2
    else:
        i2 = len(list_in) - offset2

    out = list_in[i1:i2]
    return out
