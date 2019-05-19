import os
import sys
import json
from enum import Enum

import pytest
import requests


class RESULT(Enum):
    PASSED = "passed"
    FAILURE = "failure"


unit_tests = {
    "hello": [
        ("hello", 20, "依赖安装失败")
    ],
    "icu": [
        ("icu", 30, "company_996 函数测试失败")
    ],
    "not_found": [
        ("404_data", 3, "404 测试失败"),
        ("404_code", 3, "404 测试失败"),
        ("404_file", 4, "404 测试失败")
    ],
    "reshape": [
        ("reshape_file_md5", 5, "读取图片文件 MD5 编码错误"),
        ("reshape_file_b64", 5, "读取图片文件 Base64 编码错误"),
        ("reshape_http_md5", 5, "从 HTTP 链接下载图片 MD5 编码错误"),
        ("reshape_http_b64", 5, "从 HTTP 链接下载图片 Base64 编码错误")
    ]
}


def do_unit_test(file, func, score, error_log):
    """
    执行单个单元测试函数

    :param: file: str - 测试文件名
    :param: func: str - 测试函数名
    :param: score: int - 测试函数分数
    :param: error_log: str - 测试函数报错得到的 error_log
    """
    if not pytest.main(["test_{}.py::test_{}".format(file, func)]):
        return score, "测试成功"
    else:
        return 0, error_log


def test_ssh(id: str) -> int:
    res = requests.get("https://pandora.sumsc.xin/ssh?id_tag={}".format(id))
    if res.json().get('message') and os.path.exists('../pandora/img.txt') and os.path.isfile('../pandora/img.txt'):
        return 20, "测试成功"
    else:
        return 0, "SSH Key 测试未通过"


def do_test(id: str):
    res = 0
    res_log = ""
    for i in unit_tests:
        for col in unit_tests[i]:
            score, log = do_unit_test(i, *col)
            res += score
            res_log += "test_{} 测试结果：{}\n".format(col[0], log)
    score, log = test_ssh(id)
    res += score
    res_log += "test_ssh_key 测试结果：{}\n".format(log)
    return res, res_log


def post_grade(id: str):
    """
    接受用户学号进行判题
    """
    url = "https://pandora.sumsc.xin/grade"
    headers = {
        "X-DB-Auth": "whatsmydbauth"
    }
    status, log = do_test(id)
    resp = requests.post(url, headers=headers, json={
        "id_tag": id,
        "test_status": RESULT.PASSED.value if status == 100 else RESULT.FAILURE.value,
        "error_log": log
    })
    print("id: {}, status: {}".format(id, RESULT.PASSED.value if resp.status_code == 200 and not resp.json().get(
        'error') else RESULT.FAILURE.value))
    exit(0 if resp.status_code == 200 and not resp.json().get('error') else 1)


if __name__ == "__main__":
    # 接受一个命令行参数 id_tag
    if sys.argv[1] == '--help':
        print("python grade.py [ID_TAG]")
    else:
        post_grade(sys.argv[1])
