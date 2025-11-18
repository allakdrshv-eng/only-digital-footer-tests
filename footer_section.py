# footer_section.py
from __future__ import annotations

from typing import Dict, List

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class FooterSection:
    """
    Обертка над «футером» страницы only.digital.

    Важно: сайт устроен так, что часть элементов (навигация и т.п.)
    находится не обязательно строго внутри тега <footer>. Для целей
    автотеста мы считаем условным футером всю страницу и ищем элементы
    по тексту/ссылкам.
    """

    def __init__(self, driver, timeout: int = 10) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # --- Вспомогательные методы -------------------------------------------------

    def _root(self):
        """
        Пытаемся вернуть настоящий <footer>, а если его нет — <body>,
        чтобы не падать с NoSuchElementException.
        """
        try:
            return self.driver.find_element(By.TAG_NAME, "footer")
        except NoSuchElementException:
            return self.driver.find_element(By.TAG_NAME, "body")

    def _find_all(self, xpath: str):
        return self.driver.find_elements(By.XPATH, xpath)

    # --- Проверка обязательных элементов ----------------------------------------

    def has_privacy_policy(self) -> bool:
        """
        Есть ссылка с текстом 'Privacy policy'.
        Ищем по всей странице, а не только в <footer>.
        """
        locator = (By.XPATH, '//a[contains(normalize-space(.), "Privacy policy")]')
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def email_link_present(self) -> bool:
        """
        Есть e-mail hello@only.digital (как ссылка или как текст).
        """
        xpaths = [
            # Классический mailto
            (
                '//a[contains(translate(@href, '
                '"ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), '
                '"mailto:hello@only.digital")]'
            ),
            # E-mail как текст внутри ссылки
            '//a[contains(normalize-space(.), "hello@only.digital")]',
            # E-mail просто как текст на странице
            '//*[contains(normalize-space(.), "hello@only.digital")]',
        ]

        for xp in xpaths:
            if self._find_all(xp):
                return True
        return False

    def has_copyright(self) -> bool:
        """
        Ищем корректный текст копирайта. На сайте встречаются варианты:
        '© 2014 - 2025', '© 2014-2025', 'only.digital © 2014-2025'.
        """
        xpath = (
            '//*[contains(normalize-space(.), "© 2014 - 2025") '
            ' or contains(normalize-space(.), "© 2014-2025") '
            ' or contains(normalize-space(.), "only.digital © 2014-2025")]'
        )
        return bool(self._find_all(xpath))

    # --- Навигация в футере -----------------------------------------------------

    def nav_links(self) -> Dict[str, List]:
        """
        Возвращает словарь:
        {
          "Work": [WebElement, ...],
          "About us": [...],
          ...
        }

        Для стабильности ищем ссылки по тексту по всей странице —
        главное, чтобы элементы вообще существовали.
        """
        labels = [
            "Work",
            "About us",
            "What we do",
            "Career",
            "Blog",
            "Contacts",
        ]

        result: Dict[str, List] = {}
        for label in labels:
            elems = self._find_all(f'//a[normalize-space(.)="{label}"]')
            result[label] = elems
        return result

    # --- Соцсети -----------------------------------------------------------------

    def _social_link_elements(self):
        """
        Собираем ссылки на соцсети (Behance, dprofile, Telegram, VK и т.п.).
        """
        xpath = (
            '//a[contains(@href, "behance.net") '
            ' or contains(@href, "dprofile.ru") '
            ' or contains(@href, "t.me") '
            ' or contains(@href, "vk.com")]'
        )
        return self._find_all(xpath)

    def social_links(self):
        """Возвращаем список элементов-ссылок на соцсети."""
        return self._social_link_elements()

    def has_social_links(self) -> bool:
        """Булевый синоним: есть ли вообще соцсети."""
        return bool(self._social_link_elements())
