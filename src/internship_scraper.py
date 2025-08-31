import os
import json
import asyncio
import argparse
from datetime import datetime
from typing import List, Dict, Any
from browser_use.llm import ChatOpenAI
from browser_use import Agent
from browser_use.browser.profile import BrowserProfile
from config_manager import ConfigManager, CompanyConfig

class InternshipScraper:
    def __init__(self, config_path: str = "config/companies.yaml", headless: bool = False):
        self.config_manager = ConfigManager(config_path)
        self.settings = self.config_manager.get_search_settings()
        self.headless = headless
        
        # LLM設定
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.llm = ChatOpenAI(model=model, temperature=0)
    
    def _generate_company_prompt(self, company: CompanyConfig) -> str:
        """企業用のプロンプトを生成（base_urlとsearch_termsに応じて調整）"""
        base_prompt = self.config_manager.generate_prompt(company)
        additional_info = self.config_manager.generate_additional_info(company)
        
        # プロンプトと追加情報を組み合わせ
        enhanced_prompt = f"""
{base_prompt}

{additional_info}
"""
        
        return enhanced_prompt
    
    async def scrape_company(self, company: CompanyConfig) -> Dict[str, Any]:
        """単一企業のインターン情報を取得（職種別情報を含む）"""
        print(f"\n=== {company.name} の情報を取得中 ===")
        
        if company.base_url:
            print(f"  公式サイトURL: {company.base_url}")
        else:
            print(f"  検索エンジンで公式サイトを検索します")
        
        print(f"  使用する検索キーワード: {company.search_terms}")
        print(f"  Headlessモード: {'有効' if self.headless else '無効'}")
        
        # プロンプト生成
        prompt = self._generate_company_prompt(company)
        
        try:
            # BrowserProfileを使用してHeadless設定を制御
            browser_profile = BrowserProfile(headless=self.headless)
            agent = Agent(task=prompt, llm=self.llm, browser_profile=browser_profile)
            
            # 実行
            result = await agent.run(max_steps=self.settings.max_steps)
            
            # 結果処理
            payload = {
                "company": company.name,
                "scraped_at": datetime.now().isoformat(),
                "status": "success"
            }
            
            try:
                # result.final_resultがメソッドの場合は呼び出し、そうでなければそのまま使用
                final_result = result.final_result() if callable(result.final_result) else result.final_result
                j = json.loads(final_result)
                payload.update(j)
            except Exception as e:
                # LLMが指示に従わずJSON以外を返した場合の保険
                final_result = result.final_result() if callable(result.final_result) else result.final_result
                payload["raw"] = str(final_result)
                payload["error"] = str(e)
                payload["status"] = "error"
            
            print(f"  取得完了: {len(payload.get('internships', []))}件のインターン情報")
            return payload
            
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            return {
                "company": company.name,
                "scraped_at": datetime.now().isoformat(),
                "status": "error",
                "error": str(e)
            }
    

    
    async def scrape_all_companies(self, output_dir: str = "data") -> List[Dict[str, Any]]:
        """全企業のインターン情報を取得"""
        companies = self.config_manager.get_companies()
        results = []
        
        # 出力ディレクトリ作成
        os.makedirs(output_dir, exist_ok=True)
        
        # タイムスタンプを生成（全ファイルで共通）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for i, company in enumerate(companies, 1):
            print(f"\n[{i}/{len(companies)}] {company.name} を処理中...")
            
            result = await self.scrape_company(company)
            results.append(result)
            
            # タイムスタンプ付きファイル名で保存
            company_filename = f"{company.name.replace(' ', '_')}_{timestamp}.json"
            company_filepath = os.path.join(output_dir, company_filename)
            
            with open(company_filepath, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            print(f"結果を保存しました: {company_filepath}")
        
        # 全結果をまとめて保存（タイムスタンプ付き）
        summary_filename = f"all_internships_{timestamp}.json"
        summary_filepath = os.path.join(output_dir, summary_filename)
        with open(summary_filepath, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n全結果を保存しました: {summary_filepath}")
        return results

async def main():
    parser = argparse.ArgumentParser(description="企業のインターン情報を取得")
    parser.add_argument("--config", default="config/companies.yaml", help="設定ファイルのパス")
    parser.add_argument("--output", default="data", help="出力ディレクトリ")
    parser.add_argument("--company", help="特定の企業のみ処理（企業名を指定）")
    parser.add_argument("--headless", action="store_true", help="ブラウザをHeadlessモードで実行（デフォルト: False）")
    args = parser.parse_args()
    
    scraper = InternshipScraper(args.config, headless=args.headless)
    
    # 出力ディレクトリ作成
    os.makedirs(args.output, exist_ok=True)
    
    if args.company:
        # 特定企業のみ処理
        companies = scraper.config_manager.get_companies()
        target_company = None
        for company in companies:
            if company.name == args.company:
                target_company = company
                break
        
        if target_company:
            result = await scraper.scrape_company(target_company)
            
            # タイムスタンプ付きファイル名で保存
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{args.company}_{timestamp}.json"
            filepath = os.path.join(args.output, filename)
            
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            print(f"結果を保存しました: {filepath}")
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"指定された企業 '{args.company}' が見つかりません")
    else:
        # 全企業処理
        results = await scraper.scrape_all_companies(args.output)
        
        # 成功した企業の数を表示
        success_count = sum(1 for r in results if r.get("status") == "success")
        print(f"\n=== 処理完了 ===")
        print(f"成功: {success_count}/{len(results)} 企業")

if __name__ == "__main__":
    asyncio.run(main())
