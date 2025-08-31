# 企業インターン情報スクレイピングツール

企業名リストから公式HPを検索し、直近開催されるインターン情報を取得するスクリプトです。

## 機能

- 企業名から公式サイトを自動検索
- インターン情報の自動取得
- 職種別の詳細情報収集
- JSON形式での結果出力
- **Headlessモード対応** - ブラウザウィンドウを表示せずに実行可能
- **Docker対応** - コンテナ化された環境で実行可能

## セットアップ

### 方法1: ローカル環境でのセットアップ

1. 仮想環境の作成と有効化:
```bash
# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化
# macOS/Linux の場合:
source venv/bin/activate
# Windows の場合:
# venv\Scripts\activate
```

2. 依存関係のインストール:
```bash
pip install -r requirements.txt
```

3. Playwrightのブラウザをインストール:
```bash
playwright install
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
docker-compose build
```

3. 動作確認:
```bash
# 特定企業をヘッドレスモードで処理
docker-compose run --rm internship-scraper-custom python main.py --headless --company "リクルート"
```

## 使用方法

### ローカル環境での実行

#### 基本的な使用方法

```bash
# 全企業のインターン情報を取得
python main.py

# 特定企業のみ処理
python main.py --company "リクルート"

# Headlessモードで実行（ブラウザウィンドウを表示しない）
python main.py --headless

# 特定企業をHeadlessモードで処理
python main.py --company "リクルート" --headless
```

#### コマンドライン引数

- `--config`: 設定ファイルのパス（デフォルト: `config/companies.yaml`）
- `--output`: 出力ディレクトリ（デフォルト: `data`）
- `--company`: 特定の企業のみ処理（企業名を指定）
- `--headless`: ブラウザをHeadlessモードで実行（デフォルト: False）

### Docker上での実行（推奨）

#### 前提条件

- Docker と Docker Compose がインストールされていること
- `.env`ファイルにOpenAI APIキーが設定されていること
- **セットアップ手順を先に実行してください**（上記の「セットアップ」セクションを参照）

```bash
# .envファイルの例
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

#### 実行方法

```bash
# 全企業のインターン情報を取得（ヘッドレスモード）
docker-compose up internship-scraper

# 特定企業のみ処理（ヘッドレスモード）
docker-compose up internship-scraper-company

# 開発用（GUI表示、デバッグ用）
docker-compose up internship-scraper-dev

# カスタム実行（引数で柔軟に制御）
docker-compose run --rm internship-scraper-custom python main.py --headless --company "リクルート"
```

#### Dockerサービス一覧

1. **internship-scraper** - 本番用サービス（全企業処理、ヘッドレスモード）
2. **internship-scraper-company** - 特定企業処理（ヘッドレスモード）
3. **internship-scraper-dev** - 開発用サービス（GUI表示、デバッグ用）
4. **internship-scraper-custom** - カスタム実行用サービス（引数で柔軟に制御）

#### Docker特有の設定

- **コマンドライン引数**: `--headless`引数で明示的にヘッドレスモードを制御
- **ボリュームマウント**: 設定ファイルと結果データがホストと同期
- **リソース制限**: メモリ2GB、CPU1コアに制限

#### カスタム実行の例

```bash
# ヘッドレスモードで全企業処理
docker-compose run --rm internship-scraper-custom python main.py --headless

# 通常モードで特定企業処理
docker-compose run --rm internship-scraper-custom python main.py --company "リクルート"

# ヘッドレスモードで特定企業処理
docker-compose run --rm internship-scraper-custom python main.py --headless --company "サイバーエージェント"

