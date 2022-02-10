# TERE LIYE

from modules.cache.admins import admins
from modules.clientbot import call_py, bot
from pyrogram import Client, filters
from modules.design.thumbnail import thumb
from modules.clientbot.queues import QUEUE, clear_queue
from modules.helpers.filters import command, other_filters
from modules.helpers.decorators import authorized_users_only
from modules.clientbot.utils import skip_current_song, skip_item

from modules.config import IMG_5
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)


@Client.on_message(command(["/reload"]) & other_filters)
@authorized_users_only
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        "✅ **𝐀𝐝𝐦𝐢𝐧 🦈 𝐋𝐢𝐬𝐭 📃 𝐔𝐩𝐝𝐚𝐭𝐞𝐝 👍**"
    )


@Client.on_message(command(["/skip", "/vskip"]) & other_filters)
@authorized_users_only
async def skip(c: Client, m: Message):
    await m.delete()
    user_id = m.from_user.id
    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await c.send_message(chat_id, "**❌ 𝐍𝐨𝐭𝐡𝐢𝐧𝐠 😔 𝐈𝐬 𝐂𝐮𝐫𝐫𝐞𝐧𝐭𝐥𝐲 💫 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 🎸**")
        elif op == 1:
            await c.send_message(chat_id, "**❌ 𝐄𝐦𝐩𝐭𝐲 😔 𝐐𝐮𝐞𝐮𝐞 𝐋𝐞𝐚𝐯𝐢𝐧𝐠 💫 𝐕𝐨𝐢𝐜𝐞 𝐂𝐡𝐚𝐭 🥀**")
        elif op == 2:
            await c.send_message(chat_id, "**🗑️ 𝐂𝐥𝐞𝐚𝐫𝐢𝐧𝐠 😔 𝐐𝐮𝐞𝐮𝐞𝐬 𝐋𝐞𝐚𝐯𝐢𝐧𝐠 💫 𝐕𝐨𝐢𝐜𝐞 𝐂𝐡𝐚𝐭 🥀**")
        else:
            buttons = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="💛 𝐉𝐨𝐢𝐧 𝐎𝐮𝐫 𝐂𝐡𝐚𝐭 🥀",
                            url=f"https://t.me/Smoker_feelings")

                ]
            ]
        )
 
            thumbnail = f"{IMG_5}"
            title = f"{op[0]}"
            image = await thumb(thumbnail, title, user_id)
            await c.send_photo(
                chat_id,
                photo=image,
                reply_markup=buttons,
                caption=f" **➡️ 𝐒𝐤𝐢𝐩 💫 𝐓𝐡𝐞 𝐂𝐮𝐫𝐫𝐞𝐧𝐭 ✨ 𝐒𝐨𝐧𝐠 🥀» ** [{op[0]}]({op[1]})\n💭",
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "🗑 **𝐑𝐞𝐦𝐨𝐯𝐞𝐝 💦 𝐒𝐨𝐧𝐠 🎸 𝐅𝐫𝐨𝐦 𝐐𝐮𝐞𝐮𝐞 💫:**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#{x}** - {hm}"
            await m.reply(OP)


@Client.on_message(
    command(["/stop", "/end", "/vstop"])
    & other_filters
)
@authorized_users_only
async def stop(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("**❌ 𝐒𝐭𝐨𝐩 🛑 𝐒𝐭𝐫𝐞𝐚𝐦𝐢𝐧𝐠 ✨**")
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **𝐍𝐨𝐭𝐡𝐢𝐧𝐠 😔 𝐈𝐬 💫 𝐒𝐭𝐫𝐞𝐚𝐦𝐢𝐧𝐠**")


@Client.on_message(
    command(["/pause", "/vpause"]) & other_filters
)
@authorized_users_only
async def pause(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                "⏸ ** 𝐏𝐚𝐮𝐬𝐞 😔🥀**"
            )
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **𝐍𝐨𝐭𝐡𝐢𝐧𝐠 😔 𝐈𝐬 💫 𝐒𝐭𝐫𝐞𝐚𝐦𝐢𝐧𝐠 😈**")


@Client.on_message(
    command(["/resume", "/vresume"]) & other_filters
)
@authorized_users_only
async def resume(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(
                "▶️ **𝐑𝐞𝐬𝐮𝐦𝐞 ❤️ 🤟**"
            )
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **𝐍𝐨𝐭𝐡𝐢𝐧𝐠 😔 𝐈𝐬 💫 𝐒𝐭𝐫𝐞𝐚𝐦𝐢𝐧𝐠**")
