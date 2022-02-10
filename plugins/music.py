# AdityaHalder

from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio
from modules.design.thumbnail import thumb
from modules.helpers.filters import command, other_filters
from modules.clientbot.queues import QUEUE, add_to_queue
from modules.clientbot import call_py, user
from modules.clientbot.utils import bash
from modules.config import IMG_5
from youtubesearchpython import VideosSearch


def ytsearch(query: str):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link: str):
    stdout, stderr = await bash(
        f'yt-dlp -g -f "best[height<=?720][width<=?1280]" {link}'
    )
    if stdout:
        return 1, stdout
    return 0, stderr


@Client.on_message(command(["/play"]) & other_filters)
async def play(c: Client, m: Message):
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    user_id = m.from_user.id
    if m.sender_chat:
        return await m.reply_text(
            "you're an __Anonymous__ user !\n\n» revert back to your real user account to use this bot."
        )
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 To use me, I need to be an **Administrator** with the following **permissions**:\n\n» ❌ __Delete messages__\n» ❌ __Invite users__\n» ❌ __Manage video chat__\n\nOnce done, type /reload"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "💡 To use me, Give me the following permission below:"
            + "\n\n» ❌ __Manage video chat__\n\nOnce done, try again."
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "💡 To use me, Give me the following permission below:"
            + "\n\n» ❌ __Delete messages__\n\nOnce done, try again."
        )
        return
    if not a.can_invite_users:
        await m.reply_text(
            "💡 To use me, Give me the following permission below:"
            + "\n\n» ❌ __Add users__\n\nOnce done, try again."
        )
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot)
        if b.status == "kicked":
            await c.unban_chat_member(chat_id, ubot)
            invitelink = await c.export_chat_invite_link(chat_id)
            if invitelink.startswith("https://t.me/+"):
                invitelink = invitelink.replace(
                    "https://t.me/+", "https://t.me/joinchat/"
                )
            await user.join_chat(invitelink)
    except UserNotParticipant:
        try:
            invitelink = await c.export_chat_invite_link(chat_id)
            if invitelink.startswith("https://t.me/+"):
                invitelink = invitelink.replace(
                    "https://t.me/+", "https://t.me/joinchat/"
                )
            await user.join_chat(invitelink)
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            return await m.reply_text(
                f"❌ **userbot failed to join**\n\n**reason**: `{e}`"
            )
    if replied:
        if replied.audio or replied.voice:
            suhu = await replied.reply("📥 **Ɗøωŋɭøɑɗɩŋʛ ...**")
            dl = await replied.download()
            link = replied.link
            
            try:
                if replied.audio:
                    songname = replied.audio.title[:70]
                    songname = replied.audio.file_name[:70]
                    duration = replied.audio.duration
                elif replied.voice:
                    songname = "Voice Note"
                    duration = replied.voice.duration
            except BaseException:
                songname = "Audio"
            
            if chat_id in QUEUE:
                title = songname
                userid = m.from_user.id
                thumbnail = f"{IMG_5}"
                image = await thumb(thumbnail, title, userid)
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                            text="𝐂𝐡𝐚𝐧𝐧𝐞𝐥📡",
                            url=f"https://t.me/eSport_BOTs")
               ],
               [
                    InlineKeyboardButton(
                            text="𝐒𝐦𝐨𝐊𝐞𝐫 🚬",
                            url=f"https://t.me/Sanki_Owner"),
                            
                    InlineKeyboardButton(
                            text="𝐅𝐞𝐞𝐋𝐢𝐧𝐠'𝐒 🥀",
                            url=f"https://t.me/Smoker_Feelings")
               ],
               [
                        InlineKeyboardButton(
                            text="𝐆𝐫𝐨𝐮𝐩⭐",
                            url=f"https://t.me/EsportClan")
                   
                ]
            ]
        )
                await suhu.delete()
                await m.reply_photo(
                    photo=image,
                    reply_markup=buttons,
                    caption=f"**❰ 𝐒𝐦𝐨𝐤𝐞𝐫 🚬 -|- 𝐌𝐮𝐬𝐢𝐜'𝐗 🎸 ❱ 𝐒𝐨𝐧𝐠 ❤️ 𝐏𝐨𝐬𝐢𝐭𝐢𝐨𝐧 💫🤟 `{pos}`**",
                )
            else:
                try:
                    title = songname
                    userid = m.from_user.id
                    thumbnail = f"{IMG_5}"
                    image = await thumb(thumbnail, title, userid)
                    await suhu.edit("🎵 𝐌𝐮𝐬𝐢𝐜 🔊 𝐑𝐞𝐚𝐝𝐲 𝐅𝐨𝐫 𝐟𝐮𝐜𝐤 👅 𝐕𝐨𝐢𝐜𝐞 𝐂𝐡𝐚𝐭 🥀")
                    await call_py.join_group_call(
                        chat_id,
                        AudioPiped(
                            dl,
                            HighQualityAudio(),
                        ),
                        stream_type=StreamType().local_stream,
                    )
                    add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                    await suhu.delete()
                    buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                            text="𝐂𝐡𝐚𝐧𝐧𝐞𝐥📡",
                            url=f"https://t.me/eSport_BOTs")
               ],
               [
                    InlineKeyboardButton(
                            text="𝐒𝐦𝐨𝐊𝐞𝐫 🚬",
                            url=f"https://t.me/Sanki_Owner"),
                            
                    InlineKeyboardButton(
                            text="𝐅𝐞𝐞𝐋𝐢𝐧𝐠'𝐒 🥀",
                            url=f"https://t.me/Smoker_Feelings")
               ],
               [
                        InlineKeyboardButton(
                            text="𝐆𝐫𝐨𝐮𝐩⭐",
                            url=f"https://t.me/EsportClan")
                   
                ]
            ]
        )
                    requester = (
                        f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    )
                    await m.reply_photo(
                        photo=image,
                        reply_markup=buttons,
                        caption=f"**❰ 𝐒𝐦𝐨𝐤𝐞𝐫 🚬 -|- 𝐌𝐮𝐬𝐢𝐜'𝐗 🎸 ❱ Now 😄 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 📀 𝐀𝐭 🤟 `{m.chat.title}`...**",
                    )
                except Exception as e:
                    await suhu.delete()
                    await m.reply_text(f"🚫 error:\n\n» {e}")
        else:
            if len(m.command) < 2:
                await m.reply(
                    "**✌𝐖𝐡𝐚𝐭'𝐒 𝐓𝐡𝐞 ❤️ 𝐒𝐨𝐧𝐠 🎸 𝐘𝐨𝐮 🎧 𝐖𝐚𝐧𝐭 𝐓𝐨 𝐏𝐥𝐚𝐲 ▶ ❤️**"
                )
            else:
                suhu = await c.send_message(chat_id, "🔎 **𝐅𝐢𝐧𝐝𝐢𝐧𝐠 💫 𝐓𝐡𝐞 𝐒𝐨𝐧𝐠 ❤️ ❰ 𝐒𝐦𝐨𝐤𝐞𝐫 🚬 -|- 𝐌𝐮𝐬𝐢𝐜'𝐗 🎸 ❱**")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                if search == 0:
                    await suhu.edit("**🎵 𝐌𝐮𝐬𝐢𝐜 🔊 𝐑𝐞𝐚𝐝𝐲 𝐅𝐨𝐫 𝐟𝐮𝐜𝐤 👅 𝐕𝐨𝐢𝐜𝐞 𝐂𝐡𝐚𝐭 🥀**")
                else:
                    songname = search[0]
                    title = search[0]
                    url = search[1]
                    duration = search[2]
                    thumbnail = search[3]
                    userid = m.from_user.id
                    image = await thumb(thumbnail, title, userid)
                    aditya, ytlink = await ytdl(url)
                    if aditya == 0:
                        await suhu.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Audio", 0
                            )
                            await suhu.delete()
                            buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                            text="𝐂𝐡𝐚𝐧𝐧𝐞𝐥📡",
                            url=f"https://t.me/eSport_BOTs")
               ],
               [
                    InlineKeyboardButton(
                            text="𝐒𝐦𝐨𝐊𝐞𝐫 🚬",
                            url=f"https://t.me/Sanki_Owner"),
                            
                    InlineKeyboardButton(
                            text="𝐅𝐞𝐞𝐋𝐢𝐧𝐠'𝐒 🥀",
                            url=f"https://t.me/Smoker_Feelings")
               ],
               [
                        InlineKeyboardButton(
                            text="𝐆𝐫𝐨𝐮𝐩⭐",
                            url=f"https://t.me/EsportClan")
                   
                ]
            ]
        )
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=image,
                                reply_markup=buttons,
                                caption=f"**❰ 𝐒𝐦𝐨𝐤𝐞𝐫 🚬 -|- 𝐌𝐮𝐬𝐢𝐜'𝐗 🎸 ❱ 𝐒𝐨𝐧𝐠 ❤️ 𝐏𝐨𝐬𝐢𝐭𝐢𝐨𝐧 💫🤟 `{pos}`**",
                            )
                        else:
                            try:
                                await suhu.edit("🎵 𝐌𝐮𝐬𝐢𝐜 🔊 𝐑𝐞𝐚𝐝𝐲 𝐅𝐨𝐫 𝐟𝐮𝐜𝐤 👅 𝐕𝐨𝐢𝐜𝐞 𝐂𝐡𝐚𝐭 🥀")
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioPiped(
                                        ytlink,
                                        HighQualityAudio(),
                                    ),
                                    stream_type=StreamType().local_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                                await suhu.delete()
                                buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                            text="𝐂𝐡𝐚𝐧𝐧𝐞𝐥📡",
                            url=f"https://t.me/eSport_BOTs")
               ],
               [
                    InlineKeyboardButton(
                            text="𝐒𝐦𝐨𝐊𝐞𝐫 🚬",
                            url=f"https://t.me/Sanki_Owner"),
                            
                    InlineKeyboardButton(
                            text="𝐅𝐞𝐞𝐋𝐢𝐧𝐠'𝐒 🥀",
                            url=f"https://t.me/Smoker_Feelings")
               ],
               [
                        InlineKeyboardButton(
                            text="𝐆𝐫𝐨𝐮𝐩⭐",
                            url=f"https://t.me/EsportClan")
                   
                ]
            ]
        )
                                requester = (
                                    f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                )
                                await m.reply_photo(
                                    photo=image,
                                    reply_markup=buttons,
                                    caption=f"**❰ 𝐒𝐦𝐨𝐤𝐞𝐫 🚬 -|- 𝐌𝐮𝐬𝐢𝐜'𝐗 🎸 ❱ Now 😄 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 📀 𝐀𝐭 🤟 `{m.chat.title}`...**",
                                )
                            except Exception as ep:
                                await suhu.delete()
                                await m.reply_text(f"🚫 error: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply(
                "**🤖 𝐖𝐡𝐚𝐭'𝐒 𝐓𝐡𝐞 ❤️ 𝐒𝐨𝐧𝐠 🎸 𝐘𝐨𝐮 🎧 𝐖𝐚𝐧𝐭 𝐓𝐨 𝐏𝐥𝐚𝐲 ▶ ❤️**"
            )
        else:
            suhu = await c.send_message(chat_id, "🔎 **𝐅𝐢𝐧𝐝𝐢𝐧𝐠 💫 𝐓𝐡𝐞 𝐒𝐨𝐧𝐠 ❤️ ❰ 𝐒𝐦𝐨𝐤𝐞𝐫 🚬 -|- 𝐌𝐮𝐬𝐢𝐜'𝐗 🎸 ❱**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await suhu.edit("❌ **𝐒𝐨𝐧𝐠 🎸 𝐍𝐨𝐭 🙄 𝐅𝐨𝐮𝐧𝐝 😔**")
            else:
                songname = search[0]
                title = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                userid = m.from_user.id
                image = await thumb(thumbnail, title, userid)
                aditya, ytlink = await ytdl(url)
                if aditya == 0:
                    await suhu.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await suhu.delete()
                        requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                            text="𝐂𝐡𝐚𝐧𝐧𝐞𝐥📡",
                            url=f"https://t.me/eSport_BOTs")
               ],
               [
                    InlineKeyboardButton(
                            text="𝐒𝐦𝐨𝐊𝐞𝐫 🚬",
                            url=f"https://t.me/Sanki_Owner"),
                            
                    InlineKeyboardButton(
                            text="𝐅𝐞𝐞𝐋𝐢𝐧𝐠'𝐒 🥀",
                            url=f"https://t.me/Smoker_Feelings")
               ],
               [
                        InlineKeyboardButton(
                            text="𝐆𝐫𝐨𝐮𝐩⭐",
                            url=f"https://t.me/EsportClan")
                   
                ]
            ]
        )
                        await m.reply_photo(
                            photo=image,
                            reply_markup=buttons,
                            caption=f"**❰ 𝐒𝐦𝐨𝐤𝐞𝐫 🚬 -|- 𝐌𝐮𝐬𝐢𝐜'𝐗 🎸 ❱ 𝐒𝐨𝐧𝐠 ❤️ 𝐏𝐨𝐬𝐢𝐭𝐢𝐨𝐧 💫🤟 `{pos}`**",
                        )
                    else:
                        try:
                            await suhu.edit("🎵 𝐌𝐮𝐬𝐢𝐜 🔊 𝐑𝐞𝐚𝐝𝐲 𝐅𝐨𝐫 𝐟𝐮𝐜𝐤 👅 𝐕𝐨𝐢𝐜𝐞 𝐂𝐡𝐚𝐭 🥀")
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                    HighQualityAudio(),
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                            text="𝐂𝐡𝐚𝐧𝐧𝐞𝐥📡",
                            url=f"https://t.me/eSport_BOTs")
               ],
               [
                    InlineKeyboardButton(
                            text="𝐒𝐦𝐨𝐊𝐞𝐫 🚬",
                            url=f"https://t.me/Sanki_Owner"),
                            
                    InlineKeyboardButton(
                            text="𝐅𝐞𝐞𝐋𝐢𝐧𝐠'𝐒 🥀",
                            url=f"https://t.me/Smoker_Feelings")
               ],
               [
                        InlineKeyboardButton(
                            text="𝐆𝐫𝐨𝐮𝐩⭐",
                            url=f"https://t.me/EsportClan")
                   
                ]
            ]
        )
                            await m.reply_photo(
                                photo=image,
                                reply_markup=buttons,
                                caption=f"**❰ 𝐒𝐦𝐨𝐤𝐞𝐫 🚬 -|- 𝐌𝐮𝐬𝐢𝐜'𝐗 🎸 ❱ Now 😄 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 📀 𝐀𝐭 🤟 `{m.chat.title}`...**",
                            )
                        except Exception as ep:
                            await suhu.delete()
                            await m.reply_text(f"🚫 error: `{ep}`")
                            
