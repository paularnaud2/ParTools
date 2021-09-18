import tests.test_1_utils as t
import time

t.init_PT()
t.get_duration()
t.like()
t.u.check_log(t.cl.CO)
t.u.log_print()

t.pt.cfg.FILES_DIR = t.back
t.u.g.init_PT(True)
t.u.delete_folder('PT_test_utils/')

print("Sleeping for 5 seconds...")
time.sleep(5)
