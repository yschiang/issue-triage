# 編修規則與紅線

這些是使用者在定稿過程中明確要求過的。改指南、摘要或 wizard 前先看一遍。

## 寫法

- 繁體中文、短句；主結論加粗。不寫教科書式背景，不加「多的話」。
- 每個 Step 用同一個 task 結構：**誰 → 做什麼（有序小步驟）→ 產出 → 交給誰**。
- Step 2 是重點；Step 1、3、4、5 精簡到看得出「做什麼、產出」就好，程序定義推到參考章節加連結。
- 「做什麼 → 產出什麼」用表格，不要再加一段重複說明。
- 本文只留規則；定義、模板、來源放「參考資訊」，並標明「不是規則」。
- 三層分區：本文（永遠展開）／需要時再查（可展開）／參考資訊。章節平鋪 1–12，不加階層編號。
- 每條規則只講一次；發現重複就合併，不要再抄一遍。
- 例子可以給（Sev／P 各附通用情境，不綁特定產業或系統），但註明「供對照，不是清單」。
- 這是通用流程：不寫「廠務」、機台、recipe、lot 這類特定領域用語。
- 不寫還沒發生的事：目前只有月／季班車，週／雙週交付與其版號規則不寫。Patch 頻率不寫固定數字。
- 不寫「前版」「對應舊版角色」這類只給接手者看的話；那放 HANDOFF 或 CHANGELOG。

## 流程圖

- 主頁流程圖放在前方直接顯示，**不要收起來**。
- Step 2 子流程圖：Assess 三格 → 並行止血帶 → 一個 Decide 大框，裡面四題依序、每題有出口。
- 圖的文字和本文文字一對一；改一邊要改另一邊。
- 圖是靜態 SVG，色票同頁面（teal #08786f、ink #172e3b、muted #526975、line #dce5e7、warn #c9834a）。

## 名詞

- 責任角色只有 **Product Owner（PO）** 與 **Release Manager（RM）**。**Section Manager（SM）** 是職稱，負責工程執行，提供評估，不是責任角色。不要再出現 Engineering Lead、Team Lead。
- 階層兩層：Section Manager → Manager。用 **team**，不用 squad。
- Severity 寫 **Sev1–Sev4**（避免和現有 incident S 編號撞名）；Priority 寫 P1–P4。
- Ticket 型別的變更叫 **Operation Change**；流程層的 Change（Step 4、Normal／Urgent Change）維持 Change。
- 「服務處理」涵蓋不改 code 的處理（例如 Operation Change）；不再分「不改」與「只改環境」兩個出口。
- 執行人：依產品聯絡表指定的工程師或維運。
- Triage Owner 預設受理 team 的 SM；Ticket Owner 由 Triage 指派，通常是處理工程師；對 User 只有一個窗口（Ticket Owner）。

## 決策規則（不可自行改動）

- Triage = Assess 三項（Impact → Sev、Urgency → P 與最晚解決、Feasibility → workaround 撐到、最快安全交付）+ Decide 一個決定。
- 止血並行，不排在問題裡。Sev1 現行 Incident 預設 P1。
- 不能等 Patch → Hotfix；能等 → Scheduled Patch；延到 Formal 要理由、等待風險、接受者。新功能 → Formal，可先 Beta。
- 資訊不夠 → 限時調查，不硬填版本。
- CalVer `YYYY.MM.PATCH`；Hotfix／Patch 共用遞增序號；Beta 用 `-beta.N`。
- Hotfix／Patch 一定 merge 回主幹並納入後續 Patch 或 Formal。code merged 不等於結案。

## 版本

- 三份 HTML、sop.md、SKILL.md 共用一個版本號，改任何內容都升版（重排也算）。
- 用 `scripts/bump_version.py`，不要手改版本字串；改完跑 `scripts/build_skill.py`（會重生 sop.md 與 .skill）。
- 正本是 repo 根目錄的三份 HTML；`skills/issue-triage/assets/` 是 build 產物，不進 git。
- 每次升版都 `git tag v<版本>`。
- CHANGELOG 一條一句話，寫改了什麼；不寫過程。
