#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文章转PPT增强版 - PPT生成模块
Article to PPT Pro - PPT Generator Module

功能：
- 调用create-ppt生成PPT
- 模板选择
- 风格适配
- 批量生成
"""

import json
import os
from typing import Dict, List, Optional


class PPTGenerator:
    """PPT生成器"""
    
    # 风格映射
    STYLE_MAPPING = {
        'infographic': 'A',      # 信息图风
        'illustration': 'B',     # 插画科普风
        'photo': 'C',            # 图文混排风
        'cartoon': 'D',          # 卡通绘本风
        'handdrawn': 'E'         # 手绘笔记风
    }
    
    # 场景映射到视觉风格
    SCENE_STYLE_MAPPING = {
        '投资人汇报': 'infographic',
        '述职报告': 'infographic', 
        '项目总结': 'infographic',
        '培训课件': 'illustration',
        '工作汇报': 'infographic',
        '方案分享': 'infographic',
        '知识分享': 'handdrawn'
    }
    
    def __init__(self):
        self.scripts_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            '.skills', 'skill_create-ppt', 'scripts'
        )
    
    def generate(self, ppt_data: Dict, output_dir: str = '.') -> Dict:
        """
        生成PPT
        
        Args:
            ppt_data: PPT数据
            output_dir: 输出目录
            
        Returns:
            Dict: 生成结果
        """
        # 准备生成参数
        params = self._prepare_params(ppt_data)
        
        # 调用create-ppt脚本
        try:
            result = self._call_generate_script(params)
            return {
                'success': True,
                'file': result.get('output_file', ''),
                'pages': len(ppt_data.get('outline', []))
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _prepare_params(self, ppt_data: Dict) -> Dict:
        """准备生成参数"""
        outline = ppt_data.get('outline', [])
        title = ppt_data.get('title', '演示文稿')
        style = ppt_data.get('style', 'infographic')
        template = ppt_data.get('template', 'default')
        
        # 转换风格
        style_code = self.STYLE_MAPPING.get(style, 'A')
        
        # 生成每页内容
        slides = []
        for item in outline:
            slide = self._generate_slide(item, style_code)
            slides.append(slide)
        
        return {
            'ppt_title': title,
            'channel': 'unknown',
            'template_file': self._get_template_file(template),
            'ppt_content': slides
        }
    
    def _generate_slide(self, outline_item: Dict, style_code: str) -> Dict:
        """
        生成单页幻灯片内容
        
        Args:
            outline_item: 大纲项
            style_code: 风格代码
            
        Returns:
            Dict: 幻灯片数据
        """
        page_type = outline_item.get('type', 'content')
        page_num = outline_item.get('page', 1)
        
        if page_type == 'cover':
            return self._generate_cover_slide(outline_item, style_code)
        elif page_type == 'ending':
            return self._generate_ending_slide(outline_item, style_code)
        else:
            return self._generate_content_slide(outline_item, style_code)
    
    def _generate_cover_slide(self, item: Dict, style_code: str) -> Dict:
        """生成封面页"""
        title = item.get('title', '')
        subtitle = item.get('subtitle', '')
        
        # 中文排版优化
        prompt = f"""生成一张PPT封面页。

视觉风格（以下内容仅用于指导风格，不要把文字本身写进画面）：线性扁平风格，白色工程图纸感的背景，整体呈浅蓝-白色调。标题字号中等，整体简洁大气。不要出现人像。

页面中央位置展示主标题「{title}」，粗体，字号中等，单行展示。
主标题下方展示副标题「{subtitle}」，字号更小。
页面底部小字显示「职场汇报演示」

整体留白充足，聚焦标题。"""
        
        return {
            'page_id': item.get('page', 1),
            'prompt': prompt,
            'ref_images': []
        }
    
    def _generate_content_slide(self, item: Dict, style_code: str) -> Dict:
        """生成内容页"""
        title = item.get('title', '')
        content = item.get('content', [])
        
        # 格式化内容
        if isinstance(content, list):
            content_text = '\n'.join([f'- {p}' for p in content[:5]])
        else:
            content_text = str(content)[:500]
        
        prompt = f"""生成一张信息图海报。

视觉风格（以下内容仅用于指导风格，不要把文字本身写进画面）：线性扁平风格，白色工程图纸感的背景，整体呈浅蓝-白色调。标题字号小，正文的字号非常小，保持留白充足，适当搭配少量扁平的图解元素。不要出现人像。

标题「{title}」位于页面左上角，黑色粗体。

页面内容区域展示要点：
{content_text}

