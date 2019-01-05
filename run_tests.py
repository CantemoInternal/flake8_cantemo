import ast
import unittest

from flake8_cantemo.checker import CantemoChecker

class TestCantemoFlake8(unittest.TestCase):
    def assert_codes(self, ret, codes):
        self.assertEqual(len(ret), len(codes))
        for item, code in zip(ret, codes):
            self.assertTrue(item[2].startswith(code + ' '))

    def test_setup_wo_super(self):
        tree = ast.parse(
            'class foo(object):\n'
            '    def setUp(self):\n'
            '        pass'
        )

        checker = CantemoChecker(tree, '/home/script.py')
        ret = [c for c in checker.run()]
        self.assert_codes(ret, ['CMO001'])
               
    def test_setup_w_super(self):
        tree = ast.parse(
            'class foo(object):\n'
            '    def setUp(self):\n'
            '        super(foo).setUp()\n'
        )

        checker = CantemoChecker(tree, '/home/script.py')
        ret = [c for c in checker.run()]
        self.assert_codes(ret, [])

    def test_teardown_wo_super(self):
        tree = ast.parse(
            'class foo(object):\n'
            '    def tearDown(self):\n'
            '        pass'
        )

        checker = CantemoChecker(tree, '/home/script.py')
        ret = [c for c in checker.run()]
        self.assert_codes(ret, ['CMO001'])
               
    def test_teardown_w_super(self):
        tree = ast.parse(
            'class foo(object):\n'
            '    def tearDown(self):\n'
            '        super(foo).setUp()\n'
        )

        checker = CantemoChecker(tree, '/home/script.py')
        ret = [c for c in checker.run()]
        self.assert_codes(ret, [])
        
        
    def test_super_wo_class(self):
        tree = ast.parse(
            'def setUp():\n'
            '    pass'
        )

        checker = CantemoChecker(tree, '/home/script.py')
        ret = [c for c in checker.run()]
        self.assert_codes(ret, [])
        
