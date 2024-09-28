import pytest
import time
from playwright.sync_api import sync_playwright


# Тест формы авторизации
def test_editing_leads():
    with sync_playwright() as p:
        # Запуск браузера Chromium
        browser = p.chromium.launch(headless=False)  # headless=False для визуализации теста
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        # Переход на страницу авторизации
        page.goto("https://stage.vedcrm.com/auth")

        # Ввод логина
        page.get_by_placeholder("Логин").click()
        page.get_by_placeholder("Логин").fill("testperson@testperson.com")

        # Ввод пароля
        page.get_by_placeholder("Пароль").click()
        page.get_by_placeholder("Пароль").fill("Password123")
        page.get_by_placeholder("Пароль").press("Enter")
        # Проверка загрузки страницы
        page.wait_for_load_state('networkidle')
        assert page.url == "https://stage.vedcrm.com/", "URL не соответствует ожидаемому"
        # Ожидание и клик по кнопке
        button_locator = page.locator("._titleButtons_16spm_34 > button").first
        button_locator.wait_for(state='visible')
        button_locator.click()
        # Заполнение формы
        page.get_by_label("Организация").click()
        page.get_by_label("Организация").fill(
            "11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")
        page.get_by_label("ИНН").click()
        page.get_by_label("ИНН").fill("7707083893")
        page.get_by_label("ФИО").click()
        page.get_by_label("ФИО").fill(
            "1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")
        page.get_by_label("Телефон").click()
        page.get_by_label("Телефон").fill("+1234567891234")
        page.get_by_label("Эл. почта").click()
        page.get_by_label("Эл. почта").fill(
            "1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111@test.com")
        page.get_by_label("Телеграм").click()
        page.get_by_label("Телеграм").fill("@aaaaaaaaaaaaaaaaaaaaaaaaa")
        partner_selector = page.locator("#partner._select_1iklr_46")
        partner_selector.wait_for(state='visible')
        # Клик по кнопке "Сохранить"
        page.get_by_role("button", name="Сохранить").click()
        time.sleep(2)
        # Закрытие браузера
        browser.close()


# Если хотите запускать тесты с Pytest
if __name__ == "__main__":
    pytest.main(["-v", "--tb=line"])
