#!/usr/bin/env python3
"""测试文件：用于验证 GitHub 自动化流程的数学函数示例。


def add(a, b):
    """加法函数.
    
    Args:
        a: 第一个数字
        b: 第二个数字
    
    Returns:
        两数之和
    """
    return a + b


def multiply(a, b):
    """乘法函数.
    
    Args:
        a: 第一个数字
        b: 第二个数字
    
    Returns:
        两数之积
    """
    return a * b


def divide(a, b):
    """除法函数.
    
    Args:
        a: 被除数
        b: 除数
    
    Returns:
        除法结果
    
    Raises:
        ValueError: 当除数为零时
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


if __name__ == "__main__":
    # 简单测试
    print(f"2 + 3 = {add(2, 3)}")
    print(f"4 * 5 = {multiply(4, 5)}")
    print(f"10 / 2 = {divide(10, 2)}")
