# GeocodeDDT

Автотесты для публичного API геокодирования и UI [Nominatim (OpenStreetMap)](https://nominatim.openstreetmap.org).

## Технологии

*   **Язык:** `Python 3.8`
*   **Фреймворк тестирования:** `Pytest`
*   **HTTP-клиент:** `Requests`
*   **UI-автоматизация:** `Selenium WebDriver`
*   **Отчетность:** `Allure Report`
*   **Управление зависимостями:** `Pip / Venv`

## Установка

```bash
1. Клонируйте репозиторий:
```bash
git clone https://github.com/stolnikov-ea/geocodeDDT.git
cd geocodeDDT
```

2. Создайте и активируйте виртуальное окружение:
```bash
python3 -m venv .venv
source .venv/bin/activate
 ```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Конфигурация

Основные параметры указаны в файле `config/settings.py`.

### Важное: Требования для работы с API

1. Согласно политике использования Nominatim, при интенсивном использовании API рекомендуется указывать контакт.
Чтобы избежать ошибки `403 Forbidden`, задайте переменную окружения `USER_EMAIL` перед запуском тестов.

2. Согласно политике использования Nominatim, запросы не должны отправляться чаще раза в секунду.
Этот интервал задается параметром `API_MIN_INTERVAL`. Значение по умолчанию 1.0, ставить меньше не рекомендуется.

## Запуск

1. Запуск всех тестов:
```bash
pytest
```

2. Запуск тестов с определенным маркером:
```bash
pytest -m marker
```

### Варианты маркеров:
* `api`: тесты API
* `ui`: тесты UI
* `forward`: тесты прямого геокодирования
* `reverse`: тесты обратного геокодирования
* `positive`: позитивные тесты
* `negative`: негативные тесты

## Генерация отчета Allure

Результаты тестов сохраняются в папку `allure-results` (настроено в `pytest.ini`).

Для генерации отчета понадобится Allure CLI:
```bash
allure serve ./allure-results
```