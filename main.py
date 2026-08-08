#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文章转PPT增强版 - CLI入口
Article to PPT Pro - CLI Entry
"""

import argparse
import sys
import json
from scripts import ArticleToPPT, list_templates


def main():
    parser = argparse.ArgumentParser(
        description='文章转PPT增强版 - 一键将文章转换为专业PPT'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # convert命令
    convert_parser = subparsers.add_parser('convert', help='转换文章为PPT')
    convert_parser.add_argument('source', help='文章URL或文本内容')
    convert_parser.add_argument('-t', '--template', default='auto', help='模板名称')
    convert_parser.add_argument('-s', '--style', default='infographic', help='视觉风格')
    convert_parser.add_argument('-o', '--output', help='输出文件名')
    
    # list命令
    list_parser = subparsers.add_parser('list', help='列出可用模板')
    
    # preview命令
    preview_parser = subparsers.add_parser('preview', help='预览转换效果')
    preview_parser.add_argument('source', help='文章URL或文本内容')
    preview_parser.add_argument('-o', '--output', help='输出JSON文件')
    
    args = parser.parse_args()
    
    if args.command == 'convert':
        converter = ArticleToPPT()
        result = converter.convert(args.source, args.template, args.style)
        
        if result.get('success'):
            print("✅ 转换成功!")
            print(f"   文件: {result.get('pptx_file', result.get('file', ''))}")
            print(f"   页数: {result.get('pages', 0)}")
        else:
            print(f"❌ 转换失败: {result.get('error', '未知错误')}")
            sys.exit(1)
    
    elif args.command == 'list':
        templates = list_templates()
        print("📋 可用模板:")
        for t in templates:
            print(f"\n  【{t['name']}】")
            print(f"  ID: {t['id']}")
            print(f"  描述: {t['description']}")
            print(f"  适用场景: {', '.join(t['scenes'])}")
    
    elif args.command == 'preview':
        converter = ArticleToPPT()
        preview = converter.preview(args.source)
        
        output = {
            'title': preview['title'],
            'estimated_pages': preview['estimated_pages'],
            'recommended_template': preview['recommended_template'],
            'outline': [
                {'page': item['page'], 'type': item['type'], 'title': item['title']}
                for item in preview['outline']
            ]
        }
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
            print(f"✅ 预览已保存到: {args.output}")
        else:
            print(json.dumps(output, ensure_ascii=False, indent=2))
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
