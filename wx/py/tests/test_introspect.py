#!/usr/bin/env python

__author__ = "Patrick K. O'Brien <pobrien@orbtech.com>"

import sys
import os

import unittest
from wx.py import introspect

"""
These unittest methods are preferred:
-------------------------------------
self.assertTrue(expr, msg=None)
self.assertEqual(first, second, msg=None)
self.assertRaises(excClass, callableObj, *args, **kwargs)
self.fail(msg=None)
self.failIf(expr, msg=None)
"""


class ModuleTestCase(unittest.TestCase):

    def test_module(self):
        module = introspect
        self.assertTrue(module.__author__)
        self.assertTrue(module.getAllAttributeNames)
        self.assertTrue(module.getAttributeNames)
        self.assertTrue(module.getAutoCompleteList)
        self.assertTrue(module.getBaseObject)
        self.assertTrue(module.getCallTip)
        self.assertTrue(module.getConstructor)
        self.assertTrue(module.getRoot)
        self.assertTrue(module.rtrimTerminus)


class RtrimTerminusTestCase(unittest.TestCase):

    def test_rtrimTerminus(self):
        values = (
            ('', '', ''),
            ('', None, ''),
            ('', '.', ''),
            ('', '(', ''),

            ('.', '', '.'),
            ('.', None, '.'),
            ('.', '.', '.'),
            ('.', '(', '.'),

            ('(', '', '('),
            ('(', None, '('),
            ('(', '.', '('),
            ('(', '(', '('),

            ('spam', '', 'spam'),
            ('spam', None, 'spam'),
            ('spam', '.', 'spam'),
            ('spam', '(', 'spam'),

            ('spam.', '', 'spam.'),
            ('spam.', None, 'spam.'),
            ('spam.', '.', 'spam.'),
            ('spam.', '(', 'spam.'),

            ('spam(', '', 'spam('),
            ('spam(', None, 'spam('),
            ('spam(', '.', 'spam('),
            ('spam(', '(', 'spam('),

            ('spam.eggs', '.', 'spam.'),
            ('spam.eggs.', '.', 'spam.eggs.'),
            ('spam.eggs(', '(', 'spam.eggs('),
            ('spam.eggs.', '(', 'spam.eggs.'),
            ('spam.eggs(', '.', 'spam.'),

            ('x = spam.', '.', 'x = spam.'),
            ('x = spam.eggs', '.', 'x = spam.'),
            ('x = spam.eggs.', '.', 'x = spam.eggs.'),
            ('x = spam.eggs(', '(', 'x = spam.eggs('),
        )
        for input, terminator, output in values:
            result = introspect.rtrimTerminus(input, terminator)
            self.assertEqual(result, output,
                             ':in: %r :t: %r :out: %r :result: %r' %
                             (input, terminator, output, result))


class GetRootTestCase(unittest.TestCase):

    def _checkRoot(self, input, terminator, output):
        root = introspect.getRoot(command=input, terminator=terminator)
        self.assertEqual(root, output,
                         ':in: %r :t: %r :out: %r :root: %r' %
                         (input, terminator, output, root))

    def test_getRoot(self):
        values = (
            ('', '', ''),
            ('', None, ''),
            ('', '.', ''),
            ('', '(', ''),

            ('.', '', '.'),
            ('.', None, '.'),
            ('.', '.', ''),
            ('.', '(', '.'),

            ('(', '', ''),
            ('(', None, ''),
            ('(', '.', ''),
            ('(', '(', ''),

            ('spam', '', 'spam'),
            ('spam', None, 'spam'),
            ('spam', '.', ''),
            ('spam', '(', 'spam'),

            ('spam.', '', 'spam.'),
            ('spam.', None, 'spam.'),
            ('spam.', '.', 'spam'),
            ('spam.', '(', 'spam.'),

            ('spam(', '', ''),
            ('spam(', None, ''),
            ('spam(', '.', ''),
            ('spam(', '(', 'spam'),

            ('spam.eggs', '.', 'spam'),
            ('spam.eggs.', '.', 'spam.eggs'),
            ('spam.eggs(', '(', 'spam.eggs'),
            ('spam.eggs.', '(', 'spam.eggs.'),
            ('spam.eggs(', '.', 'spam'),

            ('x = spam.', '.', 'spam'),
            ('x = spam.eggs', '.', 'spam'),
            ('x = spam.eggs.', '.', 'spam.eggs'),
            ('x = spam.eggs(', '(', 'spam.eggs'),

            ('for n in range(3):\n    d.', '.', 'd'),
            ('for n in range(3):\n...    d.', '.', 'd'),
        )
        for input, terminator, output in values:
            self._checkRoot(input, terminator, output)

    def test_getRoot_Advanced(self):
        values = (
            ('spam_', '', 'spam_'),
            ('spam_', None, 'spam_'),
            ('spam_', '.', ''),
            ('spam_', '(', 'spam_'),

            ('_spam', '', '_spam'),
            ('_spam', None, '_spam'),
            ('_spam', '.', ''),
            ('_spam', '(', '_spam'),

            ('spam_eggs', '', 'spam_eggs'),
            ('spam_eggs', None, 'spam_eggs'),
            ('spam_eggs', '.', ''),
            ('spam_eggs', '(', 'spam_eggs'),

            ('spam123', '', 'spam123'),
            ('spam123', None, 'spam123'),
            ('spam123', '.', ''),
            ('spam123', '(', 'spam123'),

            ('spam_123', '', 'spam_123'),
            ('spam_123', None, 'spam_123'),
            ('spam_123', '.', ''),
            ('spam_123', '(', 'spam_123'),
        )
        for input, terminator, output in values:
            self._checkRoot(input, terminator, output)

