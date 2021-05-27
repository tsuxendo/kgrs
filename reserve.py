import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from time import sleep

try:
    import chrome_driver
except:
    import chromedriver_binary

# うまくいかなければ'shift_jis'を試してみる。
ENCODING = 'utf-8'
# うまくいかなければのばしてみる。（時間はかかる）
WAIT_TIME = 1.0
WAIT_LONG_TIME = 10.0
# 予約種目
PURPOSE = 'バスケットボール'
# 予約施設
FACILITY = '東山地域体育館'

URL = "https://g-kyoto.pref.kyoto.lg.jp/reserve_j/core_i/init.asp?SBT=1"
DATETIMES = pd.read_csv('./datetime.csv', encoding=ENCODING)
USERS = pd.read_csv('./user.csv', encoding=ENCODING)

def main():
    driver = set_driver(URL)

    # ユーザーを一人一人実行
    for num in range(USERS.shape[0]):
        user = USERS.loc[num]
        # ログイン
        try:
            login(driver, user)
            print(f'{user.fullname}さんでログインしました。')
        except:
            print(f'{user.fullname}さんでログインに失敗しました。次の人に進みます。')
            driver = set_driver(URL)
            continue
        wait_func()
        # 目的を選択
        driver.find_element_by_partial_link_text(PURPOSE).click()
        # 予約日時を一つ一つ実行
        for num in range(DATETIMES.shape[0]):
            datetime = DATETIMES.loc[num]
            try:
                reserve(driver, datetime)
                print(f'{user.fullname}さんで{datetime.year}年{datetime.month}月{datetime.day}日の予約に成功しました。次の枠に進みます。')
            except:
                print(f'{user.fullname}さんで{datetime.year}年{datetime.month}月{datetime.day}日の予約に失敗しました。次の枠に進みます。')
                continue
            wait_func()
        try:
            logout(driver, user)
            print(f'{user.fullname}さんでログアウトしました。次の人に進みます。')
        except:
            print(f'{user.fullname}さんでログアウトに失敗しました。次の人に進みます。')
            driver = set_driver(URL)
            continue
        wait_func()


def set_driver(url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.switch_to.frame('MainFrame')
    driver.implicitly_wait(WAIT_LONG_TIME)
    return driver


def login(driver, user):
    driver.find_element_by_xpath("//input[@value='マイメニュー']").click()
    driver.find_element_by_name('txt_usr_cd').send_keys(user.user_id)
    driver.find_element_by_name('txt_pass').send_keys(user.password)
    driver.find_element_by_name('btn_ok').click()
    driver.find_element_by_name('btn_MoveMenu').click()
    return

def reserve(driver, datetime):
    # クリック
    driver.find_element_by_partial_link_text('施設、時間帯を').click()
    wait_func()

    # 施設選択
    Select(driver.find_element_by_name('lst_kaikan')).select_by_visible_text(FACILITY)
    wait_func()

    # 日時選択
    disp_date = driver.find_element_by_class_name('clsCalTitleYM').text
    # 年
    year_text = f'{datetime.year}年'
    if year_text not in disp_date:
        driver.find_element_by_link_text(year_text).click()
        wait_func()
    # 月
    month_text = f'{datetime.month}月'
    if month_text not in disp_date:
        driver.find_element_by_link_text(month_text).click()
        wait_func()
    # 日
    driver.find_element_by_link_text(str(datetime.day)).click()
    wait_func()
    # よくわからんけど一応
    alert_flg = False
    try:
        driver.find_element_by_xpath("//img[@alt=\"抽選予約\"]").is_displayed()
    except:
        alert_flg = True
    # 時間帯
    target = driver.find_element_by_name(f'ahref00000{datetime.time_code}000')
    target_text = target.find_element_by_tag_name('img').get_attribute('alt')
    if target_text != '抽選予約可能' and target_text != '抽選予約画面へ移動':
        raise Exception('抽選できません')
    target.click()
    # アラート対応
    if alert_flg:
        Alert(driver).accept()
        driver.find_element_by_name(f'ahref00000{datetime.time_code}000').click()
    wait_func()

    # コート全面を選択する処理
    win = driver.window_handles
    wait_func()
    driver.switch_to.window(win[1])
    wait_func()
    Select(driver.find_element_by_name('men_1_1')).select_by_visible_text('1')
    wait_func()
    driver.find_elements_by_name('btn_modoru')[0].click()
    wait_func()
    driver.switch_to.window(win[0])
    driver.switch_to.frame(driver.find_elements_by_xpath("//frame")[0])
    wait_func()
    driver.find_element_by_name('btn_ok').click()
    wait_func()
    driver.find_element_by_name('btn_next').click()
    wait_func()
    driver.find_element_by_name('btn_next').click()
    wait_func()
    driver.find_element_by_name('btn_cmd').click()
    wait_func()
    Alert(driver).accept()
    wait_func()
    return


def logout(driver, user):
    driver.find_element_by_name('btn_LogOut').click()
    return

def wait_func(time=WAIT_TIME):
    print('待機中...\r', end='')
    sleep(time)
    return

if __name__ == '__main__':
    main()
