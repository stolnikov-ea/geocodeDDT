# GeocodeDDT

Автотесты публичного API геокодинга openstreetmaps.org

## Установка

```bash
# Клонируем репозиторий
git clone https://github.com/stolnikov-ea/geocodeDDT.git
cd geocodeDDT

# Создаём виртуальное окружение
python3.8 -m venv .venv

# Активируем
source .venv/bin/activate

# Устанавливаем зависимости
pip install -r requirements.txt
```

## Запуск

```bash
pytest
```