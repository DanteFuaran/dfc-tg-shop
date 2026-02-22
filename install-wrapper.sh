#!/bin/bash
cd /opt >/dev/null 2>&1 || true

BLUE='\033[1;34m'
NC='\033[0m'

# Перехватываем Ctrl+C чтобы не выводить "Ошибка"
trap 'stty sane 2>/dev/null; tput cnorm 2>/dev/null; exit 130' INT TERM

echo -e "${BLUE}Пожалуйста, подождите...${NC}"

# Ветка по умолчанию (совпадает с веткой, из которой запущен этот скрипт)
REPO_BRANCH="web_dev"

# Если в version указана другая ветка — она имеет приоритет
GITHUB_RAW_URL="https://raw.githubusercontent.com/DanteFuaran/dfc-tg-shop"
_remote_branch=$(curl -s --max-time 5 "$GITHUB_RAW_URL/$REPO_BRANCH/version" 2>/dev/null | grep '^branch:' | cut -d: -f2 | tr -d ' \n')
[ -n "$_remote_branch" ] && REPO_BRANCH="$_remote_branch"

# Создаем временную папку с уникальным именем
CLONE_DIR=$(mktemp -d)

# Клонируем репозиторий
if ! git clone -b "$REPO_BRANCH" --depth 1 https://github.com/DanteFuaran/dfc-tg-shop.git "$CLONE_DIR" >/dev/null 2>&1; then
    echo "❌ Ошибка при клонировании репозитория"
    rm -rf "$CLONE_DIR"
    exit 1
fi

# Переходим в папку и запускаем установку
if ! cd "$CLONE_DIR"; then
    echo "❌ Ошибка при переходе в папку"
    rm -rf "$CLONE_DIR"
    exit 1
fi

# Даём права на выполнение скрипту установки
chmod +x ./install.sh

# Запускаем скрипт установки
./install.sh
EXIT_CODE=$?

# Проверяем код возврата
if [ $EXIT_CODE -eq 130 ]; then
    # Пользователь прервал через Ctrl+C
    true
elif [ $EXIT_CODE -eq 2 ]; then
    # Пользователь выбрал "Выход"
    true
elif [ $EXIT_CODE -ne 0 ]; then
    # Была ошибка
    echo "❌ Ошибка при выполнении установки"
    echo
    cd /opt
    rm -rf "$CLONE_DIR"
    exit 1
fi

# Удаляем временную папку после установки
cd /opt || exit 1
rm -rf "$CLONE_DIR"
stty sane 2>/dev/null || true
tput cnorm 2>/dev/null || true
