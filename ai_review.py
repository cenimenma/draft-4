"""
AI Code Review Agent - GitHub Actions Integration
极简版本：直接用公网大模型 API 进行代码审查
"""
import os
import subprocess
import requests
from openai import OpenAI


def get_git_diff():
    """获取本次提交或 PR 的代码变动"""
    try:
        # 对比上一次提交，获取纯文本的 diff 差异
        diff = subprocess.check_output(["git", "diff", "HEAD~1", "HEAD"]).decode("utf-8")
        return diff
    except Exception as e:
        return f"获取 Diff 失败: {str(e)}"


def call_ai_agent(diff_content):
    """模拟微调 Agent 进行 Prompt 调用"""
    if not diff_content.strip():
        return "本次提交没有代码变动。"

    # 初始化大模型客户端（此处以 DeepSeek 为例）
    client = OpenAI(
        api_key=os.environ.get("LLM_API_KEY"),
        base_url="https://open.bigmodel.cn/api/paas/v4"  # 开完会后可改成你国内 GPU 机器的本地 Ollama 地址
    )

    prompt = f"""
You are a strict and expert code auditor. Please review the following `git diff` changes.
1. Identify any potential logic flaws, infinite loops, or null pointer/subscriptable errors.
2. Identify security vulnerabilities (e.g., hardcoded credentials, SQL injection).
3. Provide specific, actionable refactoring suggestions.

Please output your review clearly using Markdown format. If the code looks pristine and well-written, praise the developer warmly.

Here is the diff content:
{diff_content}
"""

    response = client.chat.completions.create(
        model="glm-4.6v-flashx",  # 或者是你微调的模型名称
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content


def post_github_comment(review_text):
    """将 AI 的审查意见自动回写到 GitHub 上"""
    token = os.environ.get("GITHUB_TOKEN")
    # 从 GitHub 的环境变量中自动获取当前仓库名和当前触发的 Commit ID
    repo = os.environ.get("GITHUB_REPOSITORY")
    commit_sha = os.environ.get("GITHUB_SHA")

    url = f"https://api.github.com/repos/{repo}/commits/{commit_sha}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {"body": f"### 🤖 AI Agent 自动化代码审查报告\n\n{review_text}"}
    
    res = requests.post(url, json=payload, headers=headers)
    if res.status_code == 201:
        print("🎉 AI 审查意见已成功同步至 GitHub Commit 评论区！")
    else:
        print(f"回写失败: {res.text}")


if __name__ == "__main__":
    print("正在提取代码 Diff...")
    code_diff = get_git_diff()
    print("正在召唤 AI Agent 审计代码...")
    review = call_ai_agent(code_diff)
    print("正在将结果同步回 GitHub...")
    post_github_comment(review)