## The original intent was to detect when we were inside a string.
## That has proven to be very difficult, for little benefit.
## The fact that autocomplete or calltips might be triggered inside
## a string is not a big deal. Sometimes it is even helpful.

##    def test_getRoot_InsideStrings(self):
##        values = (
##            ('x = ".', '.', ''),
##            ("x = '.", '.', ''),
##            ('x = """.', '.', ''),
##            ("x = '''.", '.', ''),
##
##            ('x = "(', '(', ''),
##            ("x = '(", '(', ''),
##            ('x = """(', '(', ''),
##            ("x = '''(", '(', ''),
##
##            ('x = "spam', '.', ''),
##            ('x = "spam.', '.', ''),
##            ("x = 'spam.", '.', ''),
##            ('x = """spam.', '.', ''),
##            ("x = '''spam.", '.', ''),
##
##            ('x = "spam', '(', ''),
##            ('x = "spam(', '(', ''),
##            ("x = 'spam(", '(', ''),
##            ('x = """spam(', '(', ''),
##            ("x = '''spam(", '(', ''),
##
##            ('x = "spam.eggs.', '.', ''),
##            ("x = 'spam.eggs.", '.', ''),
##            ('x = """spam.eggs.', '.', ''),
##            ("x = '''spam.eggs.", '.', ''),
##
##            ('x = "spam.eggs(', '(', ''),
##            ("x = 'spam.eggs(", '(', ''),
##            ('x = """spam.eggs(', '(', ''),
##            ("x = '''spam.eggs(", '(', ''),
##        )
##        for input, terminator, output in values:
##            self._checkRoot(input, terminator, output)

    def test_getRoot_EmptyTypes(self):
        values = (
            ("''.", '.', "''"),
            ('"".', '.', '""'),
            ('"""""".', '.', '""""""'),
            ("''''''.", '.', "''''''"),

            ('[].', '.', '[]'),
            ('().', '.', '()'),
            ('{}.', '.', '{}'),

            ('[](', '(', '[]'),
            ('()(', '(', '()'),
            ('{}(', '(', '{}'),

            ("x = ''.", '.', "''"),
            ('x = "".', '.', '""'),
            ('x = """""".', '.', '""""""'),
            ("x = ''''''.", '.', "''''''"),

            ('x = [].', '.', '[]'),
            ('x = ().', '.', '()'),
            ('x = {}.', '.', '{}'),

            ('x = [](', '(', '[]'),
            ('x = ()(', '(', '()'),
            ('x = {}(', '(', '{}'),

            ('print [].', '.', '[]'),
            ('print ().', '.', '()'),
            ('print {}.', '.', '{}'),

            ('print [](', '(', '[]'),
            ('print ()(', '(', '()'),
            ('print {}(', '(', '{}'),

            ("''.attr.", '.', "''.attr"),
            ('"".attr.', '.', '"".attr'),
            ('"""""".attr.', '.', '"""""".attr'),
            ("''''''.attr.", '.', "''''''.attr"),

            ('[].attr.', '.', '[].attr'),
            ('().attr.', '.', '().attr'),
            ('{}.attr.', '.', '{}.attr'),

            ('[].attr(', '(', '[].attr'),
            ('().attr(', '(', '().attr'),
            ('{}.attr(', '(', '{}.attr'),

            ('spam().', '.', ''),
            ('spam_().', '.', ''),
            ('spam5().', '.', ''),
            ('spam[]().', '.', ''),
            ('spam()[].', '.', ''),
            ('spam[]{}.', '.', ''),

            ("spam(''.", '.', "''"),
            ('spam("".', '.', '""'),
            ('spam("""""".', '.', '""""""'),
            ("spam(''''''.", '.', "''''''"),

            ('spam([].', '.', '[]'),
            ('spam(().', '.', '()'),
            ('spam({}.', '.', '{}'),
            ('spam[[].', '.', '[]'),
            ('spam[().', '.', '()'),
            ('spam[{}.', '.', '{}'),
            ('x = {[].', '.', '[]'),
            ('x = {().', '.', '()'),
            ('x = {{}.', '.', '{}'),

            ('spam,[].', '.', '[]'),
            ('spam+[].', '.', '[]'),
            ('spam-[].', '.', '[]'),
            ('spam*[].', '.', '[]'),
            ('spam/[].', '.', '[]'),
            ('spam=[].', '.', '[]'),
            ('spam%[].', '.', '[]'),
            ('spam<[].', '.', '[]'),
            ('spam>[].', '.', '[]'),
            ('spam&[].', '.', '[]'),
            ('spam|[].', '.', '[]'),
            ('spam^[].', '.', '[]'),
            ('spam~[].', '.', '[]'),
            ('spam:[].', '.', '[]'),

            ('spam,().', '.', '()'),
            ('spam+().', '.', '()'),
            ('spam-().', '.', '()'),
            ('spam*().', '.', '()'),
            ('spam/().', '.', '()'),
            ('spam=().', '.', '()'),
            ('spam%().', '.', '()'),
            ('spam<().', '.', '()'),
            ('spam>().', '.', '()'),
            ('spam&().', '.', '()'),
            ('spam|().', '.', '()'),
            ('spam^().', '.', '()'),
            ('spam~().', '.', '()'),
            ('spam:().', '.', '()'),

            ('spam,{}.', '.', '{}'),
            ('spam+{}.', '.', '{}'),
            ('spam-{}.', '.', '{}'),
            ('spam*{}.', '.', '{}'),
            ('spam/{}.', '.', '{}'),
            ('spam={}.', '.', '{}'),
            ('spam%{}.', '.', '{}'),
            ('spam<{}.', '.', '{}'),
            ('spam>{}.', '.', '{}'),
            ('spam&{}.', '.', '{}'),
            ('spam|{}.', '.', '{}'),
            ('spam^{}.', '.', '{}'),
            ('spam~{}.', '.', '{}'),
            ('spam:{}.', '.', '{}'),
        )
        for input, terminator, output in values:
            self._checkRoot(input, terminator, output)


