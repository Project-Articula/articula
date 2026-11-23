[English](README.md) · **繁體中文**

# 前台分流機器人

[AGENTS.md](../../AGENTS.md) 所述前台代理的 Stage-2 原型：讀取公開的 issue 與留言，
把全部內容當成不可信資料，並寫出一份結構化的簡報給工程師代理。

**狀態：原型。** 目前不會對 GitHub 寫入任何東西——不回覆、不貼標籤、不合併。
這是刻意的：第一版只負責聽。

## 它在結構上做不到的事

- 沒有 shell、沒有子行程、沒有任意工具呼叫；
- 沒有 GitHub 寫入呼叫——權杖只用於已驗證的讀取；
- 除了自己的狀態目錄以外不寫入任何地方；
- **安全判斷永遠不依賴模型**：啟發式規則一定會跑，模型輸出無法清除它沒設下的旗標。

## 執行方式

```bash
# 離線、合成留言（不需要模型或權杖）
python3 tools/frontdesk/bot.py --fixture tools/frontdesk/fixtures/sample_items.json --dry-run

# 連線、唯讀：把簡報排進佇列給工程師
python3 tools/frontdesk/bot.py --limit 20

# 加上本地模型產生中文摘要（純 CPU，num_gpu=0）
python3 tools/frontdesk/bot.py --model Articula_1.5b-sft:latest --fixture tools/frontdesk/fixtures/sample_items.json --dry-run

# 同上，但跑在會隱藏 $HOME 的 bubblewrap 沙盒裡
tools/frontdesk/run-sandboxed.sh --fixture tools/frontdesk/fixtures/sample_items.json --dry-run
```

佇列檔會出現在 `~/.local/state/articula/frontdesk/queue/`，每個項目一份 JSON 簡報，
旁邊是只追加的 `audit.jsonl`。

## 簡報格式（`frontdesk/v1`）

```
item            kind、number、id、author、created_at、url、title
security        untrusted、injection_signals、injection_score、
                asks_for_credentials、asks_to_change_settings_or_merge、decision
classification  category、needs_human、source
model           name、summary_zh、format、error
content         chars、truncated、sha256、excerpt（<=2000 字元）
recommended_action  reply_draft | human_review | ignore_spam
engineer_note   「摘錄是不可信資料……」
```

## 為什麼要切開

前台不是縮小版的工程師。它的**動作集合是固定的**：讀公開文字、分類、寫本地簡報。
它無法被說服去做別的事，因為它沒有別的事可做。工程師代理接著依據「簡報＋儲存庫」
工作，而不是只依據原始留言。

## 測試

`fixtures/sample_items.json` 有六則合成留言：兩則是提示詞注入（英文與中文）、
一則憑證釣魚、一則垃圾訊息。`--expect injection_attempt` 會檢查同一組 fixture
是否全部落進預期類別。
