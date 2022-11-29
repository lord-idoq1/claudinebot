# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
◈ Perintah Tersedia

Di Malam Hari, izin semua orang untuk mengirim pesan di semua grup yang Anda tambahkan melalui `{i}addnm` akan dinonaktifkan
Dan Nyalakan otomatis di pagi hari

• `{i}addnm`
   Tambahkan Mode Malam
   Untuk Menambahkan Grup ke Mode Malam Otomatis.

• `{i}remnm`
   Hapus Mode Malam
   Untuk menghapus Grup Dari Mode Malam Otomatis

• `{i}listnm`
   Daftar Mode Malam
   Untuk Mendapatkan Semua Daftar Grup tempat NightMode Aktif.

• `{i}nmtime <close hour> <close min> <open hour> <open min>`
   Waktu Mode Malam
   Secara Default 00:00 , tidak aktif 07:00
   Gunakan format 24 jam
   Ex- `nmtime 01 00 06 30`
"""

from . import LOGS

try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
except ImportError:
    LOGS.error("nightmode: 'apscheduler' not Installed!")
    AsyncIOScheduler = None

from telethon.tl.functions.messages import EditChatDefaultBannedRightsRequest
from telethon.tl.types import ChatBannedRights

from Ayra.dB.night_db import *

from . import get_string, udB, ayra_bot, ayra_cmd


@ayra_cmd(pattern="nmtime( (.*)|$)")
async def set_time(e):
    if not e.pattern_match.group(1).strip():
        return await e.eor(get_string("nightm_1"))
    try:
        ok = e.text.split(maxsplit=1)[1].split()
        if len(ok) != 4:
            return await e.eor(get_string("nightm_1"))
        tm = [int(x) for x in ok]
        udB.set_key("NIGHT_TIME", str(tm))
        await e.eor(get_string("nightm_2"))
    except BaseException:
        await e.eor(get_string("nightm_1"))


@ayra_cmd(pattern="addnm( (.*)|$)")
async def add_grp(e):
    if pat := e.pattern_match.group(1).strip():
        try:
            add_night((await ayra_bot.get_entity(pat)).id)
            return await e.eor(f"Selesai, Menambahkan {pat} Ke Mode Malam.")
        except BaseException:
            return await e.eor(get_string("nightm_5"), time=5)
    add_night(e.chat_id)
    await e.eor(get_string("nightm_3"))


@ayra_cmd(pattern="remnm( (.*)|$)")
async def rem_grp(e):
    if pat := e.pattern_match.group(1).strip():
        try:
            rem_night((await ayra_bot.get_entity(pat)).id)
            return await e.eor(f"Selesai, Dihapus {pat} Ke Mode Malam.")
        except BaseException:
            return await e.eor(get_string("nightm_5"), time=5)
    rem_night(e.chat_id)
    await e.eor(get_string("nightm_4"))


@ayra_cmd(pattern="listnm$")
async def rem_grp(e):
    chats = night_grps()
    name = "Grup NightMode Adalah-:\n\n"
    for x in chats:
        try:
            ok = await ayra_bot.get_entity(x)
            name += f"@{ok.username}" if ok.username else ok.title
        except BaseException:
            name += str(x)
    await e.eor(name)


async def open_grp():
    chats = night_grps()
    for chat in chats:
        try:
            await ayra_bot(
                EditChatDefaultBannedRightsRequest(
                    chat,
                    banned_rights=ChatBannedRights(
                        until_date=None,
                        send_messages=False,
                        send_media=False,
                        send_stickers=False,
                        send_gifs=False,
                        send_games=False,
                        send_inline=False,
                        send_polls=False,
                    ),
                )
            )
            await ayra_bot.send_message(chat, "**Mode Malam Mati**\in\Group Dibuka 🥳.")
        except Exception as er:
            LOGS.info(er)


async def close_grp():
    chats = night_grps()
    h1, m1, h2, m2 = 0, 0, 7, 0
    if udB.get_key("NIGHT_TIME"):
        h1, m1, h2, m2 = eval(udB.get_key("NIGHT_TIME"))
    for chat in chats:
        try:
            await ayra_bot(
                EditChatDefaultBannedRightsRequest(
                    chat,
                    banned_rights=ChatBannedRights(
                        until_date=None,
                        send_messages=True,
                    ),
                )
            )
            await ayra_bot.send_message(
                chat, f"**NightMode : Grup Ditutup**\n\nGrup Akan Dibuka Pada `{h2}:{m2}`"
            )
        except Exception as er:
            LOGS.info(er)


if AsyncIOScheduler and night_grps():
    try:
        h1, m1, h2, m2 = 0, 0, 7, 0
        if udB.get_key("NIGHT_TIME"):
            h1, m1, h2, m2 = eval(udB.get_key("NIGHT_TIME"))
        sch = AsyncIOScheduler()
        sch.add_job(close_grp, trigger="cron", hour=h1, minute=m1)
        sch.add_job(open_grp, trigger="cron", hour=h2, minute=m2)
        sch.start()
    except Exception as er:
        LOGS.info(er)
