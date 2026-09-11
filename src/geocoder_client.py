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
)

logger = logging.getLogger(__name__)

class GeocoderClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.timeout = API_TIMEOUT
        self.min_interval = API_MIN_INTERVAL
        self.retry_count = API_RETRY_COUNT
        self.retry_delay = API_RETRY_DELAY
        self.session = requests.Session()
        self._last_request_time = 0.0
        logger.info("GeocoderClient создан: %s", self.base_url)

    def close(self):
        self.session.close()
        logger.info("GeocoderClient закрыт")

    def _wait_if_needed(self):
        now = time.monotonic()
        delta = now - self._last_request_time

        if delta < self.min_interval:
            wait = self.min_interval - delta
            logger.debug("Жду %.1f секунд до следующего запроса", wait)
            time.sleep(wait)

        self._last_request_time = time.monotonic()

    def _request_with_retry(self, url: str, params: Dict[str, Any]) -> requests.Response:
        last_exception = None
        response = None

        for attempt in range(1, self.retry_count + 1):
            self._wait_if_needed()

            try:
                response = self.session.get(
                    url,
                    params=params,
                    timeout = self.timeout
                )

                if response.status_code < 500:
                    return response

                logger.warning(
                    "Ошибка сервера: %d (попытка %d/%d)",
                    response.status_code,
                    attempt,
                    self.retry_count,
                )
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                logger.warning(
                    "Сетевая ошибка: %s (попытка %d/%d)",
                    e,
                    attempt,
                    self.retry_count,
                )
                last_exception = e
        if last_exception:
            raise last_exception

        return response #type: ignore

    def geocode(self, address: str):
        url = f"{self.base_url}/geocode/{address}"
        params = {"format": "json"}

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
            logger.info("Успех: %S [%d] (%.1fms)", address, response.status_code, elapsed_ms)

        return {
            "status_code": response.status_code,
            "body": body,
        }

    def geocode_reverse(self, lat: float, lon: float):
        url = f"{self.base_url}/reverse"
        params = {
            "format": "json",
            "lat": lat,
            "lon": lon,
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