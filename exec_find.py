# -*- encoding:utf-8 -*-
import os

#扫描子文件
def scan_files(directory, prefix=None, postfix=None):
    files_list = []

    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            if postfix:
                if special_file.endswith(postfix):
                    files_list.append(os.path.join(root, special_file))
            elif prefix:
                if special_file.startswith(prefix):
                    files_list.append(os.path.join(root, special_file))
            else:
                files_list.append(os.path.join(root, special_file))

    return files_list


# 扫描子目录
def scan_sub_dirs(directory, prefix=None, postfix=None):
    sub_dir_list = []

    for root, sub_dirs, files in os.walk(directory):
        for special_sub_dir in sub_dirs:
            if postfix:
                if special_sub_dir.endswith(postfix):
                    sub_dir_list.append(os.path.join(root, special_sub_dir))
            elif prefix:
                if special_sub_dir.startswith(prefix):
                    sub_dir_list.append(os.path.join(root, special_sub_dir))
            else:
                sub_dir_list.append(os.path.join(root, special_sub_dir))

    return sub_dir_list


print scan_sub_dirs('/media/sf_dev/workspace', 'WEB-INF')
