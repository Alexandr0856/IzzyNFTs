import time
import redis

import pyrogram.types
import sqlalchemy
import message_text
from auth import App
import logging as log
from pyrogram import filters
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from models import Base, Session, User, engine

Base.metadata.create_all(engine)
session = Session()
session.commit()

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
        message.reply(message_text.first_start[0], reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(
                'Add new wallet',
                callback_data='add_wallet'
            )]]
        ))

    except sqlalchemy.exc.IntegrityError:
        log.info(f'Reconnect old user: {user_info.username} - {user_info.id}')
        session.rollback()

        message.reply(message_text.second_start, reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(
                    'Add new wallet',
                    callback_data='add_wallet'
                )],
                [InlineKeyboardButton(
                    'Menu',
                    callback_data='main_menu'
                )]
            ]
        ))

    except Exception as error:
        print(error)
        log.error(error)
        session.rollback()


@App.on_message(filters.command('db') & filters.user(session.query(User).filter(User.admin == True).all()))
def db_view(client, message):

    all_rows = session.query(User).all()
    text = ''
    for row in all_rows:
        text += f'Name: {row.name}, Id: {row.user_id}, Admin: {row.admin}\n'

    message.reply(text)


@App.on_callback_query()
def on_callback(client, query):
    match query.data:
        case 'add_wallet':
            add_wallet(query)
        case 'confirm_wallet':
            confirm_wallet(query)


def add_wallet(query):
    App.send_message(query.from_user.username, message_text.add_wallet, reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(
                    'Confirm',
                    callback_data='confirm_wallet'
                )]
            ]
    ))


def confirm_wallet(query):
    with redis.Redis() as client:
        wallet = client.hget('AddedWallet', query.from_user.id).decode()
        client.hdel('AddedWallet', query.from_user.id)

    App.send_message(query.from_user.username, message_text.added_wallet(wallet), reply_markup=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(
                'MainMenu',
                callback_data='main_menu'
            )]
        ]
    ))


if __name__ == '__main__':
    App.run()
