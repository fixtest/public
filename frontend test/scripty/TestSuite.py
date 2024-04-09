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

class TestTestSuite():
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
  
  def test_tC3Prihlaseniepositivnynegativny(self):
    self.tC1Login()
    self.tC2Logout()
    value = self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"login-button\"]").get_attribute("value")
    assert value == "Login"
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"username\"]").click()
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"username\"]").send_keys("locked_out_user")
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"password\"]").click()
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"password\"]").send_keys("secret_sauce")
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"login-button\"]").click()
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"error\"]").text == "Epic sadface: Sorry, this user has been locked out."
    self.driver.close()
  
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
  
  def test_tC6Odoslanieobjednavky(self):
    self.tC1Login()
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"inventory-item-name\"]").text == "Sauce Labs Backpack"
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
    self.driver.find_element(By.CSS_SELECTOR, "#item_0_title_link > .inventory_item_name").click()
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"inventory-item-name\"]").text == "Sauce Labs Bike Light"
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"add-to-cart\"]").click()
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"shopping-cart-link\"]").click()
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"item-quantity\"]").text == "1"
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"inventory-item-name\"]").text == "Sauce Labs Backpack"
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"inventory-item-price\"]").click()
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"inventory-item-price\"]").text == "$29.99"
    assert self.driver.find_element(By.CSS_SELECTOR, ".cart_item:nth-child(4) > .cart_quantity").text == "1"
    assert self.driver.find_element(By.CSS_SELECTOR, "#item_0_title_link > .inventory_item_name").text == "Sauce Labs Bike Light"
    assert self.driver.find_element(By.CSS_SELECTOR, ".cart_item:nth-child(4) .inventory_item_price").text == "$9.99"
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"checkout\"]").click()
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"firstName\"]").click()
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"firstName\"]").send_keys("tester")
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"lastName\"]").click()
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"lastName\"]").send_keys("testerovic")
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"postalCode\"]").click()
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"postalCode\"]").send_keys("90501")
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"title\"]").text == "Checkout: Your Information"
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"continue\"]").click()
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"title\"]").text == "Checkout: Overview"
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"item-quantity\"]").text == "1"
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"inventory-item-name\"]").text == "Sauce Labs Backpack"
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"inventory-item-price\"]").text == "$29.99"
    assert self.driver.find_element(By.CSS_SELECTOR, ".cart_item:nth-child(4) > .cart_quantity").text == "1"
    assert self.driver.find_element(By.CSS_SELECTOR, "#item_0_title_link > .inventory_item_name").text == "Sauce Labs Bike Light"
    assert self.driver.find_element(By.CSS_SELECTOR, ".cart_item:nth-child(4) .inventory_item_price").text == "$9.99"
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"payment-info-label\"]").text == "Payment Information:"
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"payment-info-value\"]").text == "SauceCard #31337"
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"shipping-info-label\"]").text == "Shipping Information:"
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"shipping-info-value\"]").text == "Free Pony Express Delivery!"
    self.driver.find_element(By.CSS_SELECTOR, ".cart_footer").click()
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"total-info-label\"]").text == "Price Total"
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"subtotal-label\"]").text == "Item total: $39.98"
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"tax-label\"]").text == "Tax: $3.20"
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"total-label\"]").text == "Total: $43.18"
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"finish\"]").click()
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"complete-header\"]").text == "Thank you for your order!"
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"complete-text\"]").text == "Your order has been dispatched, and will arrive just as fast as the pony can get there!"
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"title\"]").text == "Checkout: Complete!"
    self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"back-to-products\"]").click()
    assert self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"title\"]").text == "Products"
    self.tC2Logout()
    self.driver.close()
  
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
  
