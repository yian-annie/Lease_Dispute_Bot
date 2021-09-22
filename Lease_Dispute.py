#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki 2.0 Template For Python3

    [URL] https://api.droidtown.co/Loki/BulkAPI/

    Request:
        {
            "username": "your_username",
            "input_list": ["your_input_1", "your_input_2"],
            "loki_key": "your_loki_key",
            "filter_list": ["intent_filter_list"] # optional
        }

    Response:
        {
            "status": True,
            "msg": "Success!",
            "version": "v223",
            "word_count_balance": 2000,
            "result_list": [
                {
                    "status": True,
                    "msg": "Success!",
                    "results": [
                        {
                            "intent": "intentName",
                            "pattern": "matchPattern",
                            "utterance": "matchUtterance",
                            "argument": ["arg1", "arg2", ... "argN"]
                        },
                        ...
                    ]
                },
                {
                    "status": False,
                    "msg": "No Match Intent!"
                }
            ]
        }
"""

from requests import post
from requests import codes
import math
import json
import re 

try:
    from intent import Loki_425
    from intent import Loki_425_tb1
    from intent import Loki_425_tb2 
    from intent import Loki_425_tb3
    from intent import Loki_429
    from intent import Loki_429_tb1
    from intent import Loki_Security_Deposit
    from intent import Loki_electricity_water_fees
    from intent import Loki_Come_in
    from intent import Loki_Haunted_House
    
except:
    from .intent import Loki_425
    from .intent import Loki_425_tb1
    from .intent import Loki_425_tb2 
    from .intent import Loki_425_tb3
    from .intent import Loki_429
    from .intent import Loki_429_tb1
    from .intent import Loki_Security_Deposit
    from .intent import Loki_electricity_water_fees
    from .intent import Loki_Come_in 
    from .intent import Loki_Haunted_House

with open("account.info", encoding="utf-8") as f:
    accountDICT = json.loads(f.read())

LOKI_URL = "https://api.droidtown.co/Loki/BulkAPI/"
USERNAME = accountDICT["username"]
LOKI_KEY = accountDICT["loki_key"]
# 意圖過濾器說明
# INTENT_FILTER = []        => 比對全部的意圖 (預設)
# INTENT_FILTER = [intentN] => 僅比對 INTENT_FILTER 內的意圖
INTENT_FILTER = []

class LokiResult():
    status = False
    message = ""
    version = ""
    balance = -1
    lokiResultLIST = []

    def __init__(self, inputLIST, filterLIST):
        self.status = False
        self.message = ""
        self.version = ""
        self.balance = -1
        self.lokiResultLIST = []
        # filterLIST 空的就採用預設的 INTENT_FILTER
        if filterLIST == []:
            filterLIST = INTENT_FILTER

        try:
            result = post(LOKI_URL, json={
                "username": USERNAME,
                "input_list": inputLIST,
                "loki_key": LOKI_KEY,
                "filter_list": filterLIST
            })

            if result.status_code == codes.ok:
                result = result.json()
                self.status = result["status"]
                self.message = result["msg"]
                if result["status"]:
                    self.version = result["version"]
                    self.balance = result["word_count_balance"]
                    self.lokiResultLIST = result["result_list"]
            else:
                self.message = "Connect failed."
        except Exception as e:
            self.message = str(e)

    def getStatus(self):
        return self.status

    def getMessage(self):
        return self.message

    def getVersion(self):
        return self.version

    def getBalance(self):
        return self.balance

    def getLokiStatus(self, index):
        rst = False
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["status"]
        return rst

    def getLokiMessage(self, index):
        rst = ""
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["msg"]
        return rst

    def getLokiLen(self, index):
        rst = 0
        if index < len(self.lokiResultLIST):
            if self.lokiResultLIST[index]["status"]:
                rst = len(self.lokiResultLIST[index]["results"])
        return rst

    def getLokiResult(self, index, resultIndex):
        lokiResultDICT = None
        if resultIndex < self.getLokiLen(index):
            lokiResultDICT = self.lokiResultLIST[index]["results"][resultIndex]
        return lokiResultDICT

    def getIntent(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["intent"]
        return rst

    def getPattern(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["pattern"]
        return rst

    def getUtterance(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["utterance"]
        return rst

    def getArgs(self, index, resultIndex):
        rst = []
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["argument"]
        return rst

def runLoki(inputLIST, filterLIST=[]):
    resultDICT = {}
    lokiRst = LokiResult(inputLIST, filterLIST)
    if lokiRst.getStatus():
        for index, key in enumerate(inputLIST):
            for resultIndex in range(0, lokiRst.getLokiLen(index)):
                # 429
                if lokiRst.getIntent(index, resultIndex) == "429":
                    resultDICT = Loki_429.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # electricity_water_fees
                if lokiRst.getIntent(index, resultIndex) == "electricity_water_fees":
                    resultDICT = Loki_electricity_water_fees.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # 429_tb1
                if lokiRst.getIntent(index, resultIndex) == "429_tb1":
                    resultDICT = Loki_429_tb1.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # 425_tb3
                if lokiRst.getIntent(index, resultIndex) == "425_tb3":
                    resultDICT = Loki_425_tb3.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Come_in
                if lokiRst.getIntent(index, resultIndex) == "Come_in":
                    resultDICT = Loki_Come_in.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Probe
                if lokiRst.getIntent(index, resultIndex) == "Probe":
                    resultDICT = Loki_Probe.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # 425
                if lokiRst.getIntent(index, resultIndex) == "425":
                    resultDICT = Loki_425.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Security_Deposit
                if lokiRst.getIntent(index, resultIndex) == "Security_Deposit":
                    resultDICT = Loki_Security_Deposit.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # 425_tb1
                if lokiRst.getIntent(index, resultIndex) == "425_tb1":
                    resultDICT = Loki_425_tb1.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # 425_tb2
                if lokiRst.getIntent(index, resultIndex) == "425_tb2":
                    resultDICT = Loki_425_tb2.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

    else:
        resultDICT = {"msg": lokiRst.getMessage()}
    return resultDICT

def testLoki(inputLIST, filterLIST):
    INPUT_LIMIT = 20
    for i in range(0, math.ceil(len(inputLIST) / INPUT_LIMIT)):
        resultDICT = runLoki(inputLIST[i*INPUT_LIMIT:(i+1)*INPUT_LIMIT], filterLIST)
        
def botRunLoki(inputSTR, filterLIST=[]):
    punctuationPat = re.compile("[,\.\?:;，。？、：；\n]+")
    inputLIST = punctuationPat.sub("\n", inputSTR).split("\n")

    resultDICT = runLoki(inputLIST, filterLIST)
    return resultDICT



if __name__ == "__main__":
    # 429
    #print("[TEST] 429")
    #inputLIST = ['修繕','地板腐爛','房間漏水','東西壞了','東西壞掉','東西損壞','沒有熱水','磁磚碎裂','紗窗破掉','有白蟻腐蝕','木地板腐蝕','紗窗有破洞','電風扇故障','冷氣不能運轉','房東都不來修','房東都不修理','房東都不處理','房東都不解決','抽油煙機壞掉','牆壁發霉滲水','他卻只說不知道','房東叫我自己修','他說不是他的問題','他說以前都沒有這樣','他說他之後會過來看看','他只說過幾天會過來了解','他完全沒有想要解決問題','房東說反正我也不會用到','跟房東反應他都擺爛不處理']
    #testLoki(inputLIST, ['429'])
    #print("")

    # electricity_water_fees
    #print("[TEST] electricity_water_fees")
    #inputLIST = ['水費','電費','瓦斯費','網路費','Wifi費用','wifi費用','一度5元','每度5元','一度5.6塊','天然氣費','自來水費','一度6塊錢','台電的度數','依台電度數計價']
    #testLoki(inputLIST, ['electricity_water_fees'])
    #print("")

    # 429_tb1
    #print("[TEST] 429_tb1")
    #inputLIST = ['有','沒有','上面寫房東要負責','約好房東要負責修繕']
    #testLoki(inputLIST, ['429_tb1'])
    #print("")

    # 425_tb3
    #print("[TEST] 425_tb3")
    #inputLIST = ['否','是','有','不清楚','不知道','還沒有','已經成交了','已經賣掉了','已經過戶了','有辦好過戶了','已經辦理所有權移轉登記了']
    #testLoki(inputLIST, ['425_tb3'])
    #print("")

    # Come_in
    #print("[TEST] Come_in")
    #inputLIST = ['房東隨便進來我房間','房東隨意進入我房間','房東任意進出我租屋處','房東任意帶人進來我房間','房東擅自帶人進來我房間','房東趁我不在帶人來看屋','房東未經我同意就帶人進來','房東未經同意就任意進入我房間']
    #testLoki(inputLIST, ['Come_in'])
    #print("")

    # Probe
    #print("[TEST] Probe")
    #inputLIST = ['對','是','不是','沒錯','租屋糾紛','租賃糾紛','我想要問租屋的問題','我想詢問租屋的法律問題','我想要詢問租賃糾紛的問題']
    #testLoki(inputLIST, ['Probe'])
    #print("")

    # 425
    #print("[TEST] 425")
    #inputLIST = ['房東說要賣屋','我的租屋處被賣了','房子被賣給別人了','我的租屋處被賣掉了','我租的房子被賣掉了','我現在住的地方被賣了','我現在租的地方被賣了','房東把我租的房子賣了','把我現在住的地方賣了','把我現在租的房子賣了','我現在住的地方被賣掉了','我現在租的地方被賣掉了','房東把我租的房子賣掉了','房東說要賣掉我的租屋處','把我現在住的地方賣掉了','把我現在租的房子賣掉了','我現在租的房子被房東賣了','我的租屋處被莫名其妙賣掉','房東把我板橋租的房子賣了','我板橋租的房子被房東賣掉了','我現在租的房子被房東賣掉了','房東把我板橋租的房子賣掉了','房東說要賣掉我現在住的地方','房東說他要把我現在住的房子賣掉']
    #testLoki(inputLIST, ['425'])
    #print("")

    # Security_Deposit
    #print("[TEST] Security_Deposit")
    #inputLIST = ['扣我押金','拿回押金','不退我押金','不還我押金','亂扣我押金','吃掉我的押金','把押金拿回來','拿回我的押金','惡意亂扣我押金','扣我兩個月押金','押金還在房東那','故意不退還押金','遲遲未收到押金','我想要拿回我的押金','我的押金被房東扣了']
    #testLoki(inputLIST, ['Security_Deposit'])
    #print("")

    # 425_tb1
    #print("[TEST] 425_tb1")
    #inputLIST = ['否','是','沒有','還沒有','已經簽約了','有書面簽約','只有口頭說好','有說好了但沒有寫契約']
    #testLoki(inputLIST, ['425_tb1'])
    #print("")

    # 425_tb2
    #print("[TEST] 425_tb2")
    #inputLIST = ['有','沒有','有交付','還沒有','已經交付了','他有給我鑰匙','他有跟我說大門密碼']
    #testLoki(inputLIST, ['425_tb2'])
    #print("")

    #輸入其它句子試看看
    inputLIST = ["房東跟我收電費一度十塊ㄟ"]
    filterLIST = []
    resultDICT = runLoki(inputLIST, filterLIST)
    print("Result => {}".format(resultDICT))
    
    print(resultDICT)
    
    
    if "confirm_Security_Deposit_BOOL" in resultDICT and resultDICT["confirm_Security_Deposit_BOOL"] == True:
        responseSTR = """聽起來您的問題與押金有關。其實呢，押金的作用，是為了擔保您(承租人)在租賃關係中所生的租金債務或是損害賠償責任。
                      因此，如果您沒有欠房東租金或是需要負擔損害賠償責任，那麼在租賃關係消滅(例如租期屆滿或租賃契約終止)，且您返還租賃住宅時，房東就應該要將押金全數返還給您。
                      如果房東沒有依約返還押金，您可以到郵局寄發存證信函，定相當期限，請求房    東在期限內返還押金。
                      不過，若是您確實有欠租或需要負擔損害賠償責任的情形，房東是可以扣您的押金作為擔保的，所以如果有這方面的爭議問題，
                      請您與房東確認您是否真的有欠租，或是具有需負擔損害賠償責任的情事(例如您是否有損壞屋內的家具或其他物品)，
                      如果雙方無法達成共識，建議您可以依租賃住宅條例第16條的規定，向直轄市或縣（市）政府聲請調處，來維護雙方的權益，而且無須付調處費喔。""".replace(" ", "").replace("\n", "")
    
    elif "confirm_fees_BOOL" in resultDICT and resultDICT["confirm_fees_BOOL"] == True:
        responseSTR = """聽起來您的問題是關於水電費、網路費、瓦斯費等方面的爭議，根據內政部頒布的「住宅租賃契約應約定及不得約定事項」，
                      原則上水費、電費、瓦斯費、網路費、管理費等費用，基於契約自由原則，都可以由雙方約定某一方負擔，所以請您注意您的租賃契約書面上關於這些費用的約定。
                      不過，如果在租賃期間因不可歸責於租賃雙方之事由，致管理費增加者，承租人就增加部分之金額，以負擔百分之十為限。
                      另外，關於電費的部分，雙方可以就夏季月分的費用與非夏季月分的費用分別約定，但不論怎麼約定，都不可以超過台電公司所定當月用電量最高級距的每度金額。
                      所以房東的電費收取只要不超過現在台電規定的6.41元/度，就不算違法。但畢竟電費收取是代收費用，房東不可以此營利，    
                                  如果您發現房東有超收行為，您可以向當地縣(市)政府的地政局(處)、消保官檢舉。""".replace(" ", "").replace("\n", "")
                    
    elif "confirm_comein_BOOL" in resultDICT and resultDICT["confirm_comein_BOOL"] == True:
        responseSTR = """聽起來您遇到的問題是關於房東任意進出您租屋處的問題。其實當房屋出租之後，房東(出租人)雖然仍擁有房屋的所有權，
                      但房客(承租人)已經取得了完整的使用收益的權限，所以如果房東想要進入出租房屋時，必須經過房客的同意，否則不可任意進出。
                      如果房東未經您的同意，就擅自進入您的租屋處的話，恐怕會觸犯刑法第306條「無故侵入他人住宅罪」，也可能構成民法第195條第1項個人隱私權的侵權行為。
                      若您向房東反應或溝通後未獲改善，建議您可以直接報警處理""".replace(" ", "").replace("\n", "")
                
    
    
    
    print(responseSTR)