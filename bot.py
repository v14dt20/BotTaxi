import asyncio
import psycopg2
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, Text, KeyboardButtonColor, VKAPIError, EMPTY_KEYBOARD, OpenLink
from vkbottle import GroupEventType, GroupTypes
from vkbottle import BaseStateGroup
from config import *

from random import randint

bot=Bot(token=bot_token)
bot.labeler.vbml_ignore_case=True

connection = psycopg2.connect(DB_URI)
cursor = connection.cursor()

class MyStates(BaseStateGroup):
    NONE = 0
    ANS = 1

cursor.execute("SELECT * FROM users")
dict_id_users_for_mailing = cursor.fetchall()
print(dict_id_users_for_mailing)
list_start_bot=["начать", "привет", "старт", "start", "hello", "hi", "здравствуйте", "start"]

@bot.labeler.raw_event(GroupEventType.GROUP_JOIN, dataclass=GroupTypes.GroupJoin)
async def join_handler(event: GroupTypes.GroupJoin):
    try:
        await bot.api.messages.send(user_id = event.object.user_id, message="Спасибо за подписку))))", attachment="video-209400635_456239053", random_id=0)
    except VKAPIError[30]:
        pass

@bot.labeler.raw_event(GroupEventType.GROUP_LEAVE, dataclass=GroupTypes.GroupLeave)
async def leave_handler(event: GroupTypes.GroupLeave):
    try:
        await bot.api.messages.send(user_id = event.object.user_id, message="Очень жаль, что вы от нас ушли. Но это ваш выбор, я не могу ничего сделать(((", attachment="video-209400635_456239051", random_id=0)
    except VKAPIError[30]:
        pass

@bot.labeler.raw_event(GroupEventType.MESSAGE_NEW, dataclass=GroupTypes.MessageNew)
async def new_message_handler(event: GroupTypes.MessageNew):
    id = event.object.message.from_id
    cursor.execute(f"SELECT id FROM users WHERE id = {id}")
    result = cursor.fetchone()

    if not result:
        cursor.execute("INSERT INTO users(id, status) VALUES (%s, %s)", (id, 1))
        connection.commit()
        cursor.execute("SELECT * FROM users")
        dict_id_users_for_mailing = cursor.fetchall()
        await bot.api.messages.send(
            user_id=id, 
            message="""&#10071;Я вас подписал на рассылку. Буду отправлять вам действующие акции, нововведения или важные новости по поводу нашей работы
Если хотите отказаться от неё, просто в меню "Рассылки" выберите "Отказаться от рассылки" или введите команду "/mailoff", я не обижусь))) Подписаться на рассылку можно также через меню "Рассылка" """, 
            random_id=0
            )

