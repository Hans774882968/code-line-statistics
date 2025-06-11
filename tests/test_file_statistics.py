import pytest
import os
import tempfile
from file_statistics import analyze_directory

go_file_path = os.path.join('subdir', 'test.go')


@pytest.fixture
def setup_test_files():
    '''创建临时测试文件和目录结构'''
    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建支持的扩展名文件
        test_files = [
            ('test.py', 'print(\'Hello\')\nprint(\'World\')\n'),  # 2 lines
            ('test.js', '// JS file\nconsole.log(1);\nconsole.log(2);\nconsole.log(3);\n'),  # 4 lines
            ('test.md', '# Header\n\nContent\n'),  # 3 lines
            ('test.txt', 'Line1\nLine2\nLine3\nLine4\nLine5\n'),  # 5 lines
            ('test2.txt', 'Line1\nLine2\nLine3\nLine4\nLine5\nfoo\nbar'),  # 7 lines
            ('test3.txt', 'Line1\nLine2\nLine3\nLine4\nLine5\nfoo\n'),  # 6 lines
            (go_file_path, 'package main\n\nfunc main() {\n}\n'),  # 4 lines
            ('empty.cpp', ''),  # 0 lines
            ('unsupported.xyz', 'Should not be counted\n')  # 不支持的类型
        ]

        for rel_path, content in test_files:
            full_path = os.path.join(tmpdir, rel_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)

        yield tmpdir  # 提供给测试用例使用


def test_analyze_directory_basic(setup_test_files):
    result = analyze_directory(setup_test_files)

    # 验证总文件数（不包括不支持的扩展名）
    assert result['total_files'] == 8
    assert result['total_lines'] == 2 + 4 + 3 + 5 + 7 + 6 + 4 + 0

    # 验证按扩展名统计
    assert result['by_extension']['.py']['count'] == 1
    assert result['by_extension']['.py']['lines'] == 2
    assert result['by_extension']['.js']['count'] == 1
    assert result['by_extension']['.js']['lines'] == 4
    assert result['by_extension']['.go']['count'] == 1
    assert result['by_extension']['.go']['lines'] == 4

    # 验证每种扩展名的前5文件
    assert len(result['top_files_by_extension']['.py']) == 1
    assert result['top_files_by_extension']['.py'][0]['lines'] == 2
    assert len(result['top_files_by_extension']['.txt']) == 3
    assert result['top_files_by_extension']['.txt'][0]['lines'] == 7
    assert result['top_files_by_extension']['.txt'][1]['lines'] == 6
    assert result['top_files_by_extension']['.txt'][2]['lines'] == 5


def test_empty_directory():
    '''测试空目录'''
    with tempfile.TemporaryDirectory() as empty_dir:
        result = analyze_directory(empty_dir)
        assert result['total_files'] == 0
        assert result['total_lines'] == 0
        assert len(result['by_extension']) == 0
        assert len(result['top_files_by_extension']) == 0


def test_directory_with_only_unsupported_files():
    '''测试只有不支持文件的目录'''
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, 'test.xyz'), 'w') as f:
            f.write('content\n')

        result = analyze_directory(tmpdir)
        assert result['total_files'] == 0
        assert result['total_lines'] == 0


def test_file_path_correctness(setup_test_files):
    '''测试返回的文件路径是否正确'''
    result = analyze_directory(setup_test_files)

    # 检查路径是否为相对路径
    for file_detail in result['file_details']:
        assert not os.path.isabs(file_detail['path'])
        assert os.path.exists(os.path.join(setup_test_files, file_detail['path']))

    # 检查子目录文件路径
    assert any(go_file_path in fd['path'] for fd in result['file_details'])


def test_count_lines_edge_cases():
    '''测试count_lines函数的边缘情况'''
    with tempfile.TemporaryDirectory() as tmpdir:
        # 测试空文件
        empty_file = os.path.join(tmpdir, 'empty.py')
        with open(empty_file, 'w'):
            pass
        assert analyze_directory(tmpdir)['total_lines'] == 0

        # 测试大文件(模拟)
        big_file = os.path.join(tmpdir, 'big.py')
        with open(big_file, 'w') as f:
            f.write('\n' * 1000)  # 1000行
        assert analyze_directory(tmpdir)['total_lines'] == 1000


def test_special_characters_in_files():
    '''测试包含特殊字符的文件'''
    with tempfile.TemporaryDirectory() as tmpdir:
        special_file = os.path.join(tmpdir, 'special.py')
        content = '# 中文注释\nprint(\'你好\')\n# éàè\n'
        with open(special_file, 'w', encoding='utf-8') as f:
            f.write(content)

        result = analyze_directory(tmpdir)
        assert result['total_lines'] == 3
        assert result['by_extension']['.py']['lines'] == 3
