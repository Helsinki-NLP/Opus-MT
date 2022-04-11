from aiogram import types

KEYBOARDS = {
    'hide': types.ReplyKeyboardRemove(selective=False),
    'lang': {
        'options': ['English', 'Finnish', 'German', 'Swedish', 'Ukrainian'],
        'markup': None,
    },
}

def fill_keyboards():
    # scales
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(*[types.KeyboardButton(variant) for variant in KEYBOARDS['lang']['options']])
    KEYBOARDS['lang']['markup'] = markup
    
fill_keyboards()
