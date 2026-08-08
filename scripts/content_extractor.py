#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文章转PPT增强版 - 内容提取模块
Article to PPT Pro - Content Extractor Module

功能：
- 核心要点提取
- 关键词识别
- 逻辑关系分析
- PPT大纲生成
"""

import re
from typing import Dict, List
from dataclasses import dataclass, field


@dataclass
class ContentBlock:
    """内容块"""
    type: str  # 'heading', 'paragraph', 'list', 'table', 'image'
    content: str
    level: int = 1
    children: List['ContentBlock'] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)


@dataclass
class KeyPoint:
    """关键点"""
    text: str
    importance: float  # 0-1
    keywords: List[str] = field(default_factory=list)


class ContentExtractor:
    """内容提取器"""
    
    def __init__(self):
        # 停用词
        self.stop_words = {
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人',
            '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去',
            '你', '会', '着', '没有', '看', '好', '自己', '这'
        }
        
        # 重要关键词
        self.important_keywords = [
            '核心', '关键', '重点', '主要', '重要', '显著', '大幅',
            '增长', '下降', '提升', '降低', '突破', '创新', '领先',
            '第一', '最佳', '最优秀', '唯一', '首创', '独家'
        ]
    
    def extract(self, article_data: Dict) -> Dict:
        """
        从解析的文章数据中提取PPT内容
        
        Args:
            article_data: 文章解析结果
            
        Returns:
            Dict: PPT内容结构
        """
        sections = article_data.get('sections', [])
        title = article_data.get('title', '')
        images = article_data.get('images', [])
        
        # 生成PPT大纲
        outline = self._generate_outline(title, sections)
        
        # 提取关键点
        key_points = self._extract_key_points(sections)
        
        # 分析数据
        data_analysis = self._analyze_data(article_data)
        
        return {
            'title': title,
            'outline': outline,
            'key_points': key_points,
            'data_analysis': data_analysis,
            'images': images,
            'estimated_pages': self._estimate_pages(outline)
        }
    
    def _generate_outline(self, title: str, sections: List[Dict]) -> List[Dict]:
        """
        生成PPT大纲
        
        Args:
            title: 文章标题
            sections: 文章章节
            
        Returns:
            List[Dict]: PPT大纲
        """
        outline = []
        
        # 封面
        outline.append({
            'page': 1,
            'type': 'cover',
            'title': title,
            'subtitle': self._generate_subtitle(title)
        })
        
        # 内容页
        page_num = 2
        for section in sections:
            section_title = section.get('title', '')
            content = section.get('content', [])
            
            if not content:
                continue
            
            # 判断是否需要多页
            combined_content = '\n'.join(content)
            
            if len(combined_content) > 500:
                # 内容较多，分成多页
                chunks = self._split_content(content)
                for i, chunk in enumerate(chunks):
                    outline.append({
                        'page': page_num,
                        'type': 'content',
                        'title': section_title if i == 0 else f"{section_title}（续）",
                        'content': chunk,
                        'section': section_title
                    })
                    page_num += 1
            else:
                outline.append({
                    'page': page_num,
                    'type': 'content',
                    'title': section_title,
                    'content': content,
                    'section': section_title
                })
                page_num += 1
        
        # 结尾页
        outline.append({
            'page': page_num,
            'type': 'ending',
            'title': '谢谢观看',
            'subtitle': title
        })
        
        return outline
    
    def _generate_subtitle(self, title: str) -> str:
        """生成副标题"""
        # 移除常见前缀
        subtitle = re.sub(r'^(深度|全面|详细|精简)解析[：:]?', '', title)
        subtitle = re.sub(r'^(关于|对于)\s+', '', subtitle)
        
        if len(subtitle) > 20:
            # 提取核心关键词
            keywords = self._extract_title_keywords(title)
            if keywords:
                subtitle = ' | '.join(keywords[:2])
        
        return subtitle or '职场汇报演示'
    
    def _extract_title_keywords(self, title: str) -> List[str]:
        """提取标题关键词"""
        # 移除标点
        words = re.findall(r'[\u4e00-\u9fa5]+', title)
        
        # 过滤停用词
        keywords = [w for w in words if w not in self.stop_words and len(w) > 1]
        
        return keywords[:5]
    
    def _split_content(self, content: List[str]) -> List[List[str]]:
        """分割内容"""
        chunks = []
        current_chunk = []
        current_length = 0
        
        for para in content:
            para_length = len(para)
            
            if current_length + para_length > 500:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = [para]
                current_length = para_length
            else:
                current_chunk.append(para)
                current_length += para_length
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def _extract_key_points(self, sections: List[Dict]) -> List[KeyPoint]:
        """
        提取关键点
        
        Args:
            sections: 文章章节
            
        Returns:
            List[KeyPoint]: 关键点列表
        """
        key_points = []
        
        for section in sections:
            content = section.get('content', [])
            
            for para in content:
                points = self._extract_points_from_para(para)
                key_points.extend(points)
        
        # 按重要性排序
        key_points.sort(key=lambda x: x.importance, reverse=True)
        
        return key_points[:20]  # 最多返回20个关键点
    
    def _extract_points_from_para(self, para: str) -> List[KeyPoint]:
        """从段落中提取关键点"""
        points = []
        
        # 提取带数字的要点
        numbered_pattern = r'(\d+[.、)）]\s*)([^\n。]+)'
        for match in re.finditer(numbered_pattern, para):
            prefix = match.group(1)
            content = match.group(2).strip()
            
            importance = 0.7
            for kw in self.important_keywords:
                if kw in content:
                    importance += 0.1
            
            points.append(KeyPoint(
                text=content,
                importance=min(importance, 1.0),
                keywords=self._extract_keywords(content)
            ))
        
        # 提取带"第一/第二/第三"的要点
        ordinal_pattern = r'([一二三四五六七八九十]+[、：:])([^\n。]+)'
        for match in re.finditer(ordinal_pattern, para):
            content = match.group(2).strip()
            
            points.append(KeyPoint(
                text=content,
                importance=0.6,
                keywords=self._extract_keywords(content)
            ))
        
        return points
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        words = re.findall(r'[\u4e00-\u9fa5]+', text)
        keywords = [w for w in words if w not in self.stop_words and len(w) > 1]
        return list(set(keywords))[:5]
    
    def _analyze_data(self, article_data: Dict) -> Dict:
        """分析数据"""
        tables = article_data.get('tables', [])
        content = article_data.get('content', '')
        
        # 提取数字数据
        numbers = re.findall(r'(\d+\.?\d*)\s*(%|个百分点|倍|万|亿|千人|万元|亿元)', content)
        
        # 提取趋势词
        trends = []
        if any(w in content for w in ['增长', '上升', '提升', '增加']):
            trends.append('上升')
        if any(w in content for w in ['下降', '减少', '降低', '下滑']):
            trends.append('下降')
        
        return {
            'numerical_data': numbers[:10],  # 最多10个
            'trends': trends,
            'table_count': len(tables),
            'has_chart_data': len(numbers) > 3
        }
    
    def _estimate_pages(self, outline: List[Dict]) -> int:
        """估算页数"""
        return len(outline)
    
    def generate_notes(self, outline_item: Dict) -> str:
        """
        为每页生成演讲备注
        
        Args:
            outline_item: 大纲项
            
        Returns:
            str: 演讲备注
        """
        title = outline_item.get('title', '')
        content = outline_item.get('content', [])
        page_type = outline_item.get('type', 'content')
        
        notes = []
        
        if page_type == 'cover':
            notes.append(f"欢迎各位，今天我将分享关于「{title}」的主题。")
            notes.append("请注意把握整体节奏，留出互动时间。")
        elif page_type == 'content':
            notes.append(f"本页主题：{title}")
            
            if content:
                # 提取要点
                key_point = content[0] if isinstance(content, list) else content
                notes.append(f"核心要点：{key_point[:100]}")
                
                notes.append("\n讲解提示：")
                notes.append("1. 先概述本页将讲解什么")
                notes.append("2. 逐一展开要点")
                notes.append("3. 用具体案例说明")
        else:
            notes.append("感谢各位的聆听！")
            notes.append("如有疑问，欢迎交流。")
        
        return '\n'.join(notes)


def extract_content(article_data: Dict) -> Dict:
    """
    提取PPT内容的便捷函数
    
    Args:
        article_data: 文章解析结果
        
    Returns:
        Dict: PPT内容结构
    """
    extractor = ContentExtractor()
    return extractor.extract(article_data)


if __name__ == '__main__':
    # 测试用例
    test_data = {
        'title': '2024年Q3季度工作汇报',
        'sections': [
            {
                'title': '一、工作概述',
                'level': 1,
                'content': [
                    '本季度重点工作取得显著成效，整体业绩同比增长35%。',
                    '核心成果包括：产品研发完成、用户增长突破、市场占有率提升。'
                ]
            },
            {
                'title': '二、具体成果',
                'level': 1,
                'content': [
                    '1. 产品研发：完成V2.0版本开发，新增AI智能推荐功能',
                    '2. 用户增长：月活用户突破100万，同比增长120%',
                    '3. 市场拓展：新进入3个省份，客户满意度达98%'
                ]
            }
        ],
        'tables': [],
        'images': []
    }
    
    result = extract_content(test_data)
    print(f"标题: {result['title']}")
    print(f"预估页数: {result['estimated_pages']}")
    print(f"大纲页数: {len(result['outline'])}")
    for item in result['outline']:
        print(f"  Page {item['page']}: {item['title']}")
