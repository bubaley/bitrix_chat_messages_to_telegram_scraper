import os
import time
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import schedule
from functions import get_bitrix_last_message_id, write_bitrix_last_message_id
from request_manager import RequestManager
from telegram_message_sender import TelegramMessageSender

load_dotenv()
BITRIX_URL = os.getenv('BITRIX_URL')
BITRIX_DIALOG_ID = os.getenv('BITRIX_DIALOG_ID')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

_keys = [BITRIX_URL, BITRIX_DIALOG_ID, TELEGRAM_CHAT_ID, TELEGRAM_BOT_TOKEN]
if not all(_keys):
    raise ValueError('Invalid variables')


def get_new_messages():
    params = {
        'DIALOG_ID': BITRIX_DIALOG_ID,
        'FIRST_ID': get_bitrix_last_message_id()
    }
    response = RequestManager.request(f'{BITRIX_URL}/im.dialog.messages.get', params=params)
    if response.ok:
        messages_data = response.data.get('result', [])
        users = {v['id']: v['name'] for v in messages_data['users']}
        messages = messages_data['messages']
        results = []
        for el in messages:
            try:
                message_date = datetime.fromisoformat(el['date']).astimezone(timezone.utc) + timedelta(hours=2)
                message_date = message_date.strftime('%d.%m.%Y, %H:%M:%S')
            except Exception:
                message_date = '-'

            results.append({
                'id': el['id'],
                'user': users.get(el.get('author_id')) or 'Пользователь не определен',
                'text': el.get('text') or '-',
                'date': message_date
            })
        if messages:
            write_bitrix_last_message_id(messages[0]['id'])
        return results
    else:
        return []


def send_messages(messages):
    if not messages:
        return
    values = []
    for el in messages:
        values.append('\n'.join([
            f'Текст: {el['text']}',
            '',
            f'🕝 {el['user']} | {el['date']}'
        ]))
    message = '\n\n------------\n\n'.join(values)
    TelegramMessageSender.send_message(
        title=f'⭐ Новое сообщение - {len(messages)}',
        message=message,
        chat_id=TELEGRAM_CHAT_ID,
        bot_token=TELEGRAM_BOT_TOKEN
    )


def main():
    messages = get_new_messages()
    print(f'Got messages: {len(messages)}')
    # send_messages(messages)


schedule.every(30).seconds.do(main)

if __name__ == "__main__":
    main()
    while True:
        schedule.run_pending()
        time.sleep(1)
