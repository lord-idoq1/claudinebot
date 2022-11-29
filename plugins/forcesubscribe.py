# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
◈ Perintah Tersedia

• `{i}fsub <chat username><id>`
    Aktifkan ForceSub di Obrolan Terpakai!

• `{i}checkfsub`
    Periksa/Dapatkan Pengaturan ForceSub Aktif dari Obrolan yang Digunakan.

• `{i}remfsub`
    Hapus ForceSub dari Obrolan Terpakai!

    Catatan - Anda Harus Menjadi Admin di Kedua Saluran/Obrolan
        untuk Menggunakan ForceSubscribe.
"""

import re

from telethon.errors.rpcerrorlist import ChatAdminRequiredError, UserNotParticipantError
from telethon.tl.custom import Button
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.types import (
    Channel,
    ChannelParticipantBanned,
    ChannelParticipantLeft,
    User,
)

from Ayra.dB.forcesub_db import add_forcesub, get_forcesetting, rem_forcesub

from . import (
    LOGS,
    asst,
    callback,
    events,
    get_string,
    in_pattern,
    inline_mention,
    udB,
    ayra_bot,
    ayra_cmd,
)

CACHE = {}


@ayra_cmd(pattern="fsub( (.*)|$)", admins_only=True, groups_only=True)
async def addfor(e):
    match = e.pattern_match.group(1).strip()
    if not match:
        return await e.eor(get_string("fsub_1"), time=5)
    try:
        match = await e.client.parse_id(match)
    except BaseException:
        return await e.eor(get_string("fsub_2"), time=5)
    add_forcesub(e.chat_id, match)
    await e.eor("Menambahkan ForceSub di Obrolan Ini !")
    ayra_bot.add_handler(force_sub, events.NewMessage(incoming=True))


@ayra_cmd(pattern="remfsub$")
async def remor(e):
    res = rem_forcesub(e.chat_id)
    if not res:
        return await e.eor(get_string("fsub_3"), time=5)
    await e.eor("ForceSub dihapus...")


@ayra_cmd(pattern="checkfsub$")
async def getfsr(e):
    res = get_forcesetting(e.chat_id)
    if not res:
        return await e.eor("ForceSub Tidak Aktif Dalam Obrolan Ini !", time=5)
    cha = await e.client.get_entity(int(res))
    await e.eor(f"**Status ForceSub** : `Aktif`\n- **{cha.title}** `({res})`")


@in_pattern("fsub( (.*)|$)", owner=True)
async def fcall(e):
    match = e.pattern_match.group(1).strip()
    spli = match.split("_")
    user = await ayra_bot.get_entity(int(spli[0]))
    cl = await ayra_bot.get_entity(int(spli[1]))
    text = f"Hi {inline_mention(user)}, Anda Perlu Bergabung"
    text += f" {cl.title} untuk Mengobrol di Grup ini."
    el = (
        f"https://t.me/{cl.username}"
        if cl.username
        else (await ayra_bot(ExportChatInviteRequest(cl))).link
    )

    res = [
        await e.builder.article(
            title="forcesub",
            text=text,
            buttons=[
                [Button.url(text=get_string("fsub_4"), url=el)],
                [Button.inline(get_string("fsub_5"), data=f"unm_{match}")],
            ],
        )
    ]
    await e.answer(res)


@callback(re.compile("unm_(.*)"))
async def diesoon(e):
    match = (e.data_match.group(1)).decode("UTF-8")
    spli = match.split("_")
    if e.sender_id != int(spli[0]):
        return await e.answer(get_string("fsub_7"), alert=True)
    try:
        values = await ayra_bot(GetParticipantRequest(int(spli[1]), int(spli[0])))
        if isinstance(values.participant, ChannelParticipantLeft) or (
            isinstance(values.participant, ChannelParticipantBanned) and values.left
        ):
            raise UserNotParticipantError("")
    except UserNotParticipantError:
        return await e.answer(
            "Silakan Bergabung dengan Saluran Itu!\nKemudian Klik Tombol Ini !", alert=True
        )
    await ayra_bot.edit_permissions(
        e.chat_id, int(spli[0]), send_messages=True, until_date=None
    )
    await e.edit(get_string("fsub_8"))


async def force_sub(ayra):
    if not udB.get_key("FORCESUB"):
        return
    user = await ayra.get_sender()
    joinchat = get_forcesetting(ayra.chat_id)
    if (not joinchat) or (isinstance(user, User) and user.bot):
        return
    if CACHE.get(ayra.chat_id):
        if CACHE[ayra.chat_id].get(user.id):
            CACHE[ayra.chat_id].update({user.id: CACHE[ayra.chat_id][user.id] + 1})
        else:
            CACHE[ayra.chat_id].update({user.id: 1})
    else:
        CACHE.update({ayra.chat_id: {user.id: 1}})
    count = CACHE[ayra.chat_id][user.id]
    if count == 11:
        CACHE[ayra.chat_id][user.id] = 1
        return
    if count in range(2, 11):
        return
    try:
        await ayra_bot.get_permissions(int(joinchat), user.id)
        return
    except UserNotParticipantError:
        pass
    if isinstance(user, Channel):
        try:
            await ayra_bot.edit_permissions(
                ayra.chat_id, user.id, view_messages=False
            )
            return
        except BaseException as er:
            LOGS.exception(er)
    try:
        await ayra_bot.edit_permissions(ayra.chat_id, user.id, send_messages=False)
    except ChatAdminRequiredError:
        return
    except Exception as e:
        await ayra.delete()
        LOGS.info(e)
    res = await ayra_bot.inline_query(asst.me.username, f"fsub {user.id}_{joinchat}")
    await res[0].click(ayra.chat_id, reply_to=ayra.id)


if udB.get_key("FORCESUB"):
    ayra_bot.add_handler(force_sub, events.NewMessage(incoming=True))
