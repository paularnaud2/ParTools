import partools.utils as u
from . import gl


def group_by():
    out_path = gl.OUT_PATH
    header = u.get_header(out_path, True)
    vol_fields = [elt for elt in header if is_vol_field(elt)]
    if len(vol_fields) == 0:
        return
    else:
        gl.COUNT = True
        vol_field = vol_fields[0]

    if not gl.MERGE_OK or not gl.range_query:
        return

    u.log('Group by on output file...')

    array_in = u.load_csv(out_path)
    gb_fields = [elt for elt in header if not is_vol_field(elt)]
    if gb_fields:
        import pandas as pd
        df = pd.DataFrame(data=array_in[1:], columns=header)
        df[vol_field] = df[vol_field].astype(int)
        df = df.groupby(by=gb_fields).sum()
        df = df.sort_values(by=vol_field, ascending=False)
        df.to_csv(path_or_buf=gl.OUT_PATH, sep=';', encoding='UTF-8')
    else:
        # if this is a simple count result without group by statement
        # results of different files are directly summed (pandas not needed)
        cur_list = [int(elt[0]) for elt in array_in[1:]]
        out = [array_in[0], [str(sum(cur_list))]]
        u.save_csv(out, gl.OUT_PATH)
    u.log('Group by over')


def is_vol_field(elt):
    vol_fields = ['VOL', 'NB', 'COUNT']
    for x in vol_fields:
        if x in elt:
            return True

    return False
