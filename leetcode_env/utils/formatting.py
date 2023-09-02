import ast
import re
from abc import ABC, abstractmethod
from typing import List

import astunparse


class SubmissionFormatter(ABC):
    """
    Class that converts between HumanEval and Leetcode submission formats.
    """

    @staticmethod
    @abstractmethod
    def to_leetcode(humaneval_snippet: str):
        """
        Convert the string to leetcode format
        """

    @staticmethod
    @abstractmethod
    def to_humaneval(leetcode_snippet: str):
        """
        Convert the string to humaneval format
        """

    @staticmethod
    @abstractmethod
    def add_docstring(snippet: str, description: str):
        """
        Add a docstring to the snippet
        """
    
    @staticmethod
    @abstractmethod
    def extract_signature(source: str) -> str:
        """
        Extract the signature from the function
        """



class PythonSubmissionFormatter:
    @staticmethod
    def add_docstring(snippet: str, description: str):
        snippet = snippet.strip("\n")
        # Add 4 spaces to the beginning of every line
        description = "\n".join([" " * 4 + line for line in description.splitlines()])
        docstring = f'''    """
{description}
    """'''
        return f"{snippet}\n{docstring}\n"

    @staticmethod
    def to_humaneval(leetcode_snippet: str) -> str:
        try:
            tree = ast.parse(leetcode_snippet)
        except IndentationError:
            class_source = leetcode_snippet.strip() + "\n        pass"
            tree = ast.parse(class_source)
        func_node = tree.body[0].body[0]
        func_node.args.args.pop(0)  # Remove 'self' argument

        if isinstance(func_node.body[-1], ast.Pass):
            func_node.body.pop()

        new_tree = ast.Module(body=[func_node], type_ignores=[])
        return f"{astunparse.unparse(new_tree).strip()}\n"

    @staticmethod
    def to_leetcode(humaneval_snippet: str, class_name: str = "Solution") -> str:
        # Get imports
        imports = "\n".join(
            PythonSubmissionFormatter.extract_imports(humaneval_snippet)
        )
        # Remove imports
        # humaneval_snippet = re.sub(r"^from\s+\S+\s+import.*|^import.*", "", humaneval_snippet, flags=re.MULTILINE)
        try:
            tree = ast.parse(humaneval_snippet)
        except IndentationError:
            function_source = humaneval_snippet.strip() + "\n    pass"
            tree = ast.parse(function_source)

        func_node = None
        for child in ast.iter_child_nodes(tree):
            if isinstance(child, ast.FunctionDef):
                func_node = child
                break

        docstring = ast.get_docstring(func_node)
        if docstring is not None:
            func_node.body.pop(0)

        if func_node.body and isinstance(func_node.body[-1], ast.Pass):
            func_node.body.pop()

        # Add 'self' argument back to the function
        self_arg = ast.arg(arg="self", annotation=None)
        func_node.args.args.insert(0, self_arg)
        class_node = ast.ClassDef(
            name=class_name,
            bases=[],
            keywords=[],
            body=[func_node],
            decorator_list=[],
        )
        new_tree = ast.Module(body=[class_node], type_ignores=[])
        return f"{imports}\n{astunparse.unparse(new_tree).strip()}\n"

    @staticmethod
    def extract_imports(source: str) -> List[str]:
        """
        Extract top level imports
        """
        standard_import = re.compile(r"^import (\w+(?:, \w+)*)")
        from_import = re.compile(r"^from (\w+) import (\w+(?:, \w+)*)")

        imports = []

        for line in source.splitlines():
            std_match = standard_import.match(line)
            from_match = from_import.match(line)

            if std_match:
                imports.append(std_match.group(0))

            if from_match:
                imports.append(from_match.group(0))

        return imports
    
    @staticmethod
    def extract_signature(source: str) -> str:
        return source.replace('def ', '', 1)[:-1]


class RustSubmissionFormatter:
    @staticmethod
    def add_docstring(snippet: str, description: str):
        # Formatting the docstring in Rust style using /* */
        rust_docstring = f"/*\n{description}\n*/"

        # Combining the docstring and the signature
        result = f"{rust_docstring}\n{snippet}"
        return result

    @staticmethod
    def extract_imports(source: str) -> List[str]:
        rust_import = re.compile(r"^use ([\w::]+(?:\s+as\s+\w+)?)(?:;\s*)?$")

        imports = []

        for line in source.splitlines():
            rust_match = rust_import.match(line)

            if rust_match:
                imports.append(rust_match.group(0).strip())

        return imports

    @staticmethod
    def remove_imports(source: str) -> str:
        rust_import = re.compile(r"^use ([\w::]+(?:\s+as\s+\w+)?)(?:;\s*)?$")

        lines = source.splitlines()
        new_lines = []
        for line in lines:
            if rust_import.match(line):
                print(f"Removing import: {line}")
            else:
                new_lines.append(line)

        return "\n".join(new_lines)

    @staticmethod
    def to_humaneval(leetcode_snippet: str) -> str:
        # Remove comments
        function_source = re.sub(r"//.*", "", leetcode_snippet)
        # Using the re.DOTALL flag to match across multiple lines
        function_source = re.sub(r"/\*.*?\*/", "", function_source, flags=re.DOTALL)

        # Remove solution class def
        function_source = re.sub(r"impl Solution \{\n", "", function_source)
        reversed_source = function_source[::-1]
        reversed_substituted = re.sub(r"\}", "", reversed_source, count=1)
        function_source = reversed_substituted[::-1]

        # Remove pub from function
        function_source = re.sub(r"pub ", "", function_source)

        # Unindent function
        whitespace = leading_whitespace_count(function_source)
        function_source = "\n".join(
            [line[whitespace:] for line in function_source.splitlines()]
        )
        function_source = function_source.strip()

        # Remove whitespace from every line in the function
        return f"{function_source}\n"

    @staticmethod
    def to_leetcode(humaneval_snippet: str, struct_name: str = "Solution") -> str:
        imports = "\n".join(RustSubmissionFormatter.extract_imports(humaneval_snippet))
        function_source = RustSubmissionFormatter.remove_imports(humaneval_snippet)

        function_source = re.sub(r"//.*", "", function_source)  # Remove comments
        function_source = re.sub(r"/\*.*?\*/", "", function_source, flags=re.DOTALL)
        function_source = function_source.strip()
        function_source = re.sub(
            r"fn ", "pub fn ", function_source, count=1
        )  # Add pub to root function
        return f"{imports}\nimpl {struct_name} {{\n{function_source}\n}}\n"  # Add impl struct_name { } around function
    
    @staticmethod
    def extract_signature(source: str) -> str:
        return source.strip('fn ').replace('{', '').replace('}', '').strip().strip('\n')


def leading_whitespace_count(s):
    # Split the string into lines and get the first line
    first_line = [l for l in s.splitlines() if l][0] if s else ""

    # Find the index of the first non-whitespace character
    non_whitespace_index = next(
        (i for i, char in enumerate(first_line) if not char.isspace()), None
    )

    # If the entire line consists of whitespaces (or is empty), then return its length
    if non_whitespace_index is None:
        return len(first_line)

    return non_whitespace_index