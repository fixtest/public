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

class TestTC5Kosikpridajodoberprodukt():
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
  
  def test_tC5Kosikpridajodoberprodukt(self):
    self.tC1Login()
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"inventory-item-name\"]").text == "Sauce Labs Backpack"
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"add-to-cart-sauce-labs-bike-light\"]").click()
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"shopping-cart-link\"]").click()
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"title\"]").text == "Your Cart"
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"inventory-item-name\"]").text == "Sauce Labs Backpack"
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"inventory-item-price\"]").text == "$29.99"
    assert self.driver.find_element(By.CSS_SELECTOR, "#item_0_title_link > .inventory_item_name").text == "Sauce Labs Bike Light"
    assert self.driver.find_element(By.CSS_SELECTOR, ".cart_item:nth-child(4) .inventory_item_price").text == "$9.99"
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"remove-sauce-labs-bike-light\"]").click()
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"item-quantity\"]").text == "1"
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"remove-sauce-labs-backpack\"]").click()
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"continue-shopping\"]").click()
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"shopping-cart-link\"]").click()
    assert self.driver.find_element(By.CSS_SELECTOR, ".cart_footer").text == "Continue Shopping\nCheckout"
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"continue-shopping\"]").click()
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"shopping-cart-link\"]").click()
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"item-quantity\"]").text == "1"
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"inventory-item-name\"]").text == "Sauce Labs Backpack"
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"inventory-item-price\"]").text == "$29.99"
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"continue-shopping\"]").click()
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"remove-sauce-labs-backpack\"]").click()
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"shopping-cart-link\"]").click()
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"checkout\"]").click()
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"cancel\"]").click()
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"continue-shopping\"]").click()
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"inventory-item-name\"]").text == "Sauce Labs Backpack"
    self.tC2Logout()
  
