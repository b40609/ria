# ROADMAP — competitor-code-teardown

> 交接文件（2026-10-25，從 OmniKeep session 分家）。背景讀：README.md、
> examples/self-teardown.md、research/decision-log.md、research/recommendations.md。

## 目標（用戶明確裁示）
**執行產出品質**要追平或超越 daymade/boshu2/SGRX——不是自迭代花俏功能。
已達成：v1.4.1（五模型審查吸收＋證據認識論升級＋比例閘門＋復現測試）。

## NEXT（優先序）
1. **補讀 SGRX**（alzenkastrati/sgrx）——唯一從未克隆深讀的目標，先 `python scripts/pin.py https://github.com/alzenkastrati/sgrx ./research`
2. **功能分解軸（最大差異化）**：FRAME 加 scope 軸（產品級／逐功能級／兩者）。
   功能級＝對產品每個子系統各自找 best-of-breed 競品（例：量化平台→回測找
   vectorbt/backtrader、Bot 管理找 Freqtrade/Jesse、執行找 ccxt/Hummingbot），
   逐模組 borrow list＋逐模組 moat。三個競品都沒做功能級。
   第一個實戰案例候選：CatOS（用戶本地專案，未來在 OmniKeep 監看目標內）。
3. **分層對決 benchmark**：(a) 對照組＝裸模型無 skill；(b) 全跑組＝三原型代表
   （daymade 平台型／boshu2 嚴謹型／SGRX 管線型）同一目標 repo；(c) 清單審計組＝
   其餘面板（repo-analyzer/superpowers/DeepGit/垂直簇）只審模板。
   固定評分尺：證據密度／復現測試／決策可用度／四級標記全過。
4. v1.5 backlog：決策 JSON＋驗證器、frontmatter 契約、discover.py fork 過濾。

## 環境事實
- repo：本目錄；GitHub：b40609/competitor-code-teardown（CI 綠，pytest+活體煙霧）
- 安裝副本：~/.agents/skills/competitor-code-teardown（改完記得同步）
- 測試：`python -m pytest tests/ -q`（5 個，全離線）；push 後看 CI
- 用戶已授權自主迴圈（範圍＝本 repo、紅線只增不減、CI 必綠、決策記 decision-log）
- 競品克隆在 ./research/clones（manifest.json 記 SHA/授權）
