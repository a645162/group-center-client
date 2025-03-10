from typing import List


def contains_any_keywords(text: str, keywords: List[str]) -> bool:
    """
    检查字符串中是否包含任何关键词

    Args:
        text (str): 待检查的字符串
        keywords (list): 关键词列表

    Returns:
        bool: 如果找到任何一个关键词则返回True，否则返回False
    """
    if not text or not keywords:
        return False

    for keyword in keywords:
        if keyword in text:
            return True

    return False


def any_string_contains_keywords(strings: List[str], keywords: List[str]) -> bool:
    """
    检查字符串列表中是否有任何一个字符串包含关键词列表中的任何一个关键词

    Args:
        strings (List[str]): 待检查的字符串列表
        keywords (List[str]): 关键词列表

    Returns:
        bool: 如果找到任何一个字符串包含任何一个关键词则返回True，否则返回False
    """
    if not strings or not keywords:
        return False

    for string in strings:
        if contains_any_keywords(string, keywords):
            return True

    return False


def main():
    """
    测试contains_any_keywords函数的功能
    """
    # 测试用例1：正常情况，包含关键词
    text1 = "这是一个包含Python和Java的句子"
    keywords1 = ["Python", "C++", "Java"]
    result1 = contains_any_keywords(text1, keywords1)
    print(f"测试1 - 文本: '{text1}', 关键词: {keywords1}")
    print(f"结果: {result1}, 预期: True\n")

    # 测试用例2：正常情况，不包含关键词
    text2 = "这是一个普通的句子"
    keywords2 = ["Python", "C++", "Java"]
    result2 = contains_any_keywords(text2, keywords2)
    print(f"测试2 - 文本: '{text2}', 关键词: {keywords2}")
    print(f"结果: {result2}, 预期: False\n")

    # 测试用例3：空文本
    text3 = ""
    keywords3 = ["Python", "C++", "Java"]
    result3 = contains_any_keywords(text3, keywords3)
    print(f"测试3 - 文本: '{text3}', 关键词: {keywords3}")
    print(f"结果: {result3}, 预期: False\n")

    # 测试用例4：空关键词列表
    text4 = "这是一个包含Python和Java的句子"
    keywords4 = []
    result4 = contains_any_keywords(text4, keywords4)
    print(f"测试4 - 文本: '{text4}', 关键词: {keywords4}")
    print(f"结果: {result4}, 预期: False\n")

    # 测试用例5：大小写敏感测试
    text5 = "这是一个包含python和JAVA的句子"
    keywords5 = ["Python", "Java"]
    result5 = contains_any_keywords(text5, keywords5)
    print(f"测试5 - 文本: '{text5}', 关键词: {keywords5}")
    print(f"结果: {result5}, 预期: False\n")

    # 测试新函数 any_string_contains_keywords
    print("\n测试 any_string_contains_keywords 函数:")

    # 测试用例1：列表中有字符串包含关键词
    strings1 = ["普通文本", "包含Python的文本", "其他文本"]
    kw1 = ["Python", "Java"]
    result1 = any_string_contains_keywords(strings1, kw1)
    print(f"测试1 - 字符串列表: {strings1}, 关键词: {kw1}")
    print(f"结果: {result1}, 预期: True\n")

    # 测试用例2：列表中没有字符串包含关键词
    strings2 = ["普通文本", "常规内容", "其他文本"]
    kw2 = ["Python", "Java"]
    result2 = any_string_contains_keywords(strings2, kw2)
    print(f"测试2 - 字符串列表: {strings2}, 关键词: {kw2}")
    print(f"结果: {result2}, 预期: False\n")

    # 测试用例3：空字符串列表
    strings3 = []
    kw3 = ["Python", "Java"]
    result3 = any_string_contains_keywords(strings3, kw3)
    print(f"测试3 - 字符串列表: {strings3}, 关键词: {kw3}")
    print(f"结果: {result3}, 预期: False\n")

    # 测试用例4：空关键词列表
    strings4 = ["普通文本", "包含Python的文本", "其他文本"]
    kw4 = []
    result4 = any_string_contains_keywords(strings4, kw4)
    print(f"测试4 - 字符串列表: {strings4}, 关键词: {kw4}")
    print(f"结果: {result4}, 预期: False\n")


if __name__ == "__main__":
    main()
