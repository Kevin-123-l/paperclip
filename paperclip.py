from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from decimal import Decimal

def get_wire_from_js(driver):
    val = driver.execute_script("return window.wire;")
    return Decimal(str(val or 0))
def get_js_variable(driver, variable):
    execute_string = "return " + variable + ";"
    val = driver.execute_script(execute_string)
    return Decimal(str(val or 0))
def memory_processors ():
    sequence = [(1,1),(1,2),(4,2)]
    processors = get_js_variable(driver, "window.processors")
    memory = get_js_variable(driver, "window.memory")
    get_trust = get_js_variable(driver, "window.trust")
    print(get_trust)
    if get_trust > 2:
        index_sequence = 0
        while (processors >= sequence[index_sequence][0]) and (memory >= sequence[index_sequence][1]):
            index_sequence += 1

        if processors < sequence[index_sequence][0]:
            driver.find_element(By.ID, "btnAddProc").click()
        if memory < sequence[index_sequence][1]:
            driver.find_element(By.ID, "btnAddMem").click()
    return
def is_project_visible(driver, name):
    # Returns True if the button is currently in the project list
    return len(driver.find_elements(By.XPATH, f"//div[@id='projectListTop']//button[contains(., '{name}')]")) > 0

opts = Options()
opts.add_argument("--start-maximized")
opts.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=opts)
wait = WebDriverWait(driver, 20)
driver.get("https://www.decisionproblem.com/paperclips/index2.html")
wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
print(driver.title)
make_btn = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//button[contains(., 'Make Paperclip')] | //*[@role='button' and contains(., 'Make Paperclip')]")

))
while True:
    make_btn.click()
    wire = get_wire_from_js(driver)
    if wire < 100:
        driver.find_element(By.ID,"btnBuyWire").click()
    priceperclip = get_js_variable(driver, "window.margin")
    if priceperclip > 0.04:
        driver.find_element(By.ID,"btnLowerPrice").click()
    totalmoney = get_js_variable(driver, "window.funds")
    clippercost = get_js_variable(driver, "window.clipperCost")
    wirecost = get_js_variable(driver, "window.wireCost")
    if totalmoney > (clippercost + wirecost):
        driver.find_element(By.ID,"btnMakeClipper").click()
    memory_processors()