# カスタム設定ファイルを使用
docker-compose run --rm internship-scraper-custom python main.py --headless --config custom_config.yaml
```

## 出力例

### サイバーエージェントの場合
```
{
  "company": "サイバーエージェント",
  "scraped_at": "2025-08-30T16:28:36.785134",
  "status": "success",
  "source_url": "https://www.cyberagent.co.jp/careers/students/biz/internship/",
  "internships": [
    {
      "title": "事業立案 インターンシップ",
      "period": "1期：7月11日（金）～7月13日（日）、2期：8月1日（金）～8月3日（日）",
      "application_deadline": "1次選考締切：4月24日（木）、2期：5月15日（木）",
      "target": "Students interested in business planning",
      "description": "活躍社員が最前線で戦っている「事業立案」のお題に取り組む、3日間のインターンシップです。壮大なビジョンを描き、最先端技術を駆使しながら事業を創っていく体験をしていただきます。",
      "url": "https://www.cyberagent.co.jp/careers/students/event/detail/id=31522"
    },
    {
      "title": "経営戦略 インターンシップ",
      "period": "9月12日（金）～9月14日（日）",
      "application_deadline": "1次選考締切：6月20日（金）",
      "target": "Students interested in management strategy",
      "description": "21世紀を代表する会社を目指し、増収増員を継続してきた弊社のこれまでを追体験し、これからを想像する「経営戦略」のお題に取り組む3日間のインターンシップです。第二創業期の経営戦略を像していく体験をしていただきます。",
      "url": "https://www.cyberagent.co.jp/careers/students/event/detail/id=31530"
    },
    {
      "title": "マーケティング戦略 インターンシップ",
      "period": "1期：10月10日（金）～10月12日（日）、2期：12月5日（金）～12月7日（日）",
      "application_deadline": "1期：7月11日（金）、2期：8月29日（金）",
      "target": "Students interested in marketing strategy",
      "description": "産業に革命を起こすテックカンパニーであること、クリエイティブを追求するエンターテイメント会社であること、この2つの顔を持ち合わせるサイバーエージェントだからこそ伝えられる「マーケティング」の面白さを体験していただく3日間です。",
      "url": "https://www.cyberagent.co.jp/careers/students/event/detail/id=31531"
    },
    {
      "title": "アニメ&IP インターンシップ",
      "period": "11月28日（金）～11月30日（日）",
      "application_deadline": "1次選考締切：8月29日（金）",
      "target": "Students interested in anime and IP business",
      "description": "ABEMA開局後、徐々にIP事業を拡大中のサイバーエージェント。メディアミックス戦略を中心としたアニメ&IPビジネスの展開の面白さを体感出来る3日間です。",
      "url": "https://www.cyberagent.co.jp/careers/students/event/detail/id=31802"
    }
  ]
}
```

### 出力ファイル形式

結果は`data`ディレクトリに以下の形式で保存されます：

```
data/
├── リクルート_20250831_130124.json
├── サイバーエージェント_20250831_130125.json
└── all_internships_20250831_130126.json
```

各ファイルは以下の形式で保存されます：
- **個別企業ファイル**: `{企業名}_{タイムスタンプ}.json`
- **全企業サマリーファイル**: `all_internships_{タイムスタンプ}.json`

## 設定

### 企業設定ファイル (`config/companies.yaml`)

企業の検索設定を管理します：

```yaml
search_settings:
  base_url: "https://www.google.com/search"
  search_terms: ["インターン", "インターンシップ", "採用情報"]

companies:
  - name: "リクルート"
    base_url: "https://www.recruit.co.jp"
    search_terms: ["インターン", "採用情報"]
  
  - name: "サイバーエージェント"
    base_url: "https://www.cyberagent.co.jp"
    search_terms: ["インターンシップ", "採用"]
```

### 環境変数（Docker環境のみ）

- `OPENAI_API_KEY`: OpenAI APIキー（必須）
- `OPENAI_MODEL`: 使用するOpenAIモデル（デフォルト: gpt-4o-mini）

## 技術仕様

- **Python**: 3.12
- **ブラウザ**: Playwright
- **LLM**: OpenAI GPT-4o-mini
- **コンテナ**: Docker + Docker Compose
- **OS**: Ubuntu 22.04（Docker環境）

## トラブルシューティング

### よくある問題

1. **ブラウザが起動しない（Docker環境）**
   - Docker上では`--headless`引数を明示的に指定
   - 開発用サービス（`internship-scraper-dev`）を使用してGUI表示
   - カスタム実行で`--headless`引数を明示的に指定

2. **OpenAI APIエラー**
   - `.env`ファイルに正しいAPIキーが設定されているか確認
   - APIキーの有効性を確認

3. **メモリ不足**
   - Dockerのリソース制限を調整
   - 一度に処理する企業数を減らす

### ログ確認

```bash
# Dockerログの確認
docker-compose logs internship-scraper

# リアルタイムログ
docker-compose logs -f internship-scraper

# カスタム実行のログ
docker-compose run --rm internship-scraper-custom python main.py --headless --company "リクルート"
```

## 注意事項

- 各企業の処理には時間がかかる場合があります
- エラーが発生した場合は、個別のエラーログが保存されます
- 公式サイトの構造変更により、取得できない場合があります
- 新しい企業を追加する場合は、`config/companies.yaml`の`companies`セクションに企業名のみを追加してください
- URLが分かっている場合は`base_url`を設定することで、より効率的にアクセスできます
- 検索キーワードは自動生成されますが、特殊なケースでは`search_terms`でカスタマイズできます
- **設定ファイル（`config/companies.yaml`）は必須です**。存在しない場合はエラーが発生します
- Docker環境では、結果データは`./data`ディレクトリに保存されます
