import unittest
import mtgcompiler.frontend.compilers.LarkMtgJson.MtgJsonCompiler as MtgJsonCompiler
from lark import logger
import logging
logger.setLevel(logging.DEBUG)

class TestRandomParsings(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._keywordSequenceCompiler = MtgJsonCompiler.MtgJsonCompiler(options={"parser.startRule": "ability"})

if __name__ == '__main__':
    unittest.main()