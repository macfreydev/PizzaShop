from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add(KeyboardButton('🍕 Menu'))
main.add(KeyboardButton('🛒 Cart'))
main.add(KeyboardButton('🎉 Sales'))
main.add(KeyboardButton('📞 Contact'))
main.add(KeyboardButton('🔍 Reviews'))

