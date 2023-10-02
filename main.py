"""
Короч смотри из минусов этой хрени:
1)при говорении создает на каждый вопрос ответ по файлу, раньше такого не было, это надо будет как-то подправить.
2) Википедия работает, но почему-то не ищет в самой википедии ответ, функция к ней правильная ну по крайней мере работает на других бота, тут скипает поиск и выдает что не нашла не чего.
3) Напоминалка откинулась, тут скорее всего что-то с самой библиотекой, так как летом эта хрень работала, отдельно тоже не хочет.
4) с мемами еще решим конечно, но из-за файла с говорением, а, то есть проблема из 1 пункта, картинки банально не открываются.
5) система оплаты, ну тут я особо не влезал, так как с ней будет связано все остальное.

Ну и по коду особо сильно не быч я впервые пишу в таком формате
"""


#файлы питона
import config
import wiki
import say
import randoms_memes

#остальные библиотеки
from datetime import datetime, timedelta
from enum import Enum
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
count_unforgettable = 1

class Event:
    text = None
    time = None
    chat_id = None


class ReminderBotState(Enum):
    DEFAULT = 0
    WAITING_FOR_EVENT_TEXT = 1
    WAITING_FOR_EVENT_TIME = 2
    WAITING_FOR_EVENT_WIKI = 3
    WAITING_FOR_EVENT_MENU = 4
    WAITING_FOR_EVENT_INFO = 5
    WAITING_FOR_EVENT_PAY = 6
    WAITING_FOR_EVENT_MEMES_RANDOMS = 7
    WAITING_FOR_EVENT_MEMES_CATEGORIES = 8

