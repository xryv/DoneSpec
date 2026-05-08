from __future__ import annotations

from donespec.checkers.base import Checker
from donespec.checkers.command import CommandChecker
from donespec.checkers.file_exists import FileExistsChecker
from donespec.checkers.git import FileNotModifiedChecker
from donespec.checkers.http import HttpCheckChecker
from donespec.checkers.regex import RegexAbsentChecker, RegexInFileChecker

CHECKERS: dict[str, type[Checker]] = {
    CommandChecker.type_name: CommandChecker,
    FileExistsChecker.type_name: FileExistsChecker,
    RegexInFileChecker.type_name: RegexInFileChecker,
    RegexAbsentChecker.type_name: RegexAbsentChecker,
    FileNotModifiedChecker.type_name: FileNotModifiedChecker,
    HttpCheckChecker.type_name: HttpCheckChecker,
}


def get_checker(type_name: str) -> type[Checker]:
    try:
        return CHECKERS[type_name]
    except KeyError as exc:
        available = ", ".join(sorted(CHECKERS))
        msg = f"Unknown checker type: {type_name}. Available: {available}"
        raise ValueError(msg) from exc
