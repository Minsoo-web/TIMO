from file_manager.config_reader import ConfigReader
from exception import UnknownTestTestToolError
from test_manager.tools.flake8 import Flake8Parser
from test_manager.tools.jacoco import JacocoParser
from test_manager.tools.surefire import SurefireParser
from test_manager.tools.unittest import UnittestParser
from typing import NoReturn
from utils import colored_print
import os


class Parser(object):
    """Test result parser"""

    def __init__(self) -> NoReturn:
        self.conf = ConfigReader()
        self.surefire = SurefireParser()
        self.unittest = UnittestParser()
        self.jacoco = JacocoParser()
        self.flake8 = Flake8Parser()

    def _csw(self) -> dict:
        """
        Parse Code static analysis result.

            Returns:
                dict: Test result
        """

        result = {}
        if self.test_tool == 'flake8':
            result = self.flake8.parse(path=self.path, file_type=self.file_type)

        return result

    def _unittest(self) -> dict:
        """
        Parse Unittest result.

            Returns:
                dict: Test result
        """

        if self.test_tool == 'surefire':
            result = self.surefire.parse(path=self.path, file_type=self.file_type)
        elif self.test_tool == 'unittest':
            result = self.unittest.parse(path=self.path, file_type=self.file_type)
        else:
            raise UnknownTestTestToolError

        return result

    def _coverage(self) -> dict:
        """
        Parse Coverage test result.

            Returns:
                dict: Test result
        """

        if self.test_tool == 'jacoco':
            result = self.jacoco.parse(path=self.path, file_type=self.file_type)
        else:
            raise UnknownTestTestToolError

        return result

    def _apitest(self) -> dict:
        """
        Parse API test result.

            Returns:
                dict: Test result
        """

        result = {}
        return result

    def _e2etest(self) -> dict:
        """
        Parse End to End result.

            Returns:
                dict: Test result
        """

        result = {}
        return result

    def parse(self, kind: str, file_type: str, test_tool: str) -> dict:
        """
        Parse test result

            Parameters:
                kind(str): Test kind
                report_path: Report file location
                file_type: Report file's ext
                test_tool: Test tool

            Returns:
                dict: Test result
        """

        self.path = self.conf.get_report_info(kind)['path']
        self.file_type = file_type
        self.test_tool = test_tool.lower()

        if not os.path.isfile(self.path):
            colored_print(f'We can\'t  find {self.path}.', 'red')
            colored_print('Where is it?', 'red')
            raise FileNotFoundError

        if (kind := kind.lower()) == 'csw':
            result = self._csw()
        elif kind == 'unittest':
            result = self._unittest()
        elif kind == 'coverage':
            result = self._coverage()
        elif kind == 'apitest':
            result = self._apitest()
        elif kind == 'e2etest':
            result = self._e2etest()

        return result