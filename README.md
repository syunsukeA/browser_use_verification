# インターン情報取得ツール

企業名リストから公式HPを検索し、直近開催されるインターンシップ情報を自動取得するツールです。

## 機能

- 企業名から公式サイトを自動検索
- インターンシップ情報の自動取得
- 企業ごとのカスタムプロンプト対応
- 結果のJSON形式での保存
- 個別企業処理と一括処理の両方に対応
- Docker対応
- シンプルな設定管理（企業名のみで設定可能）
- 最適化された検索キーワードの自動生成と活用
- 設定ファイルベースの動作（設定ファイルが必須）

## セットアップ

### 方法1: ローカル環境でのセットアップ

1. 依存関係のインストール:
```bash
pip install -r requirements.txt
```

2. Playwrightのブラウザをインストール:
```bash
playwright install
```

3. 環境変数の設定:
```bash
export OPENAI_API_KEY="your-api-key"
```

4. 設定ファイルの準備:
```bash
# config/companies.yaml ファイルが存在することを確認
ls config/companies.yaml
```

### 方法2: Docker環境でのセットアップ

1. 環境変数ファイルの作成:
```bash
echo "OPENAI_API_KEY=your-api-key" > .env
```

2. Dockerイメージのビルド:
```bash
docker build -t internship-scraper .
```

## 使用方法

### ローカル環境での実行

#### 全企業を一括処理:
```bash
python main.py
```

#### 特定の企業のみ処理:
```bash
python main.py --company "リクルート"
```

#### 設定ファイルを指定:
```bash
python main.py --config custom_config.yaml
```

#### 出力ディレクトリを指定:
```bash
python main.py --output results
```

### Docker環境での実行

#### Docker Composeを使用（推奨）:
```bash
# 全企業を一括処理
docker-compose up internship-scraper

# 特定企業のみ処理（開発用）
docker-compose up internship-scraper-dev
```

#### Dockerコマンドを直接使用:
```bash
# 全企業を一括処理
docker run --rm \
  -e OPENAI_API_KEY="your-api-key" \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/data:/app/data \
  internship-scraper

# 特定企業のみ処理
docker run --rm \
  -e OPENAI_API_KEY="your-api-key" \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/data:/app/data \
  internship-scraper python main.py --company "リクルート"
```

## 設定ファイルの準備

### 基本的な設定（推奨）

`config/companies.yaml` に企業情報を設定します。**企業名のみが必須**です：

```yaml
# デフォルト設定
defaults:
  # デフォルトの検索キーワードテンプレート
  search_terms_template: ["{company_name} インターン", "{company_name} 採用"]
  
  # デフォルトのプロンプトテンプレート
  prompt_template: |
    企業「{company_name}」の公式サイトから直近開催されるインターンシップ情報を取得してください。

    手順:
    1. 検索エンジンで推奨キーワードを使用して公式サイトを検索
    2. 公式サイトの採用ページにアクセス
    3. インターンシップ情報を探す
    4. 直近開催予定のインターン情報を取得
    5. 各インターンの詳細情報を記録

    制約:
    - 最終出力は**次のJSONのみ**を標準出力に出力し、他の文章は出力しない
    - JSON形式:
      {
        "company": "{company_name}",
        "source_url": "取得元URL",
        "internships": [
          {
            "title": "インターンタイトル",
            "period": "開催期間",
            "application_deadline": "応募締切",
            "target": "対象者",
            "description": "内容説明",
            "url": "詳細ページURL"
          }
        ]
      }
    - 公式サイト内の情報のみを使用
    - 直近3ヶ月以内に開催予定のインターンのみ対象

  # 検索設定
  search_settings:
    max_steps: 30
    headless: false
    timeout: 30

# 企業リスト（企業名のみが必須）
companies:
  - name: "リクルート"
  - name: "サイバーエージェント"
  - name: "DeNA"
```

### URLが分かっている場合の設定

企業の公式サイトURLが分かっている場合は、効率的にアクセスできます：

```yaml
companies:
  - name: "Google"
    base_url: "https://careers.google.com"
  
  - name: "Microsoft"
    base_url: "https://careers.microsoft.com"
```

### 特殊なケースの設定

企業によって特別な処理が必要な場合のみ、追加設定を行います：

```yaml
companies:
  - name: "特殊な企業"
    base_url: "https://special-company.com"  # オプション
    # デフォルトと異なる検索キーワード
    search_terms: ["特殊キーワード1", "特殊キーワード2"]
    # 企業特有の手順
    custom_prompt: |
      この企業特有の手順:
      1. 特別なページにアクセス
      2. 特殊な情報を取得
      3. カスタム処理を実行
```

## 設定システムの利点

