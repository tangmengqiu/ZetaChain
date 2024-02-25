# реф ссылка
REF_LINK = 'https://hub.zetachain.com/xp?code=YWRkcmVzcz0weGJDZDJCMzE3MDYxODY1RTdhZWZERTc0MDBGOGQ4REIxNDY4MzU2MzAmZXhwaXJhdGlvbj0xNzEwMjM2Mzk4JnI9MHg5YjMxYjAzMTEzOWEwNjI4YjU2NjA2YjhlMDlhODQ2YTVjNThmOGRjNzc5NjU4ZTNlNmNkMDA0ODhlYjdmMzk0JnM9MHgwOTkwM2JjNzIxOGI5ZTRiOTJkZjM4M2UxZDU0MDk2YWVhZDdiY2UzZjJkZDU4NGM0MjE4ZDhhZGI3ZjViMjMwJnY9Mjc%3D'

# задержка в секундах между аккаунтами
DELAY = (5, 10)

# Чтобы отправлять транзакции указывать True/False и через запятую кол-во монет, я указал минимум.
SENDS_QUESTS = {
    "send_zeta": [True, 1.5],         # Сколько zeta отправить самому себе?
    "send_bnb": [True, 0.03],      # How much zeta to send for a transaction zeta->bnb.bsc (izumi)
    "send_eth": [True, 0.04],     # How much zeta to send for a transaction zeta->eth.eth (izumi)
    "send_btc": [True, 0.035],      # How much zeta to send for a transaction zeta->btc.btc (izumi)
}

# To send to pools, specify True/False in use.
POOLS = {
    "use": True,              # использовать пулы
    "send_bnb": 0.0000051,       # how much to send bnb to the pool
    "send_zeta": 0.019     # how much to send zeta to the pool
}

APPROVES = {
    "bnb_approve": 0.021 # number of bnb for approval
}

# рпц
RPCs = {
    "zetachain": "https://zetachain-evm.blockpi.network/v1/rpc/public"  # zetachain rpc
}