# Support for GetBaseObjectTestCase and GetAttributeNamesTestCase.

class Foo:
    def __init__(self):
        pass

    def __del__(self):
        pass

    def _private(self):
        pass

class Bar:
    pass

class Spam:
    def __call__(self):
        pass

    def foo(self):
        pass

    def bar(spam):
        # It shouldn't matter what we call "self".
        pass

    def eggs(self):
        pass

def ham(eggs):
    pass

class GetBaseObjectTestCase(unittest.TestCase):

    def test_getBaseObject(self):
        spam = Spam()
        eggs = Spam.eggs
        listappend = [].append
        spamda = lambda: None
        values = [
            ('spam', 'spam', 0),
            (123, 123, 0),
            (12.3, 12.3, 0),
            ([], [], 0),
            ((), (), 0),
            ({}, {}, 0),
            # Builtin function.
            (len, len, 0),
            # Builtin method.
            (listappend, listappend, 0),
            # User function.
            (ham, ham, 0),
            # Lambda.
            (spamda, spamda, 0),
            # Class with no init.
            (Bar, Bar, 0),
        ]
        for object, baseObject, dropSelf in values:
            result = introspect.getBaseObject(object)
            self.assertEqual(result, (baseObject, dropSelf))


class GetAttributeTestCase(unittest.TestCase):
    """Base class for other test case classes."""

    def setUp(self):
        self.values = (
            '__abs__',
            '__add__',
            '__and__',
            '__base__',
            '__bases__',
            '__basicsize__',
            '__builtins__',
            '__call__',
            '__class__',
            '__closure__',
            '__cmp__',
            '__code__',
            '__coerce__',
            '__contains__',
            '__defaults__',
            '__del__',
            '__delattr__',
            '__delitem__',
            '__delslice__',
            '__dict__',
            '__dictoffset__',
            '__div__',
            '__divmod__',
            '__doc__',
            '__eq__',
            '__file__',
            '__flags__',
            '__float__',
            '__floordiv__',
            '__func__',
            '__ge__',
            '__get__',
            '__getattr__',
            '__getattribute__',
            '__getitem__',
            '__getslice__',
            '__globals__',
            '__gt__',
            '__hash__',
            '__hex__',
            '__iadd__',
            '__imul__',
            '__init__',
            '__int__',
            '__invert__',
            '__itemsize__',
            '__iter__',
            '__kwdefaults__',
            '__le__',
            '__len__',
            '__long__',
            '__lshift__',
            '__lt__',
            '__mod__',
            '__module__',
            '__mro__',
            '__mul__',
            '__name__',
            '__ne__',
            '__neg__',
            '__new__',
            '__nonzero__',
            '__oct__',
            '__or__',
            '__path__',
            '__pos__',
            '__pow__',
            '__qualname__',
            '__radd__',
            '__rand__',
            '__rdiv__',
            '__rdivmod__',
            '__reduce__',
            '__repr__',
            '__rfloordiv__',
            '__rlshift__',
            '__rmod__',
            '__rmul__',
            '__ror__',
            '__rpow__',
            '__rrshift__',
            '__rshift__',
            '__rsub__',
            '__rtruediv__',
            '__rxor__',
            '__self__',
            '__setattr__',
            '__setitem__',
            '__setslice__',
            '__str__',
            '__sub__',
            '__subclasses__',
            '__truediv__',
            '__warningregistry__',
            '__weakrefoffset__',
            '__xor__',
            'append',
            'capitalize',
            'center',
            'clear',
            'close',
            'closed',
            'co_argcount',
            'co_cellvars',
            'co_code',
            'co_consts',
            'co_filename',
            'co_firstlineno',
            'co_flags',
            'co_freevars',
            'co_lnotab',
            'co_name',
            'co_names',
            'co_nlocals',
            'co_stacksize',
            'co_varnames',
            'conjugate',
            'copy',
            'count',
            'decode',
            'encode',
            'endswith',
            'expandtabs',
            'extend',
            'fileno',
            'find',
            'flush',
            'get',
            'has_key',
            'imag',
            'index',
            'insert',
            'isalnum',
            'isalpha',
            'isatty',
            'isdigit',
            'islower',
            'isspace',
            'istitle',
            'isupper',
            'items',
            'iteritems',
            'iterkeys',
            'itervalues',
            'join',
            'keys',
            'ljust',
            'lower',
            'lstrip',
            'mode',
            'mro',
            'name',
            'pop',
            'popitem',
            'real',
            'read',
            'readinto',
            'readline',
            'readlines',
            'remove',
            'replace',
            'reverse',
            'rfind',
            'rindex',
            'rjust',
            'rstrip',
            'seek',
            'setdefault',
            'softspace',
            'sort',
            'split',
            'splitlines',
            'start',
            'startswith',
            'step',
            'stop',
            'strip',
            'swapcase',
            'tell',
            'title',
            'tolist',
            'translate',
            'truncate',
            'update',
            'upper',
            'values',
            'write',
            'writelines',
            'xreadlines',
        )

