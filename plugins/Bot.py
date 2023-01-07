# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.

from . import get_help

__doc__ = get_help("help_bot")

import os
import sys
import time
from platform import python_version as pyver
from random import choice

from telethon import __version__
from telethon.errors.rpcerrorlist import (
    BotMethodInvalidError,
    ChatSendMediaForbiddenError,
)

from Ayra.version import __version__ as AyraVer
from Ayra.dB import DEVLIST
from . import HOSTED_ON, LOGS

try:
    from git import Repo
except ImportError:
    LOGS.error("bot: 'gitpython' module not found!")
    Repo = None

from telethon.utils import resolve_bot_file_id

from . import (
    ATRA_COL,
    LOGS,
    OWNER_NAME,
    AYRA_IMAGES,
    Button,
    Carbon,
    Telegraph,
    Var,
    allcmds,
    asst,
    bash,
    call_back,
    callback,
    def_logs,
    eor,
    get_string,
    heroku_logs,
    in_pattern,
    inline_pic,
    restart,
    shutdown,
    start_time,
    time_formatter,
    udB,
    ayra_cmd,
    ayra_version,
    updater,
)


def AYRAPIC():
    return inline_pic() or choice(AYRA_IMAGES)


buttons = [
    [
        Button.url(get_string("bot_3"), "https://github.com/sen/wkkw"),
        Button.url(get_string("bot_4"), "t.me/idoganzzbot"),
    ]
]

# Will move to strings
alive_txt = """
◈ Miku userbot

  ◈ Version - {}
  ◈ Miku - {}
  ◈ Telethon - {}
"""

in_alive = "{}\n\n◈ <b>Miku Version -><b> <code>{}</code>\n◈ <b>Miku -></b> <code>{}</code>\n◈ <b>Python -></b> <code>{}</code>\n◈ <b>Waktu aktif -></b> <code>{}</code>\n◈ <b>Branch -></b> [ {} ]\n\n• <b>©↻˹ҡʏɴλɴ˼𐦝</b>"


@callback("alive")
async def alive(event):
    text = alive_txt.format(ayra_version, AyraVer, __version__)
    await event.answer(text, alert=True)


@ayra_cmd(
    pattern="alive( (.*)|$)",
)
async def lol(ayra):
    match = ayra.pattern_match.group(1).strip()
    inline = None
    if match in ["inline", "i"]:
        try:
            res = await ayra.client.inline_query(asst.me.username, "alive")
            return await res[0].click(ayra.chat_id)
        except BotMethodInvalidError:
            pass
        except BaseException as er:
            LOGS.exception(er)
        inline = True
    pic = udB.get_key("ALIVE_PIC")
    if isinstance(pic, list):
        pic = choice(pic)
    uptime = time_formatter((time.time() - start_time) * 1000)
    header = udB.get_key("ALIVE_TEXT") or get_string("bot_1")
    y = Repo().active_branch
    xx = Repo().remotes[0].config_reader.get("url")
    rep = xx.replace(".git", f"/tree/{y}")
    kk = f" `[{y}]({rep})` "
    if inline:
        kk = f"<a href={rep}>{y}</a>"
        parse = "html"
        als = in_alive.format(
            header,
            f"{ayra_version} [{HOSTED_ON}]",
            AyraVer,
            pyver(),
            uptime,
            kk,
        )

        if _e := udB.get_key("ALIVE_EMOJI"):
            als = als.replace("◈", _e)
    else:
        parse = "md"
        als = (get_string("alive_1")).format(
            header,
            OWNER_NAME,
            f"{ayra_version} [{HOSTED_ON}]",
            AyraVer,
            uptime,
            pyver(),
            __version__,
            kk,
        )

        if a := udB.get_key("ALIVE_EMOJI"):
            als = als.replace("◈", a)
    if pic:
        try:
            await ayra.reply(
                als,
                file=pic,
                parse_mode=parse,
                link_preview=False,
                buttons=buttons if inline else None,
            )
            return await ayra.try_delete()
        except ChatSendMediaForbiddenError:
            pass
        except BaseException as er:
            LOGS.exception(er)
            try:
                await ayra.reply(file=pic)
                await ayra.reply(
                    als,
                    parse_mode=parse,
                    buttons=buttons if inline else None,
                    link_preview=False,
                )
                return await ayra.try_delete()
            except BaseException as er:
                LOGS.exception(er)
    await eor(
        ayra,
        als,
        parse_mode=parse,
        link_preview=False,
        buttons=buttons if inline else None,
    )


@ayra_cmd(pattern="ping$", incoming=True, from_users=DEVLIST, chats=[], type=["official", "assistant"])
async def _(event):
    start = time.time()
    x = await event.eor("Pong !")
    end = round((time.time() - start) * 1000)
    uptime = time_formatter((time.time() - start_time) * 1000)
    await x.edit(get_string("ping").format(end, uptime))


@ayra_cmd(
    pattern="cmds$",
)
async def cmds(event):
    await allcmds(event, Telegraph)


