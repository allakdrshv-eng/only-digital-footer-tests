import pytest

from footer_section import FooterSection


BASE_URL = "https://only.digital"

PAGES = [
    "/en",          # главная
    "/en/projects",
    "/en/company",
    "/en/fields",
    "/en/job",
    "/en/blog",
    "/en/contacts",
]


@pytest.mark.parametrize("path", PAGES)
def test_footer_common_elements_present(driver, path):
    """Проверка, что на ключевых страницах футер содержит
    навигацию, контакты, соцсети, privacy и копирайт.
    """

    driver.get(BASE_URL + path)

    footer = FooterSection(driver)

    # 1. Есть футер и ссылка на политику конфиденциальности
    assert footer.has_privacy_policy(), "В футере нет ссылки 'Privacy policy'"

    # 2. Есть e-mail hello@only.digital
    assert footer.email_link_present(), "В футере нет email hello@only.digital"

    # 3. Есть копирайт
    assert footer.has_copyright(), "В футере нет корректного текста копирайта"

    # 4. Навигация: Work, About us, What we do, Career, Blog, Contacts
    nav_links = footer.nav_links()
    missing = [label for label, elems in nav_links.items() if not elems]
    assert not missing, f"В футере нет пунктов навигации: {', '.join(missing)}"

    # 5. Есть хотя бы одна ссылка на соцсети
    assert footer.social_links(), "В футере не найдены ссылки на социальные сети"
