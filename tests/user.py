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



