# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.

"""
◈ Perintah Tersedia 

• `{i} play` <nama lagu/link/balas audio>
   Putar lagu di obrolan suara, atau tambahkan lagu ke antrean.
   
• `{i} vplay` <nama video/link/balas video>
   Streaming Video dalam obrolan.
   
• `{i} skip`
   Lewati lagu saat ini dan putar lagu berikutnya dalam antrean, jika ada.

• `{i} pause`
   Jeda pemutaran.

• `{i} resume`
   Lanjutkan pemutaran.

• `{i} end`
   Akhiri pemutaran.
"""


import asyncio
import random

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from youtubesearchpython import VideosSearch

from config import PREFIX, bot, call_py
from Ayra.helpers.queues import QUEUE, add_to_queue, get_queue, clear_queue
from Ayra.helpers.decorators import authorized_users_only
from Ayra.helpers.handlers import skip_current_song, skip_item


AMBILFOTO = [
    "https://telegra.ph/file/c3aeea866ebeb10829861.jpg",
    "https://telegra.ph/file/c3aeea866ebeb10829861.jpg",
    "https://telegra.ph/file/c3aeea866ebeb10829861.jpg",
    "https://telegra.ph/file/c3aeea866ebeb10829861.jpg",
    "https://telegra.ph/file/c3aeea866ebeb10829861.jpg",
    "https://telegra.ph/file/c3aeea866ebeb10829861.jpg",
    "https://telegra.ph/file/c3aeea866ebeb10829861.jpg",
    "https://telegra.ph/file/c3aeea866ebeb10829861.jpg",
    "https://telegra.ph/file/c3aeea866ebeb10829861.jpg",
    "https://telegra.ph/file/c3aeea866ebeb10829861.jpg",
    "https://telegra.ph/file/c3aeea866ebeb10829861.jpg",
    "https://telegra.ph/file/c3aeea866ebeb10829861.jpg",
]

IMAGE_THUMBNAIL = random.choice(AMBILFOTO)


def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# music player
def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            if len(r["title"]) > 34:
                songname = r["title"][:35] + "..."
            else:
                songname = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
            duration = r["duration"]
        return [songname, url, duration]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        # CHANGE THIS BASED ON WHAT YOU WANT
        "bestaudio",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


# video player
def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            if len(r["title"]) > 34:
                songname = r["title"][:35] + "..."
            else:
                songname = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
            duration = r["duration"]
        return [songname, url, duration]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        # CHANGE THIS BASED ON WHAT YOU WANT
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


