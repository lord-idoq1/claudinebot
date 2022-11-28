# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.

from . import get_help

__doc__ = get_help("help_autoban")

from telethon import events
from telethon.tl.types import Channel

from Ayra.dB import autoban_db, dnd_db
from Ayra.fns.admins import get_update_linked_chat

from . import LOGS, asst, get_string, inline_mention, ayra_bot, ayra_cmd


async def dnd_func(event):
    if event.chat_id in dnd_db.get_dnd_chats():
        for user in event.users:
            try:
                await (
                    await event.client.kick_participant(event.chat_id, user)
                ).delete()
            except Exception as ex:
                LOGS.error("Error in DND:")
                LOGS.exception(ex)
        await event.delete()


async def channel_del(event):
    if not autoban_db.is_autoban_enabled(event.chat_id):
        return
    if autoban_db.is_whitelisted(event.chat_id, event.sender_id):
        return
    linked = await get_update_linked_chat(event)
    if linked == event.sender.id:
        return
    if event.chat.creator or event.chat.admin_rights.ban_users:
        try:
            await event.client.edit_permissions(
                event.chat_id, event.sender_id, view_messages=False
            )
        except Exception as er:
            LOGS.exception(er)
    await event.try_delete()


@ayra_cmd(
    pattern="autokick (on|off)$",
    admins_only=True,
    manager=True,
    require="ban_users",
    fullsudo=True,
)
async def _(event):
    match = event.pattern_match.group(1)
    if match == "on":
        if dnd_db.chat_in_dnd(event.chat_id):
            return await event.eor("`Obrolan sudah dalam mode jangan ganggu.`", time=3)
        dnd_db.add_dnd(event.chat_id)
        event.client.add_handler(
            dnd_func, events.ChatAction(func=lambda x: x.user_joined)
        )
        await event.eor("`Mode jangan ganggu diaktifkan untuk obrolan ini.`", time=3)
    elif match == "off":
        if not dnd_db.chat_in_dnd(event.chat_id):
            return await event.eor("`Obrolan tidak dalam mode jangan ganggu.`", time=3)
        dnd_db.del_dnd(event.chat_id)
        await event.eor("`Mode jangan ganggu dinonaktifkan untuk obrolan ini.`", time=3)


@ayra_cmd(pattern="cban$", admins_only=True)
async def ban_cha(ayra):
    if autoban_db.is_autoban_enabled(ayra.chat_id):
        autoban_db.del_channel(ayra.chat_id)
        return await ayra.eor("`Larangan Saluran Otomatis Dinonaktifkan...`")
    if not (
        ayra.chat.creator
        or (ayra.chat.admin_rights.delete_messages or ayra.chat.admin_rights.ban_users)
    ):
        return await ayra.eor(
            "Anda kehilangan hak admin yang diperlukan!\nAnda tidak dapat menggunakan ChannelBan tanpa hak istimewa Ban/del..`"
        )
    autoban_db.add_channel(ayra.chat_id)
    await ayra.eor("`Diaktifkan Auto ChannelBan Berhasil!`")
    ayra.client.add_handler(
        channel_del,
        events.NewMessage(
            func=lambda x: not x.is_private and isinstance(x.sender, Channel)
        ),
    )


@ayra_cmd(pattern="(list|add|rem)wl( (.*)|$)")
async def do_magic(event):
    match = event.pattern_match.group(1)
    msg = await event.eor(get_string("com_1"))
    if match == "list":
        cha = autoban_db.get_whitelisted_channels(event.chat_id)
        if not cha:
            return await msg.edit("`Tidak ada saluran Daftar Putih untuk obrolan saat ini.`")
        Msg = "**Saluran Daftar Putih di Obrolan Saat Ini**\n\n"
        for ch in cha:
            Msg += f"(`{ch}`) "
            try:
                Msg += inline_mention(await event.client.get_entity(ch))
            except Exception:
                Msg += "\n"
        return await msg.edit(Msg)
    usea = event.pattern_match.group(2).strip()
    if not usea:
        return await Msg.edit(
            "`Berikan nama pengguna/id saluran untuk ditambahkan/dihapus ke/dari daftar putih..`"
        )
    try:
        u_id = await event.client.parse_id(usea)
        cha = await event.client.get_entity(u_id)
    except Exception as er:
        LOGS.exception(er)
        return await msg.edit(f"Kesalahan Pecah!\n`{er}`")
    if match == "add":
        autoban_db.add_to_whitelist(event.chat_id, u_id)
        return await msg.edit(f"`Ditambahkan` {inline_mention(cha)} `to WhiteList..`")
    autoban_db.del_from_whitelist(event.chat_id, u_id)
    await msg.edit(f"`Dihapus` {inline_mention(cha)} `from WhiteList.`")


if dnd_db.get_dnd_chats():
    ayra_bot.add_handler(dnd_func, events.ChatAction(func=lambda x: x.user_joined))
    asst.add_handler(dnd_func, events.ChatAction(func=lambda x: x.user_joined))

if autoban_db.get_all_channels():
    ayra_bot.add_handler(
        channel_del,
        events.NewMessage(
            func=lambda x: not x.is_private and isinstance(x.sender, Channel)
        ),
    )
