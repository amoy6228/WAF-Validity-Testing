# 🔒 WAF-Validity-Testing

一个基于 Python 的轻量级脚本，用于批量检测域名是否正确配置了 Web 应用防火墙（WAF）。支持多线程加速与实时结果保存。

---

## ⚙️ 脚本原理

该脚本的核心思路为：

1. **读取域名列表**  
   从 `domains.txt` 文件中逐行读取域名，每个域名将被单独测试。

2. **HTTPS 请求测试**  
   根据domains文件自动选择HTTP协议，并自动忽略证书校验：
   - 若响应状态码为 `200`，说明服务器响应正常；
   - 若状态码异常（如 403、500 等），跳过该域名的后续检测。

3. **WAF 拦截测试**  
   对状态正常的域名追加疑似恶意参数 `/?test=alert(123)`，模拟潜在攻击行为；
   - 若响应中包含 **“https://imgcache.qq.com/qcloud/security/static/imgs/copy.svg”** 等字样，判定为 WAF 成功拦截；
   - 否则认为未拦截。
   - 可以自定义增加判断语句，增加对其他WAF的识别。

4. **Excel 实时保存**  
   所有测试结果实时追加写入 `waf_test_results.xlsx`，防止中途退出丢失数据。

5. **多线程加速**  
   使用 `ThreadPoolExecutor` 实现并发检测，大幅提升测试效率。

---

## 📦 安装依赖

请确保使用 Python 3.7+，并安装以下依赖：

```bash
pip install requests openpyxl
````

---

## 🚀 使用方法

1. **准备域名文件**（`domains.txt`）：

   ```txt
   https://example1.com
   http://example2.com:4000
   https://example3.com:8000
   ```

2. **运行脚本**：

   ```bash
   python waf_checker.py
   ```

3. **查看结果**：

   结果文件将保存在当前目录下的 `waf_test_results.xlsx`。

---

## 📁 输入输出说明

* 📥 输入文件：`domains.txt`

  * 每行一个域名，不带域名后缀 `/`

* 📤 输出文件：`waf_test_results.xlsx`

  * 含以下列：

    | 域名 | 状态码 | 服务器状态 | WAF防护 |
    | -- | --- | ----- | ----- |

---

## 📄 示例输出（Excel）

| 域名                        | 状态码 | 服务器状态    | WAF防护 |
|---------------------------| --- | -------- | ----- |
| https://example1.com      | 200 | 正常       | 拦截成功  |
| http://example2.com:4000  | 200 | 正常       | 未拦截   |
| https://example3.com:8000 | -   | 异常（连接超时） | 未检测   |

---

## 🧠 脚本特点

* ✅ **简单易用**：一个文件即可运行，无需复杂配置
* ✅ **支持 HTTP 及 HTTPS 协议**
* ✅ **多线程加速处理**
* ✅ **实时写入 Excel，防止数据丢失**
* ✅ **WAF 拦截判定准确、逻辑清晰**
