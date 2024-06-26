from threading import Thread

from request_manager import RequestManager


class TelegramMessageSender:
    @staticmethod
    def send_message(title, message: list | str = None, chat_id: list[str] | str | None = None,
                     bot_token: str | None = None):
        if not bot_token:
            return
        data = {'title': title, 'message': message, 'chat_id': chat_id, 'bot_token': bot_token}
        Thread(target=TelegramMessageSender._send_message, kwargs=data).start()

    @staticmethod
    def _send_message(title, message: list | str = None, chat_id: list[str] | str | None = None,
                      bot_token: str | None = None):
        if not chat_id:
            return
        chat_ids = chat_id if isinstance(chat_id, list) else [chat_id]
        if isinstance(message, list):
            message = '\n'.join(message)
        message = message or None
        for chat_id in chat_ids:
            try:
                url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
                send_text = f'<b>{title}</b>\n'
                if message:
                    send_text += f'\n{message}'
                send_text = send_text[:4000] + '\n...' if len(send_text) > 4000 else send_text
                params = {'chat_id': chat_id, 'text': send_text, 'parse_mode': 'html'}
                result = RequestManager.request(method='GET', url=url, params=params)
                if not result.ok:
                    raise Exception({'title': 'TELEGRAM_ERROR', 'text': result.text})
            except Exception as e:
                print(e)