heroku_api = Var.HEROKU_API


@ayra_cmd(
    pattern="restart$",
    fullsudo=False,
)
async def restart(ayra):
    ok = await ayra.eor(get_string("bot_5"))
    call_back()
    who = "bot" if ayra.client._bot else "user"
    udB.set_key("_RESTART", f"{who}_{ayra.chat_id}_{ok.id}")
    if heroku_api:
        return await restart(ok)
    await bash("git pull && pip3 install -r requirements.txt")
    if len(sys.argv) > 1:
        os.execl(sys.executable, sys.executable, "main.py")
    else:
        os.execl(sys.executable, sys.executable, "-m", "Ayra")


@ayra_cmd(
    pattern="shutdown$",
    fullsudo=False,
)
async def shutdownbot(ayra):
    await shutdown(ayra)


@ayra_cmd(
    pattern="logs( (.*)|$)",
    chats=[],
)
async def _(event):
    opt = event.pattern_match.group(1).strip()
    file = f"ayra{sys.argv[-1]}.log" if len(sys.argv) > 1 else "ayra.log"
    if opt == "heroku":
        await heroku_logs(event)
    elif opt == "carbon" and Carbon:
        event = await event.eor(get_string("com_1"))
        with open(file, "r") as f:
            code = f.read()[-2500:]
        file = await Carbon(
            file_name="ayra-logs",
            code=code,
            backgroundColor=choice(ATRA_COL),
        )
        await event.reply("**Ayra Logs.**", file=file)
    elif opt == "open":
        with open("ayra.log", "r") as f:
            file = f.read()[-4000:]
        return await event.eor(f"`{file}`")
    else:
        await def_logs(event, file)
    await event.try_delete()


@in_pattern("alive", owner=True)
async def inline_alive(ayra):
    pic = udB.get_key("ALIVE_PIC")
    if isinstance(pic, list):
        pic = choice(pic)
    uptime = time_formatter((time.time() - start_time) * 1000)
    header = udB.get_key("ALIVE_TEXT") or get_string("bot_1")
    y = Repo().active_branch
    xx = Repo().remotes[0].config_reader.get("url")
    rep = xx.replace(".git", f"/tree/{y}")
    kk = f"<a href={rep}>{y}</a>"
    als = in_alive.format(
        header, f"{ayra_version} [{HOSTED_ON}]", AyraVer, pyver(), uptime, kk
    )

    if _e := udB.get_key("ALIVE_EMOJI"):
        als = als.replace("◈", _e)
    builder = ayra.builder
    if pic:
        try:
            if ".jpg" in pic:
                results = [
                    await builder.photo(
                        pic, text=als, parse_mode="html", buttons=buttons
                    )
                ]
            else:
                if _pic := resolve_bot_file_id(pic):
                    pic = _pic
                    buttons.insert(
                        0, [Button.inline(get_string("bot_2"), data="alive")]
                    )
                results = [
                    await builder.document(
                        pic,
                        title="Inline Alive",
                        description="↻ꝛɪᴢ",
                        parse_mode="html",
                        buttons=buttons,
                    )
                ]
            return await ayra.answer(results)
        except BaseException as er:
            LOGS.info(er)
    result = [
        await builder.article(
            "Alive", text=als, parse_mode="html", link_preview=False, buttons=buttons
        )
    ]
    await ayra.answer(result)


@ayra_cmd(pattern="update( (.*)|$)")
async def _(e):
    xx = await e.eor(get_string("upd_1"))
    if e.pattern_match.group(1).strip() and (
        "fast" in e.pattern_match.group(1).strip()
        or "soft" in e.pattern_match.group(1).strip()
    ):
        await bash("git pull -f && pip3 install -r requirements.txt")
        call_back()
        await xx.edit(get_string("upd_7"))
        os.execl(sys.executable, "python3", "-m", "Ayra")
        # return
    m = await updater()
    branch = (Repo.init()).active_branch
    if m:
        x = await asst.send_file(
            udB.get_key("LOG_CHANNEL"),
            AYRAPIC(),
            caption="• **Pembaruan tersedia** •",
            force_document=False,
            buttons=Button.inline("Changelog", data="changes"),
        )
        Link = x.message_link
        await xx.edit(
            f'<strong><a href="{Link}">[ChangeLogs]</a></strong>',
            parse_mode="html",
            link_preview=False,
        )
    else:
        await xx.edit(
            f'<code>Your BOT is </code><strong>up-to-date</strong><code> with </code><strong><a href="https://github.com/Onlymeriz/Ayra/tree/{branch}">[{branch}]</a></strong>',
            parse_mode="html",
            link_preview=False,
        )


@callback("updtavail", owner=True)
async def updava(event):
    await event.delete()
    await asst.send_file(
        udB.get_key("LOG_CHANNEL"),
        AYRAPIC(),
        caption="• **Pembaruan tersedia** •",
        force_document=False,
        buttons=Button.inline("Changelog", data="changes"),
    )
