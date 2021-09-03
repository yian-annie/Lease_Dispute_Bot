#!/user/bin/env python
# -*- coding: utf-8 -*-

import logging
import discord
import json
import re

from pprint import pprint
from Lease_Dispute import runLoki
from Lease_Dispute import botRunLoki

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
                resultDICT = botRunLoki(inputLIST,filterLIST)
                print("Result => {}".format(resultDICT))

                mscDICT[message.author] = leaseTemplate
                
                if resultDICT[confirm_Security_Deposit_BOOL] == True:
                    responseSTR = """押金的作用，是為了擔保您(承租人)在租賃關係中所生的租金債務或是損害賠償責任
                                  因此，如果您沒有欠房東租金或是需要負擔損害賠償責任，
                                  那麼在租賃關係消滅(例如租期屆滿或租賃契約終止)，且您返還租賃住宅時，房東就應該要將押金全數返還給您
                                  。如果房東沒有依約返還押金，您可以到郵局寄發存證信函，定相當期限，請求房東在期限內返還押金
                                  不過，若是您確實有欠租或需要負擔損害賠償責任的情形，房東是可以扣您的押金作為擔保的，所以如果有這方面的爭議問題，
                                  請您與房東確認您是否真的有欠租，或是具有需負擔損害賠償責任的情事，
                                  如果雙方無法達成共識，建議您可以依鄉鎮市調解條例第10條第1項的規定向鄉、鎮、市公所調解委員會聲請調解，來維護雙方的權益。"""
                
                elif resultDICT[confirm_fees_BOOL] == True:
                    responseSTR = """聽起來您的問題是關於水電費、網路費、瓦斯費等方面的爭議，......."""
                    
                elif resultDICT[confirm_comein_BOOL] == True:
                    responseSTR = """聽起來您遇到的問題是關於房東任意進出您租屋處的問題，........"""
                
                await message.reply(responseSTR)


            





if __name__ == "__main__":
    client = BotClient()
    client.run(accountDICT["discord_token"])    
   
  