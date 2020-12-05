from telegram.ext import run_async
import telegram
from json import dump, dumps, load
import graph_api

class Commands():
    def __init__(self):
        pass

    def start(self, bot, update):
        kb = [[
            telegram.KeyboardButton('/coin'),
            telegram.KeyboardButton('/help'), 
            telegram.KeyboardButton('/about')
        ]]
        kb_markup = telegram.ReplyKeyboardMarkup(kb, resize_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id, text="Choose a command", reply_markup=kb_markup)

    def help(self, bot, update):
        msg = '/coin <coin name> - to get info about uniswap coin\n'
        msg += '/about - info about the bot'
        update.message.reply_text(msg)

    def about(self, bot, update):
        msg = 'Created by Thanh Phuong Vu Thi, Son Luong Tran and Phuong Lihn Thi Tran for TheGraph'
        update.message.reply_text(msg)

    @run_async
    def coin(self, bot, update, args):
        '''Shows the current price of one given cryptocurrency'''

        bot.sendChatAction(chat_id=update.message.chat_id, action='typing')

        if len(args) == 0:
            err_msg = 'You should specify coin ticker\n'
            err_msg += '/coin <coin name>'
            bot.send_message(chat_id=update.message.chat_id, text=err_msg)
            return

        coin = args[0].upper()
        coin_info = graph_api.get_token_info(coin)

        if len(coin_info) == 0:
            bot.send_message(chat_id=update.message.chat_id, text=f'Couldn\'t find coin {coin}!')
            return
        else:
            coin_info = max(coin_info, key=lambda t: float(t['totalLiquidity']) * float(t['derivedETH']))

        euro_eth = graph_api.get_euro_eth()

        id = coin_info['id']
        eth = float(coin_info['derivedETH'])
        euro = eth / euro_eth
        total_liquidity = float(coin_info['totalLiquidity']) * eth
        tx_count = int(coin_info['txCount'])
        total_supply = int(coin_info['totalSupply'])
        link = f'https://info.uniswap.org/token/{id}/'

        msg = f'Current {coin_info["name"]} ({coin}) Price:\n'
        msg += f'{euro:.6f} €\n'
        msg += f'{eth:.8f} ETH\n\n'
        msg += f'totalLiquidity: {total_liquidity:.3f} ETH\n'
        msg += f'txCount: {tx_count}\n'
        msg += f'totalSupply: {total_supply}\n'
        msg += link
        bot.send_message(chat_id=update.message.chat_id, text=msg)
