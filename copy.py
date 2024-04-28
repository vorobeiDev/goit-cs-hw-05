import argparse
import asyncio
import logging

from aiopath import AsyncPath
from aioshutil import copyfile

parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="dist")

args = parser.parse_args()

source = AsyncPath(args.source)
output = AsyncPath(args.output)


async def grabs_folder(path: AsyncPath):
    async for el in path.iterdir():
        if await el.is_dir():
            await grabs_folder(el)
        else:
            await copy_file(el)


async def copy_file(file: AsyncPath):
    ext_folder = output / file.suffix[1:]
    try:
        await ext_folder.mkdir(exist_ok=True, parents=True)
        await copyfile(file, ext_folder / file.name)
        logging.info(f"File {file.name} copied to {ext_folder}")
    except OSError as e:
        logging.error(f"Error copying file {file.name}: {e}")


if __name__ == "__main__":
    message_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=message_format, datefmt="%H:%M:%S")

    asyncio.run(grabs_folder(source))