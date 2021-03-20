import common as com

script = com.load_txt('sql/scripts/fix_tnslsnr.sql', False)
com.run_sqlplus(script)
