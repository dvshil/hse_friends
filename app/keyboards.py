from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)




start = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Давай начнем😜')]], one_time_keyboard=True,
                           resize_keyboard=True)
gender = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Я парень🧍‍♂️')],
                                     [KeyboardButton(text='Я девушка🧍‍♀️')]],
                           one_time_keyboard=True, resize_keyboard=True)
group = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='КНТ-4')],
                                      [KeyboardButton(text='КНТ-5')],
                                      [KeyboardButton(text='КНТ-6')]],
                            one_time_keyboard=True, resize_keyboard=True)
contact = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить контакт', request_contact=True)]],
                              one_time_keyboard=True, resize_keyboard=True)

action = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='1'), KeyboardButton(text='2'),
                                        KeyboardButton(text='3'), KeyboardButton(text='4')]],
                             one_time_keyboard=True, resize_keyboard=True)

profile_view = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='👍'),
                                             KeyboardButton(text='✉️'),
                                   KeyboardButton(text='👎'),
                                              KeyboardButton(text='💤')]],
                                   resize_keyboard=True)
