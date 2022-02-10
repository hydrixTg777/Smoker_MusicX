# Aditya Halder

import re
import asyncio

from modules.config import IMG_1, IMG_2, IMG_5
from modules.design.thumbnail import thumb
from modules.helpers.filters import command, other_filters
from modules.clientbot.queues import QUEUE, add_to_queue
from modules.clientbot import call_py, user
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
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


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@Client.on_message(command(["/vplay"]) & other_filters)
async def vplay(c: Client, m: Message):
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
        if replied.video or replied.document:
            loser = await replied.reply("📥 **Ɗøωŋɭøɑɗɩŋʛ ...**")
            dl = await replied.download()
            link = replied.link
            if len(m.command) < 2:
                Q = 720
            else:
                pq = m.text.split(None, 1)[1]
                if pq == "720" or "480" or "360":
                    Q = int(pq)
                else:
                    Q = 720
                    await loser.edit(
                        "» __only 720, 480, 360 allowed__ \n💡 **now streaming video in 720p**"
                    )
            try:
                if replied.video:
                    songname = replied.video.file_name[:70]
                    duration = replied.video.duration
                elif replied.document:
                    songname = replied.document.file_name[:70]
                    duration = replied.document.duration
            except BaseException:
                songname = "Video"

            if chat_id in QUEUE:
                title = songname
                userid = m.from_user.id
                thumbnail = f"{IMG_5}"
                image = await thumb(thumbnail, title, userid)
                pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
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
                title = songname
                userid = m.from_user.id
                thumbnail = f"{IMG_5}"
                image = await thumb(thumbnail, title, userid)
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                await loser.edit(" **𝐌𝐮𝐬𝐢𝐜 🔊 𝐑𝐞𝐚𝐝𝐲 𝐅𝐨𝐫 𝐟𝐮𝐜𝐤 👅 𝐕𝐨𝐢𝐜𝐞 𝐂𝐡𝐚𝐭 🥀**")
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(
                        dl,
                        HighQualityAudio(),
                        amaze,
                    ),
                    stream_type=StreamType().local_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
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
        else:
            if len(m.command) < 2:
                await m.reply(
                    "**🤖 𝐖𝐡𝐚𝐭'𝐒 𝐓𝐡𝐞 ❤️ 𝐒𝐨𝐧𝐠 🎸 𝐘𝐨𝐮 🎧 𝐖𝐚𝐧𝐭 𝐓𝐨 𝐏𝐥𝐚𝐲 ▶ ❤️**"
                )
            else:
                loser = await c.send_message(chat_id, " **🔎 𝐅𝐢𝐧𝐝𝐢𝐧𝐠 💫 𝐓𝐡𝐞 𝐒𝐨𝐧𝐠 ❤️ ❰ 𝐒𝐦𝐨𝐤𝐞𝐫 🚬 -|- 𝐌𝐮𝐬𝐢𝐜'𝐗 🎸 ❱**")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                Q = 720
                amaze = HighQualityVideo()
                if search == 0:
                    await loser.edit("❌ **𝐒𝐨𝐧𝐠 🎸 𝐍𝐨𝐭 🙄 𝐅𝐨𝐮𝐧𝐝 😔**")
                else:
                    songname = search[0]
                    title = search[0]
                    url = search[1]
                    duration = search[2]
                    thumbnail = search[3]
                    userid = m.from_user.id
                    image = await thumb(thumbnail, title, userid)
                    veez, ytlink = await ytdl(url)
                    if veez == 0:
                        await loser.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Video", Q
                            )
                            await loser.delete()
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
                                await loser.edit(" **𝐌𝐮𝐬𝐢𝐜 🔊 𝐑𝐞𝐚𝐝𝐲 𝐅𝐨𝐫 𝐟𝐮𝐜𝐤 👅 𝐕𝐨𝐢𝐜𝐞 𝐂𝐡𝐚𝐭 🥀**")
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioVideoPiped(
                                        ytlink,
                                        HighQualityAudio(),
                                        amaze,
                                    ),
                                    stream_type=StreamType().local_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                                await loser.delete()
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
                                    caption=f"**❰ 𝐌𝐮𝐬𝐢𝐜'𝐗 ❘ 𝐞𝐒𝐩𝐨𝐫𝐭 😈 ❱ Now 😄 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 📀 𝐀𝐭 🤟 `{m.chat.title}`...**",
                                )
                            except Exception as ep:
                                await loser.delete()
                                await m.reply_text(f"🚫 error: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply(
                "» reply to an **video file** or **give something to search.**"
            )
        else:
            loser = await c.send_message(chat_id, " **🔎 𝐅𝐢𝐧𝐝𝐢𝐧𝐠 💫 𝐓𝐡𝐞 𝐒𝐨𝐧𝐠 ❤️ ❰ 𝐒𝐦𝐨𝐤𝐞𝐫 🚬 -|- 𝐌𝐮𝐬𝐢𝐜'𝐗 🎸 ❱**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            amaze = HighQualityVideo()
            if search == 0:
                await loser.edit("❌ **𝐒𝐨𝐧𝐠 🎸 𝐍𝐨𝐭 🙄 𝐅𝐨𝐮𝐧𝐝 😔**")
            else:
                songname = search[0]
                title = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                userid = m.from_user.id
                image = await thumb(thumbnail, title, userid)
                veez, ytlink = await ytdl(url)
                if veez == 0:
                    await loser.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await loser.delete()
                        requester = (
                            f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        )
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
                            await loser.edit(" **𝐌𝐮𝐬𝐢𝐜 🔊 𝐑𝐞𝐚𝐝𝐲 𝐅𝐨𝐫 𝐟𝐮𝐜𝐤 👅 𝐕𝐨𝐢𝐜𝐞 𝐂𝐡𝐚𝐭 🥀**")
                            await call_py.join_group_call(
                                chat_id,
                                AudioVideoPiped(
                                    ytlink,
                                    HighQualityAudio(),
                                    amaze,
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await loser.delete()
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
                            await loser.delete()
                            await m.reply_text(f"🚫 error: `{ep}`")


@Client.on_message(command(["/vstream"]) & other_filters)
async def vstream(c: Client, m: Message):
    await m.delete()
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

    if len(m.command) < 2:
        await m.reply("» give me a live-link/m3u8 url/youtube link to stream.")
    else:
        if len(m.command) == 2:
            link = m.text.split(None, 1)[1]
            Q = 720
            loser = await c.send_message(chat_id, "🔄 **processing stream...**")
        elif len(m.command) == 3:
            op = m.text.split(None, 1)[1]
            link = op.split(None, 1)[0]
            quality = op.split(None, 1)[1]
            if quality == "720" or "480" or "360":
                Q = int(quality)
            else:
                Q = 720
                await m.reply(
                    "» __only 720, 480, 360 allowed__ \n💡 **now streaming video in 720p**"
                )
            loser = await c.send_message(chat_id, "🔄 **𝐏𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠 💫 𝐒𝐭𝐫𝐞𝐚𝐦 ❤️**")
        else:
            await m.reply("**/vstream {link} {720/480/360}**")

        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, link)
        if match:
            veez, livelink = await ytdl(link)
        else:
            livelink = link
            veez = 1

        if veez == 0:
            await loser.edit(f"❌ yt-dl issues detected\n\n» `{livelink}`")
        else:
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                await loser.delete()
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
                    photo=f"{IMG_1}",
                    reply_markup=buttons,
                    caption=f"**❰ 𝐒𝐦𝐨𝐤𝐞𝐫 🚬 -|- 𝐌𝐮𝐬𝐢𝐜'𝐗 🎸 ❱ 𝐒𝐨𝐧𝐠 ❤️ 𝐏𝐨𝐬𝐢𝐭𝐢𝐨𝐧 💫🤟 `{pos}`**",
                )
            else:
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                try:
                    await loser.edit("🔄 **𝐉𝐨𝐢𝐧𝐢𝐧𝐠 ✨ 𝐕𝐨𝐢𝐜𝐞 𝐂𝐡𝐚𝐭 😎**")
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(
                            livelink,
                            HighQualityAudio(),
                            amaze,
                        ),
                        stream_type=StreamType().live_stream,
                    )
                    add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                    await loser.delete()
                    requester = (
                        f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    )
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
                        photo=f"{IMG_2}",
                        reply_markup=buttons,
                        caption=f"**❰ 𝐒𝐦𝐨𝐤𝐞𝐫 🚬 -|- 𝐌𝐮𝐬𝐢𝐜'𝐗 🎸 ❱ Now 😄 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 📀 𝐀𝐭 🤟 `{m.chat.title}`...**",
                    )
                except Exception as ep:
                    await loser.delete()
                    await m.reply_text(f"🚫 error: `{ep}`")
