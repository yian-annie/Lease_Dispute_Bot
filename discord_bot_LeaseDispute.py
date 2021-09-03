#!/user/bin/env python
# -*- coding: utf-8 -*-

import logging
import discord
import json
import re

from pprint import pprint
from Lease_Dispute import runLoki

logging.basicConfig(level=logging.CRITICAL)

# <取得多輪對話資訊>
client = discord.Client()

leaseTemplate ={"contractStandBOOL": None, #425_tb1確認租賃契約成立
                "movedInBOOL":None,        #425_tb2租賃物已交付承租人占有
                "houseSoldBOOL": None,     #425_tb3所有權已讓與第三人
                "updatetime":"datetime"}

mscDICT = {
    # "userID": {creditTemplate, mortgageTemplate}
    #"PeterWolf":leaseTemplate,
    #"怡安":leaseTemplate
}
# </取得多輪對話資訊>


with open("account.info", encoding="utf-8") as f:
    accountDICT = json.loads(f.read())
# 另一個寫法是：accountDICT = json.load(open("account.info", encoding="utf-8"))

from ArticutAPI import Articut
articut = Articut(username=accountDICT["username"], apikey=accountDICT["apikey"])

punctuationPat = re.compile("[,\.\?:;，。？、：；\n]+")

def getLokiResult(inputSTR):
    punctuationPat = re.compile("[,\.\?:;，。？、：；\n]+")
    inputLIST = punctuationPat.sub("\n", inputSTR).split("\n")
    filterLIST = []
    resultDICT = runLoki(inputLIST, filterLIST)
    print("Loki Result => {}".format(resultDICT))
    return resultDICT


class BotClient(discord.Client):

    async def on_ready(self):
        print('Logged on as {} with id {}'.format(self.user, self.user.id))

    async def on_message(self, message):
        # Don't respond to bot itself. Or it would create a non-stop loop.
        # 如果訊息來自 bot 自己，就不要處理，直接回覆 None。不然會 Bot 會自問自答個不停。
        if message.author == self.user:
            return None

        print("收到來自 {} 的訊息".format(message.author))
        print("訊息內容是 {}。".format(message.content))
        if self.user.mentioned_in(message):
            print("本 bot 被叫到了！")
            msg = message.content.replace("<@!{}> ".format(self.user.id), "")
            if msg == 'ping':
                await message.reply('pong')
            elif msg == 'ping ping':
                await message.reply('pong pong')
            else:
                #從這裡開始接上 NLU 模型
                responseSTR = "我是預設的回應字串…你會看到我這串字，肯定是出了什麼錯！"

                inputLIST = [msg]
                filterLIST = []
                resultDICT = botRunLoki(inputLIST, filterLIST)
                print("Result => {}".format(resultDICT))

                mscDICT[message.author] = leaseTemplate
                
                
                
                await message.reply(responseSTR)


            





if __name__ == "__main__":
    client = BotClient()
    client.run(accountDICT["discord_token"])    
   
  