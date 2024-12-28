from aiogram import Router,F,types


group_router = Router()

group_router.message.filter(F.chat.type != 'private')

bad_words = ('дурак','дибил','отсталый','чмо','быдло')

@group_router.message(F.text)
async def check_bad_words(message:types.Message):
    author = message.from_user.id
    for word in bad_words:
        if word in message.text:
            await message.bot.ban_chat_member(chat_id=message.chat.id,user_id=author)

