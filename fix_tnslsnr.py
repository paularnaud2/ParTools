import common.sTools as st

script = com.load_txt('sql/scripts/fix_tnslsnr.sql', False)
st.run_sqlplus(script)
