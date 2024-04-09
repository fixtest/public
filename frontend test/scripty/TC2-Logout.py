import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestTC2Logout():
  def setup_method(self, method):
    self.driver = webdriver.Firefox()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_tC2Logout(self):
    time.sleep(1)
    self.driver.find_element(By.ID, "react-burger-menu-btn").click()
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"logout-sidebar-link\"]").text == "Logout"
    time.sleep(1)
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"logout-sidebar-link\"]").click()
    value = self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"login-button\"]").get_attribute("value")
    assert value == "Login"
  
