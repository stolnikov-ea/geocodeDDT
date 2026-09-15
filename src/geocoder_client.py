import time
import logging
import json
import requests

from typing import Any, Dict

from config.settings import (
    API_BASE_URL,
    API_TIMEOUT,
    API_MIN_INTERVAL,
    API_RETRY_COUNT,
    API_RETRY_DELAY,
    USER_EMAIL,
)

logger = logging.getLogger(__name__)

class GeocoderClient:
    def __init__(self) -> None:
        self.session = requests.Session()

        self.session.headers.update({"User-Agent": f"DDT_educational_project/1.0 (contact: {USER_EMAIL})"})

        self._last_request_time = 0.0
        logger.info("GeocoderClient создан: %s", API_BASE_URL)

    def close(self) -> None:
        self.session.close()
        logger.info("GeocoderClient закрыт")

    def _wait_if_needed(self) -> None:
        now = time.monotonic()
        delta = now - self._last_request_time

        if delta < API_MIN_INTERVAL:
            wait = API_MIN_INTERVAL - delta
            logger.debug("Жду %.1f секунд до следующего запроса", wait)
            time.sleep(wait)

        self._last_request_time = time.monotonic()

    def _request_with_retry(self, url: str, params: Dict[str, Any]) -> requests.Response:
        last_exception = None
        response = None

        for attempt in range(1, API_RETRY_COUNT + 1):
            self._wait_if_needed()

            try:
                response = self.session.get(url, params=params,timeout = API_TIMEOUT)

                if response.status_code < 500:
                    return response

                else:
                    logger.warning(
                    "Ошибка сервера: %d (попытка %d/%d)",response.status_code, attempt, API_RETRY_COUNT)

            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                logger.warning("Сетевая ошибка: %s (попытка %d/%d)", e, attempt, API_RETRY_COUNT)
                last_exception = e

            if attempt < API_RETRY_COUNT:
                logger.debug("Ожидаю %d секунд перед повторной попыткой", API_RETRY_DELAY)
                time.sleep(API_RETRY_DELAY)

        if last_exception:
            raise last_exception

        return response #type: ignore

    def geocode(self, address: str) -> Dict[str, Any]:
        url = f"{API_BASE_URL}/search"
        params = {
            "q": address,
            "format": "jsonv2",
            "limit": 1,
        }

        logger.debug("Запрос: url=%s, params=%s", url, params)

        start_time = time.monotonic()
        response = self._request_with_retry(url, params)
        elapsed_ms = (time.monotonic() - start_time) * 1000

        body = response.json()

        logger.debug(
            "Ответ: статус=%d время=%.1fms\n%s",
            response.status_code,
            elapsed_ms,
            json.dumps(body, ensure_ascii=False, indent=2),
        )

        if response.status_code >= 400:
            logger.warning("Ошибка клиента: адрес: %s статус: %d", address, response.status_code)
        else:
            logger.info("Успех: %s [%d] (%.1fms)", address, response.status_code, elapsed_ms)

        return {
            "status_code": response.status_code,
            "body": body,
        }

    def geocode_reverse(self, lat: float, lon: float) -> Dict[str, Any]:
        url = f"{API_BASE_URL}/reverse"
        params = {
            "format": "jsonv2",
            "lat": lat,
            "lon": lon,
            "limit": 1,
            "zoom": 18,
        }

        start_time = time.monotonic()
        response = self._request_with_retry(url, params)
        elapsed_ms = (time.monotonic() - start_time) * 1000

        body = response.json()

        logger.debug(
            "Обратное геокодирование. Ответ: статус=%d время=%.1fms\n%s",
            response.status_code,
            elapsed_ms,
            json.dumps(body, ensure_ascii=False, indent=2),
        )

        if response.status_code >= 400:
            logger.warning("Ошибка клиента: широта: %.4f долгота: %.4f статус: %d", lat, lon, response.status_code)
        else:
            logger.info("Успех: широта: %.4f долгота: %.4f [%d] (%.1fms)", lat, lon, response.status_code, elapsed_ms)

        return {
            "status_code": response.status_code,
            "body": body,
        }