@Client.on_message(filters.command(["play"], prefixes=f"{PREFIX}"))
async def play(client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    m.chat.title
    if replied:
        if replied.audio or replied.voice:
            await m.delete()
            huehue = await replied.reply("**◈ Memproses..**")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:35] + "..."
                else:
                    songname = replied.audio.file_name[:35] + "..."
                duration = convert_seconds(replied.audio.duration)
            elif replied.voice:
                songname = "Ayra Music"
                duration = convert_seconds(replied.voice.duration)
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/c3aeea866ebeb10829861.jpg",
                    caption=f"""
**✚ Lagu Di Antrian Ke** `{pos}`
🎵 **Judul:** [{songname}]({link})
⏰ **Duration:** `{duration}`
🎧 **Status:** `Playing`
🙋‍♂ **Permintaan:** {m.from_user.mention}
""",
                )
            else:
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(
                        dl,
                    ),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/c3aeea866ebeb10829861.jpg",
                    caption=f"""
**📀 Mulai Memutar Lagu**
🎵 **Judul:** [{songname}]({link})
⏱️ **Duration:** `{duration}`
🎧 **Status:** `Playing`
🙋‍♂ **Atas Permintaan:** {m.from_user.mention}
""",
                )

    else:
        if len(m.command) < 2:
            await m.reply("Balas ke File Audio atau berikan sesuatu untuk Pencarian")
        else:
            await m.delete()
            huehue = await m.reply("**◈ Sedang Mencari Lagu..**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await huehue.edit("`Tidak Menemukan Apapun untuk Kueri yang Diberikan`")
            else:
                songname = search[0]
                url = search[1]
                duration = search[2]
                hm, ytlink = await ytdl(url)
                if hm == 0:
                    await huehue.edit(f"**YTDL ERROR** \n\n`{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await huehue.delete()
                        # await m.reply_to_message.delete()
                        await m.reply_photo(
                            photo=f"{IMAGE_THUMBNAIL}",
                            caption=f"""
**✚ Lagu Di Antrian Ke** `{pos}` 🎵
🎵 **Judul:** [{songname}]({url})
⏱️ **Duration:** `{duration}`
🎧 **Status:** `Playing`
🙋‍♂ **Atas Permintaan:** {m.from_user.mention}
""",
                        )
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                ),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await huehue.delete()
                            # await m.reply_to_message.delete()
                            await m.reply_photo(
                                photo=f"{IMAGE_THUMBNAIL}",
                                caption=f"""
**📀 Mulai Memutar Lagu**
🎵 **Judul:** [{songname}]({url})
⏱️ **Duration** `{duration}`
🎧 **Status:** `Playing`
🙋‍♂ **Atas Permintaan:** {m.from_user.mention}
""",
                            )
                        except Exception as ep:
                            await huehue.edit(f"`{ep}`")


@Client.on_message(filters.command(["videoplay", "vplay"], prefixes=f"{PREFIX}"))
async def videoplay(client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    m.chat.title
    if replied:
        if replied.video or replied.document:
            await m.delete()
            huehue = await replied.reply("**◈ Memproses....**")
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
                    await huehue.edit(
                        "`Hanya 720, 480, 360 Diizinkan` \n`Sekarang Streaming masuk 720p`"
                    )
            try:
                if replied.video:
                    songname = replied.video.file_name[:70]
                elif replied.document:
                    songname = replied.document.file_name[:70]
            except BaseException:
                songname = "Ayra Video"

            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/c3aeea866ebeb10829861.jpg",
                    caption=f"""
**✚ Video Di Antrian Ke {pos} 🎥
🎵 Judul: [{songname}]({link})
🎥 Status: Playing
🙋‍♂ Atas Permintaan: {m.from_user.mention}**
""",
                )
            else:
                if Q == 720:
                    hmmm = HighQualityVideo()
                elif Q == 480:
                    hmmm = MediumQualityVideo()
                elif Q == 360:
                    hmmm = LowQualityVideo()
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(dl, HighQualityAudio(), hmmm),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/c3aeea866ebeb10829861.jpg",
                    caption=f"""
**🎥 Mulai Memutar Video
🎵 Judul: [{songname}]({link})
🎥 Status: Playing
🙋‍♂ Atas permintaan: {m.from_user.mention}**
""",
                )

    else:
        if len(m.command) < 2:
            await m.reply(
                "**Balas ke File Audio atau berikan sesuatu untuk Pencarian**"
            )
        else:
            await m.delete()
            huehue = await m.reply("**◈ Memprosess...**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            hmmm = HighQualityVideo()
            if search == 0:
                await huehue.edit(
                    "**Tidak Menemukan Apa pun untuk Kueri yang Diberikan**"
                )
            else:
                songname = search[0]
                url = search[1]
                duration = search[2]
                hm, ytlink = await ytdl(url)
                if hm == 0:
                    await huehue.edit(f"**YTDL ERROR** \n\n`{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await huehue.delete()
                        # await m.reply_to_message.delete()
                        await m.reply_photo(
                            photo=f"{IMAGE_THUMBNAIL}",
                            caption=f"""
**✚ Video Di Antrian Ke** `{pos}` 🎥
🎵 **Judul:** [{songname}]({url})
⏱️ **Duration:** `{duration}`
🎥 **Status:** `Playing`
🙋‍♂ **Atas Permintaan:** {m.from_user.mention}
""",
                        )
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioVideoPiped(ytlink, HighQualityAudio(), hmmm),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await huehue.delete()
                            # await m.reply_to_message.delete()
                            await m.reply_photo(
                                photo=f"{IMAGE_THUMBNAIL}",
                                caption=f"""
**🎥 Mulai Memutar Video**
🎵 **Judul:** [{songname}]({url})
⏱️ **Duration:** `{duration}`
🎥 **Status:** `Playing`
🙋‍♂ **Atas Permintaan:** {m.from_user.mention}
""",
                            )
                        except Exception as ep:
                            await huehue.edit(f"`{ep}`")


@Client.on_message(filters.command(["playfrom"], prefixes=f"{PREFIX}"))
async def playfrom(client, m: Message):
    chat_id = m.chat.id
    if len(m.command) < 2:
        await m.reply(
            f"**PENGGUNAAN:** \n\n`{PREFIX}playfrom [chat_id/username]` \n`{PREFIX}playfrom [chat_id/username]`"
        )
    else:
        args = m.text.split(maxsplit=1)[1]
        if ";" in args:
            chat = args.split(";")[0]
            limit = int(args.split(";")[1])
        else:
            chat = args
            limit = 10
            lmt = 9
        await m.delete()
        hmm = await m.reply(f"**◈ Mengambil {limit} Lagu Acak Dari {chat}**")
        try:
            async for x in bot.search_messages(chat, limit=limit, filter="audio"):
                location = await x.download()
                if x.audio.title:
                    songname = x.audio.title[:30] + "..."
                else:
                    songname = x.audio.file_name[:30] + "..."
                link = x.link
                if chat_id in QUEUE:
                    add_to_queue(chat_id, songname, location, link, "Audio", 0)
                else:
                    await call_py.join_group_call(
                        chat_id,
                        AudioPiped(location),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, songname, location, link, "Audio", 0)
                    # await m.reply_to_message.delete()
                    await m.reply_photo(
                        photo="https://telegra.ph/file/c3aeea866ebeb10829861.jpg",
                        caption=f"""
**📀 Mulai Memutar Lagu Dari {chat}
🎵 Judul: [{songname}]({link})
🎧 Status: Playing
🙋‍♂ Atas Permintaan: {m.from_user.mention}**
""",
                    )
            await hmm.delete()
            await m.reply(
                f"◈ Menambahkan {lmt} Lagu Ke Dalam Antrian\n◈ Klik {PREFIX}playlist Untuk Melihat Daftar Putar**"
            )
        except Exception as e:
            await hmm.edit(f"**ERROR** \n`{e}`")


@Client.on_message(filters.command(["playlist", "queue"], prefixes=f"{PREFIX}"))
async def playlist(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await m.delete()
            await m.reply(
                f"**📀 SEKARANG MEMUTAR:** \n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}`",
                disable_web_page_preview=True,
            )
        else:
            QUE = f"**📀 SEKARANG MEMUTAR:** \n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}` \n\n**✚ DAFTAR ANTRIAN:**"
            l = len(chat_queue)
            for x in range(1, l):
                hmm = chat_queue[x][0]
                hmmm = chat_queue[x][2]
                hmmmm = chat_queue[x][3]
                QUE = QUE + "\n" + f"**#{x}** - [{hmm}]({hmmm}) | `{hmmmm}`\n"
            await m.reply(QUE, disable_web_page_preview=True)
    else:
        await m.reply("**Tidak Memutar Apapun...**")
        
@Client.on_message(filters.command(["skip"], prefixes=f"{PREFIX}"))
@authorized_users_only
async def skip(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("**❌ Tidak ada apapun didalam antrian untuk dilewati!**")
        elif op == 1:
            await m.reply("Antrian Kosong, Meninggalkan Obrolan Suara**")
        else:
            await m.reply(
                f"**⏭️ Melewati pemutaran** \n**📀 Sekarang memutar** - [{op[0]}]({op[1]}) | `{op[2]}`",
                disable_web_page_preview=True,
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "**🗑️ Menghapus lagu-lagu berikut dari Antrian: -**"
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
                        OP = OP + "\n" + f"**#⃣{x}** - {hm}"
            await m.reply(OP)


@Client.on_message(filters.command(["end", "stop"], prefixes=f"{PREFIX}"))
@authorized_users_only
async def stop(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("**❌ Mengakhiri pemutaran**")
        except Exception as e:
            await m.reply(f"**ERROR** \n`{e}`")
    else:
        await m.reply("**❌ Tidak ada apapun yang sedang diputar!**")


@Client.on_message(filters.command(["pause"], prefixes=f"{PREFIX}"))
@authorized_users_only
async def pause(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                f"**⏸ Pemutaran dijeda.**\n\n• Untuk melanjutkan pemutaran, gunakan perintah » {PREFIX}resume"
            )
        except Exception as e:
            await m.reply(f"**ERROR** \n`{e}`")
    else:
        await m.reply("** ❌ Tidak ada apapun yang sedang diputar!**")


@Client.on_message(filters.command(["resume"], prefixes=f"{PREFIX}"))
@authorized_users_only
async def resume(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(
                f"**▶️ Melanjutkan pemutaran yang dijeda**\n\n• Untuk menjeda pemutaran, gunakan perintah » {PREFIX}pause**"
            )
        except Exception as e:
            await m.reply(f"**ERROR** \n`{e}`")
    else:
        await m.reply("**❌ Tidak ada apapun yang sedang dijeda!**")