# Since getAllAttributeNames() calls str(object),
# we need to test for a broken __str__ method.
class BrokenStr:
    def __str__(self):
        raise Exception

brokenStr = BrokenStr()

class GetAttributeNamesTestCase(GetAttributeTestCase):

    def setUp(self):
        GetAttributeTestCase.setUp(self)
        from wx import py
        spam = Spam()
        self.f = open(os.path.join(os.path.dirname(__file__), 'test_introspect.py'))
        self.items = [
            None,
            int(123),
            float(123),
            complex(123),
            "",
            [],
            (),
            {},
            # Builtin function.
            len,
            # Builtin method.
            [].append,
            # User function.
            ham,
            # Lambda.
            lambda: None,
            # Class with no init.
            Bar,
            # Instance with no init.
            Bar(),
            # Class with init and del.
            Foo,
            # Instance with init and del.
            Foo(),
            # Bound method.
            spam.foo,
            # Unbound method.
            Spam.eggs,
            # Callable instance.
            spam,
            # Module.
            introspect,
            # Package.
            py,
            # File.
            self.f,
            # Slice.
            slice(0),
            # Ellipsis.
            Ellipsis,
            # BrokenStr class.
            BrokenStr,
            # BrokenStr instance.
            brokenStr,
        ]

    def tearDown(self):
        self.items = None
        self.f.close()

    def test_getAttributeNames(self):
        for item in self.items:
            self._checkAttributeNames(item)
        if 'object' in __builtins__ if isinstance(__builtins__, dict) else vars(__builtins__):
            self._checkAttributeNames(object)

    def test_getAttributeNames_NoSingle(self):
        for item in self.items:
            result = list(introspect.getAttributeNames(item, includeSingle=0))
            attributes = [attribute for attribute in result \
                          if attribute[0] != '_' or attribute[:2] == '__']
            self.assertEqual(result, attributes,
                             ':item: %r' % (item,))

    def test_getAttributeNames_NoDouble(self):
        for item in self.items:
            result = list(introspect.getAttributeNames(item, includeDouble=0))
            attributes = [attribute for attribute in result \
                          if attribute[:2] != '__']
            self.assertEqual(result, attributes,
                             ':item: %r' % (item,))

    def test_getAttributeNames_NoSingleOrDouble(self):
        for item in self.items:
            result = list(introspect.getAttributeNames(item, includeSingle=0,
                                                       includeDouble=0))
            attributes = [attribute for attribute in result \
                          if attribute[0] != '_']
            self.assertEqual(result, attributes,
                             ':item: %r' % (item,))

    def _checkAttributeNames(self, item):
        result = introspect.getAttributeNames(item)
        attributes = [attribute for attribute in self.values \
                      if hasattr(item, attribute)]
        for attribute in attributes:
            self.assertTrue(attribute in result,
                            ':item: %r :attribute: %r' % (item, attribute))


