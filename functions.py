from pathlib import Path
import json

SERVICE_JSON_NAME = '_service.json'
BITRIX_LAST_MESSAGE_KEY = 'bitrix_last_message_id'


def get_project_root() -> Path:
    return Path(__file__).parent


def get_full_path(*args) -> Path:
    return Path(get_project_root(), *args)


def read_json_from_file(path: Path):
    file = open(path, 'r', encoding='utf8')
    data = file.read()
    return json.loads(data)


def write_json_to_file(path, data):
    file = open(path, 'w', encoding='utf8')
    file.write(json.dumps(data, ensure_ascii=False, indent=4))
    file.close()


def get_service_json():
    try:
        return read_json_from_file(get_full_path(SERVICE_JSON_NAME))
    except Exception:
        return {}


def get_bitrix_last_message_id():
    return get_service_json().get(BITRIX_LAST_MESSAGE_KEY)


def write_bitrix_last_message_id(message_id):
    data = get_service_json()
    data[BITRIX_LAST_MESSAGE_KEY] = message_id
    write_json_to_file(get_full_path(SERVICE_JSON_NAME), data)
