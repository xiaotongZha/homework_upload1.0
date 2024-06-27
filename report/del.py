import os
import shutil

def delete_files_in_subfolders(root_dir):
    # 获取当前目录下所有子目录
    subfolders = [f.path for f in os.scandir(root_dir) if f.is_dir()]
    
    # 遍历每一个子目录
    for subfolder in subfolders:
        files_path = os.path.join(subfolder, 'files')
        
        # 检查 'files' 文件夹是否存在
        if os.path.exists(files_path) and os.path.isdir(files_path):
            # 删除 'files' 文件夹中的所有文件
            for file_name in os.listdir(files_path):
                file_path = os.path.join(files_path, file_name)
                
                # 确保这是一个文件而不是目录
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"Deleted directory and its contents: {file_path}")

if __name__ == "__main__":
    # 获取当前工作目录
    current_directory = os.getcwd()
    delete_files_in_subfolders(current_directory)

