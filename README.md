# only.digital – footer UI test (Selenium + pytest)

Автотест проверяет, что на ключевых страницах английской версии сайта  
`https://only.digital` футер содержит:

- ссылку **Privacy policy**;
- email `hello@only.digital`;
- копирайт `© 2014 - 2025` / `only.digital © 2014-2025`;
- пункты навигации `Work`, `About us`, `What we do`, `Career`, `Blog`, `Contacts`;
- хотя бы одну ссылку на соцсети (Telegram/Behance/VK/и т.п.).

## Запуск локально

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / macOS

pip install -r requirements.txt
pytest -v
