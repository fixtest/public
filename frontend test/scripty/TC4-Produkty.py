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

class TestTC4Produkty():
  def setup_method(self, method):
    self.driver = webdriver.Firefox()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def tC1Login(self):
    self.vars["VAR_LOGIN"] = "standard_user"
    self.vars["VAR_PASSWORD"] = "secret_sauce"
    self.driver.get("https://www.saucedemo.com/")
    self.driver.set_window_size(1398, 747)
    value = self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"login-button\"]").get_attribute("value")
    assert value == "Login"
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"username\"]").click()
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"username\"]").send_keys(self.vars["VAR_LOGIN"])
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"password\"]").click()
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"password\"]").send_keys(self.vars["VAR_PASSWORD"])
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"login-button\"]").click()
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"title\"]").text == "Products"
  
  def tC2Logout(self):
    time.sleep(1)
    self.driver.find_element(By.ID, "react-burger-menu-btn").click()
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"logout-sidebar-link\"]").text == "Logout"
    time.sleep(1)
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"logout-sidebar-link\"]").click()
    value = self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"login-button\"]").get_attribute("value")
    assert value == "Login"
  
  def test_tC4Produkty(self):
    self.tC1Login()
    assert self.driver.find_element(By.XPATH, "//a[@id=\'item_4_title_link\']/div").text == "Sauce Labs Backpack"
    self.driver.find_element(By.XPATH, "//a[@id=\'item_4_title_link\']/div").click()
    assert self.driver.find_element(By.XPATH, "//div[@id=\'inventory_item_container\']/div/div/div[2]/div").text == "Sauce Labs Backpack"
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"inventory-item-price\"]").text == "$29.99"
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"inventory-item-desc\"]").text == "carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection."
    elements = self.driver.find_elements(By.CSS_SELECTOR, "*[data-test=\"item-sauce-labs-backpack-img\"]")
    assert len(elements) > 0
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"back-to-products\"]").click()
    assert self.driver.find_element(By.XPATH, "//a[@id=\'item_4_title_link\']/div").text == "Sauce Labs Backpack"
    self.tC2Logout()
    self.driver.close()
  
