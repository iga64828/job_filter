# 一條龍篩選器 (Full-Stack Filter)
對我來說資料工程師就是搞etl pipeline\
但是台灣一堆缺要一人兼 `DS`/`DA`/`DevOps`/`前端` 的一條龍服務\
真正符合title的缺少之又少\
我也不想每次花時間肉眼找這些缺\
所以我想把這事自動化

## 需求 (Requirements)

本專案旨在從就業網站定期抓取特定工作 title 資訊\
來看哪些工作是內容與 title 相關的。

## 主要流程
1. Call `yourator` API 抓取特定title的職缺
2. 抓取 response的 `path` 欄位(該職缺的連結)，再轉成完整的url
3. 從該url抓取職缺的 `title`, `地址`, `工作內容`, `條件要求`, `薪資範圍`


TO-DO:
- [] 寫一個config設定要抓的職缺
- 寫test
- 包成container 
