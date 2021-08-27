#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for 425_tb1

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

DEBUG_425_tb1 = True
userDefinedDICT = {"副詞": ["任意", "隨意", "擅自", "隨便"], "動詞": ["過來", "過戶"], "名詞": ["房東", "房客"], "家電": ["抽油煙機", "電風扇", "電冰箱", "飲水機", "除濕機"], "房間配備": ["木地板", "壁紙", "自來水", "Wifi", "單人床墊", "床頭櫃", "單人床"], "法律用語": ["租金", "押租金", "修繕義務", "租賃契約", "出租人", "承租人", "次承租人", "轉租人"]}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_425_tb1:
        print("[425_tb1] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "[只有]口頭說好":
        # write your code here
        pass

    if utterance == "否":
        # write your code here
        pass

    if utterance == "已經簽約了":
        # write your code here
        pass

    if utterance == "是":
        # write your code here
        pass

    if utterance == "有書面簽約":
        # write your code here
        pass

    if utterance == "有說好了但沒有寫[契約]":
        # write your code here
        pass

    if utterance == "沒有":
        # write your code here
        pass

    return resultDICT