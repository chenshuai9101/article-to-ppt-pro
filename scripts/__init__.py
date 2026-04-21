#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文章转PPT增强版 - 主入口
Article to PPT Pro - Main Entry Point

功能：
- 一键文章转PPT
- 模板选择
- 格式导出
"""

import sys
import os

# 添加scripts目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from article_parser import ArticleParser, parse_article
from content_extractor import ContentExtractor, extract_content
from ppt_generator import PPTGenerator, generate_ppt, list_templates
from template_manager import TemplateManager
from export_utils import ExportUtils

__version__ = '1.0.0'


class ArticleToPPT:
    """文章转PPT主类"""
    
    def __init__(self):
        self.parser = ArticleParser()
        self.extractor = ContentExtractor()
        self.generator = PPTGenerator()
        self.template_manager = TemplateManager()
        self.export_utils = ExportUtils()
    
    def convert(self, source: str, template: str = 'default', style: str = 'infographic') -> Dict:
        """
        将文章转换为PPT
        
        Args:
            source: 文章URL或文本内容
            template: 模板名称
            style: 视觉风格
            
        Returns:
            Dict: 转换结果
        """
        # 1. 解析文章
        print("📄 正在解析文章...")
        article_data = self.parser.parse(source)
        
        if article_data.get('error'):
            return {
                'success': False,
                'error': f"解析失败: {article_data['error']}"
            }
        
        # 2. 提取内容
        print("📊 正在提取内容...")
        ppt_data = self.extractor.extract(article_data)
        
        # 3. 选择模板
        if template == 'auto':
            template = self.template_manager.recommend_template(article_data)
            print(f"📋 推荐模板: {template}")
        
        ppt_data['template'] = template
        ppt_data['style'] = style
        
        # 4. 生成PPT
        print("🎨 正在生成PPT...")
        result = self.generator.generate(ppt_data)
        
        if result.get('success'):
            # 5. 导出PPTX
            print("📤 正在导出PPTX...")
            html_file = result.get('file', '')
            if html_file:
                pptx_file = self.export_utils.export_pptx(html_file)
                result['pptx_file'] = pptx_file
        
        return result
    
    def get_templates(self) -> list:
        """获取模板列表"""
        return self.template_manager.list_templates()
    
    def preview(self, source: str) -> Dict:
        """
        预览文章转换效果
        
        Args:
            source: 文章URL或文本内容
            
        Returns:
            Dict: 预览数据
        """
        article_data = self.parser.parse(source)
        ppt_data = self.extractor.extract(article_data)
        recommended_template = self.template_manager.recommend_template(article_data)
        
        return {
            'title': ppt_data.get('title', ''),
            'estimated_pages': ppt_data.get('estimated_pages', 0),
            'outline': ppt_data.get('outline', []),
            'recommended_template': recommended_template,
            'available_templates': self.template_manager.list_templates()
        }


def article_to_ppt(source: str, template: str = 'default', style: str = 'infographic') -> Dict:
    """
    文章转PPT便捷函数
    
    Args:
        source: 文章URL或文本内容
        template: 模板名称（可选）
        style: 视觉风格（可选）
        
    Returns:
        Dict: 转换结果
    """
    converter = ArticleToPPT()
    return converter.convert(source, template, style)


def list_templates() -> list:
    """列出可用模板"""
    manager = TemplateManager()
    return manager.list_templates()


if __name__ == '__main__':
    # 示例用法
    converter = ArticleToPPT()
    
    # 示例文章
    sample_text = """
    2024年Q3季度工作汇报
    
    一、工作概述
    本季度重点工作取得显著成效，整体业绩同比增长35%。
    
    二、具体成果
    1. 产品研发：完成V2.0版本开发
    2. 用户增长：月活突破100万
    3. 市场拓展：新进入3个省份
    
    三、下季度计划
    继续深耕产品优化，扩展新市场。
    """
    
    # 预览
    preview = converter.preview(sample_text)
    print(f"标题: {preview['title']}")
    print(f"预估页数: {preview['estimated_pages']}")
    print(f"推荐模板: {preview['recommended_template']}")
