import random
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from time import sleep
import pytest


@pytest.fixture()  # авторизация с логином standard_user
def standard_login():
    browser = webdriver.Chrome()
    browser.get('https://www.saucedemo.com/')
    log_input = browser.find_element(By.ID, 'user-name')  # нашли поле для ввода логина
    log_input.send_keys('standard_user')
    sleep(1)
    password_input = browser.find_element(By.ID, 'password')  # нашли поле для ввода логина
    password_input.send_keys('secret_sauce')
    sleep(1)
    click_Login = browser.find_element(By.ID, 'login-button')
    click_Login.click()
    return browser


@pytest.fixture()  # добавляем все товары в корзину
def add_all_items(standard_login):
    all_goods = standard_login.find_elements(By.CLASS_NAME, 'btn_primary')
    for a in range(0, len(all_goods)):
        if all_goods[a].is_displayed():
            all_goods[a].click()
            sleep(1)
    sleep(2)


@pytest.fixture()  # удаляем все товары из корзины
def delete_all_items(standard_login):
    remove_all = standard_login.find_elements(By.CLASS_NAME, 'cart_button')
    for r in range(0, len(remove_all)):
        if remove_all[r].is_displayed():
            remove_all[r].click()
            sleep(1)
    sleep(3)


def test_1_login():  # АВТОРИЗАЦИЯ
    browser = webdriver.Chrome()  # открыли хром
    browser.get('https://www.saucedemo.com/')
    log_input = browser.find_element(By.ID, 'user-name')  # нашли поле для ввода логина
    login = browser.find_element(By.CLASS_NAME, 'login_credentials')  # нашли блок с логинами по имени класса
    login = login.text.split()  # превратили строку с логинами в список
    i = random.randint(3, len(login) - 1)  # выбрали случайный индекс подходящего логина из списка
    log_input.send_keys(login[i])  # ввели логин
    print('\033[1m' + 'Авторизация с логином: ', login[i])
    sleep(1)

    password = browser.find_element(By.CLASS_NAME, 'login_password')  # нашли блок с паролем по имени класса
    password = password.text.split()[4]  # извлекли пароль secret_sauce
    password_input = browser.find_element(By.ID, 'password')  # нашли поле для ввода пароля
    password_input.send_keys(password)  # ввели пароль
    sleep(1)

    # нажатие на кнопку Login
    click_Login = browser.find_element(By.ID, 'login-button')
    click_Login.click()
    sleep(3)

    return browser


def test_2_cart(standard_login, add_all_items):  # РЕДАКТИРОВАНИЕ КОРЗИНЫ (standard_user)
    # фикстура - добавление всех товаров в корзину
    # далее перешли в корзину
    cart = standard_login.find_element(By.CLASS_NAME, 'shopping_cart_link')
    cart.click()
    # удаляем все товары из корзины
    remove_all = standard_login.find_elements(By.CLASS_NAME, 'cart_button')
    for r in range(0, len(remove_all)):
        if remove_all[r].is_displayed():
            remove_all[r].click()
            sleep(1)
    sleep(3)


def test_3_checkout_if_empty(standard_login,
                             delete_all_items):  # ОФОРМЛЕНИЕ ЗАКАЗА С КОРЗИНОЙ БЕЗ ТОВАРОВ (standard_user)
    # фикстура - удалили все товары из корзины
    # далее перешли в корзину
    cart = standard_login.find_element(By.CLASS_NAME, 'shopping_cart_link')
    cart.click()
    sleep(2)

    # нажали на Checkout
    checkout_button = standard_login.find_element(By.ID, 'checkout')
    checkout_button.click()
    # заполнили данные покупателя
    name_input = standard_login.find_element(By.ID, 'first-name')
    name_input.send_keys('Имя')
    sleep(1)
    last_name = standard_login.find_element(By.ID, 'last-name')
    last_name.send_keys('Фамилия')
    sleep(1)
    code = standard_login.find_element(By.ID, 'postal-code')
    code.send_keys('000555')
    sleep(1)

    continue_button = standard_login.find_element(By.ID, 'continue')  # нажали на Continue
    continue_button.click()
    sleep(3)

    finish_button = standard_login.find_element(By.ID, 'finish')  # нажали на Finish
    finish_button.click()
    sleep(2)

    home_button = standard_login.find_element(By.ID, 'back-to-products')  # нажали на Back Home
    home_button.click()
    sleep(3)


def test_4_checkout_with_items(standard_login, add_all_items):  # ОФОРМЛЕНИЕ ЗАКАЗА С НЕПУСТОЙ КОРЗИНОЙ (standard_user)
    # фикстура - добавили все товары в корзину
    # далее перешли в корзину
    cart = standard_login.find_element(By.CLASS_NAME, 'shopping_cart_link')
    cart.click()
    sleep(4)

    # нажали на Checkout
    checkout_button = standard_login.find_element(By.ID, 'checkout')
    checkout_button.click()
    # заполнили данные покупателя
    name_input = standard_login.find_element(By.ID, 'first-name')
    name_input.send_keys('Имя')
    sleep(1)
    last_name = standard_login.find_element(By.ID, 'last-name')
    last_name.send_keys('Фамилия')
    sleep(1)
    code = standard_login.find_element(By.ID, 'postal-code')
    code.send_keys('000555')
    sleep(1)

    continue_button = standard_login.find_element(By.ID, 'continue')  # нажали на Continue
    continue_button.click()
    sleep(4)

    finish_button = standard_login.find_element(By.ID, 'finish')  # нажали на Finish
    finish_button.click()
    sleep(4)

    home_button = standard_login.find_element(By.ID, 'back-to-products')  # нажали на Back Home
    home_button.click()
    sleep(4)


def test_5_high_to_low(standard_login):  # ПРОВЕРКА КОРРЕКТНОЙ РАБОТЫ ФИЛЬТРА ПОИСКА "PRICE(HIGH TO LOW)"
    sleep(2)
    filter_list = standard_login.find_element(By.CLASS_NAME,'product_sort_container')  # выбрали контейнер с фильтрами
    filter = Select(filter_list)
    filter.select_by_value('hilo')  # выбрали фильтр Price(high to low)
    sleep(5)

    prices = standard_login.find_elements(By.CLASS_NAME, 'inventory_item_price')  # цены всех товаров в виде списка
    for x in range(len(prices) - 1):  # сравниваем упорядоченный список с ценами
        assert float(prices[x].text[1:]) >= float(prices[x+1].text[1:])
    sleep(2)