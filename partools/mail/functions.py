import sys
from . import gl
import partools.utils as u


def check_internal(recipients):

    sint = gl.INTERNAL_STR
    u.log(f"Checking if all recipients are internal (ie. contain '{sint}')")
    not_int = [elt for elt in recipients if sint not in elt]
    if not_int:
        if len(not_int) > 1:
            s = f'Warning: "{not_int}" are not internal email addresses. Send anyways? (y/n)'
        else:
            s = f'Warning: "{not_int}" is not an internal email address. Send anyways? (y/n)'

        if gl.TEST:
            u.log(s)
            u.log_print('y (TEST = True)')
        elif not u.log_input(s) == 'y':
            sys.exit()


def save_mail(HTMLbody):

    gl.last_sent = gl.mail_dir + 'last_sent.html'
    u.save_list([HTMLbody], gl.last_sent)
    u.log(f"Mail saved to {gl.last_sent}")
