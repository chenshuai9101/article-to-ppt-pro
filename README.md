# 文章转PPT增强版

一键将文章转换为专业PPT演示文稿。

## 功能特性

- 📄 **智能解析**：自动识别文章结构，提取标题、段落、要点
- 🎨 **职场模板库**：内置4套专业职场模板
- 📊 **数据可视化**：支持图表生成和数据展示
- ✍️ **演讲备注**：每页自动生成要点提示
- 📝 **标准格式**：输出标准PPTX，可直接编辑
- 🇨🇳 **中文优化**：深度中文排版优化

## 安装

```bash
pip install -r requirements.txt
```

## 快速开始

### Python API

```python
from scripts import article_to_ppt

# 转换文章
result = article_to_ppt(
    source="https://example.com/article",
    template="project_summary",  # 项目总结模板
    style="infographic"           # 信息图风格
)

print(result)
```

### CLI 命令

```bash
# 转换文章
python main.py convert "文章URL或文本"

# 预览转换效果
python main.py preview "文章URL或文本"

# 列出所有模板
python main.py list
```

## 模板库

| 模板名称 | 适用场景 |
|---------|---------|
| 投资人汇报 | 商业计划、融资演示 |
| 述职报告 | 季度/年度述职 |
| 项目总结 | 项目复盘、经验分享 |
| 培训课件 | 内部培训、知识分享 |

## 项目结构

```
article-to-ppt-pro/
├── SKILL.md                      # 技能说明文档
├── main.py                       # CLI入口
├── package.json                  # 项目配置
├── scripts/
│   ├── __init__.py              # 主入口
│   ├── article_parser.py         # 文档解析模块
│   ├── content_extractor.py      # 内容提取模块
│   ├── ppt_generator.py         # PPT生成模块
│   ├── template_manager.py       # 模板管理器
│   └── export_utils.py           # 导出工具
├── templates/                    # 模板库
│   ├── investor_report/
│   ├── performance_review/
│   ├── project_summary/
│   └── training_course/
└── references/
    └── style_guide.md            # 排版规范
```

## 使用示例

### 示例1：转换网页文章

```python
from scripts import ArticleToPPT

converter = ArticleToPPT()
result = converter.convert(
    source="https://example.com/article",
    template="auto"  # 自动选择模板
)
```

### 示例2：转换本地文本

```python
text = """
Q3季度工作汇报

一、工作概述
本季度业绩同比增长35%。

二、具体成果
1. 产品研发：完成V2.0版本
2. 用户增长：月活突破100万
"""

result = article_to_ppt(text, template="performance_review")
```

## 验收标准

| 指标 | 目标 |
|------|------|
| 文档解析准确率 | >90% |
| 排版专业度 | >4.0/5.0 |
| 可编辑性 | 100% |
| 生成时间 | <2分钟 |

## 依赖

- Python 3.8+
- create-ppt skill（已安装）

## License

MIT
