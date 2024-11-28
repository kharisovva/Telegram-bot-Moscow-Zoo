import telebot
from telebot import types
from config import TOKEN
from extensions import questions_data, answers_data

bot = telebot.TeleBot(TOKEN)


# приветствие бота с команды start
@bot.message_handler(commands=['start'])
def greeting(message: telebot.types.Message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    letsgo_button = types.InlineKeyboardButton('Погнали 🚀', callback_data='answ_letsgo')
    markup.add(letsgo_button)
    logo = open('animals/лого.png', 'rb')
    bot.send_photo(message.chat.id, photo=logo)
    bot.send_message(message.chat.id, text=
    f'Привет, {message.chat.username}!\n\nДобро пожаловать в бот-викторину Московского зоопарка!'
    ' Сейчас тебе предстоит пройти небольшой тест и узнать, какое животное '
    'из нашего зоопарка подходит тебе больше всего. 🦥\n\nПрохождение теста займет не больше 5 минут!'
    ' В самом конце тебя ждет уникальное предложение 🤫 Вперед к тесту?', reply_markup=markup)


# генератор клавиатуры с ответами
def quiz_keyboard_generator():
    for question, button_data in questions_data.items():
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        for answer, callback in button_data.items():
            button = types.InlineKeyboardButton(text=answer, callback_data=callback)
            keyboard.add(button)
        yield question,keyboard


questions = quiz_keyboard_generator()


# отправка вопросов с ответами и обработка нажатия на кнопки
@bot.callback_query_handler(func= lambda call: call.data.startswith('answ_'))
def quiz(call: types.CallbackQuery):
    result(call)
    try:
        question, keyboard = next(questions)
        bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)
    except StopIteration:
        findout = types.ReplyKeyboardMarkup()
        findout1 = types.KeyboardButton(text='Узнать результаты 🙈')
        findout.add(findout1)
        bot.send_message(call.message.chat.id, text='Поздравляю, викторина пройдена!'
                                                    ' Самое время посмотреть на результат и узнать, какое'
                                                    ' же животное подходит именно тебе!', reply_markup=findout)


# обработка ответов
result_data = 0


def result(call):
    global result_data
    result_data += answers_data.get(call.data, 0)


