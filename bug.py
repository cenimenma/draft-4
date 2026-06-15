import os
import sqlite3

def get_user_data(username):
    # 【Bug 1：严重安全漏洞 - SQL 注入】
    # 直接用字符串拼接构造 SQL 语句，黑客只要输入类似 "' OR '1'='1" 就能脱裤
    db_path = "users.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchall()

def process_logs(log_directory):
    # 【Bug 2：逻辑/运行隐患 - 未定义变量与资源未关闭】
    # 这里故意漏掉了 conn.close() 导致句柄泄漏。
    # 并且下面莫名其妙使用了一个根本没有定义的变量 `log_files_count`
    print(f"正在处理目录: {log_directory}")
    
    # 致命低级错误：使用了未定义的变量，程序运行到这里铁定崩溃
    if log_files_count > 0:
        print("日志文件不为空")
        
    return True

def calculate_retry_timeout(attempt):
    # 【Bug 3：逻辑漏洞 - 永无止境的死循环】
    # 当失败重试次数大于 5 次时，由于忘了写退出逻辑或 break，会直接卡死服务器 CPU
    while attempt > 5:
        print("重试次数过多，正在等待重新连接...")
        # 完蛋，这里没有让 attempt 递减，也没有 break，死循环达成了！
        
    return attempt * 2