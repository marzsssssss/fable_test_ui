import logging
from playwright.sync_api import sync_playwright

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Тест формы авторизации
def login(page, username, password):
    # Функция для авторизации
    logger.info("Попытка авторизации...")
    try:
        page.get_by_placeholder("Логин").click()
        page.get_by_placeholder("Логин").fill(username)
        page.get_by_placeholder("Пароль").click()
        page.get_by_placeholder("Пароль").fill(password)
        page.get_by_placeholder("Пароль").press("Enter")
        page.wait_for_load_state('networkidle')

        # Проверка URL после авторизации
        if page.url != "https://stage.vedcrm.com/":
            raise ValueError("Неправильные креды авторизации")

        logger.info("Авторизация прошла успешно.")
    except Exception as e:
        logger.error(f"Ошибка авторизации: {e}")
        raise


def main():
    # Основная логика программы - авторизация
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # False - Запуск браузера
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        try:
            logger.info("Переход на страницу авторизации...")
            page.goto("https://stage.vedcrm.com/auth")

            # Шаг 1: Авторизация
            login(page, "testperson@testperson.com", "Password123")

        except Exception as e:
            logger.error(f"Произошла ошибка во время выполнения: {e}")
        finally:
            # Закрытие браузера
            browser.close()
            logger.info("Браузер закрыт.")


if __name__ == '__main__':
    main()
