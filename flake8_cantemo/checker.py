# the structure of this is inspired by
# https://github.com/gforcada/flake8-builtins

from __future__ import print_function

import ast


class CantemoChecker(object):
    name = "flake8_cantemo"
    version = "0.0.1"

    super_msg = 'CMO001 "{0}" should call super'

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename

    def run(self):
        for statement in ast.walk(self.tree):
            for child in ast.iter_child_nodes(statement):
                child.__flake8_cmo_parent = statement

        for statement in ast.walk(self.tree):
            value = []
            if isinstance(statement, ast.FunctionDef):
                value = self.check_function(statement)

            if value:
                for line, offset, msg, rtype in value:
                    yield line, offset, msg, rtype

    def check_function(self, function):
        # Check that setUp and tearDown makes a call to super(),
        # otherwise we get weird errors with Django's test runner
        if function.name in ["setUp", "tearDown"]:
            # Only if this is a class function
            if type(function.__flake8_cmo_parent) is ast.ClassDef:
                for value in self.check_super(function):
                    yield value

    def check_super(self, function):
        """ 
        Check that a function which should call super() actually does so
        """
        found_super = False
        supers = [x for x in ast.walk(function)
                  if getattr(x, 'id', None) == 'super']
        for su in supers:
            if isinstance(su.__flake8_cmo_parent, ast.Call):
                found_super = True

        if not found_super:
            yield self.error(
                function,
                message=self.super_msg,
                variable=function.name
            )

    def error(
        self,
        statement,
        message=None,
        variable=None,
        line=None,
        column=None,
    ):
        if not message:
            message = self.assign_msg
        if not variable:
            variable = statement.id
        if not line:
            line = statement.lineno
        if not column:
            column = statement.col_offset

        return (
            line,
            column,
            message.format(variable),
            type(self),
        )
