
# 🤖 Deep Research Agent (with FastAPI + MCP + Selenium + LLM)

本專案是一個整合多工具的生成式 AI 深度研究助手，透過 FastAPI 提供 MCP 工具註冊、Selenium 自動操作 NotebookLM、OpenAI API 生成結構化摘要，實現自動化的研究整合與分析。

---

## 📁 專案結構

```
.
├── app.py                 # FastAPI 主應用，含 NotebookLM 操作流程
├── api_server.py          # MCP 工具伺服器
├── mcp_client.py          # 啟動 LangGraph + MCP 多工具 Agent
├── front_end.html         # 簡易前端測試頁面
├── transcripts/           # 儲存逐字稿與 Markdown 摘要
├── .env                   # 儲存 OpenAI API Key（已被 .gitignore 忽略）
├── setup.py / pyproject.toml
├── README.md              # 本說明文件
```

---

## 🧑‍💻 安裝方式（建議使用 [`uv`](https://github.com/astral-sh/uv)）

```bash
# 安裝依賴（建議使用 uv）
uv pip install -r pyproject.toml
# 或使用 install 命令
uv pip install .
# 或使用 requirements.txt（如果你有產生的話）
uv pip install -r requirements.txt
```

---

## 🚀 啟動方式

### ✅ 啟動 FastAPI + MCP 工具伺服器

```bash
uvicorn app:app --reload
```

### ✅ 啟動 MCP Agent 問答介面

```bash
python mcp_client.py
```

### 前端頁面
若你已建立 `frontend.html` 前端，可使用 VSCode 的 Live Server 外掛打開(使用 VSCode Live Server 或其他即時刷新工具時，頁面可能會自動刷新，影響測試流程。
建議改用瀏覽器直接打開本地 HTML 檔案（file:/// 路徑），或使用不會自動刷新的 HTTP 伺服器（例如 python3 -m http.server）避免自動刷新。):
```bash
# 或手動開啟 HTML 檔案
open frontend.html
```

---

## 🧠 功能說明

### 🔹 會議逐字稿自動摘要
- 使用 Selenium 操控 Google NotebookLM
- 自動貼上逐字稿、觸發生成摘要
- 儲存成 `summary.txt` 以及經過 OpenAI GPT-4o 轉換後的 `summary.md`

### 🔹 MCP Agent 對話
- 整合多工具（後續可加入 news / paper / blog 爬蟲）
- 使用 LangGraph + LangChain REACT Agent
- 回傳最終摘要與推理過程

---

## 🔐 .env 設定
建立 `.env` 檔案，內容如下：

```env
OPENAI_API_KEY=your_key_here
USER_DATA_DIR=your_data_dir_here
PROFILE_DIRECTORY=your_profile_directory_here
```

或直接在 CLI 中執行：
```bash
export OPENAI_API_KEY=your_key_here
export USER_DATA_DIR=your_data_dir_here
export PROFILE_DIRECTORY=your_profile_directory_here
```

---

## 📎 TODO / 延伸規劃

- [ ] 整合新聞、論文與部落格自動爬取模組
- [ ] 支援一鍵生成分析摘要與可視化報表
- [ ] MCP 工具可串接更多分析模組（如 trend 分析、風險評估）

---

## 📜 License

MIT License

## 聯絡作者
Steve Wang | 2025