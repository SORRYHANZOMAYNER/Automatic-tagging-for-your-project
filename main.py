import argparse
import subprocess
import os
from packaging.version import parse
import git


# Писать об ошибке при попытке добавить тег между тегами

def add_to_file(file_path, a, b):
    with open(file_path, 'a') as file:
        file.write("К коммиту: " + str(a) + "записан тег -" + str(b) + "\n")
        print("Данные записаны")


def put_tags(patth):
    # Получаем список всех коммитов в репозитории
    list_commits = subprocess.check_output(['git', 'rev-list', '--all']).splitlines()
    print(list_commits)

    repo = git.Repo(patth)
    commit = repo.head.commit
    print(commit)

    current_commit_index = 0
    last_tag = ""
    # Находится индекс текущего коммита
    for c in list_commits:
        if str(commit) in str(c):
            current_commit_index = list_commits.index(c)
    print(current_commit_index)

    for i in range(current_commit_index, -1, -1):
        current_commit = list_commits[i]
        # Проверяется у текущего коммита тег
        try:
            # Если check будет истинно и процесс завершается с ненулевым выходом, то возникает исключение, его
            # атрибуты содержат stdout и stderr, если они были захвачены
            subprocess.check_output(['git', 'describe', '--exact-match', '--tags', current_commit])
            print(f"Commit {current_commit} уже используется")
        except subprocess.CalledProcessError:
            last_tag = subprocess.check_output(
                ['git', 'describe', '--tags', '--abbrev=0', '--always', current_commit]).strip()
            if last_tag != "":
                print("Выход из цикла успешен")
                break
    file_path = r"C:\Users\SESA800181\Desktop\word.txt"
    try:
        tag_number = str(last_tag)
        start_index = tag_number.index('v')
        end_index = tag_number.index('-')
        tag_number = tag_number[start_index + 1:end_index]
        v = parse(tag_number)
        change = int(input("1 - увеличить мажорную версию, 2 - минорную, 3 - микро"))
        if change == 1:
            tag_number = f"v{v.major + 1}.{v.minor}.{v.micro}"
        elif change == 2:
            tag_number = f"v{v.major}.{v.minor + 1}.{v.micro}"
        elif change == 3:
            tag_number = f"v{v.major}.{v.minor}.{v.micro + 1}"
        new_tag = f"b'{tag_number}-alpha'"
        try:
            subprocess.check_output(['git', 'tag', new_tag, current_commit])
            print(f"Тег {new_tag} добавлен к коммиту {current_commit}")
            add_to_file(file_path, current_commit, new_tag)
        except subprocess.CalledProcessError:
            print(
                "Возникла ошибка.Скорее всего вы добавлеете тег для коммита, который уже находится между коммитами с тегами")
    except ValueError:
        print("Тег не найден")
        current_commit = next(reversed(list_commits))
        new_tag = "b'v0.0.1-alpha'"
        subprocess.check_output(['git', 'tag', new_tag, current_commit])
        print(f"Тег {new_tag} добавлен к коммиту {current_commit}")
        add_to_file(file_path, current_commit, new_tag)


# python main.py  --patth="C:\Users\SESA800181\Desktop\repDir\Adventura"
def create_parser():
    parser = argparse.ArgumentParser(description="ScriptJob")
    parser.add_argument('--patth', help="dir")
    args = parser.parse_args()

    if args.patth:
        os.chdir(args.patth)
    else:
        os.chdir(os.pardir)
    put_tags(args.patth)


if __name__ == '__main__':
    create_parser()

