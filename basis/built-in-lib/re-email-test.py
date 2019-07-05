import re


def is_valid_email(addr):
    """写一个验证Email地址的正则表达式。版本一应该可以验证出类似的Email:

    someone@gmail.com
    bill.gates@microsoft.com
    """
    pat = r'\w+\.?\w+@\w+.(com|org)$'
    result = re.match(pat, addr)
    if result is not None:
        if result.group(0) == addr:
            print(result.group(0))
            return True
    return False


def name_of_email(addr):
    """版本二可以提取出带名字的Email地址

    <Tom Paris> tom@voyager.org => Tom Paris
    bob@example.com => bob
    """
    pat = r'^(<?)([\w\s]+)(>?)|[\w\s]+@'
    result = re.match(pat, addr)
    print(result.group(0))
    print(result.group(2))
    return result.group(2)

# 测试:
assert is_valid_email('someone@gmail.com')
assert is_valid_email('bill.gates@microsoft.com')
assert not is_valid_email('bob#example.com')
assert not is_valid_email('mr-bob@example.com')
print('ok')

assert name_of_email('<Tom Paris> tom@voyager.org') == 'Tom Paris'
assert name_of_email('tom@voyager.org') == 'tom'
print('ok')
