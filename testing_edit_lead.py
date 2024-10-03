import logging
from playwright.sync_api import sync_playwright

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


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


def click_edit_button(page):
    # Функция для клика по кнопке редактирования лида
    try:
        logger.info("Ожидание и клик по кнопке редактирования лида...")
        page.wait_for_selector("//button[span[contains(@class, '_editIcon_148ef_68')]]", timeout=5000)
        page.click("//button[span[contains(@class, '_editIcon_148ef_68')]]")
    except Exception as e:
        logger.error(f"Ошибка при клике по кнопке редактирования: {e}")
        raise


def fill_lead_form(page):
    # Функция для заполнения формы редактирования лида
    try:
        logger.info("Заполнение формы редактирования лида...")
        page.get_by_label("Организация").click()
        page.get_by_label("Организация").fill("1" * 500)
        page.get_by_label("ИНН").click()
        page.get_by_label("ИНН").fill("7707083893")
        page.get_by_label("ФИО").click()
        page.get_by_label("ФИО").fill("1" * 100)
        page.get_by_label("Телефон").click()
        page.get_by_label("Телефон").fill("+1234567891234")
        page.get_by_label("Эл. почта").click()
        page.get_by_label("Эл. почта").fill("1" * 91 + "@test.com")
        page.get_by_label("Телеграм").click()
        page.get_by_label("Телеграм").fill("@" + "1" * 24)
    except Exception as e:
        logger.error(f"Ошибка при заполнении формы: {e}")
        raise


def submit_form(page):
    # Функция для сохранения формы и проверки ошибок
    try:
        logger.info("Сохранение формы лида...")
        page.get_by_role("button", name="Сохранить").click()

        # Ожидание нотификации ошибки
        notification = page.locator("div._notification_1gske_13._error_1gske_31")
        notification.wait_for(state='visible', timeout=3000)
        if notification.is_visible():
            logger.error("Появилась нотификация: Проблемы с API (/companies/leads/{lead_id})")
            raise RuntimeError("Ошибка при обновлении лида через API")

        # Ожидание перехода на страницу
        page.wait_for_url("https://stage.vedcrm.com", timeout=5000)
        logger.info("Лид успешно сохранен.")
    except Exception as e:
        logger.error(f"Ошибка при сохранении формы: {e}")
        raise


def main():
    # Основная логика программы: авторизация и редактирование лида
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # False - Запуск браузера
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        try:
            logger.info("Переход на страницу авторизации...")
            page.goto("https://stage.vedcrm.com/auth")

            # Шаг 1: Авторизация
            login(page, "testperson@testperson.com", "Password123")

            # Шаг 2: Клик по кнопке редактирования
            click_edit_button(page)

            # Шаг 3: Заполнение формы
            fill_lead_form(page)

            # Шаг 4: Сохранение формы
            submit_form(page)

        except Exception as e:
            logger.error(f"Произошла ошибка во время выполнения: {e}")
        finally:
            # Закрытие браузера
            browser.close()
            logger.info("Браузер закрыт.")


if __name__ == '__main__':
    main()
