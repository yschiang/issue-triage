---
name: issue-triage
description: Issue Triage 與交付流程 SOP（v1.12）——Severity／Priority 定級、止血、Hotfix／Scheduled Patch／Formal Release 分流、PO／SM／RM 責任、CalVer 版號，附操作指南 HTML、Executive Summary 與 Triage Wizard。凡是使用者提到 triage、issue 分級、Sev、Priority、hotfix 該不該出、patch 窗口、release plan 誰決定、PO／RM 責任、止血／mitigation、班車版號，或要修改、發布、升版這份指南／wizard，都用這個 skill；即使只是問「這個 issue 該怎麼處理」也用。
metadata:
  version: "1.12"
---

# Issue Triage 與交付流程

三份產物共用一個版本號（repo 的 `VERSION`，現為 1.12）：

| 檔案 | 用途 | 版本印在哪 |
|---|---|---|
| `assets/index.html` | 操作指南本體，**內容的唯一來源** | footer「作業指南 vX.Y」 |
| `assets/executive-summary.html` | 給管理層的一頁摘要 | eyebrow「Executive Summary · vX.Y」 |
| `assets/triage-wizard.html` | 五題點選的判斷工具，規則和指南一致 | 頁尾「Triage Wizard vX.Y」 |
| `references/sop.md` | 指南的 Markdown 版，給 Claude 讀、給人貼 wiki | 標題「SOP vX.Y」；由腳本從 index.html 產生 |

## 任務一：幫使用者 triage 一個 issue

**預設直接開 wizard，不在對話裡問問題。** Wizard 五題點選就出結果，比來回問答快；使用者有疑問再回來問。

1. 有 Artifact 工具：先 `list` 找標題為「Triage Wizard」的 artifact，有就 `open`；沒有就把 `assets/triage-wizard.html` 複製到 `/mnt/user-data/outputs/` 後 `publish`（favicon 🧭）。沒有 Artifact 工具：用 present_files 給 HTML 檔。
2. 回覆只寫一兩句：wizard 已開、第一次要設定目前版本／班車／下一個 Patch 窗口、點完結果可複製貼 Ticket、有疑問直接問。不要先講一遍流程，不要列題目。
3. 使用者回來問時（「為什麼是 P2？」「這種算 Sev 幾？」「可以延到正式版嗎？」），才讀 `references/sop.md` 對應章節回答，用下面同一套規則，一段話講完。

例外：使用者在訊息裡已經把情況講清楚（影響、期限、要改什麼都有），或明說「不要工具、直接告訴我」，就直接給六行結論，並附一句「也可以用 wizard 自己點」。

判斷規則（和 wizard 完全一樣，回答疑問時照這個，不要自己發明）：

| 情況 | 路徑 |
|---|---|
| 修復且資訊不夠（期限或 workaround 不明） | 限時調查：指定調查人與回 Triage 的時間，不硬填版本 |
| 服務處理 | 依既有程序；改環境走 Step 4 Change，再 Step 5 驗證 |
| 新功能／需完整整合 | Formal Release（下一正式版），可先出 Beta；不走 Hotfix／Patch |
| 修復，今天或這幾天要好 | Hotfix，版號 = 這條線下一個修補序號 |
| 修復，Patch 前要好，沒 workaround | Hotfix |
| 修復，Patch 前要好，有 workaround | Scheduled Patch |
| 修復，可以等正式版 | 預設 Scheduled Patch；要延到 Formal 必須寫理由、等待風險、接受者 |

線上影響持續或擴大 → 先止血（Rollback／Config／受控 SQL／停用功能／安全可交付的 Hotfix），與上面並行。

Priority：Sev1 現行 Incident 預設 P1；今天要好 → P1；這幾天要好、或 Sev1–3 沒 workaround → P2；Sev4／N/A → P4；其餘 P3。

直接給結論時用固定六行，可貼 Ticket：

```
Severity／Priority：Sev2 / P2（一句依據）
止血：進行中（並行）／不需要
處置／交付路徑：Hotfix 2026.06.2
為什麼：撐不到 10 月上旬的 Patch 窗口
下一步：Step 3 準備（加速 readiness，不等例會）
Ticket Owner／期限／驗收條件／下次回覆：（填）
```

角色只有兩個責任角色：**PO 決定要什麼，RM 說能不能上**；SM 是職稱，提供工程評估。談不攏 → 產品聯絡表上的具名升級主管決定。緊急事件走值班／War room 預授權，不等例會。

## 任務二：修改指南、摘要或 wizard

內容的正本在 GitHub repo 根目錄（`index.html`、`executive-summary.html`、`triage-wizard.html`）；skill 裡的 `assets/` 是 build 時複製來的，不要只改這裡。改之前先讀 `references/editing-rules.md`（使用者定過的寫法與紅線）。

1. 使用者有提供 repo 檔案就改那份；只有這個 skill 時，把 `assets/` 的 HTML 複製到工作目錄改，交付時說明要放回 repo 根目錄。
2. `index.html` 是內容來源。子流程圖是內嵌 SVG，文字改了圖一起改。規則有變同步改 `triage-wizard.html` 的 `decide()` 與題目；「立即三件事」有變才改摘要。
3. 在 repo 裡：`python3 scripts/bump_version.py 1.13 "一句話"` 升版（重排也要升），再 `python3 scripts/build_skill.py` 重生 `sop.md` 與 `.skill`。不要手改版本字串或 sop.md。
4. 交付：present_files 匯出改過的檔案；有 Artifact 工具就重新發布（先發摘要拿網址，再把指南裡 `./executive-summary.html` 換成該網址）。
5. 回覆用繁體中文短句，說改了什麼、為什麼，並提醒 commit 與 `git tag v<版本>`。

## 任務三：回答「這份流程為什麼這樣定」

直接引用 `references/sop.md` 對應章節，一段話講完；不要擴寫成教科書。使用者反覆強調的原則：

- Triage = Assess 三項 + Decide 一個決定，不是分類完再交另一個規劃流程。
- 止血不等任何評估；Severity 不自動等於 Priority。
- 不能等 Patch → Hotfix；能等 → Scheduled Patch；延到 Formal 要有理由和接受者。
- Hotfix／Patch 修復一定 merge 回主幹並納入後續版本；code merged 不等於結案。
- 現在只有月／季班車，不寫週／雙週的規則。

## 檔案地圖

- `references/sop.md` — 全文（約 400 行，章節見標題），由 repo 的 `scripts/html_to_md.py` 產生；使用者對 wizard 結果有疑問時讀第 1、4、5 章，任務三照章節找。
- `references/editing-rules.md` — 寫法與紅線。
- `assets/` — 三份 HTML，自包含，可直接開或發布。
- Repo 結構：根目錄三份 HTML（正本）、`scripts/`（升版、build）、`skills/issue-triage/`（本 skill）、`CHANGELOG.md`、`VERSION`。
