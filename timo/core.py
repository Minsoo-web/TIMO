from database_manager.database import DatabaseManager
from file_manager.config_reader import ConfigReader
from test_manager.command_runner import CommandRunner
from test_manager.result_parser import Parser
from typing import NoReturn
from utils import colored_print
from utils import pretty_print
import fire


class Main(object):
    def __init__(self):
        self.conf = ConfigReader()
        self.runner = CommandRunner()

    def run(self, test_name: str) -> NoReturn:
        # test_kinds = ['CSW', 'Unittest', 'Coverage', 'APItest', 'E2Etest']
        colored_print(f'Running {test_name} in now.', 'magenta')
        command_list = self.conf.get_test_suites(test_name)
        self.runner.run_all(command_list)


class AfterTest(object):
    def __init__(self):
        self.config = ConfigReader()
        self.db = DatabaseManager()
        self.parser = Parser()

    def parse(self, test_name, db, build_number):
        report_conf = self.config.get_report_info(test_name=test_name)
        test_tool = self.config.get_test_tool(test_name=test_name)
        test_result = self.parser.parse(kind=test_name, file_type=report_conf['type'], test_tool=test_tool['uses'])
        if db is not None and build_number is not None:
            test_result['build_number'] = build_number
            self.db.insert_test_result(
                test_name,
                test_result,
                db
            )
        else:
            pretty_print(test_result)


class Pipeline(object):
    def __init__(self):
        self.conf = ConfigReader()
        self.test = Main()
        self.after_test = AfterTest()

    def setting(self, ext: str):
        self.conf.read_config_file(ext)

    def run(self, test_name: str):
        self.test.run(test_name)

    def parse(self, test_name: str, db=None, build_number=None):
        self.after_test.parse(test_name=test_name, db=db, build_number=build_number)


if __name__ == "__main__":
    fire.Fire(Pipeline)
