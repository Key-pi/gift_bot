#!/bin/bash

# Настройки
PROJECT_DIR="$HOME/gift_bot"  # путь к проекту на сервере
VENV_DIR="$PROJECT_DIR/venv"
PYTHON_BIN="python3"          # или python3.11, зависит от сервера
GIT_BRANCH="main"

echo "=== Deploy started ==="

# Переходим в проект
cd "$PROJECT_DIR" || { echo "Folder not found"; exit 1; }

# Если репозиторий не клонирован, клонируем
if [ ! -d ".git" ]; then
    echo "Cloning repo..."
    git clone -b $GIT_BRANCH https://github.com/Key-pi/gift_bot.git "$PROJECT_DIR"
fi

# Получаем последние изменения
echo "Pulling latest changes..."
git fetch origin $GIT_BRANCH
git reset --hard origin/$GIT_BRANCH

# Создаём venv если нет
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    $PYTHON_BIN -m venv "$VENV_DIR"
fi

# Активируем venv
source "$VENV_DIR/bin/activate"

# Устанавливаем зависимости
echo "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# Перезапуск бота
# Убиваем старый процесс main.py
echo "Stopping old bot process..."
pkill -f "python main.py" || echo "No existing bot process"

# Запускаем нового
echo "Starting bot..."
nohup python main.py &> deploy.log &

echo "=== Deploy finished ==="