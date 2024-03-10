from data import config
from core import ZetaChain
from core.utils import random_line, logger
import asyncio
import random
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

async def add_bnb_pool(zetachain,thread):
    # approval bnb
    if not await zetachain.check_completed_task("POOL_DEPOSIT_ANY_POOL"):
        logger.info(f"Thread {thread} | {zetachain.web3_utils.acct.address} do not need to add bnb pool, task completed already.")
        return
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
            logger.success(f"Thread {thread} | Added liquidity zeta-bnb! {zetachain.web3_utils.acct.address}:{tx_hash}")
        else:
            logger.error(f"Thread {thread} | Cant Added liquidity zeta-bnb! {zetachain.web3_utils.acct.address}:{tx_hash}")

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

async def stake_on_accumulated(zetachain,thread):
    if await zetachain.check_completed_task("ACCUMULATED_FINANCE_DEPOSIT"):
         # swap zeta to stzeta accumulated
        if await zetachain.get_balance_stzeta_accumulated_finance() < config.ACCUMULATED_FINANCE['zeta_to_stzeta']:
            status, tx_hash = await retry_function(zetachain.swap_zeta_to_stzeta_accumulated_finance, thread)
            if status:
                logger.success(f"Thread {thread} | Swap on accumulated finance: zeta -> stzeta! {zetachain.web3_utils.acct.address}:{tx_hash}")
                await zetachain.sleep(config.DELAY['transaction'], logger, thread)
            else:
                logger.error(f"Thread {thread} | Cannot Swap on accumulated finance: zeta -> stzeta! {zetachain.web3_utils.acct.address}:{tx_hash}")
            await zetachain.sleep(config.DELAY['quest'], logger, thread)
        else:
            logger.info(f"Thread {thread} | {zetachain.web3_utils.acct.address} had enough stzeta to stake on accumulated, skip the stake ...")
        # approval stzeta accumulated finance
        if float(await zetachain.allowance_stzeta_accumulated_finance()) + 0.1 < config.APPROVES['stzeta_accumulated_approve']:
            status, tx_hash = await retry_function(zetachain.approve_stzeta_accumulated_finance, thread)
            if status:
                logger.success(f"Thread {thread} | Approved {config.APPROVES['stzeta_accumulated_approve']} stzeta for accumulated finance! {zetachain.web3_utils.acct.address}:{tx_hash}")
                await zetachain.sleep(config.DELAY['transaction'], logger, thread)
            else:
                logger.success(f"Thread {thread} | Cannot Approved stzeta! {zetachain.web3_utils.acct.address}:{tx_hash}")
        else:
            logger.info(f"Thread {thread} | {zetachain.web3_utils.acct.address} had approved enough stzeta to stake, skip approval...")

        # deposite stzeta accumulated finance to wstzeta
        if not await zetachain.allowance_stzeta_accumulated_finance() >= config.ACCUMULATED_FINANCE['stzeta_to_wstzeta']: 
            logger.error(f"Thread {thread} | {zetachain.web3_utils.acct.address} cannot deposite stzeta accumulated finance to wstzeta, stzeta allowance not enough, check config!")
        elif not await zetachain.get_balance_stzeta_accumulated_finance() >= config.ACCUMULATED_FINANCE['stzeta_to_wstzeta']:
            logger.error(f"Thread {thread} | {zetachain.web3_utils.acct.address} cannot deposite stzeta accumulated finance to wstzeta, stzeta balance not enough, check config!")
        else:
            status, tx_hash = await retry_function(zetachain.swap_stzeta_to_wstzeta_accumulated_finance, thread)
            if status:
                logger.success(f"Thread {thread} | Swap on accumulated finance: stzeta -> wstzeta! {zetachain.web3_utils.acct.address}:{tx_hash}")
                await zetachain.sleep(config.DELAY['transaction'], logger, thread)
            else:
                logger.success(f"Thread {thread} | Cannot Swap on accumulated finance: stzeta -> wstzeta! {zetachain.web3_utils.acct.address}:{tx_hash}")
    else:
        logger.info(f"Thread {thread} | {zetachain.web3_utils.acct.address} had staked on accumulated before.")

