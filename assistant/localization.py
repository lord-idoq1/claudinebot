# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.

import re

from . import (
    Button,
    AyConfig,
    callback,
    get_back_button,
    get_languages,
    get_string,
    udB,
)


@callback("lang", owner=True)
async def setlang(event):
    languages = get_languages()
    tayrad = [
        Button.inline(
            f"{languages[ayra]['natively']} [{ayra.lower()}]",
            data=f"set_{ayra}",
        )
        for ayra in languages
    ]
    buttons = list(zip(tayrad[::2], tayrad[1::2]))
    if len(tayrad) % 2 == 1:
        buttons.append((tayrad[-1],))
    buttons.append([Button.inline("« Back", data="mainmenu")])
    await event.edit(get_string("ast_4"), buttons=buttons)


@callback(re.compile(b"set_(.*)"), owner=True)
async def settt(event):
    lang = event.data_match.group(1).decode("UTF-8")
    languages = get_languages()
    AyConfig.lang = lang
    udB.del_key("language") if lang == "id" else udB.set_key("language", lang)
    await event.edit(
        f"Bahasa Anda telah disetel ke {languages[lang]['natively']} [{lang}].",
        buttons=get_back_button("lang"),
    )
