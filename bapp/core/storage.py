from os import path
from beancount import loader
from beancount.parser import printer
from beancount.query import query
from beancount.query.query_compile import CompilationError
from beancount.query.query_parser import ParseError

from bapp.core.exception import BaseApiException


class Storage:

    # 初始化
    def load(self, basedir, filename):
        self.basedir = basedir
        self.filename = filename
        self.reload()

    # 根目录
    def basedir(self):
        return self.basedir

    # 加载文件
    def reload(self):
        self.entries, errors, self.options = loader.load_file(path.join(self.basedir, self.filename))
        if errors:
            printer.print_errors(errors)
            raise BaseApiException("Error loading file" + self.filename + "!")

    # 运行查询
    def run_query(self, query_string):
        try:
            return query.run_query(self.entries, self.options, query_string)
        except (CompilationError, ParseError) as exc:
            raise BaseApiException('Query failed: ' + str(exc)) from exc

    # 设置价格
    def set_price(self, prices, filename):
        with open(path.join(self.basedir, filename), 'a') as output:
            printer.print_entries(prices, file=output)

    # 添加交易
    def add_transaction(self, entries, filename):
        with open(path.join(self.basedir, filename), 'a') as output:
            printer.print_entry(entries, file=output)


# 实例
storage = Storage()