async def liquidity_on_range(zetachain,thread):
    if not await zetachain.check_completed_task("RANGE_PROTOCOL_VAULT_TRANSACTION"):
        logger.info(f"Thread {thread} | {zetachain.web3_utils.acct.address} had add liquidity on range before... ")
        return
    # approval stzeta 
    if float(await zetachain.allowance_stzeta())+0.1 < config.APPROVES['stzeta_approve']:
        status, tx_hash = await retry_function(zetachain.approve_stzeta, thread)
        if status:
            logger.success(f"Thread {thread} | Approved {config.APPROVES['stzeta_approve']} stzeta! {zetachain.web3_utils.acct.address}:{tx_hash}")
            await zetachain.sleep(config.DELAY['transaction'], logger, thread)
        else:
            logger.success(f"Thread {thread} | Not Approved stzeta! {zetachain.web3_utils.acct.address}:{tx_hash}")
    else:
        logger.info(f"Thread {thread} | {zetachain.web3_utils.acct.address} had approved enough stzeta to add liquidity on range, skip approval...")

    # approve wzeta
    if float(await zetachain.allowance_wzeta()) + 0.1 < config.APPROVES['wzeta_approve']:
        status, tx_hash = await retry_function(zetachain.approve_wzeta, thread)
        if status:
            logger.success(
                f"Thread {thread} | Approved {config.APPROVES['wzeta_approve']} wzeta! {zetachain.web3_utils.acct.address}:{tx_hash}")
            await zetachain.sleep(config.DELAY['transaction'], logger, thread)
        else:
            logger.success(
                f"Thread {thread} | Cannot Approved wzeta! {zetachain.web3_utils.acct.address}:{tx_hash}")
    else:
        logger.info(f"Thread {thread} | {zetachain.web3_utils.acct.address} had approved enough wzeta to add liquidity on range, skip approval...")
    # swap zeta to wzeta on eddy
    if await zetachain.get_wzeta_balance() < config.EDDY_SWAP['zeta_to_wzeta']:
        status, tx_hash = await retry_function(zetachain.swap_zeta_to_wzeta, thread)
        if status:
            logger.success(f"Thread {thread} | made a swap zeta -> wzeta! {zetachain.web3_utils.acct.address}:{tx_hash}")
            await zetachain.sleep(config.DELAY['transaction'], logger, thread)
        else:
            logger.success(
                f"Thread {thread} | Cannot made a swap zeta -> wzeta! {zetachain.web3_utils.acct.address}:{tx_hash}")
    else:
        logger.info(f"Thread {thread} | {zetachain.web3_utils.acct.address} had enough wzeta to add liquidity on range, skip swap zeta -> wzeta ...")
    
    # adds liquidity to the range protocol zeta/stzeta if 
    # the balance stzeta is greater than/equal to POOLS['stzeta'], 
    # if the balance wzeta is greater than/equal to EDDY_SWAP['zeta_to_wzeta'], 
    # if the approval stzeta is greater than/equal to POOLS['stzeta'],
    #  if the approval wzeta is greater than/equal to EDDY_SWAP['zeta_to_wzeta']
    if not await zetachain.check_completed_task("RANGE_PROTOCOL_VAULT_TRANSACTION"):
        logger.info(f"Thread {thread} | {zetachain.web3_utils.acct.address} had add liquidity on range before... ")
    elif not  await zetachain.get_stzeta_balance() >= config.POOLS['stzeta']:
        logger.error(f"Thread {thread} | {zetachain.web3_utils.acct.address} cannot add liquidity on range, not enough stzeta balance... ")
    elif not  await zetachain.get_wzeta_balance() >= config.EDDY_SWAP['zeta_to_wzeta'] - config.EDDY_SWAP['wzeta_offset']:
        logger.error(f"Thread {thread} | {zetachain.web3_utils.acct.address} cannot add liquidity on range, not enough wzeta balance... ")
    elif not await zetachain.allowance_stzeta() >= config.POOLS['stzeta']:
        logger.error(f"Thread {thread} | {zetachain.web3_utils.acct.address} cannot add liquidity on range, not enough stzeta allowance... ")
    elif not await zetachain.allowance_wzeta() >= config.EDDY_SWAP['zeta_to_wzeta']:
        logger.error(f"Thread {thread} | {zetachain.web3_utils.acct.address} cannot add liquidity on range, not enough wzeta allowance... ")
    else:
        status, tx_hash = await retry_function(zetachain.add_liquidity_range, thread)
        if status:
            logger.success(
                f"Thread {thread} | Added liquidity stzeta-wzeta! {zetachain.web3_utils.acct.address}:{tx_hash}")
            await zetachain.sleep(config.DELAY['transaction'], logger, thread)
        else:
            logger.error(
                f"Thread {thread} | Cannot Added liquidity stzeta-wzeta! {zetachain.web3_utils.acct.address}:{tx_hash}")
        await zetachain.sleep(config.DELAY['quest'], logger, thread)

#  swaps zeta to stzeta on eddy finance
async def swap_on_eddy(zetachain,thread):
    if await zetachain.check_completed_task("EDDY_FINANCE_SWAP"):
        status, tx_hash = await retry_function(zetachain.swap_zeta_to_stzeta, thread)
        if status:
            logger.success(f"Thread {thread} | Made a swap on eddy zeta -> stzeta! {zetachain.web3_utils.acct.address}:{tx_hash}")
            await zetachain.sleep(config.DELAY['transaction'], logger, thread)
        else:
            logger.error(f"Thread {thread} | Not Made a swap on eddy zeta -> stzeta! {zetachain.web3_utils.acct.address}:{tx_hash}")
        await zetachain.sleep(config.DELAY['quest'], logger, thread)
    else:
        logger.info(f"Thread {thread} | {zetachain.web3_utils.acct.address} had swap on eddy before.")
