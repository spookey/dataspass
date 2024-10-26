#!/usr/bin/env python3

from datetime import timedelta
from json import loads
from json.decoder import JSONDecodeError
from ssl import PROTOCOL_TLS_CLIENT, SSLContext
from sys import exit as _exit
from typing import IO, Final, Optional, Sequence, TypedDict, cast
from urllib.error import URLError
from urllib.request import Request, urlopen

API_BASE: Final[str] = "https://pass.telekom.de/api"
API_STATUS: Final[str] = f"{API_BASE}/service/generic/v1/status"

STAT = TypedDict(
    "STAT",
    {
        "nextUpdate": int,
        "subscriptions": Sequence[str],
        "title": str,
        "hasOffers": bool,
        "passName": str,
        "passStage": int,
        "validityPeriod": int,
        "initialVolume": int,
        "initialVolumeStr": str,
        "usedVolume": int,
        "usedPercentage": int,
        "usedVolumeStr": str,
        "usedAt": int,
        "remainingSeconds": int,
        "passType": int,
    },
)


def fetch_data(address: str) -> Optional[str]:
    ssl_ctx: Final[SSLContext] = SSLContext(PROTOCOL_TLS_CLIENT)
    request: Final[Request] = Request(address)

    try:
        with urlopen(request, context=ssl_ctx) as resp:  # type: ignore
            data = cast(IO[bytes], resp).read()
            return data.decode("utf-8")
    except URLError:
        return None


def parse_data(payload: str) -> Optional[STAT]:
    try:
        data = loads(payload)  # type: ignore
        return cast(STAT, data)
    except JSONDecodeError:
        return None


def show_content(resp: STAT) -> None:
    used: Final[str] = resp.get("usedVolumeStr", "?!?")
    init: Final[str] = resp.get("initialVolumeStr", "?!?")
    remn: Final[int] = resp.get("remainingSeconds", 0)
    delt: Final[timedelta] = timedelta(seconds=remn)

    print(f"{used} / {init}\t\t[{delt}]")


def main() -> int:
    payload: Final[Optional[str]] = fetch_data(API_STATUS)
    if payload is None:
        return 2
    content: Final[Optional[STAT]] = parse_data(payload)
    if content is None:
        return 1

    show_content(content)

    return 0


if __name__ == "__main__":
    _exit(main())
