#!/usr/bin/env python3
"""
测试文件：用于验证 GitHub 自动化流程
"""


def add(a, b):
    """加法函数"""
    return a + b


def multiply(a, b):
    """乘法函数"""
    return a * b


def divide(a, b):
    """除法函数"""
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b


def main():
    """主函数"""
    print("测试自动化流程")
    print(f"2 + 3 = {add(2, 3)}")
    print(f"4 * 5 = {multiply(4, 5)}")
    print(f"10 / 2 = {divide(10, 2)}")


if __name__ == "__main__":
    main()
