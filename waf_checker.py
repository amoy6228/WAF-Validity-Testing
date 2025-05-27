# encoding: utf-8
# @author: 爱喝水的仙人掌
# @file: waf_checker.py
# @time: 2025/5/27 16:45
import requests
import openpyxl
import threading
import os
from concurrent.futures import ThreadPoolExecutor

# 禁用 SSL 证书警告
requests.packages.urllib3.disable_warnings()

lock = threading.Lock()
EXCEL_FILE = "waf_test_results.xlsx"
DOMAIN_FILE = "domains.txt"
MAX_WORKERS = 10

# 初始化 Excel 文件
def init_excel():
    if not os.path.exists(EXCEL_FILE):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["域名", "状态码", "服务器状态", "WAF防护"])
        wb.save(EXCEL_FILE)

# 写入单条测试结果
def write_result(result):
    with lock:
        wb = openpyxl.load_workbook(EXCEL_FILE)
        ws = wb.active
        ws.append([result["域名"], result["状态码"], result["服务器状态"], result["WAF防护"]])
        wb.save(EXCEL_FILE)

# 测试单个域名
def test_domain(domain):
    base_url = f"{domain}"
    test_url = f"{base_url}/?test=alert(123)"
    result = {
        "域名": domain,
        "状态码": "",
        "服务器状态": "异常",
        "WAF防护": "未检测"
    }

    try:
        resp = requests.get(base_url, verify=False, timeout=10)
        result["状态码"] = resp.status_code
        if resp.status_code == 200:
            result["服务器状态"] = "正常"
            test_resp = requests.get(test_url, verify=False, timeout=10)
            if "https://imgcache.qq.com/qcloud/security/static/imgs/copy.svg" in test_resp.text:
                # print(test_resp.text)
                result["WAF防护"] = "腾讯云WAF拦截成功"
            elif "https://errors.aliyun.com/images/TB1TpamHpXXXXaJXXXXeB7nYVXX-104-162.png" in test_resp.text:
                # print(test_resp.text)
                result["WAF防护"] = "阿里云WAF拦截成功"
            else:
                result["WAF防护"] = "未拦截"
        else:
            result["服务器状态"] = f"异常（{resp.status_code}）"
    except Exception as e:
        result["服务器状态"] = f"异常（{str(e)}）"

    write_result(result)
    print(f"[完成] {domain} 状态: {result['服务器状态']} | WAF: {result['WAF防护']}")

# 主函数
def main():
    if not os.path.exists(DOMAIN_FILE):
        print(f"[错误] 未找到域名文件：{DOMAIN_FILE}")
        return

    init_excel()

    with open(DOMAIN_FILE, 'r', encoding='utf-8') as f:
        domains = [line.strip() for line in f if line.strip()]

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(test_domain, domains)

    print(f"\n所有测试完成，结果保存在：{EXCEL_FILE}")

if __name__ == "__main__":
    main()
