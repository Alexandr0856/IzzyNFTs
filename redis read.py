from models import Base, Session, User, Wallet, engine
import logging as log
import redis

log.basicConfig(filename='redis_read.log', format='%(asctime)s - %(message)s\n\n', level=log.INFO)


def main():
    with redis.Redis() as client:
        with Session() as session:
            while True:
                try:
                    redis_msg = client.brpop('Queue')[1].decode().split(',')
                    user_id = int(redis_msg[0])
                    address = redis_msg[1]

                    wallets_of_user = session.query(Wallet).filter(Wallet.user_id == user_id).all()
                    if address not in [wal.address for wal in wallets_of_user]:
                        wallet = Wallet(
                            address=address,
                            chain=redis_msg[2],
                            user_id=user_id,
                            name=f'Wallet {len(wallets_of_user)+1}')
                        session.add(wallet)
                        session.commit()
                    else:
                        address = 'OLD'

                    client.hset('AddedWallet', user_id, address)
                    msg = f'User: {user_id}, wallet: {address}, chain: {redis_msg[2]}'
                    log.info(msg)
                    print(msg)

                except Exception as error:
                    log.error(error)
                    print(error)


if __name__ == '__main__':
    main()
