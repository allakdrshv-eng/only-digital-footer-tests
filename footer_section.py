from dataclasses import dataclass
from typing import Dict, List

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@dataclass
class FooterSection:
    """Компонент футера только.digital.

    Инкапсулирует локаторы и базовые проверки, чтобы в тесте была
    только бизнес-логика, а не XPATH-ы.
    """

    driver: WebDriver
    timeout: int = 10

    NAV_ITEMS = ["Work", "About us", "What we do", "Career", "Blog", "Contacts"]
    SOCIAL_HREF_PARTS = (
        "t.me",          # Telegram
        "behance.net",
        "vk.com",
        "dribbble.com",
        "instagram.com",
        "facebook.com",
        "twitter.com",
        "x.com",
    )

    @property
    def wait(self) -> WebDriverWait:
        return WebDriverWait(self.driver, self.timeout)

    def _locate_footer_root(self):
        """Ищем корневой контейнер футера.

        Сначала пробуем семантический тег <footer>, если его нет –
        берём ближайший родитель для ссылки Privacy policy.
        """
        try:
            return self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "footer")))
        except TimeoutException:
            privacy = self.wait.until(
                EC.presence_of_element_located((By.LINK_TEXT, "Privacy policy"))
            )
            return privacy.find_element(By.XPATH, "ancestor::*[1]")

    def text(self) -> str:
        """Весь видимый текст футера."""
        return self._locate_footer_root().text

    def has_privacy_policy(self) -> bool:
        footer = self._locate_footer_root()
        links = footer.find_elements(By.LINK_TEXT, "Privacy policy")
        return bool(links)

    def nav_links(self) -> Dict[str, List]:
        """Собираем ссылки навигации по тексту."""
        footer = self._locate_footer_root()
        result: Dict[str, List] = {}
        for label in self.NAV_ITEMS:
            result[label] = footer.find_elements(By.LINK_TEXT, label)
        return result

    def email_link_present(self, email: str = "hello@only.digital") -> bool:
        footer = self._locate_footer_root()
        # либо mailto-ссылка, либо просто текстовая ссылка
        mailto = footer.find_elements(By.XPATH, f".//a[contains(@href, 'mailto:{email}')]")
        if mailto:
            return True
        text_links = footer.find_elements(
            By.XPATH,
            f".//a[normalize-space(text())='{email}']",
        )
        return bool(text_links)

    def social_links(self) -> List:
        """Возвращает все ссылки на соцсети в футере."""
        footer = self._locate_footer_root()
        xpath_parts = " or ".join(
            [f"contains(@href, '{part}')" for part in self.SOCIAL_HREF_PARTS]
        )
        if not xpath_parts:
            return []
        return footer.find_elements(By.XPATH, f".//a[{xpath_parts}]")

    def has_copyright(self) -> bool:
        text = self.text()
        return ("© 2014 - 2025" in text) or ("only.digital © 2014-2025" in text)
