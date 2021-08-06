import partools.utils as pt


def simple(in1,
           in2,
           log=False,
           elt_nb=False,
           raise_e=True,
           e_infos='',
           comp='equal',
           type='float'):

    if comp in ['inferior', 'superior'] and type == 'float':
        in1str = pt.big_number(in1)
        in2str = pt.big_number(in2)
        in1 = float(in1)
        in2 = float(in2)
    else:
        in1str = f"'{in1}'"
        in2str = f"'{in2}'"

    scomp = comp if comp == 'contains' else f'is {comp} to'

    if log:
        pt.log(f"Checking: {in1str} {scomp} {in2str}")

    equal = comp == 'equal' and in1 == in2
    inf = comp == 'inferior' and in1 < in2
    sup = comp == 'superior' and in1 > in2
    contains = comp == 'contains' and in2 in in1
    if equal or inf or sup or contains:
        return True
    else:
        s1 = f"for elt No. {elt_nb}" if elt_nb else ''
        s2 = f' is not {comp} to '
        s = f"Check failed{s1}: {in1str}{s2}{in2str}"
        pt.log(s)
        if raise_e:
            if e_infos:
                pt.log_print("Detailed infos:")
                pt.log_print(e_infos)
            raise AssertionError
        else:
            return False


def ar_col(ar,
           ref,
           col,
           col_name='',
           transfo_elt='',
           comp='equal',
           type='float'):

    if col_name:
        s = f"Checking: all '{col_name}' values are {comp} to '{ref}'"
        pt.log(s)
    for i, elt in enumerate(ar):
        if transfo_elt:
            cur = transfo_elt(elt[col])
        else:
            cur = elt[col]
        if not simple(
                cur, ref, elt_nb=i + 1, raise_e=False, comp=comp, type=type):
            pt.log_print("Current table:")
            pt.log_array(ar)
            raise AssertionError
    return True
