import pytest
from playwright.sync_api import sync_playwright


# Тест формы авторизации
def test_authorization_form():
    with sync_playwright() as p:
        # Запуск браузера Chromium
        browser = p.chromium.launch(headless=False)  # headless=False для визуализации теста
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        page.goto("https://stage.vedcrm.com/auth")
        page.get_by_placeholder("Логин").click()
        page.get_by_placeholder("Логин").fill("testperson@testperson.com")
        page.get_by_placeholder("Пароль").click()
        page.get_by_placeholder("Пароль").fill("Password123")
        page.get_by_placeholder("Пароль").press("Enter")
        # Проверка загрузки страницы
        page.wait_for_load_state('networkidle')
        assert page.url == "https://stage.vedcrm.com/", "URL не соответствует ожидаемому"
        # Закрытие браузера
        browser.close()