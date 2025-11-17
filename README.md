# Автотест футера only.digital

Тест проверяет, что на выбранных страницах сайта:

- присутствует футер;
- в футере есть email `hello@only.digital`;
- есть копирайт `© 2014 - 2025` или `only.digital © 2014-2025`;
- есть ссылка `Privacy policy`;
- есть ссылки на соцсети;
- продублированы пункты основной навигации.

## Установка

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
