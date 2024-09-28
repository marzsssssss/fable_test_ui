import pytest
from playwright.sync_api import sync_playwright

# Тест формы авторизации
def test_authorization_form():
    with sync_playwright() as p:
        # Запуск браузера Chromium
        browser = p.chromium.launch(headless=False)  # headless=False для визуализации теста
        context = browser.new_context(viewport= {"width": 1920, "height": 1080})
        page = context.new_page()
        page.goto("https://stage.vedcrm.com/")
        page.goto("https://stage.vedcrm.com/auth")
        page.get_by_placeholder("Логин").click()
        page.get_by_placeholder("Логин").fill("testperson@testperson.com")
        page.get_by_placeholder("Пароль").click()
        page.get_by_placeholder("Пароль").fill("Password123")
        page.get_by_placeholder("Пароль").press("Enter")
        page.locator("._titleButtons_16spm_34 > button").first.click()
        page.get_by_label("Организация").click()
        page.get_by_label("Организация").fill("ООО Макаров11")
        page.get_by_label("Тип компании").select_option("export")
        page.get_by_label("ИНН").click()
        page.get_by_label("ИНН").fill("92284893531")
        page.get_by_label("Партнёр компании").select_option("d4bd7d95-8ef1-47a1-a43d-155e31836497")
        page.get_by_label("Тариф").select_option("8cd8f5bb-ab4c-4648-be51-9d4335a5a003")
        page.get_by_role("button", name="Сохранить").click()

        
        # Закрытие браузера
        browser.close()

# Если хотите запускать тесты с Pytest
if __name__ == "__main__":
    pytest.main(["-v", "--tb=line"])
