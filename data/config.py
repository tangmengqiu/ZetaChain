# реф ссылка
REF_LINK = 'https://hub.zetachain.com/xp?code=YWRkcmVzcz0weGJDZDJCMzE3MDYxODY1RTdhZWZERTc0MDBGOGQ4REIxNDY4MzU2MzAmZXhwaXJhdGlvbj0xNzEwMjM2Mzk4JnI9MHg5YjMxYjAzMTEzOWEwNjI4YjU2NjA2YjhlMDlhODQ2YTVjNThmOGRjNzc5NjU4ZTNlNmNkMDA0ODhlYjdmMzk0JnM9MHgwOTkwM2JjNzIxOGI5ZTRiOTJkZjM4M2UxZDU0MDk2YWVhZDdiY2UzZjJkZDU4NGM0MjE4ZDhhZGI3ZjViMjMwJnY9Mjc%3D'

# задержка в секундах между аккаунтами

DELAY = {
    "account": (5, 10),       # Задержка в секундах между аккаунтами
    "transaction": (20, 30),  # Задержка в секундах между транзакциями
    "quest": (5, 10)          # Задержка в секундах между квестами
}

# Чтобы отправлять транзакции указывать True/False и через запятую кол-во монет, я указал минимум.
SENDS_QUESTS = {
    "send_zeta": [True, 1.5],         # Сколько zeta отправить самому себе?
    "send_bnb": [True, 0.03],      # How much zeta to send for a transaction zeta->bnb.bsc (izumi)
    "send_eth": [True, 0.02],     # How much zeta to send for a transaction zeta->eth.eth (izumi)
    "send_btc": [True, 0.025],      # How much zeta to send for a transaction zeta->btc.btc (izumi)
}

# To send to pools, specify True/False in use.
POOLS = {
    "use": True,              # использовать пулы
    "send_bnb": 0.0000055,       # how much to send bnb to the pool
    "send_zeta": 0.001,     # how much to send zeta to the pool
    # range pool
    "stzeta": 0.001  #должно быть меньше zeta_to_stzeta и zeta_to_wzeta с EDDY_SWAP
}
# POOLS = {
#     "send_bnb": 0.0001,       # сколько отправлять бнб в пул
#     "send_zeta": 0.0001,      # сколько отправлять zeta в пул

#     # range pool
#     "stzeta": 0.001  #должно быть меньше zeta_to_stzeta и zeta_to_wzeta с EDDY_SWAP
# }

# APPROVES = {
#     "bnb_approve": 0.03 # number of bnb for approval
# }
APPROVES = {
    "bnb_approve": 0.03,  # кол-во бнб для апрува
    "stzeta_approve": 0.1,  # кол-во stzeta для апрува
    "wzeta_approve": 0.1,   # кол-во wzeta для апрува
    "stzeta_accumulated_approve": 0.2
}

# свап на app.eddy.finance/swap
EDDY_SWAP = {
    "zeta_to_stzeta": 0.0013,  # кол-во zeta для свапа на stzeta
    "zeta_to_wzeta": 0.001,   # кол-во zeta для свапа на wzeta, можно не больше zeta_to_stzeta
}

ACCUMULATED_FINANCE = {
    "zeta_to_stzeta": 0.0001,     # кол-во zeta для свапа на stzeta на accumulated finance
    "stzeta_to_wstzeta": 0.0001  # кол-во stzeta для свапа на wstzeta на accumulated finance, должно быть не больше zeta_to_stzeta
}

FAST_MODE = True #set to true if you run the second time(to finish the task not completed in the 1st round) or want to quickly end

# рпц
RPCs = {
    "zetachain": "https://zetachain-evm.blockpi.network/v1/rpc/public"  # zetachain rpc
}
