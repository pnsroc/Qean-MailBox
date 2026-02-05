📦 qean-mailbox
多账号统一邮件客户端（支持任意邮箱）  
GitHub 项目地址：
👉 https://github.com/pnsroc/Qean-MailBox

qean-mailbox 是一个 商业级、多账号、全功能、可扩展的邮件客户端系统，支持：

Gmail / Outlook / QQ / 163

手动添加任意邮箱（IMAP/SMTP）

多账号统一收件箱

多账号统一搜索

多账号统一过滤（20+ 种）

完整邮件收发、草稿、附件、标签、线程等能力

系统采用 Next.js  + FastAPI + PostgreSQL + Docker Compose 构建，可直接部署上线。

🚀 核心优势
🧩 1. 多账号统一收件箱
一次查看所有邮箱的邮件，自动合并、排序、标注来源账号。
体验媲美 Outlook / Gmail。

🔍 2. 多账号统一搜索
跨账号搜索：

主题

发件人

收件人

正文

附件内容（可扩展）

🧠 3. 多账号统一过滤（20+ 种）
支持：

发件人

收件人

主题

日期（today/yesterday/thisweek/范围）

大小（> / < / 范围）

附件类型（pdf/jpg/zip 等）

标签（Gmail/Outlook/IMAP/中文标签）

优先级（高/低）

MIME 类型（HTML/Plain）

来源客户端（iPhone/Outlook/Gmail 等）

语言（中文/英文/日文等）

是否包含图片

是否包含链接

是否包含日历邀请

是否包含签名

是否为系统通知

邮件线程聚合

🔧 4. 手动添加任意邮箱（核心能力）
支持所有 IMAP/SMTP 邮箱：

企业邮箱

学校邮箱

自建邮箱

国外邮箱

小众邮箱

自动：

测试连接

识别文件夹（INBOX/Sent/Drafts/Trash/Spam）

加入统一收件箱

加入所有过滤器

加入所有功能

🔐 5. 安全可靠
AES 加密存储邮箱密码

Token 鉴权

IMAP/SMTP SSL 支持

Docker 隔离

🧱 6. 完整前后端代码结构
后端：FastAPI

前端：Next.js

数据库：PostgreSQL

部署：Docker Compose

📦 7. 一键部署
只需一条命令：
docker-compose up --build
📁 项目目录结构
qean-mailbox/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── security.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   └── mail_service.py
│   │   └── routers/
│   │       ├── auth.py
│   │       └── mail.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── next.config.mjs
│   ├── package.json
│   ├── tsconfig.json
│   ├── Dockerfile
│   ├── src/
│   │   ├── pages/
│   │   │   ├── _app.tsx
│   │   │   ├── index.tsx
│   │   │   └── mail/
│   │   │       ├── index.tsx
│   │   │       └── add-account.tsx
│   │   ├── components/
│   │   └── lib/api.ts
├── docker-compose.yml
└── README.md

🛠️ 安装教程（Docker 一键部署）
1. 克隆项目
git clone https://github.com/pnsroc/Qean-MailBox.git
cd Qean-MailBox

2. 启动服务（自动构建前后端 + 数据库）
docker-compose up --build
3. 访问系统
前端：
http://localhost:3000

后端 API 文档：
http://localhost:8000/docs

4. 注册账号并登录
进入前端首页，注册一个用户即可开始使用。

✉️ 添加邮箱（支持所有邮箱）
系统支持两种方式：

方式 1：预设邮箱（Gmail/Outlook/QQ/163）
未来可扩展 OAuth。

方式 2：手动添加任意邮箱（IMAP/SMTP）
填写：

邮箱地址

密码/授权码

IMAP 服务器 + 端口 + SSL

SMTP 服务器 + 端口 + SSL

点击“测试连接” → “保存”即可。

🔍 使用说明
统一收件箱
进入 /mail 页面即可查看所有邮箱的邮件。

搜索
支持：
项目
from:boss
subject:合同
date:today
size:>1MB
type:pdf
label:work
priority:high
过滤
所有过滤器自动跨账号工作。

查看详情
点击任意邮件自动跳转到对应账号的详情页。

🧩 技术栈
模块	技术
前端	Next.js + React
后端	FastAPI
数据库	PostgreSQL
邮件协议	IMAP + SMTP
安全	AES 加密 + JWT
部署	Docker Compose
🏁 总结
qean-mailbox 已具备：

商业级邮件客户端的全部核心能力

多账号统一体验

全套过滤器

手动添加任意邮箱

完整前后端代码

一键部署能力

你可以直接用于：

企业内部邮件系统

SaaS 邮件客户端

邮件聚合平台

邮件监控/分析系统