class GetAutoCompleteListTestCase(GetAttributeTestCase):

    def setUp(self):
        GetAttributeTestCase.setUp(self)
        self.items = (
            'None.',
            '123 .',
            '"".',
            '[].',
            '().',
            '{}.',
            # Builtin function.
            'len.',
            # Builtin method.
            '[].append.',
        )

    def test_getAutoCompleteList(self):
        for item in self.items:
            result = introspect.getAutoCompleteList(item)
            object = eval(item[:-1])
            attributes = [attribute for attribute in self.values \
                          if hasattr(object, attribute)]
            for attribute in attributes:
                self.assertTrue(attribute in result,
                                ':item: %r :attribute: %r' % (item, attribute))

    def test_getAutoCompleteList_NoSingle(self):
        for item in self.items:
            result = list(introspect.getAutoCompleteList(item, includeSingle=0))
            attributes = [attribute for attribute in result \
                          if attribute[0] != '_' or attribute[:2] == '__']
            self.assertEqual(result, attributes,
                             ':item: %r' % (item,))

    def test_getAutoCompleteList_NoDouble(self):
        for item in self.items:
            result = list(introspect.getAutoCompleteList(item, includeDouble=0))
            attributes = [attribute for attribute in result \
                          if attribute[:2] != '__']
            self.assertEqual(result, attributes,
                             ':item: %r' % (item,))

    def test_getAutoCompleteList_NoSingleOrDouble(self):
        for item in self.items:
            result = list(introspect.getAutoCompleteList(item, includeSingle=0,
                                                         includeDouble=0))
            attributes = [attribute for attribute in result \
                          if attribute[0] != '_']
            self.assertEqual(result, attributes,
                             ':item: %r' % (item,))


# Support for GetConstructorTestCase.

class A1:
    def __init__(self, a):
        self.a = a

class B1(A1):
    def __init__(self, b):
        self.b = b

class C1(A1):
    pass

class D1(C1, B1):
    pass

if 'object' in __builtins__ if isinstance(__builtins__, dict) else vars(__builtins__):
    class A2(object):
        def __init__(self, a):
            self.a = a

    class B2(A2):
        def __init__(self, b):
            self.b = b

    class C2(A2):
        pass

    class D2(C2, B2):
        pass

class N:
    pass

class O:
    def __init__(self, a, b=2, *args, **kwargs):
        pass

class P(O):
    pass

class Q(P):
    def __init__(self, c, d=4):
        pass

class GetConstructorTestCase(unittest.TestCase):

    def test_getConstructor_None(self):
        values = (N, 1, 'spam', {}, [], (), dir)
        for value in values:
            self.assertEqual(introspect.getConstructor(N), None)


if __name__ == '__main__':
    sys.ps2 = '... '
    unittest.main()
