import zipfile
import string

zip_file_path = "标书（2DNS+1移动）.zip"

letters = string.ascii_lowercase  # 获取小写字母
numbers = string.digits  # 获取数字
special_chars = ['#', '$']  # 特殊字符

password_found = False

for number1 in numbers:
    for number2 in numbers:
        for number3 in numbers:
            for number4 in numbers:
                password = 'n' + number1 + number2 + '#' + 'n' + number3 + number4 + '$'

                try:
                    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                        zip_ref.extractall(pwd=bytes(password, 'utf-8'))
                    print("解压成功，密码为:", password)
                    password_found = True
                    break
                except Exception as e:
                    continue

            if password_found:
                break

        if password_found:
            break

    if password_found:
        break

if not password_found:
    print("密码破解失败。")