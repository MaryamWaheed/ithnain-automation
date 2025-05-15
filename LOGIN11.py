import time
import random
import logging
from appium import webdriver
from appium.options.common import AppiumOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# Set up Appium driver
def set_up_appium():
    options = AppiumOptions()
    options.set_capability('platformName', 'android')
    options.set_capability('platformVersion', '11')
    options.set_capability('deviceName', 'RZ8M61HGKEK')
    options.set_capability('automationName', 'UiAutomator2')
    options.set_capability('appPackage', 'com.ithnain.ithnainapp')
    options.set_capability('appActivity', 'com.ithnain.ithnainapp.MainActivity')
    options.set_capability('uiautomator2ServerLaunchTimeout', 60000)
    return webdriver.Remote("http://127.0.0.1:4723", options=options)


# Wait for element and click
def wait_and_click(driver, locator, timeout=50):
    try:
        element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
        element.click()
        logging.info(f"Clicked on element: {locator}")
    except Exception as e:
        logging.error(f"Failed to click on element: {locator}, Error: {e}")
        raise


# Wait for element and send keys
def wait_and_send_keys(driver, locator, text, timeout=20):
    try:
        element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
        element.send_keys(text)
        driver.hide_keyboard()
        logging.info(f"Sent keys to element: {locator}")
    except Exception as e:
        logging.error(f"Failed to send keys to element: {locator}, Error: {e}")
        raise


# Set specific value in NumberPicker via keyboard
def set_date_picker_value(driver, xpath, value):
    field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    field.clear()
    field.send_keys(value)
    logging.info(f"Set value {value} for {xpath}")
    time.sleep(0.5)


def select_full_date(driver):
    try:
        # Wait until picker is ready
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//android.widget.NumberPicker[1]//android.widget.EditText'))
        )

        # Generate values
        desired_day = str(random.randint(1, 28))
        desired_year = str(random.randint(1990, 2023))

        # Set Day
        day_field = driver.find_element(By.XPATH, '//android.widget.NumberPicker[1]//android.widget.EditText')
        day_field.clear()
        day_field.send_keys(desired_day)
        time.sleep(0.5)

        # Set Year
        year_field = driver.find_element(By.XPATH, '//android.widget.NumberPicker[3]//android.widget.EditText')
        year_field.clear()
        year_field.send_keys(desired_year)
        time.sleep(0.5)

        # Tap the month picker to force UI refresh (we're not changing it)
        month_picker = driver.find_element(By.XPATH, '//android.widget.NumberPicker[2]')
        driver.tap([(month_picker.location['x'] + 10, month_picker.location['y'] + 10)])

        time.sleep(0.5)

        # Confirm selection
        ok_button = (By.ID, "android:id/button1")
        wait_and_click(driver, ok_button)
        logging.info(f"Selected Day={desired_day}, Year={desired_year}")

    except Exception as e:
        logging.error(f"Date selection failed: {e}")
        raise



def wait_until_dialog_closes(driver, timeout=5):
    try:
        WebDriverWait(driver, timeout).until_not(
            EC.presence_of_element_located((By.ID, "android:id/button1"))
        )
    except:
        pass




# Main script logic
def main():
    driver = set_up_appium()
    driver.implicitly_wait(50)

    try:
        # Locators
        LANG_BUTTON = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("English")')
        LOGIN_BUTTON = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Login")')
        TEXT_FIELD = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("🇸🇦")')
        COUNTRY_FIELD = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("text-input-country-filter")')
        PAK_FIELD = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Pakistan (+92)")')
        PHONE_FIELD = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Phone number")')
        LOGIN1_BUTTON = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Login")')
        VERIFICATION_CODE_FIELD = lambda fn: (By.ANDROID_UIAUTOMATOR, f'new UiSelector().resourceId("textInput").instance({fn})')
        AGREE_BUTTON = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Agree")')
        NEXT_BUTTON = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.PathView").instance(1)')
        NEXT2_BUTTON = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.PathView").instance(2)')
        EDIT_BUTTON = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Edit")')
        EDIT1_BUTTON = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Edit")')
        CHECKBOX = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("RNE__ICON__Component").instance(0)')
        CHECKBOX1 = lambda fn: (By.ANDROID_UIAUTOMATOR, f'new UiSelector().resourceId("RNE__Checkbox__Icon").instance({fn})')
        GOAL_SELECT = lambda text, fn: (By.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}").instance({fn})')
        SUBMIT_BUTTON = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Submit")')
        NOT_NOW = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Not Now")')

        # Begin flow
        wait_and_click(driver, LANG_BUTTON)
        wait_and_click(driver, LOGIN_BUTTON)
        wait_and_click(driver, TEXT_FIELD)
        wait_and_send_keys(driver, COUNTRY_FIELD, 'Pakistan')
        wait_and_click(driver , PAK_FIELD)
        wait_and_send_keys(driver, PHONE_FIELD, '3314104028')
        wait_and_click(driver, LOGIN1_BUTTON)

        for idx, digit in enumerate('1234'):
            wait_and_send_keys(driver, VERIFICATION_CODE_FIELD(idx), digit)

        wait_and_click(driver, AGREE_BUTTON)
        wait_and_click(driver, NEXT_BUTTON)
        wait_and_click(driver, NEXT2_BUTTON)
        wait_and_click(driver, NEXT2_BUTTON)
        wait_and_click(driver, EDIT_BUTTON)

        # Date selection (first)
        select_full_date(driver)
        wait_until_dialog_closes(driver)
        wait_and_click(driver, NEXT2_BUTTON)

        wait_and_click(driver, EDIT1_BUTTON)

        # Date selection (second)
        select_full_date(driver)
        wait_until_dialog_closes(driver)
        wait_and_click(driver, NEXT2_BUTTON)

        wait_and_click(driver, CHECKBOX)

        for idx in range(3):
            wait_and_click(driver, CHECKBOX1(idx))

        wait_and_click(driver, NEXT2_BUTTON)

        # Select goals
        goals = [("Carb Counting", 0), ("Reduce Diabetes", 0)]
        for goal_text, instance_idx in goals:
            wait_and_click(driver, GOAL_SELECT(goal_text, instance_idx))

        wait_and_click(driver, SUBMIT_BUTTON)
        wait_and_click(driver, NOT_NOW)

        # Final date picker again
        select_full_date(driver)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
