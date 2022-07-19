first_start = [
    """Hi 👋Please, connect your crypto wallet to use the bot. \
    It will sync with your Telegram username for convenience, \
    this will allow other users to view your NFTs and for you to purchase NFTs of others.""",

    """To do this, click on the button below, \
    connect the wallet on the site and wait for the message about registration completion"""
]


second_start = """Рад тебя снова здесь видеть"""


add_wallet = """1. Follow this link to the page: [go to site](https://t.me/c/1766695668/7249)
2. Connect your wallet.
3. Click on the confirm button."""


def added_wallet(wallet):
    if wallet is None:
        return 'No new wallets added.'
    elif wallet == 'OLD':
        return 'This address has already been added.'
    return f'You have added the following address as a wallet:\n{wallet}'