#========================================================================================================
# Menu
#========================================================================================================
@bot.on.message(text=list_start_bot)
async def start_bot_handler(message: Message):
    key=Keyboard()

    key.add(Text("Цены", payload={"menu": "price"}), color=KeyboardButtonColor.POSITIVE)
    key.add(Text("Рассылки", payload={"menu": "mailing"}))
    key.row()
    key.add(Text("Развлечения", payload={"menu": "fun"}), color=KeyboardButtonColor.PRIMARY)
    key.row()
    if message.from_id == 403603979:
        key.add(Text("Создать рассылку", {"menu": "admin_mail"}), color=KeyboardButtonColor.PRIMARY)
        key.add(Text("Список", {"menu": "admin_check"}))
        key.row()

    key.add(OpenLink("https://play.google.com/store/apps/details?id=ru.taximaster.tmtaxicaller.id1583", "Наше приложение"))
    key.add(Text("Выход", payload={"menu": "exit"}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer(
        message="""Здравствуйте!&#128521; Меня зовут BotТройки. Я могу подсказать вам цены или развлечь

Я ещё совсем молодой&#128118;, поэтому некоторые слова я могу не понять, старайтесь пользоваться кнопками. Но я обещаю, что буду учиться расспозновать как можно больше ваших сообщений. Спасибо за понимание

У нас есть собственное мобильное приложение для заказа такси: https://play.google.com/store/apps/details?id=ru.taximaster.tmtaxicaller.id1583. К сожалению пока доступно только в GooglePlay, но мы работаем над тем, чтобы и AppStore его принял) 

Если вы нашли какую-то ошибку или хотите что-то добавить в меня, то введите команду "/ansdev", мой создатель рассмотрит ваш вопрос и попытается его решить
        """,
        keyboard=key
        )

@bot.on.message(payload={"menu": "main"})
async def main_menu_handler(message: Message):
    key=Keyboard()

    key.add(Text("Цены", {"menu": "price"}), color=KeyboardButtonColor.POSITIVE)
    key.add(Text("Рассылки", {"menu": "mailing"}))
    key.row()
    key.add(Text("Развлечения", {"menu": "fun"}), color=KeyboardButtonColor.PRIMARY)
    key.row()
    if message.from_id == 403603979:
        key.add(Text("Создать рассылку", {"menu": "admin_mail"}), color=KeyboardButtonColor.PRIMARY)
        key.add(Text("Список", {"menu": "admin_check"}))
        key.row()
    key.add(OpenLink("https://play.google.com/store/apps/details?id=ru.taximaster.tmtaxicaller.id1583", "Наше приложение"))
    key.add(Text("Выход", payload={"menu": "exit"}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer("Основные команды, которые я знаю", keyboard=key)

@bot.on.message(payload={"menu": "price"})
@bot.on.message(text="цены")
async def main_menu_handler(message: Message):
    key = Keyboard()

    key.add(Text("Заказ через диспетчера", {"price": "operator"}))
    key.add(Text("Заказ через приложение", {"price": "app"}))
    key.row()
    key.add(Text("Выход", payload={"menu": "exit"}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer("Как вы хотите сделать заказ?", keyboard=key)

@bot.on.message(payload={"menu": "mailing"})
async def main_menu_handler(message: Message):
    key = Keyboard()

    key.add(Text("Подписаться на рассылку", {"mailing": "subscribe"}), color=KeyboardButtonColor.POSITIVE)
    key.add(Text("Отписаться от рассылки", {"mailing": "off"}), color=KeyboardButtonColor.NEGATIVE)
    key.row()
    key.add(Text("Назад", {"menu": "main"}), color=KeyboardButtonColor.NEGATIVE)
    await message.answer("Выберите режим", keyboard=key)

@bot.on.message(payload={"menu": "fun"})
async def main_menu_handler(message: Message):
    key = Keyboard()

    key.add(Text("Анекдот", {"fun": "joke"}))
    key.add(Text("Видео", {"fun": "video"}))
    key.row()
    key.add(Text("Назад", {"menu": "main"}), color=KeyboardButtonColor.NEGATIVE)
    await message.answer("Я могу рассказать вам анекдот или показать смешное видео", keyboard=key)

@bot.on.message(payload={"menu": "exit"})
async def main_menu_handler(message: Message):
    key = Keyboard()

    key.add(Text("Начать"), color=KeyboardButtonColor.PRIMARY)
    await message.answer("До свидания, рад был вам помочь, заходите ещё)", keyboard=key)

#========================================================================================================
# Mailing for admin and users
#========================================================================================================
@bot.on.message(payload={"menu": "admin_mail"})
async def mail_handler(message: Message):
    await bot.state_dispenser.set(message.peer_id, MyStates.NONE)
    return "Введите сообщение для рассылки"

@bot.on.message(state=MyStates.NONE)
async def get_mail_handler(message: Message):
    cursor.execute("SELECT * FROM users")
    dict_id_users_for_mailing = cursor.fetchall()
    for id_user in dict_id_users_for_mailing:
        if id_user[1] == 1:
            await bot.api.messages.send(
                peer_id=id_user[0],
                message=f"{message.text}\n\nЕсли не хотите получать рассылки, то отключите их в меню либо пропишите команду \"/mailoff\"",
                random_id=0
            )
    await bot.state_dispenser.delete(message.peer_id)

@bot.on.message(payload={"menu": "admin_check"})
async def check_mail_handler(message: Message):
    list_users_mail = []
    cursor.execute(f"SELECT * FROM users")
    dict_id_users_for_mailing = cursor.fetchall()
    for user in dict_id_users_for_mailing:
        arr = await bot.api.users.get(user[0])
        if user[1] == 1:
            list_users_mail.append(f"{arr[0].first_name} {arr[0].last_name} @id{user[0]} - подписан")
        elif user[1] == 0:
            list_users_mail.append(f"{arr[0].first_name} {arr[0].last_name} @id{user[0]} - не подписан")
    await message.answer('\n'.join(list_users_mail))

@bot.on.message(payload={"mailing": "subscribe"})
async def mail_subscribe_handler(message: Message):
    cursor.execute("SELECT * FROM users")
    dict_id_users_for_mailing = cursor.fetchall()
    for user in dict_id_users_for_mailing:
        if user[0] == message.from_id and user[1] == 1:
            await message.answer("Вы и так подписаны на рассылку")
        elif user[0] == message.from_id and user[1] == 0:
            cursor.execute(f"UPDATE users SET status = {1} WHERE id = {message.from_id}")
            connection.commit()
            await message.answer("Спасибо, я подписал вас на рассылку")
    

@bot.on.message(payload={"mailing": "off"})
@bot.on.message(command="mailoff")
async def mail_off_handler(message: Message):
    cursor.execute("SELECT * FROM users")
    dict_id_users_for_mailing = cursor.fetchall()
    for user in dict_id_users_for_mailing:
        if user[0] == message.from_id and user[1] == 0:
            await message.answer("Вы и так не подписаны на рассылку")
        elif user[0] == message.from_id and user[1] == 1:
            cursor.execute(f"UPDATE users SET status = {0} WHERE id = {message.from_id}")
            connection.commit()
            await message.answer("Я отписал вас от рассылки")


#========================================================================================================
# Fun
#========================================================================================================

@bot.on.message(payload={"fun": "joke"})
async def fun_joke_handler(message: Message):
    key = Keyboard()

    key.add(Text("Ещё", payload={"fun": "joke"}), color=KeyboardButtonColor.PRIMARY)
    key.add(Text("Выход", payload={"menu": "main"}), color=KeyboardButtonColor.NEGATIVE)

    with open("joke.txt", "r", encoding="utf-8") as file:
        jokes_list = file.readlines()

    await message.answer(jokes_list[randint(0, len(jokes_list)-1)], keyboard=key)

@bot.on.message(payload={"fun": "video"})
async def fun_video_handler(message: Message):
    key = Keyboard()

    key.add(Text("Ещё", payload={"fun": "video"}), color=KeyboardButtonColor.PRIMARY)
    key.add(Text("Выход", payload={"menu": "main"}), color=KeyboardButtonColor.NEGATIVE)

    with open("video.txt", "r", encoding="utf-8") as file:
        video_list = file.readlines()

    await message.answer(attachment=video_list[randint(0, len(video_list)-1)], keyboard=key)

#========================================================================================================
# Answer for dev
#========================================================================================================

@bot.on.message(command="ansdev")
async def answer_dev_handler(message: Message):
    await bot.state_dispenser.set(message.peer_id, MyStates.ANS)
    await message.answer("Введите свой вопрос/предложение. Я его передам папе :)")

@bot.on.message(state=MyStates.ANS)
async def ans(message: Message):
    await bot.api.messages.send(user_id=403603979, message=f"\"{message.text}\" от @id{message.from_id}", random_id=0)
    await bot.state_dispenser.delete(message.peer_id)
    await message.answer ("Спасибо за обращение! Так я стану лучше")

#========================================================================================================
# Price
#========================================================================================================

@bot.on.message(payload={"price": "operator"})
async def price_operator_handler(message: Message):
    with open("price.txt", "r", encoding="utf-8") as file:
        price = file.readlines()
    
    await message.answer(''.join(price))

@bot.on.message(payload={"price": "app"})
async def price_app_handler(message: Message):
    await message.answer(
        """
        В черте г.Верещагино - от 100 рублей (входит - 3 км. пути, 5 мин. ожидания)
Далее
По городу - 15 руб./км.
За город - 20 руб./км.
Ожидание - 5 руб./мин.
        """
    )

bot.run_forever()