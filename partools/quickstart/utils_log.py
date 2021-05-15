# This script shows you simple examples of use for the log and step_log functions

import time
import partools.utils as u

u.log("This won't be logged in a file")
u.init_log('test')
u.log("This will be logged in a file")

out_list = []
u.init_sl_time()
for i in range(1, 21):
    time.sleep(0.05)  # simulates io / calculation
    out_list.append(i)
    u.step_log(i, 5, "elements appended")

u.log_print(f'out_list: {out_list}')
