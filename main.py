import message_text
import auth
import logging as log
import sqlalchemy
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from models import Base, Session, User, engine

App = Client("IzzyNFTs", api_id=auth.API_ID, api_hash=auth.API_HASH, bot_token=auth.BOT_TOKEN)

log.basicConfig(filename='app.log', format='%(asctime)s - %(message)s\n\n', level=log.INFO)


@App.on_message(filters.command('start'))
def start(client, message):
    user_info = message.from_user
    session.add(User(
        id=user_info.id,
        name=user_info.username
        ))

    try:
        session.commit()
        log.info(f'Connect new user: {user_info.username} - {user_info.id}')
        message.reply(message_text.first_start, reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(
                'Add new wallet',
                callback_data='add_wallet'
            )]]
        ))

    except sqlalchemy.exc.IntegrityError:
        message.reply(message_text.second_start)
        log.info(f'Reconnect old user: {user_info.username} - {user_info.id}')
        session.rollback()

    except Exception as error:
        log.error(error)
        session.rollback()


@App.on_message(filters.command('db'))
def db_view(client, message):
    user = session.query(User).filter(User.user_id == message.from_user.id).first()
    if user.admin:
        all_rows = session.query(User).all()
        text = ''
        for row in all_rows:
            text += f'Name: {row.name}, Id: {row.user_id}, Admin: {row.admin}\n'
        print(text)
        message.reply(text)
    else:
        message.reply("I don't know this command")


@App.on_callback_query()
def add_wallet(client, query):
    if query.data == 'add_wallet':
        App.send_message(query.from_user.username, 'Please input your public key:')
    else:
        print(10)


if __name__ == '__main__':
    session = Session()
    Base.metadata.create_all(engine)

    App.run()
