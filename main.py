from data import config
from core import ZetaChain
from core.utils import random_line, logger
import asyncio
import random

async def retry_function(func, thread, *args, **kwargs):
    while True:
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            logger.error(f"Thread {thread} | Function execution error {func.__name__}: {e}")
            await asyncio.sleep(10)

async def send_self_zeta(zetachain,thread):
    if await retry_function(zetachain.check_completed_task, thread, "SEND_ZETA") and config.SENDS_QUESTS['send_zeta'][0]:
        # status, tx_hash = await zetachain.transfer_zeta()
        status, tx_hash = await retry_function(zetachain.transfer_zeta, thread)
        if status:
            logger.success(f"Thread {thread} | Sent zeta to myself! {zetachain.web3_utils.acct.address}:{tx_hash}")
        else:
            logger.error(f"Thread {thread} | Didn't send zeta to myself! {zetachain.web3_utils.acct.address}:{tx_hash}")
        await zetachain.sleep_random(10,12)
    else:
        logger.info(f"Thread {thread} | {zetachain.web3_utils.acct.address} had sent and recieved before.")

async def swap_bnb(zetachain,thread):
    if await zetachain.check_completed_task("RECEIVE_BNB") and config.SENDS_QUESTS['send_bnb'][0]:
        # status, tx_hash = await zetachain.transfer_bnb()
        status, tx_hash = await retry_function(zetachain.transfer_bnb, thread)
        if status:
            logger.success(f"Thread {thread} | Made transaction zeta -> bnb.bsc! {zetachain.web3_utils.acct.address}:{tx_hash}")
            have_bnb = True
        else:
            logger.error(f"Thread {thread} | Didn't do transaction zeta -> bnb.bsc! {zetachain.web3_utils.acct.address}:{tx_hash}")
            have_bnb = False
        await zetachain.sleep_random(10,15)
    else:
        logger.info(f"Thread {thread} | {zetachain.web3_utils.acct.address} had swap bnb before.")

async def swap_eth(zetachain,thread):
    if await zetachain.check_completed_task("RECEIVE_ETH") and config.SENDS_QUESTS['send_eth'][0]:
        # status, tx_hash = await zetachain.transfer_eth()
        status, tx_hash = await retry_function(zetachain.transfer_eth, thread)
        if status:
            logger.success(f"Thread {thread} | Made transaction zeta -> eth.eth! {zetachain.web3_utils.acct.address}:{tx_hash}")
        else:
            logger.error(f"Thread {thread} |  Didn't do transaction zeta -> eth.eth! {zetachain.web3_utils.acct.address}:{tx_hash}")
        await zetachain.sleep_random(10,15)       
    else:
        logger.info(f"Thread {thread} | {zetachain.web3_utils.acct.address} had swap eth before.")

async def swap_btc(zetachain,thread):
    if await zetachain.check_completed_task("RECEIVE_BTC") and config.SENDS_QUESTS['send_btc'][0]:
        # status, tx_hash = await zetachain.transfer_btc()
        status, tx_hash = await retry_function(zetachain.transfer_btc, thread)
        if status:
            logger.success(f"Thread {thread} | Made transaction zeta -> btc.btc! {zetachain.web3_utils.acct.address}:{tx_hash}")
        else:
            logger.error(f"Thread {thread} |  Didn't do transaction zeta-> btc.btc! {zetachain.web3_utils.acct.address}:{tx_hash}")
            await zetachain.sleep_random(10,15)
    else:
        logger.info(f"Thread {thread} | {zetachain.web3_utils.acct.address} had swap btc before.")

functions = [send_self_zeta, swap_bnb, swap_eth, swap_btc]

