import telebot
from config import keys , TOKEN
from extensions import ConvertionException, CryptoConverter

print("Бот запущен")

bot = telebot.TeleBot (TOKEN)



@bot.message_handler(commands=['start', 'help'])
def send_welcome_help(message: telebot.types.Message):
    text = f"Приветствую, {message.from_user.first_name}, я прекрасно разбираюсь в курсах валют!"
    bot.reply_to(message,text)
    text = f"Чтобы начать работу, введите команду в следующем формате:\n \
<x> <y> <z>,\n\
где x - имя валюты, y - в какую валюту перевести, z - количество переводимой валюты\n\
увидеть список доступных валют:/values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text= f"Доступные валюты:"
    for key in keys.keys():
        text='\n'.join((text,key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message:telebot.types.Message):
    try:

        if message.text == "Привет":
            bot.send_message(message.chat.id, 'Привет! Введите команду /start или /help')
            return

        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('Слишком много или мало параметров.Для уточнения введите команду /help')


        quote, base, amount = values
        total_base = CryptoConverter.convert(quote.lower(),base.lower(),amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message,f'Не удалось обработать команду\n{e}')
    else:
      text= f'Цена {amount} {quote} в {base}-{total_base}'
      bot.send_message(message.chat.id,text)

@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message: telebot.types.Message):
    text= f'Интересуют курсы валют? Введите,пожалуйста команду /start или /help'
    bot.reply_to(message, text)

@bot.message_handler(content_types=['photo', ])
def say_lmao(message: telebot.types.Message):
    text= f"Классное фото!\n\
После введения команды  /start или /help мы сможем пообщаться еще!"
    bot.reply_to(message, text)


bot.polling(none_stop=True)
print("Запустите бот")