class ReminderBot:
    def __init__(self):
        self.events = dict()
        self.states = dict()
        self.init_bot()
    def init_bot(self):

        self.bot = ApplicationBuilder().token(config.Token).build()

        handler = CommandHandler("start", self.start_handler)
        self.bot.add_handler(handler)

        handler = CommandHandler("add_event", self.add_event_handler)
        self.bot.add_handler(handler)

        handler = CommandHandler("say", self.say_handler)
        self.bot.add_handler(handler)

        handler = CommandHandler("wiki", self.wiki_handler)
        self.bot.add_handler(handler)

        handler = CommandHandler("menu", self.menu_handler)
        self.bot.add_handler(handler)

        handler = CommandHandler("info", self.info_handler)
        self.bot.add_handler(handler)

        handler = CommandHandler("pay", self.pay_handler)
        self.bot.add_handler(handler)

        handler = CommandHandler("profile", self.profile_handler)
        self.bot.add_handler(handler)

        handler = CommandHandler("memes", self.memes_handler)
        self.bot.add_handler(handler)

        handler = CommandHandler("randoms", self.randoms_handler)
        self.bot.add_handler(handler)

        handler = CommandHandler("categories", self.categories_handler)
        self.bot.add_handler(handler)

        handler = MessageHandler(filters.TEXT, self.text_handler)
        self.bot.add_handler(handler)


    def run(self):
        self.bot.run_polling()


    async def start_handler(self, update, context):
        await context.bot.send_message(
            text="Привет 😎, я бот-напоминалка моя основная задача - это напоминать вам о каких либо событиях, будь то минута или года, чтобы ознакомиться с моими функциями зайдите в меню /menu",
            chat_id=update.effective_chat.id,
        )
        self.states[update.effective_chat.id] = ReminderBotState.DEFAULT
    async def menu_handler(self, update, context):
        await context.bot.send_message(
            text="👋 Приветствуем!" + "                                                                                                             "
            "/memes - выдача мемов ""                                                                                                             "
            "/add_event - ⏰ добавление напоминаний" + "                                                                              "
            "/wiki - 🌐 поиск в Википедии" + "                                                                                           "
            "/pay - 💍 200 руб на месяц и без ограничений" + "                                                  "
            "/profile - 💂 ваш профиль"+ "                                                                                                          "
            "/info - 🌌данные о боте"+ "                                                                                       "
            "/say - 🧠состояние разговора"+ "                                                                                             "

            ,
            chat_id=update.effective_chat.id,
        )
        self.states[update.effective_chat.id] = ReminderBotState.WAITING_FOR_EVENT_MENU
    async def info_handler(self, update, context):
        await context.bot.send_message(
            text="👨🏻‍🎓Данный бот умеет сохранять данные и воспроизводить их через определенное время, "
                 "также в его функционал входит умение поиска значения слов в Википедии 🔎, в дефолтном состоянии он может разговаривать 😊"
            ,
            chat_id=update.effective_chat.id,
        )
        self.states[update.effective_chat.id] = ReminderBotState.DEFAULT

    async def memes_handler(self, update, context):
        await context.bot.send_message(
            text="Выбирите желаемый продукт: " "                                                                                                "
                 "/randoms - случайный мем" "                                                                                              "
                 "/categories - мемы отсортированные по категориям"
            ,
            chat_id=update.effective_chat.id,
        )
        self.states[update.effective_chat.id] = ReminderBotState.DEFAULT

    async def randoms_handler(self, update, context):
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=randoms_memes.random_memes(),
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="/next чтобы посмотреть следующий мем",
        )
        self.states[update.effective_chat.id] = ReminderBotState.WAITING_FOR_EVENT_MEMES_RANDOMS

    async def categories_handler(self, update, context):
        await context.bot.send_message(
            text="Купи подписку братик"
            ,
            chat_id=update.effective_chat.id,
        )
        self.states[update.effective_chat.id] = ReminderBotState.DEFAULT

    async def say_handler(self, update, context):
        await context.bot.send_message(
            text="Привет 👋"
            ,
            chat_id=update.effective_chat.id,
        )
        self.states[update.effective_chat.id] = ReminderBotState.DEFAULT
    async def pay_handler(self, update, context):
        await context.bot.send_message(
            text="не трать на хуйню", chat_id=update.effective_chat.id
        )
        self.states[
            update.effective_chat.id
        ] = ReminderBotState.DEFAULT

    async def profile_handler(self, update, context):

        await context.bot.send_message(
            text="💬 Доступно запросов для напоминания:" + " " + str(count_unforgettable) + "                                                                   " +
                 "Зачем нужны напоминания?""                                                                                "
                 " Задавая вопросы - ты тратишь 1 запрос. Бесплатно можно тратить 1 запросов каждый день. "
                "Запросы восстанавливаются каждый день в 08:00 по Московскому времени."
                "Не хватает запросов бота с напоминаниями  и хочется новых мемов?""                                                                  "
                 "1️⃣ Вы можете купить премиум-подписку для нашего бота 200 рублей на месяц и не париться о лимитах.", chat_id=update.effective_chat.id
        )
        self.states[
            update.effective_chat.id
        ] = ReminderBotState.DEFAULT
    async def add_event_handler(self, update, context):
        await context.bot.send_message(
            text="Введите название события", chat_id=update.effective_chat.id
        )
        self.states[
            update.effective_chat.id
        ] = ReminderBotState.WAITING_FOR_EVENT_TEXT
    async def wiki_handler(self, update, context):
        await context.bot.send_message(
            text="Вас приветствует функция Википедии, напишите слово, значение которого хотите узнать", chat_id=update.effective_chat.id
        )
        self.states[update.effective_chat.id] = ReminderBotState.WAITING_FOR_EVENT_WIKI
    async def text_handler(self, update, context):
        global count_unforgettable
        chat_id = update.effective_chat.id
        if chat_id not in self.states:
            self.states[chat_id] = ReminderBotState.DEFAULT

        if self.states[chat_id] == ReminderBotState.DEFAULT:
            await context.bot.send_message(
                chat_id=chat_id,
                text=say.speake(update.message.text, chat_id),
            )
            self.states[chat_id] = ReminderBotState.DEFAULT
        elif self.states[chat_id] == ReminderBotState.WAITING_FOR_EVENT_WIKI:
            await context.bot.send_message(
                chat_id=chat_id,
                text=wiki.getwiki(update.message.text),
            )
            self.states[chat_id] = ReminderBotState.DEFAULT

        elif self.states[chat_id] == ReminderBotState.WAITING_FOR_EVENT_MEMES_RANDOMS:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=randoms_memes.random_memes(),
            )
            print("хой")
            await context.bot.send_message(
                chat_id=chat_id,
                text="/next чтобы посмотреть следующий мем",
            )
            self.states[chat_id] = ReminderBotState.WAITING_FOR_EVENT_MEMES_RANDOMS

        elif self.states[chat_id] == ReminderBotState.WAITING_FOR_EVENT_TEXT:
            self.events[chat_id] = Event()
            self.events[chat_id].chat_id = chat_id
            self.events[chat_id].text = update.message.text
            await context.bot.send_message(
                chat_id=chat_id,
                text="Введите дату и время события (например 01.01.2001 00:00)",
            )
            self.states[chat_id] = ReminderBotState.WAITING_FOR_EVENT_TIME
        elif self.states[chat_id] == ReminderBotState.WAITING_FOR_EVENT_TIME:
            time = datetime.strptime(
                update.message.text, "%d.%m.%Y %H:%M"
            )
            time += timedelta(hours=-3)
            self.events[chat_id].time = time
            context.job_queue.run_once(
                self.process_event_job,
                self.events[chat_id].time,
                data=self.events[chat_id],
                chat_id=chat_id,
            )

            await context.bot.send_message(
                chat_id=chat_id,
                text="Событие добавлено"
            )
            count_unforgettable -= 1
            self.states[chat_id] = ReminderBotState.DEFAULT

    async def process_event_job(self, context):
        event = context.job.data
        for i in range(3):
            await context.bot.send_message(chat_id=event.chat_id, text=event.text)


if __name__ == "__main__":
    app = ReminderBot()
    app.run()
