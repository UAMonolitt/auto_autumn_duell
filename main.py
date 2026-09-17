from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, logging
from secrets_config import secrets

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

options = Options()
options.add_argument('--headless=new')
options.add_argument("--no-sandbox")   
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)
driver.execute_cdp_cmd(
    "Emulation.setTimezoneOverride", {"timezoneId": "Europe/Oslo"}
)
def get_text(element):
    try:
        return element.text
    except:
        for func, argument in [(element.get_attribute, 'innerHTML'), (element.get_attribute, 'textContent')]:
            try:
                return func(argument)
            except:
                pass
        else:
            return None

def work():
    logging.info('Start working')
    while True:
        time.sleep(1)  
        try:
            driver.find_element(By.XPATH, '/html/body/div/div/div/div/main/div/div/div[4]/div/div[2]/div/div[2]/div[2]/div/button[2]/span')
            driver.save_screenshot('images/finish.png')
        except:
            pass 
        try:
            oppgave = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div/div/main/div/div/div[3]/div/div[1]/div[1]/div/div/h1')))
        except:
            driver.save_screenshot('images/no_task.png')
            logging.info('No task found')
            logging.info(f'Trying to find task...')
            for y in range(5):
                try:
                    driver.find_element(By.XPATH, '/html/body/div/div/div/div/main/div/div/div[4]/div/div[2]/div/div[2]/div[2]/div/button[2]/span')
                except:
                    pass
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
                    oppgave = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div/main/div/div/div[3]/div/div[1]/div[1]/div/div/h1')))
                except:
                    driver.get('https://skolenmin.cdu.no/komponent/multiplikasjon-6a85583e4939621a37bd6c8c?&_=hostduell-6a8467758a5d4d1392dc6936')
                    continue
        oppgave = get_text(oppgave)
        if oppgave is None or len(oppgave.split()) != 5:
            logging.info('No task found?')
            continue
        logging.info('Found task')
        oppgave = oppgave.split()
        assert len(oppgave) == 5, f'Length is not 5, length is {len(oppgave)}'
        if oppgave[2] == '?':
            answer = int(oppgave[-1]) // int(oppgave[0])
        elif oppgave[0] == '?':
            answer = int(oppgave[-1]) // int(oppgave[2])
        elif oppgave[-1] == '?':
            answer = int(oppgave[0]) * int(oppgave[2])
        else:
            raise ValueError('No answer')
        logging.info(f'Task: {oppgave}')
        WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, '/html/body/div/div/div/div/main/div/div/div[3]/div/div[1]/div[2]/ul/li')))
        logging.info(f'Answer: {answer}')
        for check_id in range(1,5):
            locator = (By.XPATH, f'(/html/body/div/div/div/div/main/div/div/div[3]/div/div[1]/div[2]/ul/li)[{check_id}]//button')
            try:
                check = WebDriverWait(driver, 2.5).until(EC.visibility_of_element_located(locator))
            except:
                logging.info('No alternative found?')
                driver.save_screenshot('images/no_answer.png')
                break
            check_text = get_text(check)
            if check_text is None:
                break
            logging.info(f'Variant {check_id}: {check_text}')
            try:
                if str(check_text) == str(answer):
                    logging.info(f'Variant {check_id}: ({check.text}) is right')
                    check.click()
                    break
            except:
                pass
try:
    try:
        logging.info('start')
        driver.get("https://skolenmin.cdu.no")
        enter_box = WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.ID, 'org_selector_filter')))
        enter_box.send_keys('Eigersund municipality')
        driver.save_screenshot("images/viewport.png")

        eigersund_kommunne = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/article/section[2]/form[1]/div[1]/ul/li[750]")))
        eigersund_kommunne.click()
        sumbit = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'selectorg_button')))
        sumbit.click()
        username = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/article/section[2]/div[1]/form[1]/div[1]/input')))
        username.send_keys(secrets.username)
        logging.info('Logging inn')
        password = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/article/section[2]/div[1]/form[1]/div[2]/input')))    # Wait briefly to view the results
        password.send_keys(secrets.password)
        submit = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/article/section[2]/div[1]/form[1]/button')))
        submit.click()
        try:
            WebDriverWait(driver, 2.5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/article/section[2]/ul/li/a'))).click()
        except: 
            pass
        driver.get('https://skolenmin.cdu.no/komponent/multiplikasjon-6a85583e4939621a37bd6c8c?&_=hostduell-6a8467758a5d4d1392dc6936')
    except:
        logging.error('Wrong password, username or something else! See images/error.png')
        raise ValueError('Wrong password, username or somethin else!')
    logging.info('Login successfull. Starting to work.')
    work()
except Exception as exception:
    driver.save_screenshot('images/error.png')
    raise exception
finally:
    driver.quit()
