import time
from datetime import datetime

from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.support import expected_conditions as EC

from sel import cfg
import partools.utils as pt

from . import g


def catch_nswe(func):
    def new_f(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NoSuchWindowException:
            switch_to_window(0)
            return func(*args, **kwargs)

    new_f.__name__ = func.__name__
    return new_f


def start_driver():

    if not g.driver:
        options = wd.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        pt.log(f"Starting Chrome driver ({cfg.DRIVER_PATH})...")
        g.driver = wd.Chrome(cfg.DRIVER_PATH, options=options)
        g.driver.set_window_size(1800, 900)
        g.driver.implicitly_wait(10)
        pt.log("Chrome driver started")


def quit_driver():

    if g.driver:
        pt.log("Closing Chrome driver...")
        g.driver.quit()
        g.driver = None
        pt.log("Chrome driver closed")


@catch_nswe
def wait_until(xpath, timeout=10, text=False):

    wait = WebDriverWait(g.driver, timeout)
    pt.log(f"Waiting for element '{xpath}' (timeout={timeout})")
    elt = (By.XPATH, xpath)
    elt_is_present = EC.visibility_of_element_located(elt)
    if text:
        elt_is_present = EC.text_to_be_present_in_element(elt)
        elt = wait.until(elt_is_present)
        pt.log("Element found")
    return elt


@catch_nswe
def wait_until_clickable(xpath, timeout=10):

    pt.log(
        f"Waiting for element to be clickable '{xpath}' (timeout={timeout})")
    wait = WebDriverWait(g.driver, timeout)
    elt = (By.XPATH, xpath)
    button_is_clickable = EC.element_to_be_clickable(elt)
    elt = wait.until(button_is_clickable)
    pt.log("Element is clickable")
    return elt


@catch_nswe
def click_elt(xpath, sleep_before=False, sleep_after=False, timeout=10):

    elt = wait_until_clickable(xpath, timeout)
    sleep(sleep_before)
    elt.click()
    pt.log("Element clicked")
    sleep(sleep_after)


def sleep(inp):

    if inp:
        pt.log(f"Sleeping for {inp} seconds...")
        time.sleep(inp)


@catch_nswe
def send_keys(xpath, keys, hide=False, clear=False, sleep_after=False):

    elt = wait_until(xpath)
    if clear:
        elt.clear()

    skeys = '*' * len(keys) if hide else keys
    shide = ' (hidden)' if hide else ''
    pt.log(f"Sending keys '{skeys}{shide}")
    elt.send_keys(keys)
    pt.log("Keys sent")

    if sleep_after:
        sleep(sleep_after)


@catch_nswe
def load_webpage(url,
                 reget=False,
                 refresh=False,
                 iFrame=False,
                 sleep_after=False,
                 clear_cache_bool=False):

    if not g.driver:
        start_driver()

    pt.log(f"Loading webpage {url}...")

    if clear_cache_bool:
        clear_cache()

    try:
        g.driver.get(url)
    except NoSuchWindowException:
        switch_to_window(0)
        g.driver.get(url)

    if reget:
        pt.log('Regetting...')
        g.driver.get(url)
        time.sleep(2)

    if refresh:
        pt.log('Refreshing...')
        g.driver.refresh()

    if iFrame:
        switch_to_frame(iFrame)

    if sleep_after:
        sleep(sleep_after)

    screenshot()
    g.cur_url = url

    pt.log("Webpage successfully loaded")


@catch_nswe
def switch_to_frame(iFrame, timeout=10):

    pt.log(f"Switching to iFram '{iFrame}'...")
    wait_until(f'//*[@id="{iFrame}"l', timeout)
    g.driver.switch_to.frame(iFrame)


def switch_to_window(i):
    h = g.driver.window_handles
    g.driver.switch_to.window(h[i])
    pt.log(f"Switched to windows No. {i}")


@catch_nswe
def screenshot():
    if not g.driver:
        return

    t = datetime.now().strftime('%H%M%S')
    rnd = pt.gen_random_string(4)
    g.s_dir = f"{g.path}SCREENSHOTS/"
    pt.mkdirs(g.s_dir)
    path = f"{g.s_dir}{t}_{rnd}.png"
    g.driver.save_screenshot(path)
    pt.log(f"Screenshot saved in {path}")


@catch_nswe
def clear_cache():
    pt.log("Clearing Chrome cache...")
    g.driver.delete_all_cookies()
    pt.log("Cache cleared")


@catch_nswe
def save_source(name='SOURCE'):
    source = g.driver.page_source
    path = f"{g.path}{name}.html"
    pt.save_list([source], path)
    pt.log(f"Page source saved in {path}")


def load_source(name='SOURCE'):
    path = f'{g.path}{name}.html'
    out = pt.load_txt(path, False)
    g.source = out
    # pt.log(f"Source loaded from {path}")
    return out


def save_infos(infos, name='INFOS'):
    path = f'{g.path}{name}.txt'
    pt.save_list([infos], path)
    pt.log(f"Infos saved in {path}")


def load_infos(name='INFOS'):
    path = f"{g.path}{name}.txt"
    out = pt.load_txt(path, False)
    pt.log(f"Infos loaded from {path}")
    return out
