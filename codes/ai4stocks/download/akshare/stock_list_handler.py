# 下载沪深股票列表
import akshare as ak
from pandas import DataFrame

from ai4stocks.common.stock_code import StockCode
from ai4stocks.download.connect.mysql_common import MysqlConstants, MysqlColAddReq, MysqlColType
from ai4stocks.download.connect.mysql_operator import MysqlOperator


class StockListHandler:
    def __init__(self, op: MysqlOperator):
        self.op = op

    def Download(self) -> DataFrame:
        stocks = ak.stock_info_a_code_name()

        '''
        # StockList返回的股票代码是“000001”，“000002”这样的格式
        # 但是stock_zh_a_daily（）函数中，要求代码的格式为“sz000001”，或“sh600001”
        # 即必须有sz或者sh作为前序
        # 因此，通过for循环对股票代码code进行格式变换
        for i in range(len(stocks)):
            temp = stocks.iloc[i, 0]
            if temp[0] == "6":
                temp = "sh" + temp
            elif temp[0] == "0":
                temp = "sz" + temp
            elif temp[0] == "3":
                temp = "sz" + temp
            stocks.iloc[i, 0] = temp
        '''

        return stocks

    def Save2Database(self, stocks: DataFrame) -> None:
        cols = [
            ['code', MysqlColType.STOCK_CODE, MysqlColAddReq.PRIMKEY],
            ['name', MysqlColType.STOCK_NAME, MysqlColAddReq.NONE]
        ]
        table_meta = DataFrame(data=cols, columns=MysqlConstants.META_COLS)
        self.op.CreateTable(MysqlConstants.STOCK_LIST_TABLE, table_meta)
        self.op.TryInsertData(MysqlConstants.STOCK_LIST_TABLE, stocks) # 忽略重复Insert
        self.op.Disconnect()

    def DownloadAndSave(self) -> DataFrame:
        stocks = self.Download()
        self.Save2Database(stocks)
        return stocks

    def GetTable(self) -> DataFrame:
        stocks = self.op.GetTable(MysqlConstants.STOCK_LIST_TABLE)
        stocks['code'] = stocks.apply(lambda x: StockCode(x['code']), axis=1)
        return stocks
