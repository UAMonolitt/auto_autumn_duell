from selenium import webdriver
from selenium.webdriver.common.by import By
from password import PASSWORD, USERNAME
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 1. Start a browser session (e.g., Chrome)
options = Options()
options.add_argument('--headless=new')
options.add_argument("--no-sandbox")     # Bypasses OS security model (required for Docker/Codespaces)
options.add_argument("--disable-dev-shm-usage")  # Overcomes limited resource problems in containers
driver = webdriver.Chrome(options=options)
driver.execute_cdp_cmd(
    "Emulation.setTimezoneOverride", {"timezoneId": "Europe/Oslo"}
)
def work():
    logging.info('Start working')
    while True:
        time.sleep(0.5)   #wait for task to load 
        try:
            oppgave = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div/main/div/div/div[3]/div/div[1]/div[1]/div/div/h1')))
        except:
            driver.save_screenshot('no_task.png')
            logging.info('No task found')
            for y in range(5):
                logging.info(f'Trying to find task...')
                try:
                    driver.find_element(By.XPATH, '/html/body/div/div/div/div/main/div/div/div[4]/div/div/div/div[2]/div[2]/div/button').click()
                except:
                    pass
                try:
                    driver.find_element(By.XPATH, '/html/body/div/div/div/div/main/div/div/div[3]/div/div/div[2]/button').click()
                except:
                    pass
                try:
                    driver.find_element(By.XPATH, '/html/body/div/div/div/div/main/div/div/div[3]/div/div/div[2]/div/div/div[2]/button').click()
                except:
                    pass
            if y == 4:
                try:
                    oppgave = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div/main/div/div/div[3]/div/div[1]/div[1]/div/div/h1')))
                except:
                    driver.save_screenshot('finish.png')
                    driver.get('https://skolenmin.cdu.no/komponent/multiplikasjon-6a85583e4939621a37bd6c8c?&_=hostduell-6a8467758a5d4d1392dc6936')
                    continue
        logging.info('Found task')
        oppgave = oppgave.text
        oppgave = oppgave.split()
        assert len(oppgave) == 5, 'Length is not 5'
        if oppgave[2] == '?':
            answer = int(oppgave[-1]) // int(oppgave[0])
        elif oppgave[0] == '?':
            answer = int(oppgave[-1]) // int(oppgave[2])
        elif oppgave[-1] == '?':
            answer = int(oppgave[0]) * int(oppgave[2])
        else:
            raise ValueError('No answer')
        WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, '/html/body/div/div/div/div/main/div/div/div[3]/div/div[1]/div[2]/ul/li')))
        logging.info(f'Task: {oppgave}')
        logging.info(f'Answer: {answer}')
        for check_id in range(1,5):
            locator = (By.XPATH, f'(/html/body/div/div/div/div/main/div/div/div[3]/div/div[1]/div[2]/ul/li)[{check_id}]//button')
            try:
                check = WebDriverWait(driver, 2.5).until(EC.visibility_of_element_located(locator))
            except:
                logging.info('No alternative found?')
                driver.save_screenshot('no_answer.png')
                break
            logging.info(f'Variant {check_id}: {check.text}')
            try:
                if WebDriverWait(driver, 0.5).until(EC.text_to_be_present_in_element(locator, str(answer))) or (driver.find_element(*locator)).text == str(answer):
                    logging.info(f'Variant {check_id}: ({check.text}) is right')
                    check.click()
                    break
            except:
                pass
try:
    try:
        logging.info('start')
        driver.get("https://skolenmin.cdu.no")
        enter_box = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'org_selector_filter')))
        enter_box.send_keys('Eigersund municipality')
        driver.save_screenshot("viewport.png")

        eigersund_kommunne = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/article/section[2]/form[1]/div[1]/ul/li[750]")))
        eigersund_kommunne.click()
        sumbit = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'selectorg_button')))
        sumbit.click()
        username = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/article/section[2]/div[1]/form[1]/div[1]/input')))
        username.send_keys(USERNAME)
        logging.info('Logging inn')
        password = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/article/section[2]/div[1]/form[1]/div[2]/input')))    # Wait briefly to view the results
        password.send_keys(PASSWORD)
        submit = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/article/section[2]/div[1]/form[1]/button')))
        submit.click()
        try:
            WebDriverWait(driver, 2.5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/article/section[2]/ul/li/a'))).click()
        except: 
            pass
        driver.get('https://skolenmin.cdu.no/komponent/multiplikasjon-6a85583e4939621a37bd6c8c?&_=hostduell-6a8467758a5d4d1392dc6936')
    except:
        logging.error('Wrong password, username or something else! See error.png')
        raise ValueError('Wrong password')
    logging.info('Login successfull. Starting to work.')
    work()
except Exception as exception:
    driver.save_screenshot('error.png')
    raise exception
finally:
    driver.quit()
