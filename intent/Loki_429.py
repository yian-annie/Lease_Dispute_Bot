#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for 429

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

DEBUG_429 = True
userDefinedDICT = {"副詞": ["任意", "隨意", "擅自", "隨便"], "動詞": ["過來", "過戶"], "名詞": ["房東", "房客"], "家電": ["抽油煙機", "電風扇", "電冰箱", "飲水機", "除濕機"], "房間配備": ["木地板", "壁紙", "自來水", "Wifi", "單人床墊", "床頭櫃", "單人床"], "法律用語": ["租金", "押租金", "修繕義務", "租賃契約", "出租人", "承租人", "次承租人", "轉租人"]}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_429:
        print("[429] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "[他][只]說過[幾天][會][過來]了解":
        # write your code here
        pass

    if utterance == "[他][完全]沒有想要解決[問題]":
        # write your code here
        pass

    if utterance == "[他]卻[只]說不知道":
        # write your code here
        pass

    if utterance == "[他]說[他][之後][會][過來]看看":
        # write your code here
        pass

    if utterance == "[他]說[以前][都]沒有這樣":
        # write your code here
        pass

    if utterance == "[他]說不是[他]的[問題]":
        # write your code here
        pass

    if utterance == "[冷氣]不[能]運轉":
        # write your code here
        pass

    if utterance == "[地板]腐爛":
        # write your code here
        pass

    if utterance == "[房間]漏水":
        # write your code here
        pass

    if utterance == "[木地板]腐蝕":
        # write your code here
        pass

    if utterance == "[東西]壞了":
        # write your code here
        pass

    if utterance == "[東西]壞掉":
        # write your code here
        pass

    if utterance == "[東西]損壞":
        # write your code here
        pass

    if utterance == "[牆壁]發霉滲水":
        # write your code here
        pass

    if utterance == "[磁磚]碎裂":
        # write your code here
        pass

    if utterance == "[紗窗]有破[洞]":
        # write your code here
        pass

    if utterance == "[紗窗]破掉":
        # write your code here
        pass

    if utterance == "[電風扇]故障":
        # write your code here
        pass

    if utterance == "修繕":
        # write your code here
        pass

    if utterance == "房東[都]不來修":
        # write your code here
        pass

    if utterance == "房東[都]不修理":
        # write your code here
        pass

    if utterance == "房東[都]不處理":
        # write your code here
        pass

    if utterance == "房東[都]不解決":
        # write your code here
        pass

    if utterance == "房東叫我[自己]修":
        # write your code here
        pass

    if utterance == "房東說[反正][我][也]不[會]用到":
        # write your code here
        pass

    if utterance == "有[白蟻]腐蝕":
        # write your code here
        pass

    if utterance == "沒有熱水":
        # write your code here
        pass

    if utterance == "跟房東反應[他][都]擺爛不處理":
        # write your code here
        pass

    return resultDICT