from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, Text, KeyboardButtonColor
from vkbottle import BaseStateGroup

from config import *

bot=Bot(token=bot_token)
bot.labeler.vbml_ignore_case=True

class MyStates(BaseStateGroup):
    NONE = 0

list_start_bot=["начать", "привет", "старт", "start", "hello", "hi"]


@bot.on.message(text=list_start_bot)
async def start_bot_handler(message: Message):
    key=Keyboard()

    key.add(Text("Цены", payload={"menu": "price"}), color=KeyboardButtonColor.POSITIVE)
    key.add(Text("Рассылки", payload={"menu": "mailing"}))
    key.row()
    key.add(Text("Развлечения", payload={"menu": "fun"}), color=KeyboardButtonColor.PRIMARY)
    key.row()
    key.add(Text("Выход", payload={"menu": "exit"}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer(
        message="""Здравствуйте!&#128521; Меня зовут BotТройки. Я могу подсказать вам цены или развлечь

&#10071;Я вас подписал на рассылку. Буду отправлять вам действующие акции, нововведения или важные новости по поводу нашей работы

Если хотите отказаться от неё, просто в меню "Рассылки" выберите "Отказаться от рассылки" или введите команду "/mailoff", я не обижусь)))

Я ещё совсем молодой&#128118;, поэтому некоторые слова я могу не понять, старайтесь пользоваться кнопками. Но я обещаю, что буду учиться расспозновать как можно больше ваших сообщений. Спасибо за понимание
        """,
        keyboard=key
        )

@bot.on.message(payload={"menu": "price"})
async def main_menu_handler(message: Message):
    await message.answer("Price")

@bot.on.message(payload={"menu": "mailing"})
async def main_menu_handler(message: Message):
    await message.answer("Mailing")

@bot.on.message(payload={"menu": "fun"})
async def main_menu_handler(message: Message):
    await message.answer("Fun")

@bot.on.message(payload={"menu": "exit"})
async def main_menu_handler(message: Message):
    await message.answer("Exit")

if __name__ == "__main__":
    bot.run_forever()