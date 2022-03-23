import ast
import sys
from typing import Generator, Tuple, Type, Any, List

if sys.version_info < (3, 8):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata

PLY801 = 'PLY801 `:has-text()` pseudo-class should have an html tag specified at the start'
PLY802 = 'PLY802 string starting with `..` denotes x-path which is not allowed'
PLY803 = 'PLY803 string starting with `//` denotes x-path which is not allowed'
PLY804 = 'PLY804 use of `nth-child` is discouraged. ' \
         'Select a more specific selector to avoid structural dependency issues.'
PLY805 = 'PLY805 use of more than one query operator `>>` may cause structural dependency issues.'


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.problems: List[Tuple[int, int, str]] = []

    # def visit_Call(self, node: ast.Call) -> None:
    #     for keyword in node.keywords:
    #         if (
    #                 keyword.arg is None and
    #                 isinstance(keyword.value, ast.Dict) and
    #                 all(
    #                     isinstance(key, ast.Str)
    #                     for key in keyword.value.keys
    #                 ) and
    #                 all(
    #                     key.s.isidentifier()
    #                     for key in keyword.value.keys
    #
    #                 )
    #         ):
    #             self.problems.append((node.lineno, node.col_offset))
    #
    #     self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> Any:
        if node.value.value.startswith(':has-text("'):
            self.problems.append((node.lineno, node.col_offset, PLY801))
        if '(:has-text("' in node.value.value:
            self.problems.append((node.lineno, node.col_offset, PLY801))
        if node.value.value.startswith('..'):
            self.problems.append((node.lineno, node.col_offset, PLY802))
        if node.value.value.startswith('//'):
            self.problems.append((node.lineno, node.col_offset, PLY803))
        if 'nth-child' in node.value.value:
            self.problems.append((node.lineno, node.col_offset, PLY804))
        query_operator_list = node.value.value.split('>>')
        if len(query_operator_list) > 2:
            self.problems.append((node.lineno, node.col_offset, PLY805))
        self.generic_visit(node)


class Plugin:
    name = __name__
    version = importlib_metadata.version(__name__)

    def __init__(self, tree: ast.AST) -> None:
        self.tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor()
        visitor.visit(self.tree)
        for line, col, msg in visitor.problems:
            yield line, col, msg, type(self)
