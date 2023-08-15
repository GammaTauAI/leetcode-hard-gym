from typing import Optional
from pydantic import BaseModel
from enum import Enum


class ProgrammingLanguage(Enum):
    """
    Enum for valid LeetCodeSubmission programming languages
    """

    CPP = "c++"
    JAVA = "java"
    PYTHON = "python"
    PYTHON3 = "python3"
    C = "c"
    C_SHARP = "c#"
    JAVASCRIPT = "javascript"
    RUBY = "ruby"
    SWIFT = "swift"
    GO = "go"
    SCALA = "scala"
    KOTLIN = "kotlin"
    RUST = "rust"
    PHP = "php"
    TYPESCRIPT = "typescript"
    RACKET = "racket"
    ERLANG = "erlang"
    ELIXIR = "elixir"
    DART = "dart"
    MYSQL = "mysql"
    MS_SQL_SERVER = "ms sql server"
    ORACLE = "oracle"


class LeetCodeSubmission(BaseModel):
    """
    Model for a Leetcode Code Submission
    """

    code: str
    lang: ProgrammingLanguage
    question_id: str
    question_slug: str
    question_id: Optional[str] = None
    timeout: int = 5