# вывод результата
@bot.message_handler(content_types=['text'])
def print_result(message: telebot.types.Message):
    if message.text == 'Узнать результаты 🙈':
        website = types.InlineKeyboardMarkup(row_width=1)
        website1 = types.InlineKeyboardButton('Как стать опекуном? 🐾',
                                              url='https://moscowzoo.ru/about/guardianship')
        website.add(website1)
        global result_data
        if result_data <= 9:
            result_text = ('Тебе подходит южноафриканская черная антилопа! '
                           '\n\nКрупная, стройная, вооруженная длинными, великолепной формы рогами, изысканной чёрно-белой '
                           'окраски антилопа относится к наиболее красивым животным Африки. '
                           'Первые две чёрные антилопы появились в нашем зоопарке в 1971 году, их привезла в подарок '
                           'зоопарку известная голландская фирма по торговле дикими животными. Через несколько месяцев '
                           'появилось потомство. С тех пор небольшая группа этих красивейших антилоп постоянно содержится в '
                           'нашем зоопарке.\n\n'
                           'Московский зоопарк - единственный на территории бывшего Советского Союза, который имеет в '
                           'своей коллекции этих редких и ценных антилоп, наши животные занесены в международную '
                           'племенную книгу чёрных антилоп и изредка удается получить от них потомство. Необходимо '
                           'отметить, что и в зоопарках Европы чёрная антилопа – большая редкость.\n\n'
                           'Ты можешь стать другом черной антилопы и быть ее опекуном по программе нашего зоопарка '
                           '- переходи на сайт за подробностями')
            photo1 = open('animals/антилопа.jpg', 'rb')
            bot.send_photo(message.chat.id, photo=photo1)
            bot.send_message(message.chat.id, result_text, reply_markup=website)

        if 9 < result_data <= 20:
            result_text = ('Твое животное - морж!\n\n'
                           'Морж - морской зверь с очень характерной внешностью, самое крупное ластоногое Арктики.'
                           'Неповоротливые на суше, моржи очень подвижны в воде. Ласты моржей очень гибкие и напоминают '
                           'руки с пятью пальцами. Когтями задних ласт морж может почесать шею.\n\n'
                           'Моржи в нашем зоопарке являются почти постоянными обитателями. Впервые они появились на '
                           'экспозиции в 1931 году. Ты можешь стать другом моржа и быть его опекуном по программе '
                           'нашего зоопарка - переходи на сайт за подробностями')
            photo2 = open('animals/морж.jpg', 'rb')
            bot.send_photo(message.chat.id, photo=photo2)
            bot.send_message(message.chat.id, result_text, reply_markup=website)

        if 21 <= result_data < 25:
            result_text = ('Тебе подходит альпака!\n\n'
                           'Альпака – коренной житель Южной Америки, обитает в суровых условиях высокогорья Анд. Это самый '
                           'маленький из безгорбых верблюдов, рост животного не превышает одного метра, а вес – 70 кг. '
                           'Альпака стройная, легко сложенная, с короткой мордочкой, узкими заострёнными ушами, коротким '
                           'мохнатым хвостом, длинными ногами и длинной шеей.\n\n'
                           'Пара альпак содержится в нашем зоопарке на Старой территории в небольшом вольере рядом со '
                           'скалой хищных птиц. Ты можешь стать другом альпаки и быть ее опекуном по программе '
                           'нашего зоопарка - переходи на сайт за подробностями')
            photo3 = open('animals/альпака.jpeg', 'rb')
            bot.send_photo(message.chat.id, photo=photo3)
            bot.send_message(message.chat.id, result_text, reply_markup=website)

        if 26 <= result_data:
            result_text = ('Твое животное - африканский марабу!\n\n'
                           'Марабу – один из наиболее крупных аистов, его длина 115-152 см, размах крыльев 225-287 см, '
                           'масса 4-9 кг. Марабу довольно молчаливы, но могут с помощью резонатора издавать громкие мычащие '
                           'звуки. При демонстрационном поведении стучат клювом, как некоторые другие аисты. В колоде карт '
                           'Таро имеется группа «Птицы», куда обычно входит и изображение марабу.\n\n'
                           'В нашем зоопарке африканские марабу появились в 2023 году, раньше марабу в у нас не '
                           'содержались. Это молодые и совершенно ручные птицы. Ты можешь стать другом марабу и быть его '
                           'опекуном по программе нашего зоопарка - переходи на сайт за подробностями')
            photo4 = open('animals/марабу.jpg', 'rb')
            bot.send_photo(message.chat.id, photo=photo4)
            bot.send_message(message.chat.id, result_text, reply_markup=website)
        result_data = 0
        restart = types.InlineKeyboardMarkup(row_width=1)
        one_more_time = types.InlineKeyboardButton('Пройти викторину еще раз', callback_data='answ_letsgo')
        share_vk = types.InlineKeyboardButton('Поделиться результатом ВКонтакте ↗️',
                                              url='https://vk.com/share.php?url=https://t.me/what_is_your_animal_bot&title=Узнай, какое животное тебе подходит')
        share_twitter = types.InlineKeyboardButton('Поделиться результатом в Twitter ↗️',
                                                   url='https://twitter.com/share?url=https://t.me/what_is_your_animal_bot&text=Узнай, какое животное тебе подходит')
        share_classmates = types.InlineKeyboardButton('Поделиться результатом в Одноклассниках ↗️',
                                                      url='https://connect.ok.ru/offer?url=https://t.me/what_is_your_animal_bot')
        contact_us = types.InlineKeyboardButton('Связаться с сотрудником зоопарка 🧑🏼‍💻', url='https://t.me/kharisovva')
        restart.add(one_more_time, share_vk, share_twitter, share_classmates, contact_us)
        bot.send_message(message.chat.id, '🐻🐻🐻\n\nМожешь пройти тест еще раз и познакомиться с другими животными, '
                                         'а также можешь поделиться своим результатом в социальных сетях.\n\n'
                                         'Связаться с сотрудником зоопарка для дополнительной информации можно также по кнопке ниже:',
                         reply_markup=restart)
    else:
        bot.send_message(message.chat.id, 'Извини, но я тебя не понял 😔 Воспользуйся командой по кнопке!')


bot.polling(non_stop=True)