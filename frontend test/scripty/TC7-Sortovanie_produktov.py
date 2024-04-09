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

class TestTC7Sortovanieproduktov():
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
  
  def test_tC7Sortovanieproduktov(self):
    self.tC1Login()
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"inventory-item-name\"]").text == "Sauce Labs Backpack"
    element = self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"product-sort-container\"]")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"product-sort-container\"]").click()
    self.driver.find_element(By.CSS_SELECTOR, "option:nth-child(2)").click()
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"inventory-item-name\"]").text == "Test.allTheThings() T-Shirt (Red)"
    element = self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"product-sort-container\"]")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"product-sort-container\"]").click()
    self.driver.find_element(By.CSS_SELECTOR, "option:nth-child(1)").click()
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"inventory-item-name\"]").text == "Sauce Labs Backpack"
    element = self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"product-sort-container\"]")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"product-sort-container\"]").click()
    self.driver.find_element(By.CSS_SELECTOR, "option:nth-child(3)").click()
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"inventory-item-name\"]").text == "Sauce Labs Onesie"
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"inventory-item-price\"]").text == "$7.99"
    element = self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"product-sort-container\"]")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"product-sort-container\"]").click()
    self.driver.find_element(By.CSS_SELECTOR, "option:nth-child(4)").click()
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"inventory-item-name\"]").text == "Sauce Labs Fleece Jacket"
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"inventory-item-price\"]").text == "$49.99"
    self.tC2Logout()
    self.driver.close()
  
