from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class FooterSection:
    """Объект футера для проверок общих элементов.

    Специально не жёстко привязан к тегу <footer>,
    так как на only.digital футер реализован без него.
    """

    def __init__(self, driver, timeout: int = 10) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # --- Общие элементы ---

    def has_privacy_policy(self) -> bool:
        """Есть ссылка/элемент с текстом 'Privacy policy'."""
        try:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[normalize-space(text())='Privacy policy']")
                )
            )
            return True
        except TimeoutException:
            return False

    def email_link_present(self) -> bool:
        """На странице есть текст hello@only.digital (не важно, в каком теге)."""
        try:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'hello@only.digital')]")
                )
            )
            return True
        except TimeoutException:
            return False

    def has_copyright(self) -> bool:
        """Есть копирайт за период 2014–2025.

        Поддерживаем оба варианта:
        - '© 2014 - 2025'
        - 'only.digital © 2014-2025'
        """
        xpath = (
            "//*[contains(text(), '© 2014') and contains(text(), '2025')]"
            " | //*[contains(normalize-space(.), 'only.digital © 2014-2025')]"
        )
        try:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, xpath)
                )
            )
            return True
        except TimeoutException:
            return False

    # --- Навигация футера ---

    def nav_links(self) -> dict:
        """Находим ссылки навигации по тексту.

        Возвращаем словарь: label -> список найденных элементов.
        Тест проверяет, что списки не пустые.
        """
        labels = {
            "Work": "Work",
            "About us": "About us",
            "What we do": "What we do",
            "Career": "Career",
            "Blog": "Blog",
            "Contacts": "Contacts",
        }

        result: dict[str, list] = {}
        for label, text in labels.items():
            elements = self.driver.find_elements(
                By.XPATH,
                f"//a[normalize-space(text())='{text}']"
            )
            result[label] = elements

        return result
