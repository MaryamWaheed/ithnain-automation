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
        logging.info(f"Sent keys to element: {locator}")
    except Exception as e:
        logging.error(f"Failed to send keys to element: {locator}, Error: {e}")
        raise

# Swipe element for scrolling
def swipe_element(driver, element, direction="up", duration=800):
    loc = element.location
    size = element.size
    start_x = loc['x'] + size['width'] // 2
    start_y = loc['y'] + (3 * size['height']) // 4
    end_y = loc['y'] + size['height'] // 4

    if direction == "up":
        driver.swipe(start_x, start_y, start_x, end_y, duration)
    elif direction == "down":
        driver.swipe(start_x, end_y, start_x, start_y, duration)

# Select Date, Month, and Year in Date Picker
def select_full_date(driver):
    try:
        # Open date picker
        date_field = (By.XPATH, '//android.widget.NumberPicker[1]//android.widget.EditText')
        wait_and_click(driver, date_field)
        time.sleep(2)

        # Generate random date
        desired_day = str(random.randint(1, 28))
        desired_month = random.choice(["January", "February", "March", "April", "May", "June",
                                       "July", "August", "September", "October", "November", "December"])
        desired_year = str(random.randint(1990, 2023))

        # Select day
        day_locator = (By.XPATH, f'//android.view.View[@text="{desired_day}"]')
        wait_and_click(driver, day_locator)
        print(f"Day selected: {desired_day}")
        time.sleep(1)

        # Select month
        month_dropdown = (By.XPATH, '//android.widget.NumberPicker[2]//android.widget.EditText')
        wait_and_click(driver, month_dropdown)
        time.sleep(1)
        month_option = (By.XPATH, f'//android.widget.TextView[@text="{desired_month}"]')
        wait_and_click(driver, month_option)
        print(f"Month selected: {desired_month}")
        time.sleep(1)

        # Select year
        year_button = (By.XPATH, '//android.widget.NumberPicker[3]//android.widget.EditText')
        wait_and_click(driver, year_button)
        time.sleep(1)

        for _ in range(5):
            try:
                year_option = driver.find_element(By.XPATH, f'//android.widget.TextView[@text="{desired_year}"]')
                year_option.click()
                print(f"Year selected: {desired_year}")
                break
            except:
                year_list = driver.find_element(By.CLASS_NAME, "android.widget.ScrollView")
                swipe_element(driver, year_list, direction="up")

        time.sleep(1)

        # Confirm selection
        ok_button = (By.ID, "android:id/button1")
        wait_and_click(driver, ok_button)
        print("Date selection confirmed.")

    except Exception as e:
        logging.error(f"Date selection failed: {e}")
        raise

# Retrieve OTP from WhatsApp and return it
def retrieve_otp_from_whatsapp(driver):
    try:
        driver.activate_app("com.whatsapp")
        time.sleep(15)
        chat_locator = (By.XPATH, '//android.widget.TextView[@text="Ithnainofficial"]')
        chat_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(chat_locator))
        chat_element.click()
        time.sleep(10)

        otp_message_locator = (By.XPATH, '//android.widget.TextView[contains(@text, "is your verification code")]')
        otp_message_elements = driver.find_elements(*otp_message_locator)

        if not otp_message_elements:
            raise Exception("No OTP messages found in the chat")

        latest_otp_message_element = otp_message_elements[-1]
        otp_text = latest_otp_message_element.get_attribute('text')
        otp = ''.join(filter(str.isdigit, otp_text))

        if not otp:
            raise Exception("No OTP found in the message text")

        print(f"Retrieved OTP: {otp}")
        driver.set_clipboard_text(otp)
        driver.activate_app("com.ithnain.ithnainapp")
        return otp

    except Exception as e:
        logging.error(f"Failed to retrieve OTP, Error: {e}")
        raise

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

        # Click on Language Button
        wait_and_click(driver, LANG_BUTTON)

        # Click on Login Button
        wait_and_click(driver, LOGIN_BUTTON)

        # Click on Text Field
        wait_and_click(driver, TEXT_FIELD)

        # Send keys to Country Field and select Pakistan
        wait_and_send_keys(driver, COUNTRY_FIELD, 'Pakistan')
        wait_and_click(driver, PAK_FIELD)

        # Send keys to Phone Number Field
        wait_and_send_keys(driver, PHONE_FIELD, '3091431565')

        # Click on Login Button
        wait_and_click(driver, LOGIN1_BUTTON)

        # Retrieve and enter the verification code from WhatsApp
        retrieve_otp_from_whatsapp(driver)

        # Click on Agree Button
        wait_and_click(driver, AGREE_BUTTON)

        # Click on Medical Referral
        # wait_and_click(driver, OTHER_PATIENTS)

        # Click on Next Button
        wait_and_click(driver, NEXT_BUTTON)

        # Select "I am the patient" option
        # wait_and_click(driver, I_AM_PATIENT)

        # Send keys to Patient Name
        # wait_and_send_keys(driver, PATIENT_NAME, 'AHMAD')

        # Select Male Gender
        # wait_and_click(driver, MALE_GENDER)

        # Click on Next Button again
        wait_and_click(driver, NEXT2_BUTTON)

        # Select Type 1 Diabetes
        # wait_and_click(driver, DIABETES_TYPE1)

        # Click on Next Button again
        wait_and_click(driver, NEXT2_BUTTON)

        # Click on Edit Button
        wait_and_click(driver, EDIT_BUTTON)

        # Select the date again
        select_full_date(driver)

        # Click on Next Button again
        wait_and_click(driver, NEXT2_BUTTON)

        # Click on Edit Button
        wait_and_click(driver, EDIT1_BUTTON)

        # Select the date again
        select_full_date(driver)

        # Click on Next Button again
        wait_and_click(driver, NEXT2_BUTTON)

        # Click on Next Button again
        wait_and_click(driver, CHECKBOX)

        # Check checkboxes
        for idx in range(3):
            wait_and_click(driver, CHECKBOX1(idx))

        # Click on Next Button
        wait_and_click(driver, NEXT2_BUTTON)

        # Select Goal
        goals = [("Carb Counting", 0), ("Reduce Diabetes", 0)]
        for goal_text, instance_idx in goals:
            wait_and_click(driver, GOAL_SELECT(goal_text, instance_idx))

        # Click on submit button
        wait_and_click(driver, SUBMIT_BUTTON)

        # Click on Not Now button
        wait_and_click(driver, NOT_NOW)

        # Add final date selection step
        select_full_date(driver)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()


