"""示例测试模块，用于验证 CI 配置"""

import pytest


def test_example_assertion():
    """示例测试：验证基本断言"""
    assert 1 + 1 == 2
    assert 2 * 2 == 4


def test_string_operations():
    """测试字符串操作"""
    text = "Hello, World!"
    assert text.startswith("Hello")
    assert text.endswith("!")
    assert "World" in text


def test_list_operations():
    """测试列表操作"""
    items = [1, 2, 3, 4, 5]
    assert len(items) == 5
    assert 3 in items
    assert items[0] == 1


def test_dictionary_operations():
    """测试字典操作"""
    data = {"name": "AI Code", "version": "0.1.0"}
    assert data["name"] == "AI Code"
    assert "version" in data
    assert len(data) == 2


@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_multiplication(input, expected):
    """参数化测试：乘法"""
    result = input * 2
    assert result == expected


class TestMathOperations:
    """测试类：数学运算"""

    def test_addition(self):
        """加法测试"""
        assert 5 + 3 == 8

    def test_subtraction(self):
        """减法测试"""
        assert 10 - 4 == 6


def test_exception_handling():
    """测试异常处理"""
    with pytest.raises(ZeroDivisionError):
        result = 1 / 0


def test_import_github_assistant():
    """测试导入 github_assistant 模块"""
    try:
        import github_assistant
        assert github_assistant is not None
    except ImportError:
        pytest.skip("github_assistant 模块不存在或无法导入")


if __name__ == "__main__":
    # 可以直接运行此文件进行测试
    pytest.main([__file__, "-v"])
