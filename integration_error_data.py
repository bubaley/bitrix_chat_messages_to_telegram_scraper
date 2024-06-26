import json
from dataclasses import dataclass


@dataclass
class IntegrationErrorData:
    data: str | dict | list
    code: str = 'Unhandled'

    def __str__(self):
        values = []
        if self.code:
            values.append(self.code)
        data = self.data
        if type(data) in [list, dict]:
            try:
                data = json.dumps(data, ensure_ascii=False, default=str, indent=2)
            except Exception:
                data = 'Cannot format data to string'
        if data:
            values.append(data)
        return ' | '.join(values) if values else 'Empty error'

    def to_dict(self):
        return {
            'code': self.code,
            'data': self.data
        }
