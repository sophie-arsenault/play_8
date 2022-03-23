import ast
from typing import Set

from play_8 import Plugin

has_text_bad_01 = '''
selector = ':has-text("sample text")'
'''

has_text_bad_02 = '''
selector = ':other-text(:has-text("sample text"))'
'''

has_text_good = '''
selector = 'span:has-text("sample text")'
'''

sample_x_path_01 = '''
selector = '..this is another example'
'''

sample_x_path_02 = '''
selector = '//this is a sample'
'''

nth_child = '''
selector = 'div:text-is("Amie") nth-child operator'
'''

more_than_one = '''
selector = 'div:text-is("Friend") >> div.input-container >> input'
'''

only_one = '''
selector = 'div:text-is("Amigos") >> div.input-container'
'''


def _results(s: str) -> Set[str]:
    tree = ast.parse(s)
    plugin = Plugin(tree)
    return {f'{line}:{col + 1} {msg}' for line, col, msg, _ in plugin.run()}


def test_trivial_case():
    assert _results('') == set()


def test_no_value_preceding_has_text():
    ret = _results(has_text_bad_01)
    assert ret == {'2:1 PLY801 `:has-text()` pseudo-class should have an html tag specified at the start'}
    ret_2 = _results(has_text_bad_02)
    assert ret_2 == {'2:1 PLY801 `:has-text()` pseudo-class should have an html tag specified at the start'}


def test_value_preceding_has_text():
    assert _results(has_text_good) == set()


def test_x_path_string():
    ret_1 = _results(sample_x_path_01)
    assert ret_1 == {'2:1 PLY802 string starting with `..` denotes x-path which is not allowed'}
    ret_2 = _results(sample_x_path_02)
    assert ret_2 == {'2:1 PLY803 string starting with `//` denotes x-path which is not allowed'}


def test_nth_child():
    ret = _results(nth_child)
    assert ret == {'2:1 PLY804 use of `nth-child` is discouraged. '
                   'Select a more specific selector to avoid structural dependency issues.'}


def test_more_than_one_query_operator():
    ret = _results(more_than_one)
    assert ret == {'2:1 PLY805 use of more than one query operator `>>` may cause structural dependency issues.'}


def test_only_one_query_operator():
    assert _results(only_one) == set()


def test_allowed_splat_arguments():
    assert _results('f(**{"foo-bar": "baz"})') == set()
