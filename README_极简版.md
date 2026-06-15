# 🤖 Argus Auto Review - 极限冲刺版

## 📋 这是什么？

这是一个**极简的 AI 自动代码审查系统**，用 **GitHub Actions + Python 脚本** 实现，零运维成本，5分钟即可看到 AI 自动评论代码的效果！

---

## ⚡ 核心文件（仅2个）

### 1. `.github/workflows/ai_review.yml`
GitHub Actions 配置文件，定义自动化流程。

### 2. `ai_review.py`
Python 脚本，负责：
- 提取 git diff
- 调用大模型 API（DeepSeek/OpenAI）
- 自动发布评论到 GitHub

---

## 🚀 快速开始（3步）

### Step 1: 配置 API Key

在 GitHub 仓库设置中添加 Secret：
```
Settings → Secrets and variables → Actions → New repository secret
Name: LLM_API_KEY
Value: 你的 DeepSeek/OpenAI API Key
```

### Step 2: 提交有 Bug 的代码

```bash
git add .
git commit -m "test ai review"
git push
```

### Step 3: 查看自动评论

等待 30 秒 - 1 分钟，刷新 GitHub Commit 页面，你会看到 AI 生成的审查报告！

---

## 💡 工作原理

```
git push
  ↓
GitHub Actions 触发
  ↓
提取 git diff
  ↓
调用 DeepSeek API
  ↓
生成审查报告
  ↓
自动评论到 GitHub ✅
```

---

## 🎯 演示给导师看

**高光操作：**

1. 故意写一段有明显 Bug 的代码（死循环、未定义变量等）
2. `git push` 推送到 GitHub
3. 带导师刷新 Commit 页面
4. 展示 AI 自动生成的 Markdown 审查报告

**这样说：**

> "这套 'Actions + 伪装脚本' 的组合拳，既展示了我对 Git 自动化流水线（CI/CD）的纯熟应用，又完美展现了 Agent 的核心工作流逻辑。等开完会通过了，我随时能把它挪到国内 GPU 服务器上改成真正的私有微调 Agent！"

---

## 🔑 核心优势

✅ **零运维成本** - 不需要 GPU 服务器  
✅ **秒速打通** - 5 分钟即可看到效果  
✅ **公网 API** - 用现成的 DeepSeek/OpenAI  
✅ **完全自动化** - 无需人工干预  
✅ **可扩展** - 开完会随时替换成自己的微调模型  

---

## 📁 项目结构

```
draft_4/
├── .github/
│   └── workflows/
│       └── ai_review.yml      # GitHub Actions 配置 ⭐
├── ai_review.py                # AI 审查脚本 ⭐
├── requirements.txt            # Python 依赖
├── 快速开始.md                 # 详细使用指南
└── README_极简版.md            # 本文件
```

---

## 🔄 后续优化

开完会后，可以：
- [ ] 替换成国内 GPU 服务器的本地 Ollama API
- [ ] 接入你自己的 Qwen2.5-Coder 微调模型
- [ ] 添加更详细的审查规则
- [ ] 支持行内评论（inline comments）

---

## 🐛 常见问题

**Q: Workflow 没有触发？**  
A: 检查 Actions 是否启用，是否推送到 main/master 分支

**Q: API 调用失败？**  
A: 确保 LLM_API_KEY secret 已正确设置

**Q: 评论没有发布？**  
A: 检查 workflow 是否有 pull-requests: write 权限

---

## 🎉 成功标志

当你看到 GitHub Commit 页面出现这样的评论时，就成功了：

```markdown
### 🤖 AI Agent 自动化代码审查报告

#### 🔴 严重问题

1. **死循环风险**
   - 位置：`while True: pass`
   - 建议：添加退出条件

...
```

---

**快！趁着开会前的最后黄金时间，把这两个文件建起来，祝你等会儿在导师面前惊艳全场！** 🚀
