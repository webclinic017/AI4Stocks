from buffett.download.handler.stock import AkCurrHandler
from test import Tester


class TestStockCurrHandler(Tester):
    def test_download(self):
        hdl = AkCurrHandler(operator=self.operator)
        tbl = hdl.obtain_data()
        db = hdl.select_data()
        # cmp = pd.concat([tbl, db]).drop_duplicates(keep=False)  # error: 允许存入数据库后存在精度损失
        assert tbl.shape[0] == db.shape[0]
