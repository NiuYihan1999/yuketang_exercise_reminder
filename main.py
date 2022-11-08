import time
import ddddocr
import winsound

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver import ActionChains
from urllib.request import urlretrieve, urlopen

from win32api import GetSystemMetrics
from win32con import DESKTOPHORZRES
from win32gui import GetDC
from win32print import GetDeviceCaps

ykt_url = "http://pro.yuketang.cn/"
normal_login_xpath = '/html/body/div[2]/div[2]/div[2]/div[1]/img'
account_xpath = "/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/input"
password_xpath = "/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div/input"
login_xpath = "/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div[5]"
slide_xpath = '//*[@id="tcaptcha_drag_thumb"]'

listen_xpath = '//*[@id="tab-student"]'

timeout_time = 5


def get_user_data(file_name: str):
    f = open(file_name, 'r')
    user_data = eval(f.read())
    get_account = user_data['account']
    get_password = user_data['password']

    f.close()
    return get_account, get_password


def get_distance(target_bytes=None, background_bytes=None):
    det = ddddocr.DdddOcr(det=False, ocr=False)
    if target_bytes is None:
        with open('./target.png', 'rb') as f:
            target_bytes = f.read()
    if background_bytes is None:
        with open('./background.png', 'rb') as f:
            background_bytes = f.read()
    res = det.slide_match(target_bytes, background_bytes, simple_target=True)
    proportion = GetDeviceCaps(GetDC(0), DESKTOPHORZRES) / GetSystemMetrics(0)
    # print(res, proportion)
    return round((res["target"][0]) * 1.01 / proportion)


# def download_img(imgsrc, filename):
#     print(imgsrc)
#     # img_str = imgsrc.split(',')[1]
#     img_data = base64.b64decode(imgsrc)
#
#     with open(f'./{filename}.png', 'wb') as f:
#         f.write(img_data)


def login(login_driver: webdriver.Chrome, login_account, login_password):
    cnt = 0
    while True:
        try:
            login_driver.find_element(By.XPATH, normal_login_xpath).click()
            login_driver.find_element(By.XPATH, account_xpath).send_keys(login_account)
            login_driver.find_element(By.XPATH, password_xpath).send_keys(login_password)
            login_driver.find_element(By.XPATH, login_xpath).click()
            break
        except:
            time.sleep(0.2)
            cnt += 1
            if cnt > timeout_time / 0.2:
                return False
            continue

    # 切换到验证码的frame！！！！！！
    login_driver.switch_to.default_content()
    captcha_frame = None
    cnt = 0
    while True:
        time.sleep(0.2)
        try:
            captcha_frame = login_driver.find_element(By.XPATH, '//*[@id="tcaptcha_iframe"]')
            break
        except:
            cnt += 1
            if cnt > timeout_time / 0.2:
                return False
            continue
    login_driver.switch_to.frame(captcha_frame)

    target_src = None
    background_src = None
    cnt = 0
    while True:
        time.sleep(0.5)
        try:
            target_src = login_driver.find_element(By.XPATH, '//*[@id="slideBlock"]').get_attribute('src')
            background_src = login_driver.find_element(By.XPATH, '//*[@id="slideBg"]').get_attribute('src')
            break
        except:
            cnt += 1
            if cnt > timeout_time / 0.5:
                return False
            continue

    # urlretrieve(target_src, "target.png")
    # urlretrieve(background_src, "background.png")
    target_bytes = urlopen(target_src).read()
    background_bytes = urlopen(background_src).read()

    distance = get_distance(target_bytes, background_bytes)

    # time.sleep(1)
    action_chains = ActionChains(login_driver)
    ele = login_driver.find_element(By.XPATH, slide_xpath)
    action_chains.drag_and_drop_by_offset(ele, xoffset=distance, yoffset=0).perform()
    # action_chains.click_and_hold(ele).perform()
    # action_chains.move_by_offset(1, 0).perform()
    # time.sleep(1)
    # action_chains.release().perform()
    login_driver.find_element(By.XPATH, slide_xpath).click()
    # time.sleep(3)
    # action_chains.click().perform()

    cnt = 0
    while True:
        if str(driver.current_url).find('index') >= 0:
            return True
        time.sleep(0.2)
        cnt += 1
        if cnt > 25:
            return False


def init(options: dict = None):
    if options is None:
        options = webdriver.ChromeOptions()
        options.page_load_strategy = 'none'
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 实现了规避监测
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--start-maximized')
        options.add_argument('disable-infobars')
        options.add_argument('log-level=3')  # INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0

    init_driver = webdriver.Chrome(options=options)
    # init_driver.maximize_window()
    # init_driver.minimize_window()
    return init_driver


if __name__ == "__main__":
    account, password = get_user_data('user_data.txt')
    driver = init()
    while True:
        driver.get(ykt_url)
        if login(driver, account, password):
            break

    while True:
        try:
            driver.switch_to.default_content()
            driver.find_element(By.XPATH, listen_xpath).click()
            break
        except:
            time.sleep(0.2)
            continue

    exercise_list = []
    while True:
        now_handle = driver.window_handles[-1]
        try:
            if now_handle != driver.current_window_handle:
                driver.switch_to.window(now_handle)
        except:
            driver.switch_to.window(now_handle)

        # for window_handle in driver.window_handles:
        #     driver.switch_to.window(window_handle)

        if str(driver.current_url).find('exercise') >= 0:
            if driver.current_url not in exercise_list:
                exercise_list.append(driver.current_url)
                exercise_num = len(exercise_list)
            else:
                exercise_num = exercise_list.index(driver.current_url) + 1

            print(time.strftime('%Y-%m-%d %H:%M:%S:', time.localtime(time.time())), 'exercise %d!' % exercise_num)
            winsound.Beep(440, 300)
            for i in range(4):
                winsound.Beep(650, 550)
                winsound.Beep(900, 750)

            time.sleep(3)
        time.sleep(2)
