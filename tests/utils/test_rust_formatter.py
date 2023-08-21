from leetcode_env.utils.formatting import RustSubmissionFormatter
import pytest

to_humaneval_samples = [
    ("""
impl Solution {
    pub fn some_function(x: i32, y: i32) -> i32 {
    }
}
    """,
    """
fn some_function(x: i32, y: i32) -> i32 {
}
    """.strip()),

    ("""
impl Solution {
    pub fn some_function(x: i32, y: i32) -> i32 {
        x = 1;
        return x + y;
    }
}
    """,
    """
fn some_function(x: i32, y: i32) -> i32 {
    x = 1;
    return x + y;
}
    """.strip()),
]

to_leetcode_samples = [
    ("""
fn some_function(x: i32, y: i32) -> i32 {
}
    """.strip(),
    """
impl Solution {
pub fn some_function(x: i32, y: i32) -> i32 {
}
}
    """.strip()),

    ("""
fn some_function(x: i32, y: i32) -> i32 {
    x = 1;
    return x + y;
}
    """,
    """
impl Solution {
pub fn some_function(x: i32, y: i32) -> i32 {
    x = 1;
    return x + y;
}
}
    """.strip()),

    ("""
use std::collections::HashMap;
fn some_function(x: i32, y: i32) -> i32 {
    let z = x + y;
    return z;
}
    """,

    """
use std::collections::HashMap;
impl Solution {
pub fn some_function(x: i32, y: i32) -> i32 {
    let z = x + y;
    return z;
}
}
    """.strip()),
]

@pytest.mark.parametrize("leetcode_snippet, expected", to_humaneval_samples)
def test_to_humaneval(leetcode_snippet, expected):
    result = RustSubmissionFormatter.to_humaneval(leetcode_snippet).strip()
    print(f'Input:\n {leetcode_snippet}')
    print('-'*20)
    print(f"Expected:\n {expected}")
    print('-'*20)
    print(f"Result:\n {result}")
    assert result == expected

@pytest.mark.parametrize("humaneval_snippet, expected", to_leetcode_samples)
def test_to_leetcode(humaneval_snippet, expected):
    result = RustSubmissionFormatter.to_leetcode(humaneval_snippet).strip()
    print(f'Input:\n {humaneval_snippet}')
    print('-'*20)
    print(f"Expected:\n {expected}")
    print('-'*20)
    print(f"Result:\n {result}")
    assert result == expected
