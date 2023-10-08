from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import pytest


# Absolute path for the browser driver.
# e.g. for Linux and Firefox: "/home/<user>/Download/geckodriver-v0.33.0-linux32/geckodriver"
os.environ["PATH"] = "/home/nubian/Download/geckodriver-v0.33.0-linux32/geckodriver"


# True user data You didn't create for testing purposes.
valid_username = "User2"
valid_email_input = "user2@email.com"
valid_password_input = 12345

# Fake data You didn't create for testing purposes.
invalid_username = "bloblabli"
invalid_email_input = "blabla@email.com"
invalid_password_input = 123456789


@pytest.fixture
def driver():
    """
    `@pytest.fixture` is implemented to initialize and close the browser before and after each test.

    The `driver()` function is passed as an argument to each test as a "fixture",
    which means that it will be usable inside the test functions without having to initialize it each time.
    """
    driver = webdriver.Firefox()
    # driver.maximize_window()
    driver.get("http://127.0.0.1:5000/")
    yield driver
    driver.quit()


def test_passwords_that_are_not_identical(driver):
    driver.get("http://127.0.0.1:5000/signup")

    username = driver.find_element(by=By.NAME, value="username")
    email_input = driver.find_element(by=By.NAME, value="email")
    password_input = driver.find_element(by=By.NAME, value="password")
    confirm_password_input = driver.find_element(by=By.NAME, value="confirm_password")
    submit_button = driver.find_element(by=By.NAME, value="submit")

    username.send_keys(valid_username)
    email_input.send_keys(valid_email_input)
    password_input.send_keys(valid_password_input)
    confirm_password_input.send_keys(invalid_password_input)
    submit_button.click()

    message = driver.find_element(by=By.CLASS_NAME, value="errors")
    expected_message_text = "Field must be equal to Password."

    assert message.text == expected_message_text
    assert driver.current_url == "http://127.0.0.1:5000/signup"


def test_adding_a_new_user_to_database(driver):
    driver.get("http://127.0.0.1:5000/signup")

    username = driver.find_element(by=By.NAME, value="username")
    email_input = driver.find_element(by=By.NAME, value="email")
    password_input = driver.find_element(by=By.NAME, value="password")
    confirm_password_input = driver.find_element(by=By.NAME, value="confirm_password")
    submit_button = driver.find_element(by=By.NAME, value="submit")

    username.send_keys(valid_username)
    email_input.send_keys(valid_email_input)
    password_input.send_keys(valid_password_input)
    confirm_password_input.send_keys(valid_password_input)
    submit_button.click()

    message = driver.find_element(by=By.CLASS_NAME, value="success")
    expected_message_text = "×\nThe account has been created. You can log in now."

    assert message.text == expected_message_text
    assert driver.current_url == "http://127.0.0.1:5000/login"


def test_username_that_is_already_in_the_db(driver):
    driver.get("http://127.0.0.1:5000/signup")

    username = driver.find_element(by=By.NAME, value="username")
    email_input = driver.find_element(by=By.NAME, value="email")
    password_input = driver.find_element(by=By.NAME, value="password")
    confirm_password_input = driver.find_element(by=By.NAME, value="confirm_password")
    submit_button = driver.find_element(by=By.NAME, value="submit")

    username.send_keys(valid_username)
    email_input.send_keys(invalid_email_input)
    password_input.send_keys(invalid_password_input)
    confirm_password_input.send_keys(invalid_password_input)
    submit_button.click()

    message = driver.find_element(by=By.CLASS_NAME, value="errors")
    expected_message_text = "That username is already taken."

    assert message.text == expected_message_text
    assert driver.current_url == "http://127.0.0.1:5000/signup"


def test_email_that_is_already_in_the_db(driver):
    driver.get("http://127.0.0.1:5000/signup")

    username = driver.find_element(by=By.NAME, value="username")
    email_input = driver.find_element(by=By.NAME, value="email")
    password_input = driver.find_element(by=By.NAME, value="password")
    confirm_password_input = driver.find_element(by=By.NAME, value="confirm_password")
    submit_button = driver.find_element(by=By.NAME, value="submit")

    username.send_keys(invalid_username)
    email_input.send_keys(valid_email_input)
    password_input.send_keys(invalid_password_input)
    confirm_password_input.send_keys(invalid_password_input)
    submit_button.click()

    message = driver.find_element(by=By.CLASS_NAME, value="errors")
    expected_message_text = "That email is already taken."

    assert message.text == expected_message_text
    assert driver.current_url == "http://127.0.0.1:5000/signup"


def test_shortcut_login_link(driver):
    driver.get("http://127.0.0.1:5000/signup")

    logout = driver.find_element(by=By.LINK_TEXT, value="Login")
    logout.click()

    assert driver.current_url == "http://127.0.0.1:5000/login"
