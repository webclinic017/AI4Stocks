from buffett.common.pendelum import Date, DateTime
from buffett.common.wrapper import Wrapper
from buffett.download import Para
from buffett.download.mysql import Operator
from buffett.download.handler.stock import AkDailyHandler
from buffett.task.task import Task


class StockDailyTask(Task):
    def __init__(self,
                 operator: Operator,
                 start_time: DateTime = None):
        super().__init__(wrapper=Wrapper(AkDailyHandler(operator=operator).obtain_data),
                         args=(Para().with_start_n_end(start=Date(2000, 1, 1), end=Date.today()),),
                         start_time=start_time)
        self._operator = operator

    def get_subsequent_task(self, success: bool):
        if success:
            return StockDailyTask(operator=self._operator,
                                  start_time=self._start_time.add(days=1))
        else:
            return StockDailyTask(operator=self._operator,
                                  start_time=self._start_time.add(minutes=5))
