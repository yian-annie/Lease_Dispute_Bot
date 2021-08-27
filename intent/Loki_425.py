#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for 425

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

DEBUG_425 = True
userDefinedDICT = {"副詞": ["任意", "隨意", "擅自", "隨便"], "動詞": ["過來", "過戶"], "名詞": ["房東", "房客"], "家電": ["抽油煙機", "電風扇", "電冰箱", "飲水機", "除濕機"], "房間配備": ["木地板", "壁紙", "自來水", "Wifi", "單人床墊", "床頭櫃", "單人床"], "法律用語": ["租金", "押租金", "修繕義務", "租賃契約", "出租人", "承租人", "次承租人", "轉租人"]}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_425:
        print("[425] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "[我][板橋]租的[房子]被房東賣掉了":
        # write your code here
        pass

    if utterance == "[我][現在]住的[地方]被賣了":
        # write your code here
        pass

    if utterance == "[我][現在]住的[地方]被賣掉了":
        # write your code here
        pass

    if utterance == "[我][現在]租的[地方]被賣了":
        # write your code here
        pass

    if utterance == "[我][現在]租的[地方]被賣掉了":
        # write your code here
        pass

    if utterance == "[我][現在]租的[房子]被房東賣了":
        # write your code here
        pass

    if utterance == "[我][現在]租的[房子]被房東賣掉了":
        # write your code here
        pass

    if utterance == "[我]的[租屋處]被莫名其妙賣掉":
        # write your code here
        pass

    if utterance == "[我]的[租屋處]被賣了":
        # write your code here
        pass

    if utterance == "[我]的[租屋處]被賣掉了":
        # write your code here
        pass

    if utterance == "[我]租的[房子]被賣掉了":
        # write your code here
        pass

    if utterance == "[房子]被賣給[別人]了":
        # write your code here
        pass

    if utterance == "房東把[我][板橋]租的[房子]賣了":
        # write your code here
        pass

    if utterance == "房東把[我][板橋]租的[房子]賣掉了":
        # write your code here
        pass

    if utterance == "房東把[我]租的[房子]賣了":
        # write your code here
        pass

    if utterance == "房東把[我]租的[房子]賣掉了":
        # write your code here
        pass

    if utterance == "房東說[他]要把[我][現在]住的[房子]賣掉":
        # write your code here
        pass

    if utterance == "房東說要賣屋":
        # write your code here
        pass

    if utterance == "房東說要賣掉[我][現在]住的[地方]":
        # write your code here
        pass

    if utterance == "房東說要賣掉[我]的[租屋處]":
        # write your code here
        pass

    if utterance == "把[我][現在]住的[地方]賣了":
        # write your code here
        pass

    if utterance == "把[我][現在]住的[地方]賣掉了":
        # write your code here
        pass

    if utterance == "把[我][現在]租的[房子]賣了":
        # write your code here
        pass

    if utterance == "把[我][現在]租的[房子]賣掉了":
        # write your code here
        pass

    return resultDICT