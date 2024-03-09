# реф ссылка
REF_LINK = 'https://hub.zetachain.com/xp?code=YWRkcmVzcz0weGJDZDJCMzE3MDYxODY1RTdhZWZERTc0MDBGOGQ4REIxNDY4MzU2MzAmZXhwaXJhdGlvbj0xNzEwMjM2Mzk4JnI9MHg5YjMxYjAzMTEzOWEwNjI4YjU2NjA2YjhlMDlhODQ2YTVjNThmOGRjNzc5NjU4ZTNlNmNkMDA0ODhlYjdmMzk0JnM9MHgwOTkwM2JjNzIxOGI5ZTRiOTJkZjM4M2UxZDU0MDk2YWVhZDdiY2UzZjJkZDU4NGM0MjE4ZDhhZGI3ZjViMjMwJnY9Mjc%3D'

# задержка в секундах между аккаунтами
# api key native.org. You can use mine, but preferably yours. Guide on how to get it - https://telegra.ph/Kak-sozdat-api-key-dlya-nativeorg-03-09
NATIVE_API_KEY = "96787ef44ed0ecd6ec8533aa317e37ef75fc5010"

DELAY = {
    "account": (5, 6),       # Задержка в секундах между аккаунтами
    "transaction": (20, 30),  # Задержка в секундах между транзакциями
    "quest": (20, 30)          # Задержка в секундах между квестами
}
# Чтобы отправлять транзакции указывать True/False и через запятую кол-во монет, я указал минимум.
SENDS_QUESTS = {
    "send_zeta": [True, 1.5],         # Сколько zeta отправить самому себе?
    "send_offset": 0.005,
    "send_bnb": [True, 0.03],      # How much zeta to send for a transaction zeta->bnb.bsc (izumi)
    "send_eth": [True, 0.02],      # How much zeta to send for a transaction zeta->eth.eth (izumi)
    "send_btc": [True, 0.025],     # How much zeta to send for a transaction zeta->btc.btc (izumi)
}
# To send to pools, specify True/False in use.
POOLS = {
    "use": True,            # использовать пулы
    "send_bnb": 0.0001,  # how much to send bnb to the pool
    "send_bnb_offset": 0.00003,
    "send_zeta": 0.02,     # how much to send zeta to the pool
    # to make zeta random from [send_zeta- offset, send_zeta + offset] to zeta-bnb pool,
    "offset":  0.005,
    # range pool
    # must be less than zeta_to_stzeta and zeta_to_wzeta with EDDY_SWAP
    "stzeta": 0.0015  
}
APPROVES = {
    "bnb_approve": 0.2,  # кол-во бнб для апрува
    "stzeta_approve": 0.25,  # кол-во stzeta для апрува
    "wzeta_approve": 0.25,   # кол-во wzeta для апрува
    #approve random from [approve - offset, approve + offset]
    "offset": 0.05, 
    "stzeta_accumulated_approve": 0.3,
    "zetaswap_wzeta_approve": [1, 2]
}
# swap on app.eddy.finance
# so can add liqility on range
EDDY_SWAP = {
    "zeta_offset": 0.002,
    "zeta_to_stzeta": 0.02,  # кол-во zeta для свапа на stzeta
    "wzeta_offset": 0.002,
    "zeta_to_wzeta": 0.015,   # number of zeta for swap on wzeta, no more than zeta_to_stzeta possible
}
# mint and stake on accumulated
ACCUMULATED_FINANCE = {
    "zeta_to_stzeta": 0.02,     # кол-во zeta для свапа на stzeta на accumulated finance
    "offset": 0.002,
    # number of stzeta for swap to wstzeta for accumulated finance, should not be more than zeta_to_stzeta
    "stzeta_to_wstzeta": 0.015  
}

# стейк на ZetaChain
STAKE_ZETACHAIN= {
    "zeta_count": 0.0012,  # кол-во zeta для стейка. минимум 0.0011
    "offset": 0.00003
}

# свап wzeta на ETH.ETH через zetaswap. [x,y]. х - минимальное кол-во, у - максимальное кол-во. Рандом до 5 цифр после точки
ZETASWAP = {
    "wzeta_count": [0.0015, 0.0025]
}
FAST_MODE = True #set to true if you run the second time(to finish the task not completed in the 1st round) or want to quickly end
# рпц
RPCs = {
    "zetachain": "https://zetachain-evm.blockpi.network/v1/rpc/public"  # zetachain rpc
}
