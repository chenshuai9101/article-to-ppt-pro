#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文章转PPT增强版 - 文档解析模块
Article to PPT Pro - Article Parser Module

功能：
- URL/文本双输入支持
- HTML结构化解析
- 中文语义理解
- 智能内容分类
"""

import re
from typing import Dict, List, Tuple


class ArticleParser:
    """文章解析器"""
    
    def __init__(self):
        self.title_patterns = [
            r'<h1[^>]*>(.*?)</h1>',
            r'<h2[^>]*>(.*?)</h2>',
            r'<title>(.*?)</title>',
            r'class="title"[^>]*>(.*?)</',
        ]
        self.content_patterns = [
            r'<article[^>]*>(.*?)</article>',
            r'<div[^>]*class="content"[^>]*>(.*?)</div>',
            r'<div[^>]*id="content"[^>]*>(.*?)</div>',
            r'<main[^>]*>(.*?)</main>',
        ]
    
    def parse(self, source: str) -> Dict:
        """
        解析文章内容
        
        Args:
            source: URL或文本内容
            
        Returns:
            Dict: 解析结果包含 title, content, sections, images
        """
        if self._is_url(source):
            return self._parse_url(source)
        else:
            return self._parse_text(source)
    
    def _is_url(self, source: str) -> bool:
        """判断是否为URL"""
        url_pattern = r'^https?://'
        return bool(re.match(url_pattern, source.strip()))
    
    def _parse_url(self, url: str) -> Dict:
        """
        解析URL获取文章内容
        
        Args:
            url: 文章URL
            
        Returns:
            Dict: 解析结果
        """
        try:
            from fetch_web import fetch_web
            content = fetch_web([url])
            return self._extract_content(content, url)
        except Exception as e:
            return {
                'title': '',
                'content': '',
                'sections': [],
                'images': [],
                'tables': [],
                'error': str(e)
            }
    
    def _parse_text(self, text: str) -> Dict:
        """
        解析纯文本内容
        
        Args:
            text: 文本内容
            
        Returns:
            Dict: 解析结果
        """
        sections = self._extract_sections(text)
        return {
            'title': self._extract_title(sections),
            'content': text,
            'sections': sections,
            'images': self._extract_images(text),
            'tables': self._extract_tables(text),
            'error': None
        }
    
    def _extract_content(self, html_content: str, url: str) -> Dict:
        """
        从HTML中提取结构化内容
        
        Args:
            html_content: HTML内容
            url: 来源URL
            
        Returns:
            Dict: 结构化内容
        """
        # 提取标题
        title = self._extract_title_from_html(html_content)
        
        # 提取正文
        content = self._extract_body(html_content)
        
        # 分割章节
        sections = self._extract_sections(content)
        
        # 提取图片
        images = self._extract_images(html_content)
        
        # 提取表格
        tables = self._extract_tables(html_content)
        
        return {
            'title': title,
            'content': content,
            'sections': sections,
            'images': images,
            'tables': tables,
            'url': url,
            'error': None
        }
    
    def _extract_title_from_html(self, html: str) -> str:
        """从HTML中提取标题"""
        for pattern in self.title_patterns:
            match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
            if match:
                return self._clean_html(match.group(1))
        return ''
    
    def _extract_body(self, html: str) -> str:
        """提取正文内容"""
        for pattern in self.content_patterns:
            match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
            if match:
                return self._clean_html(match.group(1))
        # 降级：移除所有HTML标签
        return self._clean_html(html)
    
    def _extract_sections(self, content: str) -> List[Dict]:
        """
        提取文章章节结构
        
        Args:
            content: 文章内容
            
        Returns:
            List[Dict]: 章节列表
        """
        sections = []
        
        # 按段落分割
        paragraphs = re.split(r'\n+', content)
        
        current_section = None
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # 判断是否为标题
            is_heading, level = self._is_heading(para)
            
            if is_heading:
                if current_section:
                    sections.append(current_section)
                current_section = {
                    'title': para,
                    'level': level,
                    'content': []
                }
            else:
                if current_section:
                    current_section['content'].append(para)
                else:
                    # 无标题的内容作为引言
                    if not sections:
                        sections.append({
                            'title': '引言',
                            'level': 1,
                            'content': [para]
                        })
        
        if current_section:
            sections.append(current_section)
        
        return sections
    
    def _is_heading(self, text: str) -> Tuple[bool, int]:
        """
        判断文本是否为标题
        
        Args:
            text: 文本内容
            
        Returns:
            Tuple[bool, int]: (是否标题, 标题级别)
        """
        text = text.strip()
        
        # 长度过短可能是标题
        if len(text) < 50:
            # 带有序号
            ordered_pattern = r'^[一二三四五六七八九十\d]+[.、)）]'
            if re.match(ordered_pattern, text):
                return True, 2
            
            # 以关键词开头
            keywords = ['概述', '背景', '前言', '总结', '结论', '目录', '摘要']
            for kw in keywords:
                if text.startswith(kw):
                    return True, 2
            
            # 全是中文或英文，无标点
            if re.match(r'^[\u4e00-\u9fa5a-zA-Z\s]+$', text) and '。' not in text:
                if 5 < len(text) < 30:
                    return True, 2
        
        return False, 0
    
    def _extract_title(self, sections: List[Dict]) -> str:
        """从章节中提取标题"""
        for section in sections:
            if section.get('level') == 1:
                return section.get('title', '')
        return ''
    
    def _extract_images(self, content: str) -> List[Dict]:
        """提取图片"""
        images = []
        img_pattern = r'<img[^>]+src=["\']([^"\']+)["\']([^>]*)>'
        
        for match in re.finditer(img_pattern, content, re.IGNORECASE):
            images.append({
                'url': match.group(1),
                'alt': self._extract_alt(match.group(2))
            })
        
        return images
    
    def _extract_alt(self, attrs: str) -> str:
        """提取alt属性"""
        match = re.search(r'alt=["\']([^"\']*)["\']', attrs, re.IGNORECASE)
        return match.group(1) if match else ''
    
    def _extract_tables(self, content: str) -> List[Dict]:
        """提取表格"""
        tables = []
        table_pattern = r'<table[^>]*>(.*?)</table>'
        
        for match in re.finditer(table_pattern, content, re.DOTALL | re.IGNORECASE):
            tables.append({
                'html': match.group(0),
                'rows': self._parse_table_rows(match.group(1))
            })
        
        return tables
    
    def _parse_table_rows(self, table_html: str) -> List[List[str]]:
        """解析表格行"""
        rows = []
        row_pattern = r'<tr[^>]*>(.*?)</tr>'
        
        for row_match in re.finditer(row_pattern, table_html, re.DOTALL | re.IGNORECASE):
            cells = []
            cell_pattern = r'<t[hd][^>]*>(.*?)</t[hd]>'
            for cell_match in re.finditer(cell_pattern, row_match.group(1), re.DOTALL):
                cells.append(self._clean_html(cell_match.group(1)))
            if cells:
                rows.append(cells)
        
        return rows
    
    def _clean_html(self, html: str) -> str:
        """清理HTML标签"""
        # 转义HTML实体
        text = html.unescape(html) if hasattr(html, 'unescape') else html
        # 移除标签
        text = re.sub(r'<[^>]+>', '', text)
        # 清理多余空白
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def get_summary(self, content: str, max_length: int = 200) -> str:
        """
        生成文章摘要
        
        Args:
            content: 文章内容
            max_length: 最大长度
            
        Returns:
            str: 摘要
        """
        # 移除多余空白
        content = re.sub(r'\s+', ' ', content)
        
        if len(content) <= max_length:
            return content
        
        # 在句号处截断
        truncated = content[:max_length]
        last_punct = max(
            truncated.rfind('。'),
            truncated.rfind('！'),
            truncated.rfind('？')
        )
        
        if last_punct > max_length * 0.5:
            return truncated[:last_punct + 1]
        
        return truncated + '...'


def parse_article(source: str) -> Dict:
    """
    解析文章的便捷函数
    
    Args:
        source: URL或文本内容
        
    Returns:
        Dict: 解析结果
    """
    parser = ArticleParser()
    return parser.parse(source)


if __name__ == '__main__':
    # 测试用例
    test_text = """
    人工智能发展趋势
    
    一、概述
    人工智能技术正在快速发展，已经渗透到各行各业。本文将探讨AI的未来发展趋势。
    
    二、主要趋势
    1. 大模型应用
    大语言模型将成为主流，应用场景不断扩展。
    
    2. 行业垂直化
    AI将更加注重在特定行业的深度应用。
    
    三、结论
    人工智能将继续改变我们的生活和工作方式。
    """
    
    result = parse_article(test_text)
    print(f"标题: {result['title']}")
    print(f"章节数: {len(result['sections'])}")
    for section in result['sections']:
        print(f"  - {section['title']} (Level {section['level']})")