async def ZC(thread):
    logger.info(f"Thread {thread} | Started work")
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

        # Do enroll
        # if not await zetachain.check_enroll():
        #     # status, tx_hash = await zetachain.enroll()
        #     status, tx_hash = await retry_function(zetachain.enroll, thread)
        #     if status:
        #         logger.success(f"Thread {thread} | Completed enroll! {zetachain.web3_utils.acct.address}:{tx_hash}")
        #         logger.info(f"Thread {thread} | Sleeps 2s after enroll!")

        #         await asyncio.sleep(20)
        #         await zetachain.new_session()
        #     else:
        #         logger.error(f"Thread {thread} | Didn't comply enroll! {zetachain.web3_utils.acct.address}:{tx_hash}")
        # else:
        #     logger.info(f"Thread {thread} | {zetachain.web3_utils.acct.address} already enrolled before.")
        
        # random launch
        if not config.FAST_MODE:
            await zetachain.sleep_random(10,50)
        
        random.shuffle(functions)
        for func in functions:
            await func(zetachain,thread)
            if not config.FAST_MODE:
                await zetachain.sleep_random(120,150)
            else:
                await zetachain.sleep_random(3,10)
        
        # approval bnb
        if float(await zetachain.check_approve_bnb())+0.001 < config.APPROVES['bnb_approve']:
            # status, tx_hash = await zetachain.approve_bnb()
            status, tx_hash = await retry_function(zetachain.approve_bnb, thread)
            if status:
                logger.success(
                    f"Thread {thread} | Approved {config.APPROVES['bnb_approve']} bnb! {zetachain.web3_utils.acct.address}:{tx_hash}")
            else:
                logger.success(f"Thread {thread} | Not Approved bnb! {zetachain.web3_utils.acct.address}:{tx_hash}")
            await zetachain.sleep_random(10,15)        
        else:
            logger.info(f"Thread {thread} | {zetachain.web3_utils.acct.address} had enough bnb approved before.")

        # adds BNB to the pool
        #  1. not completed
        #  2. config send_bnb true
        #  3. config pool use is true
        #  4. bnb balance > pools send_bnb value
        if not await zetachain.check_completed_task("POOL_DEPOSIT_ANY_POOL"):
            logger.info(f"Thread {thread} | {zetachain.web3_utils.acct.address} do not need to add bnb pool, task completed already.")
        elif not config.SENDS_QUESTS['send_bnb'][0]:
            logger.info(f"Thread {thread} | {zetachain.web3_utils.acct.address} do not need to add bnb pool, send_bnb is false")
        elif not config.POOLS['use']:
            logger.info(f"Thread {thread} | {zetachain.web3_utils.acct.address} do not need to add bnb pool, use pool is false")
        elif not float(await zetachain.check_approve_bnb())+0.0001 >= config.POOLS['send_bnb']:
            logger.error(f"Thread {thread} | {zetachain.web3_utils.acct.address} can not add bnb pool, bnb approval not enough:{config.POOLS['send_bnb']} ")
        elif not zetachain.web3_utils.w3.from_wei(zetachain.web3_utils.balance_of_erc20(zetachain.web3_utils.acct.address, '0x48f80608B672DC30DC7e3dbBd0343c5F02C738Eb'), 'ether') >= config.POOLS['send_bnb']:
            logger.error(f"Thread {thread} | {zetachain.web3_utils.acct.address} can not add bnb pool, bnb balance not enough:{config.POOLS['send_bnb']} ")
        else:
        # status, tx_hash = await zetachain.add_liquidity()
            status, tx_hash = await retry_function(zetachain.add_liquidity, thread)
            if status:
                logger.success(f"Thread {thread} | Added liquidityzeta-bnb! {zetachain.web3_utils.acct.address}:{tx_hash}")
            else:
                logger.error(f"Thread {thread} | Cant Added liquidity zeta-bnb! {zetachain.web3_utils.acct.address}:{tx_hash}")
        
        
        # marks completed quests
        logger.info(f"Thread {thread} | wait 180s to claim xps...")
        # await asyncio.sleep(180)
        if not config.FAST_MODE:
            await zetachain.sleep_random(120,180)
        else:
            await zetachain.sleep_random(3,10)
    
        claimed = await zetachain.claim_tasks()
        if claimed:
            logger.success(f"Thread {thread} | Claimed {claimed} quests!! {zetachain.web3_utils.acct.address}")
        else:
            logger.warning(f"Thread {thread} | No quests for claim! {zetachain.web3_utils.acct.address}")

        await zetachain.logout()
        logger.info(f"Thread {thread} | Slept {await zetachain.sleep()} seconds")

    logger.info(f"Thread {thread} | Finished work")


async def main():
    # print("Автор софта: https://t.me/ApeCryptor")

    thread_count = int(input("thread account: "))
    thread_count = 10 if thread_count > 10 else thread_count
    # thread_count = 1
    tasks = []
    for thread in range(1, thread_count+1):
        tasks.append(asyncio.create_task(ZC(thread)))

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
