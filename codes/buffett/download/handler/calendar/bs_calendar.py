from typing import Optional

from buffett.adapter import logging
from buffett.adapter.baostock import bs
from buffett.adapter.pandas import DataFrame
from buffett.common import create_meta
from buffett.common.pendelum import Date
from buffett.common.tools import dataframe_not_valid
from buffett.common.constants.col import DATE
from buffett.common.constants.table import TRA_CAL
from buffett.download import Para
from buffett.download.handler.fast.handler import FastHandler
from buffett.download.mysql import Operator
from buffett.download.mysql.types import ColType, AddReqType

_RENAME_DICT = {'calendar_date': DATE}

_META = create_meta(meta_list=[
    [DATE, ColType.DATE, AddReqType.NONE]])


# 交易日查询
class CalendarHandler(FastHandler):
    def __init__(self, operator: Operator):
        super().__init__(operator)

    def _download(self) -> DataFrame:
        #### 登陆系统 ####
        lg = bs.login()
        # 显示登陆返回信息
        logging.info('login respond error_code:' + lg.error_code)
        logging.info('login respond  error_msg:' + lg.error_msg)

        #### 获取交易日信息 ####
        rs = bs.query_trade_dates(
            start_date='2000-01-01',
            end_date=Date.today().add(months=2).format('YYYY-MM-01'))

        #### 打印结果集 ####
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        res = DataFrame(data_list, columns=rs.fields)

        # 仅保留交易日
        res = res[res['is_trading_day'] == '1']

        res.rename(columns=_RENAME_DICT, inplace=True)
        res = res[[DATE]]

        return res

    def _save_to_database(self,
                          df: DataFrame):
        self._operator.create_table(name=TRA_CAL, meta=_META)
        self._operator.try_insert_data(name=TRA_CAL, df=df)  # 忽略重复Insert
        self._operator.disconnect()

    def select_data(self,
                    para: Para = None) -> Optional[DataFrame]:
        df = self._operator.select_data(TRA_CAL)
        if dataframe_not_valid(df):
            return

        df.index = df[DATE]
        return df
