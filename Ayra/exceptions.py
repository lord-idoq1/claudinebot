# Ayra - UserBot
# Copyright (C) 2021-2022 Teamayra
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/senpai80/Ayra/blob/main/LICENSE>.

"""
Exceptions which can be raised by py-Ayra Itself.
"""


class pyAyraError(Exception):
    ...


class TelethonMissingError(ImportError):
    ...


class DependencyMissingError(ImportError):
    ...


class RunningAsFunctionLibError(pyAyraError):
    ...
