import os
import re
from datetime import datetime, timezone, timedelta  # 新增timezonefrom pathlib import Path
import sys
from pathlib import Path

def extract_metadata(file_path):
    """
    提取Markdown文件中的元数据
    返回包含date和title的字典（如无则使用默认值）
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检测元数据块（被---包围的YAML格式）
        if content.startswith('---'):
            metadata_block = re.search(r'^---\n(.+?)\n---', content, re.DOTALL)
            if metadata_block:
                metadata_str = metadata_block.group(1)
                metadata = {}
                
                # 提取date字段
                date_match = re.search(r'^date:\s*(.+)$', metadata_str, re.MULTILINE)
                if date_match:
                    try:
                        metadata['date'] = datetime.fromisoformat(date_match.group(1).strip())
                    except ValueError:
                        pass
                
                # 提取title字段（可选）
                title_match = re.search(r'^title:\s*"?(.+?)"?$', metadata_str, re.MULTILINE)
                if title_match:
                    metadata['title'] = title_match.group(1).strip()
                
                return metadata
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
    
    return {}

def generate_note_index(vault_path, output_file="最近更新.md"):
    """
    生成按日期排序的笔记索引
    """
    note_data = []
    vault_path = Path(vault_path)
    
    # 遍历所有Markdown文件[1,2,3](@ref)
    for root, _, files in os.walk(vault_path):
        for file in files:
            if file.lower().endswith('.md'):
                file_path = Path(root) / file
                
                # 获取元数据
                metadata = extract_metadata(file_path)
                
                # 获取相对路径（用于Obsidian内部链接）
                rel_path = file_path.relative_to(vault_path).as_posix()
                
                # 确定链接标题（优先使用元数据中的title）
                title = metadata.get('title', file_path.stem)
                
                # 确定日期（优先元数据，其次文件修改时间）
                note_date = metadata.get('date')
                if not note_date:
                    note_date = datetime.fromtimestamp(
                        os.path.getmtime(file_path), 
                        tz=timezone.utc
                    )
                else:
                    # 确保元数据日期统一为UTC时区
                    if note_date.tzinfo is None:  # 如果是naive
                        note_date = note_date.replace(tzinfo=timezone.utc)
                    else:  # 如果是aware
                        note_date = note_date.astimezone(timezone.utc)
                    
                east8_time = note_date + timedelta(hours=8)
                note_data.append({
                    'title': title,
                    'path': rel_path,
                    'date': east8_time
                })
    
    # 按日期倒序排序[5](@ref)
    note_data.sort(key=lambda x: x['date'], reverse=True)
    
    # 生成索引文件[6,10](@ref)
    with open(vault_path / output_file, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("title: 最近更新\n")
        f.write("date: {}\n".format(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')))
        f.write("---\n")
        idx = 0
        max_cnt = 10
        for note in note_data:
            # 使用Obsidian内部链接格式[[文件名]]
            if note['title'] != "首页":
                f.write(f"- **[{note['date'].strftime('%Y-%m-%d %H:%M')}]** ")
                f.write(f"[[{note['path']}|{note['title']}]]\n")
            idx += 1
            if idx >= max_cnt:
                f.write(f"\n\n> 只显示最近{max_cnt}条笔记，更多请查看目录。\n")
                break
    
    print(f"成功生成索引文件: {vault_path/output_file}")
    print(f"共索引笔记数量: {len(note_data)}")

if __name__ == "__main__":
    # 配置你的Obsidian库路径
    dir_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    generate_note_index(dir_path)