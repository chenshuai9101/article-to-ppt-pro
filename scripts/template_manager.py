#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文章转PPT增强版 - 模板管理器
Article to PPT Pro - Template Manager Module

功能：
- 模板注册与查询
- 模板预览
- 模板下载
"""

import os
import json
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Template:
    """PPT模板"""
    id: str
    name: str
    description: str
    scenes: List[str]
    style: str
    colors: Dict[str, str]
    path: str


class TemplateManager:
    """模板管理器"""
    
    def __init__(self):
        self.templates_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'templates'
        )
        self._load_templates()
    
    def _load_templates(self):
        """加载模板列表"""
        self.templates = {
            'default': Template(
                id='default',
                name='默认模板',
                description='通用职场风格，简洁大方',
                scenes=['工作汇报', '通用演示', '日常分享'],
                style='infographic',
                colors={
                    'primary': '#2563EB',
                    'secondary': '#3B82F6',
                    'background': '#FFFFFF',
                    'text': '#1F2937'
                },
                path='default'
            ),
            'investor_report': Template(
                id='investor_report',
                name='投资人汇报',
                description='专业商业风格，数据图表突出，适合融资路演和投资人沟通',
                scenes=['投资人汇报', '商业计划', '融资路演'],
                style='infographic',
                colors={
                    'primary': '#1E40AF',
                    'secondary': '#3B82F6',
                    'background': '#F8FAFC',
                    'text': '#1F2937',
                    'accent': '#10B981'
                },
                path='investor_report'
            ),
            'performance_review': Template(
                id='performance_review',
                name='述职报告',
                description='简洁商务风格，重点突出，适合季度/年度述职汇报',
                scenes=['述职报告', '绩效考核', '工作汇报'],
                style='infographic',
                colors={
                    'primary': '#0F172A',
                    'secondary': '#334155',
                    'background': '#FFFFFF',
                    'text': '#1F2937',
                    'accent': '#F59E0B'
                },
                path='performance_review'
            ),
            'project_summary': Template(
                id='project_summary',
                name='项目总结',
                description='结构清晰风格，成果导向，适合项目复盘和经验分享',
                scenes=['项目总结', '项目复盘', '经验分享'],
                style='infographic',
                colors={
                    'primary': '#059669',
                    'secondary': '#10B981',
                    'background': '#F0FDF4',
                    'text': '#1F2937',
                    'accent': '#F59E0B'
                },
                path='project_summary'
            ),
            'training_course': Template(
                id='training_course',
                name='培训课件',
                description='循序渐进风格，要点明确，适合内部培训和学生教学',
                scenes=['培训课件', '知识分享', '教学培训'],
                style='illustration',
                colors={
                    'primary': '#7C3AED',
                    'secondary': '#8B5CF6',
                    'background': '#FAF5FF',
                    'text': '#1F2937',
                    'accent': '#EC4899'
                },
                path='training_course'
            )
        }
    
    def list_templates(self) -> List[Dict]:
        """
        列出所有模板
        
        Returns:
            List[Dict]: 模板列表
        """
        return [
            {
                'id': t.id,
                'name': t.name,
                'description': t.description,
                'scenes': t.scenes,
                'style': t.style,
                'colors': t.colors
            }
            for t in self.templates.values()
        ]
    
    def get_template(self, template_id: str) -> Optional[Template]:
        """
        获取指定模板
        
        Args:
            template_id: 模板ID
            
        Returns:
            Optional[Template]: 模板对象
        """
        return self.templates.get(template_id)
    
    def search_templates(self, keyword: str) -> List[Dict]:
        """
        搜索模板
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            List[Dict]: 匹配的模板列表
        """
        keyword = keyword.lower()
        results = []
        
        for template in self.templates.values():
            # 匹配名称
            if keyword in template.name.lower():
                results.append({
                    'id': template.id,
                    'name': template.name,
                    'description': template.description,
                    'scenes': template.scenes,
                    'match_type': 'name'
                })
                continue
            
            # 匹配场景
            for scene in template.scenes:
                if keyword in scene.lower():
                    results.append({
                        'id': template.id,
                        'name': template.name,
                        'description': template.description,
                        'scenes': template.scenes,
                        'match_type': 'scene'
                    })
                    break
        
        return results
    
    def recommend_template(self, article_data: Dict) -> str:
        """
        根据文章内容推荐模板
        
        Args:
            article_data: 文章数据
            
        Returns:
            str: 推荐模板ID
        """
        title = article_data.get('title', '').lower()
        content = article_data.get('content', '').lower()
        combined = title + ' ' + content
        
        # 关键词映射
        keywords_map = {
            '投资人汇报': ['投资', '融资', '商业计划', 'bp', '路演', '资本', '上市'],
            'performance_review': ['述职', '季度总结', '年度总结', '绩效考核', 'kpi', '述职报告'],
            'project_summary': ['项目', '复盘', '项目总结', '交付', '里程碑', '迭代'],
            'training_course': ['培训', '课件', '课程', '教学', '学习', '教程', '分享会']
        }
        
        # 统计匹配次数
        scores = {}
        for template_id, keywords in keywords_map.items():
            score = sum(1 for kw in keywords if kw in combined)
            scores[template_id] = score
        
        # 返回得分最高的模板
        if scores:
            best_template = max(scores.items(), key=lambda x: x[1])
            if best_template[1] > 0:
                return best_template[0]
        
        return 'default'
    
    def get_template_styles(self) -> Dict[str, Dict]:
        """
        获取各模板的样式配置
        
        Returns:
            Dict[str, Dict]: 样式配置
        """
        styles = {}
        
        for template_id, template in self.templates.items():
            styles[template_id] = {
                'name': template.name,
                'colors': template.colors,
                'style': template.style,
                'layout_guide': self._get_layout_guide(template)
            }
        
        return styles
    
    def _get_layout_guide(self, template: Template) -> Dict:
        """
        获取模板布局指南
        
        Args:
            template: 模板对象
            
        Returns:
            Dict: 布局指南
        """
        guides = {
            'default': {
                'cover': {'align': 'center', 'elements': ['title', 'subtitle']},
                'content': {'align': 'left', 'elements': ['title', 'bullets']},
                'ending': {'align': 'center', 'elements': ['thanks']}
            },
            'investor_report': {
                'cover': {'align': 'center', 'elements': ['title', 'subtitle', 'date', 'company']},
                'content': {'align': 'left', 'elements': ['title', 'data_chart', 'analysis']},
                'ending': {'align': 'center', 'elements': ['thanks', 'contact']}
            },
            'performance_review': {
                'cover': {'align': 'left', 'elements': ['title', 'period', 'name']},
                'content': {'align': 'left', 'elements': ['title', 'achievements', 'metrics']},
                'ending': {'align': 'center', 'elements': ['summary', 'thanks']}
            },
            'project_summary': {
                'cover': {'align': 'center', 'elements': ['title', 'project_name', 'date']},
                'content': {'align': 'left', 'elements': ['title', 'timeline', 'results']},
                'ending': {'align': 'center', 'elements': ['lessons', 'thanks']}
            },
            'training_course': {
                'cover': {'align': 'center', 'elements': ['title', 'course_name', 'instructor']},
                'content': {'align': 'left', 'elements': ['title', 'objectives', 'content']},
                'ending': {'align': 'center', 'elements': ['summary', 'qa']}
            }
        }
        
        return guides.get(template.id, guides['default'])
    
    def export_template_config(self, template_id: str, output_path: str):
        """
        导出模板配置
        
        Args:
            template_id: 模板ID
            output_path: 输出路径
        """
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"模板不存在: {template_id}")
        
        config = {
            'id': template.id,
            'name': template.name,
            'description': template.description,
            'scenes': template.scenes,
            'style': template.style,
            'colors': template.colors,
            'layout_guide': self._get_layout_guide(template)
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)


def list_templates() -> List[Dict]:
    """列出所有模板"""
    manager = TemplateManager()
    return manager.list_templates()


def get_template(template_id: str) -> Optional[Dict]:
    """获取指定模板"""
    manager = TemplateManager()
    template = manager.get_template(template_id)
    if template:
        return {
            'id': template.id,
            'name': template.name,
            'description': template.description,
            'scenes': template.scenes,
            'style': template.style,
            'colors': template.colors
        }
    return None


if __name__ == '__main__':
    manager = TemplateManager()
    
    # 列出所有模板
    print("=== 所有模板 ===")
    for t in manager.list_templates():
        print(f"{t['id']}: {t['name']}")
        print(f"  场景: {', '.join(t['scenes'])}")
        print()
