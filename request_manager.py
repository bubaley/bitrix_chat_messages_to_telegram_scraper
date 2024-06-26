import requests
from requests import Response
from dataclasses import dataclass
from http.client import responses

from integration_error_data import IntegrationErrorData


@dataclass
class ResponseData:
    ok: bool = False
    status_code = None
    data: dict | list | None = None
    text: str = None
    response: Response | None = None

    def build_integration_error_data(self):
        if self.ok:
            return
        return IntegrationErrorData(
            code='No response' if self.response is None else responses.get(self.response.status_code, 'Unhandled'),
            data=self.data or self.text or 'Empty message',
        )

    @property
    def data_or_error_data(self):
        if self.data:
            return self.data
        error_data = self.build_integration_error_data()
        if error_data:
            return error_data.to_dict()


class RequestManager:
    @staticmethod
    def request(url, method='GET', **kwargs) -> ResponseData:
        result = ResponseData()
        try:
            response = requests.request(url=url, method=method, **kwargs)
            result.response = response
            result.ok = response.ok
            result.text = response.text
            result.status_code = response.status_code
            result.data = RequestManager._parse_data(response)
        except Exception as e:
            result.text = f'{type(e).__name__} | {str(e)}'
        return result

    @staticmethod
    def _parse_data(response: Response):
        try:
            return response.json()
        except Exception:
            pass
