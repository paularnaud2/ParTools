from reqlist import run_reqList
from reqlist import gl

if __name__ == '__main__':
    # QDD SMO ADAM/GINKO
    ""
    DB = 'ADAM'
    QUERY_FILE = 'reqlist/queries/ADAM_INFOS_SRV.sql'
    run_reqList(DB, QUERY_FILE, gl.IN_FILE, gl.OUT_FILE)

    DB = 'GINKO'
    QUERY_FILE = 'reqlist/queries/GINKO_INFOS_SMO.sql'
    run_reqList(DB, QUERY_FILE, gl.OUT_FILE, gl.OUT_FILE)
    ""

    # QDD ctr_frn SGE/GINKO
    """
    DB = 'SGE'
    QUERY_FILE = 'reqlist/queries/PRM_INFOS_PDL.sql'
    run_reqList(DB, QUERY_FILE, gl.IN_FILE, gl.OUT_FILE)

    DB = 'GINKO'
    QUERY_FILE = 'reqlist/queries/GINKO_INFOS_PDS.sql'
    run_reqList(DB, QUERY_FILE, gl.OUT_FILE, gl.OUT_FILE)
    """

    # QDD oppositions ADAM/GINKO
    """
    DB = 'SGE'
    QUERY_FILE = 'reqlist/queries/PRM_ETAT-SI-NIV.sql'
    run_reqList(DB, QUERY_FILE, gl.IN_FILE, gl.IN_FILE)

    DB = 'ADAM'
    QUERY_FILE = 'reqlist/queries/ADAM_OPPENR.sql'
    run_reqList(DB, QUERY_FILE, gl.IN_FILE, gl.IN_FILE)
    """

    # QDD ctr SGE/GINKO
    """
    DB = 'SGE'
    QUERY_FILE = 'reqlist/queries/SGE_ETAT_SI.sql'
    run_reqList(DB, QUERY_FILE, gl.IN_FILE, gl.IN_FILE)

    DB = 'GINKO'
    QUERY_FILE = 'reqlist/queries/GINKO_DATE_MODIF.sql'
    run_reqList(DB, QUERY_FILE, gl.IN_FILE, gl.IN_FILE)
    """
