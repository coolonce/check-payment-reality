import os
from attr import fields

from flask import Flask, escape, request
import requests
from bitrix24 import *

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import message
from aiogram.utils import executor

TOKEN = "1920575611:AAFIuquH_Z7lDvj8ZuJk0LHa00YnpQbHHzo"


import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.DEBUG)

bot = Bot(token=TOKEN)

bx24 = Bitrix24('https://property.bitrix24.ru/rest/2955/0uxepsze4xzwu3vk/')

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/success', methods=["GET"])
    def success():
        tg_id = request.args.get("invId")
        # result = bx24.callMethod('crm.deal.list', filter={'ID': tg_id})
        result = bx24.callMethod('crm.deal.get/?id='+str(tg_id))
        print(result)
        send_message(result)
        return "true"
    

    

    @app.route('/')
    def hello():
        return "hello"

    return app

def send_message(deal):
    chat_id = deal['TITLE'].split(':')[1]

    method = "sendMessage"
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    data = {"chat_id": chat_id, "text": deal['COMMENTS']}
    requests.post(url, data=data)

    # await bot.send_message(chat_id=chat_id, text=deal['COMMENTS'])
    print(chat_id)
    close_deal(deal['ID'])


def close_deal(deal_id):
    result = bx24.callMethod('crm.deal.update/?id='+str(deal_id), fields={'STAGE_ID':'CLOSE'})
    print("CLOSE")
    print(result)
    