from .default import get_id_message, get_state_message

def init_default_handlers(dp):
    dp.register_message_handler(get_id_message, state='*', commands=['get_id'])
    dp.register_message_handler(get_state_message, state='*', commands=['get_state'])