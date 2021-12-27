# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import win32com.client
import statistics
from numpy import log as ln


if __name__ == '__main__':
    instCpStockCode = win32com.client.Dispatch("CpUtil.CpStockCode")
    instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
    instCpMarketEye = win32com.client.Dispatch("CpSysDib.MarketEye")
    stock_list = instCpCodeMgr.GetStockListByMarket(1)
    objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")

    kospi_200 = {}
    for i in stock_list:
        if instCpCodeMgr.getStockKospi200Kind(i):
            kospi_200[i] = instCpCodeMgr.CodeToName(i)

    req_field = [0, 150, 4, 161]
    instCpMarketEye.SetInputValue(0, req_field)
    instCpMarketEye.SetInputValue(1, list(kospi_200.keys()))
    instCpMarketEye.BlockRequest()

    cnt = instCpMarketEye.GetHeaderValue(2)
    result = []
    for i in range(cnt):
        temp = []
        code = instCpMarketEye.GetDataValue(0, i)
        name = instCpCodeMgr.CodeToName(code)
        beta = instCpMarketEye.GetDataValue(1, i)
        price_now = instCpMarketEye.GetDataValue(2, i)
        price_60d = instCpMarketEye.GetDataValue(3, i)

        if price_60d == 0:
            continue

        objStockChart.SetInputValue(0, code)  # 종목코드
        objStockChart.SetInputValue(1, ord('2'))  # 개수로 받기
        objStockChart.SetInputValue(4, 60)  # 최근 120일치
        objStockChart.SetInputValue(5, [5])  # 요청항목 - 종가
        objStockChart.SetInputValue(9, ord('1'))  # 수정주가 사용
        objStockChart.BlockRequest()

        leng = objStockChart.GetHeaderValue(3)
        calc = []
        former = objStockChart.GetDataValue(0, 0)

        for j in range(1, leng):
            value = objStockChart.GetDataValue(0, j)
            calc.append(ln(value/former))
            former = value

        std = statistics.stdev(calc)
        print(std, i)
        temp.append(code)
        temp.append(name)
        temp.append(beta)
        temp.append(price_now)
        temp.append(price_60d)
        temp.append(std)
        temp.append(ln(price_now/price_60d))

        result.append(temp)

    print(result)

    f = open('../../output/kospi_200.csv', 'w')
    f.write("종목코드,종목명,현재가,베타계수,60일전가격,변동성,수익률\n")
    for i in result:
        for j in range(len(i)-1):
            f.write("%s," % i[j])
        f.write("%s\n" % i[-1])
    f.close()