整体布局清晰，层次分明。"""
        
        return {
            'page_id': item.get('page', 1),
            'prompt': prompt,
            'ref_images': []
        }
    
    def _generate_ending_slide(self, item: Dict, style_code: str) -> Dict:
        """生成结尾页"""
        title = item.get('title', '谢谢观看')
        subtitle = item.get('subtitle', '')
        
        prompt = f"""生成一张PPT结尾页。

视觉风格（以下内容仅用于指导风格，不要把文字本身写进画面）：线性扁平风格，白色工程图纸感的背景，整体呈浅蓝-白色调。与封面呼应。不要出现人像。

页面中央位置展示感谢语「{title}」，大号字。
{f'页面底部小字显示「{subtitle}」' if subtitle else ''}

整体简洁，大量留白。"""
        
        return {
            'page_id': item.get('page', 1),
            'prompt': prompt,
            'ref_images': []
        }
    
    def _get_template_file(self, template: str) -> Optional[str]:
        """获取模板文件"""
        if template == 'default':
            return None
        
        template_files = {
            'investor_report': 'templates/investor_report/template.pptx',
            'performance_review': 'templates/performance_review/template.pptx',
            'project_summary': 'templates/project_summary/template.pptx',
            'training_course': 'templates/training_course/template.pptx'
        }
        
        return template_files.get(template)
    
    def _call_generate_script(self, params: Dict) -> Dict:
        """
        调用generate_batch.py脚本
        
        Args:
            params: 生成参数
            
        Returns:
            Dict: 脚本执行结果
        """
        import subprocess
        
        script_path = os.path.join(self.scripts_dir, 'generate_batch.py')
        
        # 构造命令
        cmd = ['python', script_path]
        
        # 使用管道传递参数
        result = subprocess.run(
            cmd,
            input=json.dumps(params, ensure_ascii=False),
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode != 0:
            raise Exception(f"生成失败: {result.stderr}")
        
        return json.loads(result.stdout)
    
    def select_template(self, article_data: Dict) -> str:
        """
        根据文章内容选择模板
        
        Args:
            article_data: 文章数据
            
        Returns:
            str: 推荐模板
        """
        title = article_data.get('title', '').lower()
        content = article_data.get('content', '').lower()
        
        # 关键词匹配
        if any(kw in title + content for kw in ['投资', '融资', '商业计划', 'bp']):
            return 'investor_report'
        
        if any(kw in title + content for kw in ['述职', '季度', '年度', '考核']):
            return 'performance_review'
        
        if any(kw in title + content for kw in ['项目', '复盘', '总结', '交付']):
            return 'project_summary'
        
        if any(kw in title + content for kw in ['培训', '教学', '课件', '课程']):
            return 'training_course'
        
        # 默认模板
        return 'project_summary'
    
    def select_style(self, article_data: Dict) -> str:
        """
        根据文章内容选择风格
        
        Args:
            article_data: 文章数据
            
        Returns:
            str: 推荐风格
        """
        # 默认使用信息图风，适合职场汇报
        return 'infographic'


def generate_ppt(ppt_data: Dict, output_dir: str = '.') -> Dict:
    """
    生成PPT的便捷函数
    
    Args:
        ppt_data: PPT数据
        output_dir: 输出目录
        
    Returns:
        Dict: 生成结果
    """
    generator = PPTGenerator()
    return generator.generate(ppt_data, output_dir)


def list_templates() -> List[Dict]:
    """
    列出可用模板
    
    Returns:
        List[Dict]: 模板列表
    """
    return [
        {
            'id': 'default',
            'name': '默认模板',
            'description': '通用职场风格',
            'scenes': ['工作汇报', '通用演示']
        },
        {
            'id': 'investor_report',
            'name': '投资人汇报',
            'description': '专业商业风格，适合融资路演',
            'scenes': ['投资人汇报', '商业计划']
        },
        {
            'id': 'performance_review',
            'name': '述职报告',
            'description': '简洁商务风格，适合述职汇报',
            'scenes': ['述职报告', '绩效考核']
        },
        {
            'id': 'project_summary',
            'name': '项目总结',
            'description': '结构清晰风格，适合项目复盘',
            'scenes': ['项目总结', '经验分享']
        },
        {
            'id': 'training_course',
            'name': '培训课件',
            'description': '循序渐进风格，适合教学培训',
            'scenes': ['培训课件', '知识分享']
        }
    ]


if __name__ == '__main__':
    # 测试模板列表
    templates = list_templates()
    for t in templates:
        print(f"{t['id']}: {t['name']} - {t['description']}")
