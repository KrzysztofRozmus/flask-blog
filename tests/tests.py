from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import pytest


# Absolute path for the browser driver.
# e.g. for Linux and Firefox: "/home/<user>/Download/geckodriver-v0.33.0-linux32/geckodriver"
os.environ["PATH"] = ""

# True data You created in db for testing purposes.
valid_admin_email = "admin@email.com"
valid_admin_password = "admin123"

# Fake data You didn't create for testing purposes.
invalid_email = "blabla@email.com"
invalid_password = 123456789


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


def test_home_page(driver):
    assert driver.title == "Flask Blog"
    assert driver.current_url == "http://127.0.0.1:5000/"


def test_login_page(driver):
    login_link = driver.find_element(by=By.CLASS_NAME, value="login-link")
    login_link.click()

    assert driver.current_url == "http://127.0.0.1:5000/login"


def test_email_that_is_not_in_the_database(driver):
    driver.get("http://127.0.0.1:5000/login")
    email = driver.find_element(by=By.NAME, value="email")
    password = driver.find_element(by=By.NAME, value="password")
    submit_button = driver.find_element(by=By.NAME, value="submit")
    email.send_keys(invalid_email)
    password.send_keys(invalid_password)
    submit_button.click()
    error_message = driver.find_element(by=By.CLASS_NAME, value="errors")
    expected_error_text = "Invalid email."

    assert error_message.text == expected_error_text


def test_password_that_is_not_in_the_database(driver):
    driver.get("http://127.0.0.1:5000/login")
    email = driver.find_element(by=By.NAME, value="email")
    password = driver.find_element(by=By.NAME, value="password")
    submit_button = driver.find_element(by=By.NAME, value="submit")
    email.send_keys(valid_admin_email)
    password.send_keys(123456789)
    submit_button.click()
    error_message = driver.find_element(by=By.CLASS_NAME, value="errors")
    expected_error_text = "Invalid password."

    assert error_message.text == expected_error_text


def test_proper_admin_email_and_password_that_are_in_the_database(driver):
    driver.get("http://127.0.0.1:5000/login")
    email = driver.find_element(by=By.NAME, value="email")
    password = driver.find_element(by=By.NAME, value="password")
    submit_button = driver.find_element(by=By.NAME, value="submit")
    email.send_keys(valid_admin_email)
    password.send_keys(valid_admin_password)
    submit_button.click()

    assert driver.current_url == "http://127.0.0.1:5000/admin/"
    logout = driver.find_element(by=By.LINK_TEXT, value="Logout")
    logout.click()


def test_logout_from_admin_account(driver):
    # Log in first.
    driver.get("http://127.0.0.1:5000/login")
    email = driver.find_element(by=By.NAME, value="email")
    password = driver.find_element(by=By.NAME, value="password")
    submit_button = driver.find_element(by=By.NAME, value="submit")
    email.send_keys(valid_admin_email)
    password.send_keys(valid_admin_password)
    submit_button.click()

    # Then test logout
    logout = driver.find_element(by=By.LINK_TEXT, value="Logout")
    logout.click()
    message = driver.find_element(by=By.CLASS_NAME, value="info")
    expected_message_text = "×\nYou have been log out."

    assert message.text == expected_message_text
    assert driver.current_url == "http://127.0.0.1:5000/login"
