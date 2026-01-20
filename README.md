# nlm-connect: NotebookLM 財經筆記自動化工具

這個專案非常有潛力！身為資深工程師，你選擇使用 `notebooklm-py` 來自動化這個過程非常精明。由於 NotebookLM 目前主要還是透過網頁介面操作，利用 Python 套件進行「抓取」並整合進你的 NixOS 開發流，能大幅提升效率。

這份 `README.md` 的規劃重點在於自動化流程與環境配置，特別是考慮到 NotebookLM 的 API 並非官方正式釋出，通常需要處理 Cookie 或 Token 的驗證。

`nlm-connect` 是一個利用 `notebooklm-py` 與 Google NotebookLM 互動的工具，旨在自動提取「財經筆記」中的語音轉文字（Speech-to-Text）內容，方便進行後續的檢索與存檔。

## 🚀 功能特點

- **自動對接**：透過 `notebooklm-py` 連接指定的 Notebook 空間。
- **內容提取**：精準抓取音檔上傳後產生的轉錄文字（Transcripts）。
- **格式轉換**：將抓取到的內容存為 Markdown，方便 Neovim 閱讀與搜尋。
- **同步機制**：僅抓取尚未處理的新音檔轉錄內容。

## 🛠 技術棧

- **Language**: Python 3.10+
- **Library**: `notebooklm-py`
- **Environment**: NixOS (flake-compatible)
- **Editor**: Neovim (建議搭配 Telescope 進行內容檢索)

## 📦 安裝與設定

### 1. 取得認證 (Authentication)

#### 如何獲取 NOTEBOOK_ID？

這是最簡單的部分。當你打開瀏覽器進入特定的 NotebookLM 筆記頁面時，URL 中就包含了這個 ID。

1. **開啟筆記**：在瀏覽器中打開你的「財經筆記」。
2. **觀察網址**：網址格式通常如下： `https://notebooklm.google.com/notebook/<YOUR_NOTEBOOK_ID>`
3. **複製 ID**：`<YOUR_NOTEBOOK_ID>` 這一串由亂數、數字與底線組成的字串，就是我們要的 ID。

#### 如何獲取 COOKIE？

由於 NotebookLM 沒有提供 API Token，我們必須模擬瀏覽器的身份。最穩定的做法是抓取整個 Cookie 字串。

1. **打開開發者工具**：在 Google Chrome 或 Brave 瀏覽器中打開 NotebookLM 並確保已登入。按下 `F12` 或 `Ctrl+Shift+I`。
2. **切換到 Network**：點擊 **Network (網路)** 頁籤。
3. **重新整理**：按下 `F5` 重新整理頁面，讓工具抓取請求。
4. **選擇請求**：在左側列表中隨便找一個發送到 `notebooklm.google.com` 的請求（例如名稱為 `list` 或 `get` 的請求）。
5. **複製 Headers**：
    - 在右側面板點擊 **Headers (標頭)** 頁籤。
    - 向下滾動找到 **Request Headers (請求標頭)** 區塊。
    - 找到 `cookie:` 這一行，將後面那一長串完整內容**全部複製**下來。
    - **注意**：這一串內容非常長，包含 `__Secure-3PSID` 等關鍵資訊，請確保全部選取，不要有遺漏（常見錯誤是只複製到 `...` 省略號）。

### 2. 配置環境變數

在 `.env` 檔案中填入你的相關資訊：
```bash
NOTEBOOK_ID="你的財經筆記ID"
COOKIE="你的認證Cookie"
```

### 3. 建立開發環境 (NixOS)

本專案使用 Nix Flakes 管理環境。

進入開發環境：
```bash
nix develop
# 或者如果你有安裝 direnv
direnv allow
```

### 4. 安裝依賴

進入環境後，使用 Makefile 安裝 Python 套件：
```bash
make install
```

## 🖥 使用說明

### 執行抓取

```bash
make run
# 或者直接執行
python src/main.py --sync --output ./transcripts
```

### 常用指令 (Makefile)
- `make install`: 安裝依賴
- `make run`: 執行主要程式
- `make clean`: 清除暫存檔

## 📂 專案結構

```
.
├── src/
│   ├── client.py      # 封裝 notebooklm-py 的通訊邏輯
│   ├── parser.py      # 處理 Speech-to-Text 內容解析
│   └── main.py        # 程式入口
├── transcripts/       # 存放抓下來的 Markdown 筆記
├── .env.example
├── flake.nix
└── README.md
```

## 📝 待辦事項 (Roadmap)

- [ ] 支援批次處理多個音檔
- [ ] 整合 LLM 對轉錄內容進行摘要
- [ ] 自動提交到私人 Git 倉庫備份
