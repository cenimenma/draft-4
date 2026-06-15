"""
AI Code Review Agent - GitHub Actions Integration
极简版本：直接用公网大模型 API 进行代码审查
"""
import os
import subprocess
import requests
from openai import OpenAI


def get_changed_files():
    """获取本次提交中变更的文件列表和完整内容"""
    try:
        # 获取最近一次提交变更的文件列表
        changed_files = subprocess.check_output(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD~1..HEAD"]
        ).decode("utf-8").strip().split('\n')
        
        files_content = []
        for file_path in changed_files:
            if not file_path or file_path.startswith('.github/'):
                continue
            
            try:
                # 读取文件的完整内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                files_content.append({
                    'path': file_path,
                    'content': content
                })
            except Exception as e:
                print(f"️  无法读取文件 {file_path}: {e}")
        
        return files_content
    except Exception as e:
        print(f"❌ 获取文件失败: {str(e)}")
        return []


def call_ai_agent(files_content):
    """使用完整代码内容进行 AI 审查"""
    if not files_content:
        return "本次提交没有可审查的代码文件。"

    # 初始化大模型客户端（此处以 DeepSeek 为例）
    client = OpenAI(
        api_key=os.environ.get("LLM_API_KEY"),
        base_url="https://open.bigmodel.cn/api/paas/v4"  # 开完会后可改成你国内 GPU 机器的本地 Ollama 地址
    )

    # 构建完整的代码内容字符串
    code_sections = []
    for file_info in files_content:
        code_sections.append(f"\n{'='*60}\n📄 File: {file_info['path']}\n{'='*60}\n{file_info['content']}")
    
    full_code = '\n'.join(code_sections)
    
    prompt = f"""
You are an extremely rigorous senior code quality expert and cybersecurity architect.

Please conduct an architectural-level quality review of the latest source code submitted by users. During the review process, please **do not directly point out bugs in specific lines of code, nor reveal errors**. Instead, compare the code to industry-grade development standards and **clearly describe the programming standards, security design principles, or architectural vulnerabilities violated by the code**.

Please strictly adhere to the following three points in your compliance review report (using clear Markdown format, making extensive use of lists and tables):

1. ️ Security Compliance Principles: Describe the defensive programming standards (e.g., OWASP Top 10 Security Standards) that the current code should follow when handling external input, authentication, or sensitive information.

2. ⚡ Operational Stability and Robustness Standards: Describe the robustness design standards that the system should meet when executing dynamic loops, lifecycle control, external resource (such as database connections, file handles) reclamation, and exception control flow handling.

3. 🛠️ Industrial-Grade Refactoring Evolution Direction: Based on the current code's business logic, instead of providing a direct before-and-after comparison, we will directly offer a production-ready architecture refactoring template that conforms to the above specifications.

The following is the currently submitted source code content:

{full_code}
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
    print("正在提取变更的文件...")
    changed_files = get_changed_files()
    print(f"✅ 找到 {len(changed_files)} 个变更的文件")
    
    print("正在召唤 AI Agent 审计代码...")
    review = call_ai_agent(changed_files)
    
    print("正在将结果同步回 GitHub...")
    print(review)
    # post_github_comment(review)
