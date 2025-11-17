import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://only.digital"

# Набор страниц, где проверяем футер
PAGES = [
    "/en",          # главная (англ. версия)
    "/en#projects", # секция projects
    "/en#clients",  # секция clients
]

FOOTER_NAV_ITEMS = ["Work", "About us", "What we do", "Career", "Blog", "Contacts"]


def get_footer(driver):
    """
    Вспомогательная функция: скроллим вниз и возвращаем элемент <footer>.
    """
    wait = WebDriverWait(driver, 15)

    # Убеждаемся, что страница прогрузилась
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Скроллим в самый низ, чтобы футер гарантированно был в DOM и виден
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Ждём появления футера
    footer = wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "footer"))
    )
    return footer


@pytest.mark.parametrize("path", PAGES)
def test_footer_presence_and_elements(driver, path):
    """
    Проверяем:
    - футер присутствует на странице;
    - есть email;
    - есть копирайт;
    - есть ссылка Privacy policy;
    - есть ссылки на соцсети;
    - дублируются пункты навигации.
    """
    driver.get(BASE_URL + path)

    footer = get_footer(driver)
    footer_text = footer.text

    # 1. Privacy policy — как базовый якорь футера
    privacy_link = footer.find_element(By.LINK_TEXT, "Privacy policy")
    assert privacy_link.is_displayed(), "Ссылка 'Privacy policy' не отображается в футере"

    # 2. Контактные данные
    assert "hello@only.digital" in footer_text, "В футере нет email hello@only.digital"

    # 3. Копирайт (оба варианта, которые могут быть)
    assert "© 2014 - 2025" in footer_text or "only.digital © 2014-2025" in footer_text, \
        "В футере нет текста копирайта"

    # 4. Соцсети (Behance, Telegram, VK и т.п.)
    social_links = footer.find_elements(
        By.XPATH,
        ".//a[contains(@href, 'behance.net') or "
        "contains(@href, 't.me') or "
        "contains(@href, 'vk.com')]"
    )
    assert social_links, "В футере не найдены ссылки на социальные сети"

    # 5. Навигационные пункты (дубликат основного меню)
    for item in FOOTER_NAV_ITEMS:
        links = footer.find_elements(By.LINK_TEXT, item)
        assert links, f"В футере нет пункта навигации '{item}'"
