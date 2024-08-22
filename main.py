from data import config
from core import ZetaChain
from core.utils import random_line, logger
import asyncio


async def ZC(thread):
    logger.info(f"Thread {thread} | Started work")
    run_once = False
    while True:
        act = await random_line('data/accounts.txt')
        if not act: break

        if '::' in act:
            private_key, proxy = act.split('::')
        else:
            private_key = act
            proxy = None
        logger.info(f"Thread {thread} | with proxy {proxy}")
        zetachain = ZetaChain(key=private_key, thread=thread, proxy=proxy)  
        await zetachain.claim_rewards()
        await zetachain.collect_zrc20()
        await zetachain.collect_zeta()
        await zetachain.logout()
      

    logger.info(f"Thread {thread} | Finished work")


async def main():
    thread_count = 1
    tasks = []
    for thread in range(1, thread_count+1):
        tasks.append(asyncio.create_task(ZC(thread)))

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
