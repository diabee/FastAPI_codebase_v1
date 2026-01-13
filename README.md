# FastAPI Codebase Template

FastAPI 後端服務專案模板，採用分層架構設計。

## 專案結構

```
.
├── app/                      # 應用程式主目錄
│   ├── config/               # 專案配置
│   │   ├── cors_config.py    # CORS 設定
│   │   ├── db_config.py      # 資料庫設定
│   │   ├── logging_config.py # 日誌設定
│   │   └── router_config.py  # 路由設定
│   ├── example/              # 範例模組
│   │   ├── controller/       # API 路由
│   │   ├── service/          # 商業邏輯
│   │   ├── repository/       # 資料庫操作
│   │   ├── models/           # 資料模型
│   │   │   ├── entity/       # SQLAlchemy Entity
│   │   │   ├── schema/       # Pydantic Schema
│   │   │   └── dto/          # Data Transfer Object
│   │   ├── dependencies.py   # 依賴注入
│   │   └── exception.py      # 例外處理
│   ├── models/               # 共用模型
│   │   └── response.py       # 統一回應格式
│   ├── utility/              # 工具類
│   └── main.py               # 入口點
├── config/                   # 環境設定檔
│   ├── .env                  # 環境變數 (gitignored)
│   └── .env.example          # 環境變數範本
├── docker/                   # Docker 配置
│   └── Dockerfile
├── tests/                    # 單元測試
├── pyproject.toml            # Poetry 設定
├── EXAMPLE.md                # 開發教學
└── README.md
```

## 依賴套件

### Core Dependencies
- Python 3.14.2
- FastAPI 0.128.0
- Uvicorn 0.40.0
- SQLAlchemy 2.0.45
- PyMySQL 1.1.2
- python-dotenv 1.2.1
- marshmallow 4.2.0
- requests 2.32.5
- python-dateutil 2.9.0.post0

### Dev Dependencies
- pytest 9.0.2
- pytest-fastapi 0.1.0
- ruff 0.14.11
- ipython 9.9.0

## 快速開始

### 1. 安裝 Poetry

```bash
pip install poetry
```

### 2. 安裝依賴

```bash
poetry install
```

### 3. 設定環境變數

```bash
cp config/.env.example config/.env
# 編輯 config/.env 填入實際設定
```

### 4. 建立 Log 目錄

```bash
mkdir -p /tmp/log/
```

### 5. 啟動應用程式

```bash
# 方式一：使用 uvicorn
uvicorn app.main:app --reload

# 方式二：使用 poetry
poetry run uvicorn app.main:app --reload
```

API 文件：http://localhost:8000/docs

## 開發指南

### 執行測試

```bash
pytest -v
```

### 程式碼檢查

```bash
ruff check
ruff check --fix
```

## Docker

### 建置映像

```bash
docker build -f docker/Dockerfile -t fastapi-codebase:latest .
```

### 執行容器

```bash
docker run -d --name app -p 8080:8080 --env-file config/.env fastapi-codebase:latest
```

## 分層架構

每個功能模組遵循分層架構：

```
module/
├── controller/       # API 路由定義 (HTTP 處理)
├── service/          # 商業邏輯層
├── repository/       # 資料庫操作層
├── models/
│   ├── entity/       # SQLAlchemy 資料庫實體
│   ├── schema/       # Pydantic 請求/回應模型
│   └── dto/          # Data Transfer Object (POJO)
├── dependencies.py   # 依賴注入
└── exception.py      # 模組專屬例外處理
```

### 資料流

```
HTTP Request
     ↓
Controller (Schema 驗證)
     ↓
Service (商業邏輯，回傳 DTO)
     ↓
Repository (資料庫操作，回傳 Entity)
     ↓
Database
```

## 環境變數

| 變數名稱 | 說明 | 預設值 |
|---------|------|--------|
| `DEBUG` | 除錯模式 | `False` |
| `PORT` | 服務埠號 | `8080` |
| `HOST` | 服務主機 | `0.0.0.0` |
| `APP_TITLE` | API 標題 | `FastAPI Service` |
| `LOG_PATH` | 日誌路徑 | `/tmp/log/web.log` |
| `LOG_LEVEL` | 日誌等級 | `DEBUG` |
| `MYSQL_HOST` | 資料庫連線字串 | - |
| `POOL_SIZE` | 連線池大小 | `32` |
| `AUTO_CREATE_TABLES` | 自動建立資料表 | `True` |

完整環境變數請參考 `config/.env.example`

## 相關文件

- [EXAMPLE.md](./EXAMPLE.md) - 完整開發教學與程式碼範例
