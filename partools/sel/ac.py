from selenium.webdriver.common.action_chains import ActionChains

from sel import g
from sel import cfg
from sel import browse as b

b.load_webpage("https://www.geeksforgeeks.org/")
e = g.driver.find_element_by_link_text("Courses")
action = ActionChains(g.driver)

# click the item
action.move_to_element(e)
action.click()

# perform the operation
action.perform()

print('ok')
