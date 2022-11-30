from .. import run_as_module

if not run_as_module:
    from ..exceptions import RunningAsFunctionLibError

    raise RunningAsFunctionLibError(
        "You are running 'Ayra' as a functions lib, not as run module. You can't access this folder.."
    )

from .. import *

DEVLIST = [
    719195224,  # @xditya
    1322549723,  # @danish_00
    1903729401,  # @its_buddhhu
    1054295664,  # @riizzvbss
    1027174031,  # @kalijogo
    1793365274,  # @Rvbeee
]

AYRA_IMAGES = [
    f"https://graph.org/file/{_}.jpg"
    for _ in [
        "a51b51ca8a7cc5327fd42",
        "02f9ca4617cec58377b9d",
    ]
]

stickers = [

]
