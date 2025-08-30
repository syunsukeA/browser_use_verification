import yaml
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class CompanyConfig:
    name: str
    base_url: Optional[str] = None
    search_terms: Optional[List[str]] = None
    custom_prompt: str = ""

@dataclass
class SearchSettings:
    max_steps: int
    headless: bool
    timeout: int
    max_retries: int
    retry_delay: int

@dataclass
class DefaultConfig:
    search_terms_template: List[str]
    prompt_template: str
    additional_info_template: str
    search_settings: SearchSettings

class ConfigManager:
    def __init__(self, config_path: str = "config/companies.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.defaults = self._load_defaults()
    
    def _load_config(self) -> Dict[str, Any]:
        """設定ファイルを読み込む"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"設定ファイルが見つかりません: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _load_defaults(self) -> DefaultConfig:
        """デフォルト設定を読み込む"""
        defaults_data = self.config.get('defaults', {})
        
        # 検索設定のデフォルト
        search_settings_data = defaults_data.get('search_settings', {})
        search_settings = SearchSettings(
            max_steps=search_settings_data.get('max_steps', 30),
            headless=search_settings_data.get('headless', False),
            timeout=search_settings_data.get('timeout', 30),
            max_retries=search_settings_data.get('max_retries', 1),
            retry_delay=search_settings_data.get('retry_delay', 2)
        )
        
        return DefaultConfig(
            search_terms_template=defaults_data.get('search_terms_template', ["{company_name} インターン"]),
            prompt_template=defaults_data.get('prompt_template', ''),
            additional_info_template=defaults_data.get('additional_info_template', ''),
            search_settings=search_settings
        )
    
    def get_companies(self) -> List[CompanyConfig]:
        """企業設定のリストを取得（デフォルト値を適用）"""
        companies = []
        for company_data in self.config.get('companies', []):
            # 必須項目
            name = company_data['name']
            
            # オプション項目（デフォルト値を適用）
            base_url = company_data.get('base_url')  # Noneの場合は企業名で検索
            
            search_terms = company_data.get('search_terms')
            if search_terms is None:
                # デフォルトテンプレートを使用
                search_terms = [
                    term.format(company_name=name) 
                    for term in self.defaults.search_terms_template
                ]
            
            custom_prompt = company_data.get('custom_prompt', '')
            
            company = CompanyConfig(
                name=name,
                base_url=base_url,
                search_terms=search_terms,
                custom_prompt=custom_prompt
            )
            companies.append(company)
        return companies
    
    def get_search_settings(self) -> SearchSettings:
        """検索設定を取得"""
        return self.defaults.search_settings
    
    def generate_prompt(self, company: CompanyConfig) -> str:
        """企業用のプロンプトを生成（YAMLファイルの内容を参照）"""
        # カスタムプロンプトがある場合は組み合わせ、なければデフォルトテンプレートを使用
        if company.custom_prompt:
            base_prompt = self.defaults.prompt_template.format(
                company_name=company.name
            )
            prompt = f"{company.custom_prompt}\n\n{base_prompt}"
        else:
            # デフォルトテンプレートを使用
            prompt = self.defaults.prompt_template.format(
                company_name=company.name
            )
        
        return prompt
    
    def generate_additional_info(self, company: CompanyConfig) -> str:
        """企業用の追加情報を生成"""
        # base_urlの情報を設定
        if company.base_url:
            base_url_info = company.base_url
            access_instruction = "可能であれば、上記URLから直接アクセスしてください"
        else:
            base_url_info = "不明"
            access_instruction = "検索エンジンで上記キーワードを使用して検索してください"
        
        # search_termsの情報を設定
        search_terms_info = ", ".join([f'"{term}"' for term in company.search_terms]) if company.search_terms else f'"{company.name} 公式サイト"'
        
        # 追加情報テンプレートを適用
        additional_info = self.defaults.additional_info_template.format(
            base_url_info=base_url_info,
            search_terms_info=search_terms_info,
            access_instruction=access_instruction
        )
        
        return additional_info
    
    def get_defaults_info(self) -> Dict[str, Any]:
        """デフォルト設定の情報を取得（デバッグ用）"""
        return {
            "search_terms_template": self.defaults.search_terms_template,
            "prompt_template_length": len(self.defaults.prompt_template),
            "search_settings": {
                "max_steps": self.defaults.search_settings.max_steps,
                "headless": self.defaults.search_settings.headless,
                "timeout": self.defaults.search_settings.timeout,
                "max_retries": self.defaults.search_settings.max_retries,
                "retry_delay": self.defaults.search_settings.retry_delay
            }
        }
