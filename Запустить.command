#!/bin/zsh
set -e
cd -- "${0:A:h}"

if ! command -v python3 >/dev/null; then
    print -u2 'Для запуска Django нужен Python 3.10 или новее. Для просмотра откройте файл «Открыть сайт.html».'
    exit 1
fi

exec python3 start_local.py
