import argparse
import asyncio
import platform
from threading import Lock

import aiofiles
import aiohttp
from colorama import Fore

LOCK = Lock()

async def check_vanity(vanity: str, session: aiohttp.ClientSession) -> None:
    async with session.head(f"https://discord.com/invite/{vanity}") as resp:
        LOCK.acquire()
        if "X-Robots-Tag" in resp.headers.keys():
            print(f"{Fore.LIGHTGREEN_EX}[ /{vanity} ]{Fore.RESET} is available.")
        else:
            print(f"{Fore.LIGHTRED_EX}[ /{vanity} ]{Fore.RESET} is NOT available.")
        LOCK.release()


async def main() -> None:
    parser = argparse.ArgumentParser(description="https://github.com/drooling")
    parser.add_argument("vanity_list")
    args = parser.parse_args()

    VANITIES = [vanity.strip() for vanity in set(await (await aiofiles.open(args.vanity_list, "r")).readlines())]
    session = aiohttp.ClientSession()
    pending = []

    for vanity in VANITIES:
        pending.append(asyncio.ensure_future(check_vanity(vanity, session)))
    await asyncio.gather(*pending, return_exceptions=False)

    await session.close()
    exit(0)


if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