- **超シンプル**: 企業名のみで設定可能
- **URL調査不要**: 企業名から自動検索
- **効率性**: 既知のURLがある場合は直接アクセス
- **柔軟性**: 未知の企業でも自動検索で対応
- **保守性**: 設定ファイルが最小限
- **拡張性**: 新しい企業の追加が非常に簡単
- **最適化された検索**: 企業名ベースの検索キーワードを自動生成・活用
- **設定ファイルベース**: すべての動作が設定ファイルで制御される

## 検索キーワードの活用

### 自動生成される検索キーワード

企業名のみを設定した場合、以下のキーワードが自動生成されます：
- `{企業名} インターン`
- `{企業名} 採用`

例：
- リクルート → `["リクルート インターン", "リクルート 採用"]`
- サイバーエージェント → `["サイバーエージェント インターン", "サイバーエージェント 採用"]`

### カスタム検索キーワード

企業によって特別な検索キーワードが必要な場合は、`search_terms`を指定できます：

```yaml
companies:
  - name: "特殊な企業"
    search_terms: ["特殊キーワード1", "特殊キーワード2", "企業名 採用"]
```

## アクセス方法

### URLが設定されている場合
1. 設定されたURLに直接アクセス
2. 推奨検索キーワードを使用して公式サイト内を検索
3. インターン情報を取得

### URLが設定されていない場合
1. 検索エンジンで推奨キーワードを使用して検索
2. 公式サイトを特定
3. 採用ページにアクセス
4. インターン情報を検索・取得

## 出力形式

各企業の結果は以下の形式で保存されます:

```json
{
  "company": "企業名",
  "scraped_at": "2024-01-01T12:00:00",
  "status": "success",
  "source_url": "取得元URL",
  "internships": [
    {
      "title": "インターンタイトル",
      "period": "開催期間",
      "application_deadline": "応募締切",
      "target": "対象者",
      "description": "内容説明",
      "url": "詳細ページURL"
    }
  ]
}
```

## ファイル構成

```
.
├── main.py                   # メインスクリプト
├── config/
│   └── companies.yaml        # 企業設定ファイル（必須）
├── src/
│   ├── __init__.py          # パッケージ初期化
│   ├── config_manager.py    # 設定管理（YAMLファイルベース）
│   └── internship_scraper.py # スクレイピングロジック
├── data/                    # 結果保存ディレクトリ
├── requirements.txt         # 依存関係
├── Dockerfile              # Docker設定
├── docker-compose.yml      # Docker Compose設定
├── .dockerignore           # Docker除外設定
└── README.md               # 使用方法
```

## 設定ファイルの詳細

### companies.yaml

#### デフォルト設定（defaults）
- `search_terms_template`: 検索キーワードのテンプレート
- `prompt_template`: 共通のプロンプトテンプレート（制約を含む）
- `search_settings`: 検索設定
  - `max_steps`: 最大ステップ数
  - `headless`: ヘッドレスモード
  - `timeout`: タイムアウト時間

#### 企業設定（companies）
- `name`: 企業名（必須）
- `base_url`: 基本URL（オプション、未設定の場合は検索エンジンで検索）
- `search_terms`: 検索キーワード（オプション、デフォルト値を使用）
- `custom_prompt`: カスタムプロンプト（オプション、デフォルト値を使用）

## エラーハンドリング

### 設定ファイルが存在しない場合
設定ファイル（`config/companies.yaml`）が存在しない場合は、以下のエラーが発生します：
```
FileNotFoundError: 設定ファイルが見つかりません: config/companies.yaml
```

### 設定ファイルの形式エラー
YAMLファイルの形式が正しくない場合は、YAMLパースエラーが発生します。

### 推奨される対処法
1. 設定ファイルが存在することを確認
2. YAMLファイルの構文が正しいことを確認
3. 必要な設定項目が含まれていることを確認

## Docker環境の利点

- **環境の統一**: どの環境でも同じ動作を保証
- **依存関係の管理**: システムライブラリの自動インストール
- **分離された実行**: ホスト環境に影響を与えない
- **スケーラビリティ**: 複数インスタンスの並行実行が可能
- **CI/CD対応**: 自動化パイプラインへの組み込みが容易

## 注意事項

- 各企業の処理には時間がかかる場合があります
- エラーが発生した場合は、個別のエラーログが保存されます
- 公式サイトの構造変更により、取得できない場合があります
- 新しい企業を追加する場合は、`config/companies.yaml`の`companies`セクションに企業名のみを追加してください
- URLが分かっている場合は`base_url`を設定することで、より効率的にアクセスできます
- 検索キーワードは自動生成されますが、特殊なケースでは`search_terms`でカスタマイズできます
- **設定ファイル（`config/companies.yaml`）は必須です**。存在しない場合はエラーが発生します
- Docker環境では、結果データは`./data`ディレクトリに保存されます