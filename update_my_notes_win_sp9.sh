python3 ./generate_recent_notes.py /mnt/c/Users/lixy5/OneDrive/Documents/obsidian/xiaoyili/deploy
npx quartz build
rm -rf /mnt/c/Users/lixy5/Documents/xiaoyi_space/deploy/*
cp -a -f ./public/. /mnt/c/Users/lixy5/Documents/xiaoyi_space/deploy/
rm -rf /mnt/c/Users/lixy5/OneDrive/Documents/obsidian/xiaoyili/deploy/最近更新.md
