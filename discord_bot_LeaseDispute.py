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

leaseTemplate = {"confirm425tb1_BOOL":None, #425_tb1確認租賃契約成立
                 "confirm425tb2_BOOL":None, #425_tb2租賃物已交付承租人占有
                 "confirm425tb3_BOOL":None, #425_tb3所有權已讓與第三人
                 "updatetime":"datetime"}

fixTemplate = {"confirm429tb1_BOOL":None,  #429_tb1確認房東為修繕義務人
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
            msgSTR = message.content.replace("<@!{}> ".format(self.user.id), "")
            if msgSTR == 'ping':
                await message.reply('pong')
            elif msgSTR == 'ping ping':
                await message.reply('pong pong')
                
            elif msgSTR in ["哈囉","嗨","你好","您好","在嗎","Hi","hi","Hello","hello"]: #在使用者以問候開啟對話時，計算對話時間差
                if message.author in mscDICT.keys():  #有講過話
                    nowDATETIME = datetime.datetime.now()
                    timeDIFF = nowDATETIME - mscDICT[message.author]["updatetime"]
                    if timeDIFF.total_seconds() >= 300:   #有講過話，但與上次差超過5分鐘(視為沒有講過話)
                        mscDICT[message.author] = {"confirm425_BOOL":None,
                                                   "confirm425tb1_BOOL":None,
                                                   "confirm425tb2_BOOL":None,
                                                   "confirm425tb3_BOOL":None,
                                                   "confirm429_BOOL":None,
                                                   "confirm429tb1_BOOL":None,
                                                   "confirm_Security_Deposit_BOOL":None,
                                                   "confirm_fees_BOOL":None,
                                                   "confirm_comein_BOOL":None}
                        
                        await message.reply("嗨嗨，您好，我是您的租賃法律問題小幫手，請問您遇到什麼問題了呢？")
                    else:  #有講過話，而且還沒超過5分鐘
                        await message.reply("我還在等您的回覆喔")  
                else:  #沒有講過話
                    mscDICT[message.author] = {"confirm425_BOOL":None,
                                               "confirm425tb1_BOOL":None,
                                               "confirm425tb2_BOOL":None,
                                               "confirm425tb3_BOOL":None,
                                               "confirm429_BOOL":None,
                                               "confirm429tb1_BOOL":None,
                                               "confirm_Security_Deposit_BOOL":None,
                                               "confirm_fees_BOOL":None,
                                               "confirm_comein_BOOL":None}
                    await message.reply("嗨嗨，您好，我是您的租賃法律問題小幫手，請問您遇到什麼問題了呢？")
            
            else: #開始處理正式對話
                #從這裡開始接上 NLU 模型
                replySTR = "我是預設的回應字串…你會看到我這串字，肯定是出了什麼錯！"

                resultDICT = botRunLoki(msgSTR)
                print("Result => {}".format(resultDICT))
                    
                #425買賣不破租賃的問題
                if "confirm425_BOOL" in resultDICT and resultDICT["confirm425_BOOL"] == True:  #確認問題為425
                    mscDICT[message.author] = leaseTemplate #開始處理425的多輪對話部分
                    replySTR = "您的問題是您的租處被出租人(房東)賣掉了是嗎？"
                    await message.reply(replySTR)
                    
                    
                    
                
                
                
                
                
                #不需要處理多輪對話的租賃問題
                if "confirm_Security_Deposit_BOOL" in resultDICT and resultDICT["confirm_Security_Deposit_BOOL"] == True:
                    replySTR = """聽起來您的問題與押金有關。其實呢，押金的作用，是為了擔保您(承租人)在租賃關係中所生的租金債務或是損害賠償責任。
                                因此，如果您沒有欠房東租金或是需要負擔損害賠償責任，那麼在租賃關係消滅(例如租期屆滿或租賃契約終止)，且您返還租賃住宅時，房東就應該要將押金全數返還給您。
                                如果房東沒有依約返還押金，您可以到郵局寄發存證信函，定相當期限，請求房東在期限內返還押金。
                                不過，若是您確實有欠租或需要負擔損害賠償責任的情形，房東是可以扣您的押金作為擔保的，所以如果有這方面的爭議問題，
                                請您與房東確認您是否真的有欠租，或是具有需負擔損害賠償責任的情事(例如您是否有損壞屋內的家具或其他物品)，
                                如果雙方無法達成共識，建議您可以依租賃住宅條例第16條的規定，向直轄市或縣（市）政府聲請調處，來維護雙方的權益，而且無須付調處費喔。""".replace(" ", "").replace("\n", "")
                
                elif "confirm_fees_BOOL" in resultDICT and resultDICT["confirm_fees_BOOL"] == True:
                    replySTR = """聽起來您的問題是關於水電費、網路費、瓦斯費等方面的爭議，根據內政部頒布的「住宅租賃契約應約定及不得約定事項」，
                                原則上水費、電費、瓦斯費、網路費、管理費等費用，基於契約自由原則，都可以由雙方約定某一方負擔，所以請您注意您的租賃契約書面上關於這些費用的約定。
                                不過，如果在租賃期間因不可歸責於租賃雙方之事由，致管理費增加者，承租人就增加部分之金額，以負擔百分之十為限。
                                另外，關於電費的部分，雙方可以就夏季月分的費用與非夏季月分的費用分別約定，但不論怎麼約定，都不可以超過台電公司所定當月用電量最高級距的每度金額。
                                所以房東的電費收取只要不超過現在台電規定的6.41元/度，就不算違法。但畢竟電費收取是代收費用，房東不可以此營利，
                                如果您發現房東有超收行為，您可以向當地縣(市)政府的地政局(處)、消保官檢舉。""".replace(" ", "").replace("\n", "")
                    
                elif "confirm_comein_BOOL" in resultDICT and resultDICT["confirm_comein_BOOL"] == True:
                    replySTR = """聽起來您遇到的問題是關於房東任意進出您租屋處的問題。其實當房屋出租之後，房東(出租人)雖然仍擁有房屋的所有權，
                                但房客(承租人)已經取得了完整的使用收益的權限，所以如果房東想要進入出租房屋時，必須經過房客的同意，否則不可任意進出。
                                如果房東未經您的同意，就擅自進入您的租屋處的話，恐怕會觸犯刑法第306條「無故侵入他人住宅罪」，也可能構成民法第195條第1項個人隱私權的侵權行為。
                                若您向房東反應或溝通後未獲改善，建議您可以直接報警處理。""".replace(" ", "").replace("\n", "")
                
                else:
                    replySTR = "我是租賃法律問題小幫手，你可以對我說「我的房東都不還我租金」、「我的房東亂算水電費」、「我的租屋處被賣掉了」，或是跟我說你遇到了什麼問題喔！"
                    await message.reply(replySTR)


            





if __name__ == "__main__":
    client = BotClient()
    client.run(accountDICT["discord_token"])    
   
  