# swaps zeta to wzeta on zetaswap
async def swap_on_zetaswap(zetachain,thread):
    if not await zetachain.check_completed_task("ZETA_SWAP_SWAP"):
        logger.info(f"Thread {thread} | {zetachain.web3_utils.acct.address} had swap on zetaswap before... ")
    else:
        if float(await zetachain.allowance_zetaswap_wzeta()) + 0.1 < config.APPROVES['zetaswap_wzeta_approve'][0]:
            status, tx_hash = await retry_function(zetachain.approve_zetaswap_wzeta, thread)
            if status:
                logger.success(
                    f"Thread {thread} | Approved wzeta for zetaswap! {zetachain.web3_utils.acct.address}:{tx_hash}")
                await zetachain.sleep(config.DELAY['transaction'], logger, thread)
            else:
                logger.error(
                    f"Thread {thread} | cannot approved wzeta for zetaswap! {zetachain.web3_utils.acct.address}:{tx_hash}")
        else:
            logger.info(f"Thread {thread} | {zetachain.web3_utils.acct.address} had swap enough allowance for zetaswap ")
        status, tx_hash = await retry_function(zetachain.zetaswap_wzeta_to_eth, thread)
        if status:
            logger.success(f"Thread {thread} | swap on zetaswap: wzeta -> eth.eth! {zetachain.web3_utils.acct.address}:{tx_hash}")
            await zetachain.sleep(config.DELAY['transaction'], logger, thread)
        else:
            logger.error(f"Thread {thread} | cannot swap on zetaswap: wzeta -> eth.eth! {zetachain.web3_utils.acct.address}:{tx_hash}")

async def stake_on_zetaearn(zetachain,thread):
    if await zetachain.check_completed_task("ZETA_EARN_STAKE"):
            status, tx_hash = await retry_function(zetachain.stake_on_zetachain, thread)
            if status:
                logger.success(f"Thread {thread} | stake zeta! {zetachain.web3_utils.acct.address}:{tx_hash}")
                await zetachain.sleep(config.DELAY['transaction'], logger, thread)
            else:
                logger.error(
                    f"Thread {thread} | Cant stake zeta! {zetachain.web3_utils.acct.address}:{tx_hash}")
    else:
        logger.info(f"Thread {thread} | {zetachain.web3_utils.acct.address} had staked on zetaearn before... ")

async def mint_on_ultiverse_badge(zetachain,thread):
    if await zetachain.check_completed_task("ULTIVERSE_MINT_BADGE"):
        status, tx_hash = await retry_function(zetachain.min_ultiverse_badge, thread)
        if status:
            logger.success(f"Thread {thread} | Mint on ultiverse! {zetachain.web3_utils.acct.address}:{tx_hash}")
            await zetachain.sleep(config.DELAY['transaction'], logger, thread)
        else:
            logger.error(
                f"Thread {thread} | Cant mint on ultiverse! {zetachain.web3_utils.acct.address}:{tx_hash}")
    else:
        logger.info(f"Thread {thread} | {zetachain.web3_utils.acct.address} had mint badge before... ")    
# functions = [send_self_zeta, swap_bnb, swap_eth, swap_btc,swap_eddy_then_range_pool,stake_on_accumulated]




async def execute_graph(graph, zetachain, thread):
    nodes = list(graph.keys())
    random.shuffle(nodes)

    for node in nodes:
        predecessors = [func for func in graph if node in graph[func]]
        if not predecessors:
            # print(f"execute: {node}")
            await node(zetachain, thread)
            if node in graph:
                del graph[node]
            if not config.FAST_MODE:
                await zetachain.sleep_random(20,30)
            else:
                await zetachain.sleep_random(3,10)
            break

async def ZC(thread):
    logger.info(f"Thread {thread} | Started work")
    run_once = True
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
        # random launch
        if not config.FAST_MODE:
            await zetachain.sleep_random(10,50)
        
        # random.shuffle(functions)
        # for func in functions:
        #     await func(zetachain,thread)
        #     if not config.FAST_MODE:
        #         await zetachain.sleep_random(120,150)
        #     else:
        #         await zetachain.sleep_random(3,10)
        # 有向无环图
        DAG = {
            # make sure a excuted before b
            # function_a: [function_b],
            send_self_zeta: [],
            swap_bnb: [add_bnb_pool],
            add_bnb_pool:[],
            swap_eth:[],
            swap_btc:[],
            swap_on_eddy:[liquidity_on_range],
            liquidity_on_range:[],
            stake_on_accumulated:[],
            swap_on_zetaswap:[],
            stake_on_zetaearn:[],
            mint_on_ultiverse_badge:[]
        }   
        
        while DAG:
            await execute_graph(DAG, zetachain, thread)
        # marks completed quests
        logger.info(f"Thread {thread} | wait xx s to claim xps...")
        # await asyncio.sleep(180)
        if not config.FAST_MODE:
            await zetachain.sleep_random(12,30)
        else:
            await zetachain.sleep_random(3,10)
    
        claimed = await zetachain.claim_tasks()
        if claimed:
            logger.success(f"Thread {thread} | Claimed {claimed} quests!! {zetachain.web3_utils.acct.address}")
        else:
            logger.warning(f"Thread {thread} | No quests for claim! {zetachain.web3_utils.acct.address}")

        await zetachain.logout()
        await zetachain.sleep(config.DELAY['account'], logger, thread)
        if run_once:
            break

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
