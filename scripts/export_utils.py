#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文章转PPT增强版 - 导出工具
Article to PPT Pro - Export Utilities

功能：
- PPTX导出
- 文件格式转换
- 批量导出
"""

import os
import shutil
from datetime import datetime
from typing import Dict, List, Optional


class ExportUtils:
    """导出工具类"""
    
    def __init__(self):
        self.export_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'exports'
        )
        os.makedirs(self.export_dir, exist_ok=True)
    
    def export_pptx(self, html_file: str, output_name: Optional[str] = None) -> str:
        """
        将PPTX.html导出为PPTX
        
        Args:
            html_file: HTML文件路径
            output_name: 输出文件名
            
        Returns:
            str: 导出的PPTX文件路径
        """
        # 导入create-ppt的导出脚本
        import subprocess
        
        scripts_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            '.skills', 'skill_create-ppt', 'scripts'
        )
        export_script = os.path.join(scripts_dir, 'export_pptx.py')
        
        # 生成输出文件名
        if not output_name:
            base_name = os.path.splitext(os.path.basename(html_file))[0]
            output_name = f"{base_name}.pptx"
        
        output_path = os.path.join(self.export_dir, output_name)
        
        # 调用导出脚本
        try:
            result = subprocess.run(
                ['python', export_script, html_file],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                # 移动到输出目录
                generated_file = os.path.join(
                    os.path.dirname(html_file),
                    output_name.replace('.pptx', '.pptx')
                )
                if os.path.exists(generated_file):
                    shutil.move(generated_file, output_path)
                    return output_path
            
            raise Exception(f"导出失败: {result.stderr}")
            
        except Exception as e:
            # 如果导出失败，返回原HTML路径
            return html_file
    
    def batch_export(self, html_files: List[str], output_dir: Optional[str] = None) -> List[str]:
        """
        批量导出PPTX
        
        Args:
            html_files: HTML文件列表
            output_dir: 输出目录
            
        Returns:
            List[str]: 导出的PPTX文件列表
        """
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        results = []
        for html_file in html_files:
            try:
                result = self.export_pptx(html_file)
                results.append(result)
            except Exception as e:
                print(f"导出失败 {html_file}: {e}")
                results.append('')
        
        return results
    
    def get_export_history(self, limit: int = 20) -> List[Dict]:
        """
        获取导出历史
        
        Args:
            limit: 返回数量限制
            
        Returns:
            List[Dict]: 导出历史
        """
        history = []
        
        if not os.path.exists(self.export_dir):
            return history
        
        for filename in os.listdir(self.export_dir):
            if filename.endswith('.pptx'):
                filepath = os.path.join(self.export_dir, filename)
                stat = os.stat(filepath)
                
                history.append({
                    'filename': filename,
                    'path': filepath,
                    'size': stat.st_size,
                    'created': datetime.fromtimestamp(stat.st_ctime).isoformat()
                })
        
        # 按时间倒序
        history.sort(key=lambda x: x['created'], reverse=True)
        
        return history[:limit]
    
    def cleanup_exports(self, days: int = 7):
        """
        清理过期导出文件
        
        Args:
            days: 保留天数
        """
        if not os.path.exists(self.export_dir):
            return
        
        from datetime import timedelta
        
        cutoff = datetime.now() - timedelta(days=days)
        
        for filename in os.listdir(self.export_dir):
            filepath = os.path.join(self.export_dir, filename)
            if os.path.isfile(filepath):
                stat = os.stat(filepath)
                created = datetime.fromtimestamp(stat.st_ctime)
                
                if created < cutoff:
                    os.remove(filepath)


def export_pptx(html_file: str, output_name: Optional[str] = None) -> str:
    """
    导出PPTX的便捷函数
    
    Args:
        html_file: HTML文件路径
        output_name: 输出文件名
        
    Returns:
        str: 导出的PPTX文件路径
    """
    utils = ExportUtils()
    return utils.export_pptx(html_file, output_name)


def batch_export(html_files: List[str], output_dir: Optional[str] = None) -> List[str]:
    """
    批量导出
    
    Args:
        html_files: HTML文件列表
        output_dir: 输出目录
        
    Returns:
        List[str]: 导出的PPTX文件列表
    """
    utils = ExportUtils()
    return utils.batch_export(html_files, output_dir)


if __name__ == '__main__':
    # 测试
    utils = ExportUtils()
    
    # 获取导出历史
    history = utils.get_export_history()
    print(f"导出历史: {len(history)} 个文件")
    for item in history[:5]:
        print(f"  {item['filename']} - {item['size']} bytes")
