python3 generate_recent_notes.py /Users/lixiaoyi/Documents/obsidian/xiaoyili/deploy
npx quartz build
rm -rf ~/Documents/xiaoyi.space/deploy/*
cp -a -f ./public/. ~/Documents/xiaoyi.space/deploy/
rm /Users/lixiaoyi/Documents/obsidian/xiaoyili/deploy/最近更新.md