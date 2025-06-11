from collections import defaultdict
import os

# 支持的扩展名
SUPPORTED_EXTENSIONS = {'.js', '.ts', '.jsx', '.tsx', '.html', '.css',
                        '.java', '.py', '.go', '.cpp', '.txt', '.md'}


def count_lines(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except BaseException:
        print(f'[code-line-statistics] Error reading file: {filepath}')
        return 0


def analyze_directory(directory):
    stats = {
        'total_files': 0,
        'total_lines': 0,
        'by_extension': defaultdict(lambda: {'count': 0, 'lines': 0}),
        'file_details': [],
        'top_files_by_extension': defaultdict(list)
    }

    for root, _, files in os.walk(directory):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, directory)
                lines = count_lines(filepath)

                stats['total_files'] += 1
                stats['total_lines'] += lines
                stats['by_extension'][ext]['count'] += 1
                stats['by_extension'][ext]['lines'] += lines
                file_detail = {
                    'path': rel_path,
                    'lines': lines,
                    'extension': ext
                }
                stats['file_details'].append(file_detail)
                # 按扩展名收集文件
                stats['top_files_by_extension'][ext].append(file_detail)

    # 对每种扩展名的文件按行数排序并取前5
    for ext in stats['top_files_by_extension']:
        stats['top_files_by_extension'][ext] = sorted(
            stats['top_files_by_extension'][ext],
            key=lambda x: x['lines'],
            reverse=True
        )[:5]

    return stats
