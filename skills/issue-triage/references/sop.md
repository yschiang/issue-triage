# Issue Triage 與交付流程 — SOP v1.12

此檔由 `scripts/html_to_md.py` 從 `index.html` 產生；改內容請改 HTML 再重跑，不要直接改這裡。

*\[圖：Issue Triage、版本交付與緊急處置\]*

## 1 Issue 進來：核心是 Triage，前後四步把它接進來、送出去

**Step 2 Triage 是這條流程的重點**：評估影響、急迫性、修復可行性，做出處置決定。Step 1 把 Issue 接進來；Step 3–5 把決定準備好、執行、驗證。

### Step 1 受理：把 Issue 接進來

**誰**：Support／值班人員，照既有受理流程

**做什麼**：來源不限：報案、Alarm、UAT、內部測試／維運、服務申請／新需求。開單或連主單。**線上影響持續或擴大，先通知值班／Incident Owner 止血。**

**產出**：**一張 Ticket：環境、現象、影響誰、聯絡人。**

**交給**：Triage Owner → Step 2

### Step 2 Triage：評估三件事，做一個決定

**誰**：Triage Owner（預設受理 team 的 Section Manager，SM）召集 Product Owner（PO）與 Release Manager（RM）

**做什麼**：**Assess 三項評估 → Decide 一個決定。**Triage 就是這兩件事，不是分類完再交另一個規劃流程。

*\[圖：Step 2 Triage 子流程：三項評估、並行止血、一個決定（四個問題）選出交付路徑\]*

#### Assess 三項評估

| 做什麼                                                                           | 產出什麼                                                |
|----------------------------------------------------------------------------------|---------------------------------------------------------|
| 評估影響（Impact）：影響誰、業務受阻程度                                         | Severity 與影響範圍                                     |
| 評估急迫性（Urgency）：最晚何時要解決，結合業務影響                              | Priority 與最晚解決時間                                 |
| 評估修復可行性（Feasibility）：workaround 是否有效、能撐多久，最快何時可安全交付 | workaround 能撐到何時、最快安全交付時間、可行選項與風險 |

**定級速查**：Sev1–Sev4 與 P1–P4 一句話定義（完整規則見 [4](#section-3)）

- **Severity（有多嚴重）**：Sev1 核心服務大範圍失效或重大生產／資料風險 · Sev2 重要功能失效，影響特定客戶或關鍵流程 · Sev3 局部異常，核心流程可運作 · Sev4 輕微 · N/A 服務申請／需求
- **Priority（有多急）**：P1 正在發生或迫近重大影響，立即控制 · P2 重要流程受阻、無可接受 workaround，加速處理 · P3 可接受正常排程 · P4 納入 backlog
- Sev1 現行 Incident 預設 P1；其餘 Priority 依影響、急迫性、workaround 與期限綜合決定，不只看回報件數。

#### Decide 一個決定：處置與交付安排

**止血是並行動作，不排在問題裡。**線上影響持續或擴大 → 立即止血（Rollback、Config、受控 SQL、停用功能或安全可交付的 Hotfix），Step 1 受理時就啟動；Decide 只確認止血方式與 Owner，永久修復照下面走。

**四個問題依序問，每題有出口；四題合起來只做一個決定。**

1.  **資訊夠決定嗎？**Severity、Priority、三個時間（最晚解決、workaround 能撐到、最快安全交付含測試／核准／部署）都抓得到。抓不到 → **限時調查**：指定調查人與回 Triage 的時間，不硬填版本。
2.  **要改 code 嗎？**不改 → 服務處理（例如 Operation Change：權限、設定、資料修正），改環境走 Step 4 依授權執行，再 Step 5 驗證，不經 Step 3。
3.  **是修復，還是新功能？**新功能或需完整整合 → **Formal Release**；可先出 Beta 給指定客戶 pilot（選用，PO＋RM 確認範圍與日期）。
4.  **修復：比時間，選路徑。**把「最晚解決時間、workaround 能撐到」和「最快安全交付、下一個 Patch 窗口」放一起看：

| 情況                    | 路徑                    | 備註                                               |
|-------------------------|-------------------------|----------------------------------------------------|
| 撐不到下一個 Patch 窗口 | **Hotfix**              | 必要驗證與核准完成即出                             |
| 撐得到近期修補窗口      | **Scheduled Patch**     | 進下一班修補                                       |
| 可以等到正式版          | **延到 Formal Release** | 必須寫理由、等待風險、接受者；不能只為少走一次流程 |

交付安排由 **PO＋RM 依 SM 的評估共同確認**；沒共識怎麼辦見 [第 2 章](#section-2)。

**產出**：**是否立即止血；Hotfix／Scheduled Patch／Formal Release 或其他處理；Ticket Owner、下一步與期限；驗收條件、下次回覆時間，與一句「為什麼這樣決定」。**

**交給**：改 code → SM 與 RM，Step 3；服務處理 → 執行人，Step 4／Step 5

### Step 3 準備：把修復與發布準備好

**誰**：SM（修復與測試）、RM（版本與 Readiness）

**做什麼**：

1.  SM 協調修復與測試。
2.  RM 定版本號，依路徑選 Readiness 範圍（[6.1](#section-5)）；Hotfix 走加速審查，不等例行班車。
3.  確認部署、監控與 Rollback 方式。

**產出**：**可交付的修復、驗證證據、發布安排。**

**交給**：執行人 → Step 4

### Step 4 Change：依授權執行

**誰**：執行人（依產品聯絡表指定的工程師或維運）；授權人與實際 protocol 也查聯絡表

**做什麼**：

1.  依影響與授權選程序：Normal／Urgent／War room（[6.2](#section-5)）。
2.  核准完成才執行；War room 依預授權處置、同步記錄。
3.  執行後補齊允許延後的項目；超出授權範圍現場升級。

**產出**：**實際操作、版本、範圍與執行結果；需補辦項目有 Owner 與期限。**

**交給**：Ticket Owner → Step 5

### Step 5 驗證：確認有效，回覆並結案

**誰**：Ticket Owner，會同 User／服務負責人

**做什麼**：

1.  在受影響環境驗證，回覆 User。
2.  通過 → 結案；未通過、影響擴大或 workaround 失效 → **回 Step 2 重新 Triage**。
3.  服務恢復可結束 Incident；永久修復、主線整合、其他客戶交付另開追蹤。code merged 不等於結案。

**產出**：**驗證證據、User 確認、剩餘工作的 Owner 與期限。**

**交給**：結案；剩餘工作回到各自 Owner

## 2 角色與決策責任

**兩個責任角色：PO 決定要什麼，RM 說能不能上。**責任角色不是職稱，依產品與發布範圍具名指定。SM 是職稱，負責工程執行，把「怎麼做、要多久、風險、證據」交給 PO 與 RM 判斷。

*\[圖：兩個責任角色 PO 與 RM 共同確認交付安排，SM 提供工程評估；沒共識由具名升級主管決定\]*

| 角色            | 組織歸屬與任命原則                                        | 核心責任                                                                                                  |
|-----------------|-----------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| Product Owner   | PM side；依產品範圍與業務決策授權指定                     | What／Priority／Business Value／Acceptance：做什麼、先做什麼、業務價值與驗收                              |
| Section Manager | Engineering side 職稱，不是責任角色；負責 team 的技術交付 | Build／Technical execution：技術方案、工作拆解、工程執行、修復與測試                                      |
| Release Manager | Engineering side；依發布範圍指定                          | Release readiness／Quality gate／Dependency／Deployment／Rollback：發布準備、品質關卡、相依性、部署與回退 |

Engineering 與 PM 各有 Section Manager → Manager 兩層。RM 由誰擔任：

| 發布範圍        | Release Manager 通常由誰擔任               |
|-----------------|--------------------------------------------|
| 單 team release | Engineering Section Manager 兼任           |
| 跨 team release | Engineering Manager 或專職 Release Manager |

- 交付安排由 PO 與 RM 依 SM 的工程評估共同確認；工程師不單方承諾 release plan。
- 每個產品／Release Plan 寫明具名 PO 與 RM。SM 兼 RM 時，仍分別確認「工程完成」與「具備發布條件」。
- PO 與 RM 談不攏：PO 說期限與延後損失，RM 說缺哪些發布條件，SM 給可行選項。期限內沒共識 → 產品聯絡表上的具名升級主管決定，不能只填「主管」。
- 主管的取捨不免除品質關卡；例外由既定授權者核准，RM 記錄結論與部署安排。
- 緊急事件直接走值班／War room 預授權，不等協調或例會。

## 3 版本與交付紀錄

採 CalVer：`YYYY.MM.PATCH`，月份代表正式班車基準月份。

| 用途                    | 範例                                   |
|-------------------------|----------------------------------------|
| 正式班車首次發布        | `2026.06.0`                            |
| 該版本線 Hotfix         | `2026.06.1`                            |
| 後續 Scheduled Patch    | `2026.06.2`，包含已納入的 Hotfix 修復  |
| 下一正式班車            | `2026.09.0`                            |
| 下一正式版的新功能 Beta | `2026.09.0-beta.1`、`2026.09.0-beta.2` |

Hotfix 與 Scheduled Patch 是交付節奏，不必各建一套版號；相同版本線的修補序號依發布順序遞增，不預設奇數或偶數代表特定路徑。六月版本在七月修補，仍屬 `2026.06.x`。

**每個 Hotfix／Patch 的修復一定要 merge 回主幹，並納入後續的 Patch 或 Formal Release。**先在 main 修再移植到 release branch，或先在 release branch 修再回主線，都可以；但整合要有 Owner 與期限，客戶已驗證不代表主線已納入（見 [5.3](#section-4)）。

Beta 使用 `-beta.N`，指向預定正式版；已發布版本不可覆寫。Patch 原則只含修復，不夾帶新功能或破壞相容性的變更。

每次交付記錄 Affected version、候選／已確認 Target version、實際部署 version／build、日期、客戶／範圍及驗證結果。Release Manager 維護受支援版本、班車與 Patch Calendar；Ticket Owner 將安排及變更回覆 User。

## 需要時再查

處理案件時會用到的判斷規則。

## 4 Severity 與 Priority

**Severity 是影響有多嚴重；Priority 是處理有多急。**例子供對照，不是清單。

| Severity      | 判斷                                                   | 例子                                                             |
|---------------|--------------------------------------------------------|------------------------------------------------------------------|
| Sev1 Critical | 核心服務全面／大範圍失效，或重大生產、品質、資料風險   | 核心系統全面停擺，使用者無法完成主要作業；資料寫錯且已被下游使用 |
| Sev2 Major    | 重要功能失效，影響特定客戶、區域或關鍵流程             | 某項主要功能失效，需人工介入才能繼續；某客戶的報表全部錯誤       |
| Sev3 Moderate | 局部異常，核心流程仍可運作，影響可控制                 | 單一功能偶發錯誤，重試即過；dashboard 資料延遲十分鐘             |
| Sev4 Minor    | 輕微呈現或便利性問題，不影響核心結果                   | 畫面欄位錯字、排版跑掉、匯出檔案欄位順序不對                     |
| N/A           | 一般 Service Request、Enhancement 或不適用嚴重度的工作 | 開帳號、加權限、要一份歷史資料匯出、新增一個報表欄位             |

Incident 按實際影響評級；Bug 要註明正式環境、UAT、Pilot 或尚未啟用，並區分已發生與潛在影響。恢復服務後保留事件最高 Severity，另外更新目前影響。

| Priority    | 判斷與處置                                                         | 例子                                                          |
|-------------|--------------------------------------------------------------------|---------------------------------------------------------------|
| P1 Critical | 正在發生或迫近重大影響，需要立即控制；啟動應變                     | Sev1 現行 Incident；Sev2 但明天客戶驗收或出貨受阻             |
| P2 High     | 重要流程受阻、缺乏可接受 workaround，或無法等待正常排程；加速處理  | Sev2 沒有 workaround；Sev3 但擋住本週 UAT 驗收                |
| P3 Normal   | 影響可控制，能接受正常排程；評估 Scheduled Patch 或 Formal Release | Sev3 有 workaround；Sev2 已止血、workaround 可撐到 Patch 窗口 |
| P4 Low      | 影響輕微、急迫性低；納入 backlog 並定期重審                        | Sev4；一般 Enhancement                                        |

**Sev 和 P 不一樣的三個常見情況：**

- Sev2，但客戶明天驗收 → P1。急迫性把它拉高。
- Sev1 已 rollback 恢復 → 事件仍記 Sev1，永久修復的 Ticket 是 P2 或 P3。影響已控制，急迫性降下來。
- Sev3，但卡住已承諾的上線日 → P2。不因還沒上 Production 就當成不急。

Sev1 現行 Incident 預設 P1。Priority 依影響、急迫性、workaround 與期限綜合決定，不只看回報件數、Alarm 數量或要求者職級。升降級須記錄時間、依據、決定者與通知對象。

## 5 Mitigation 與交付路徑

### 5.1 Mitigation 與 Hotfix 的關係

Mitigation 是恢復目標，Hotfix 是修復交付方式；兩者可重疊或先後。手段：Rollback、關閉功能、改 config、受控 SQL／資料修正或緊急修復。

操作依適用授權與 Change／War room protocol 執行，留下操作內容、範圍、驗證與恢復方式。是否改 code 不是唯一風險判斷。

### 5.2 需要修復版本時的三種節奏

| 路徑            | 選用條件                                                                 | 交付安排                                             |
|-----------------|--------------------------------------------------------------------------|------------------------------------------------------|
| Hotfix          | 無法等下次固定 Patch，或目前 workaround 不足以支撐到該時點               | 今天、明天或本週；完成必要驗證與核准即發布，不等班車 |
| Scheduled Patch | 修復需要交付，但影響可控制且能等近期修補窗口                             | 合併已具備 readiness 的修復，於固定 Patch 窗口交付   |
| Formal Release  | 新功能／較完整整合；既有功能修復須有延後至正式版的理由，且等待風險可接受 | 納入月／季班車，記錄修復延後原因、風險與接受者       |

分流依據是影響能否承受等待、workaround 是否可靠、最快何時能安全交付；不只看 Severity，也不為少走一次流程。**既有修復預設進最早可安全交付且適合的 Patch；不能等就 Hotfix；延到 Formal Release 由 PO 與 Release Manager 記錄原因、殘餘風險與接受者。**涉及班車容量取捨時，再整合到產品 Release Plan。

以下只列 Step 2 沒有直接講到的情境：

| 判斷情境                                     | 處置原則                                                                                                                                   |
|----------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| UAT 問題阻擋驗收、上線或已承諾日期           | 依期限、替代方案及修復可行性加速交付，不因尚未上 Production 就自動降低 Priority；依修復所屬版本提供 Hotfix、近期 Patch 或下一個 Beta build |
| 修復可很快完成，但問題不急                   | 不自動選 Hotfix；可依影響與交付成本安排 Patch 或 Formal Release                                                                            |
| 問題緊急，但暫時找不到 workaround 或快速修復 | 保持應變、限時調查、升級資源，評估停用、隔離或其他恢復方式；持續更新風險與預估時間，不直接改排下一個 Formal Release                        |

UAT 是驗證階段，不是版本類型：正式支援版本的修復走 Hotfix／Patch；尚未正式發布的新功能以新的 Beta build 修正。時效與風險原則相同。

### 5.3 Hotfix 先交付與後續納入

Hotfix 可先完成必要工程測試，再由最急迫且適合的指定 User／客戶進行 UAT。若在正式環境限定範圍部署，記錄為受控上線與上線驗證，走適用 Change，不把它只當成測試環境 UAT。

以下三項結果須分開追蹤，不代表固定執行先後：

- **已交付客戶**：實際版本、部署範圍、驗證結果與觀察。
- **主線整合**：修復 commit 經 PR 納入 main／trunk，避免未來版本遺漏。
- **後續版本**：將修復納入適用的 Patch／Formal Release 分支，於各目標分支執行必要 CI 與回歸測試。

可採 main 先修再移植，或受影響 release branch 先修再回主線；應有明確 Owner 與追蹤期限。避免把不相關的 release-specific 變更一併帶回主線。客戶 UAT 通過不取代整合後的驗證，也不代表其他客戶已部署。

### 5.4 Beta 提前驗收新功能

**Beta 用於下一個 Formal Release 的新功能，提前提供指定 User 做 UAT；不是 Hotfix 的另一個名稱。** 可以在兩班正式 Release 之間交付。

例如目前正式版為 `2026.06.0`，七～八月提供 `2026.09.0-beta.1`；UAT 修正為 `2026.09.0-beta.2`，達到正式發布條件後再交付 `2026.09.0`。

Product Owner 與 Release Manager 共同確認：功能範圍、試跑對象、Beta 日期、UAT 成功／停止條件、已知限制及正式版目標；Section Manager 提供技術 readiness 與風險判斷。

Beta／UAT 日期與正式交付日期分開記錄。未通過時修正、延後或移出當班範圍；正式交付仍須完成整合、回歸測試及發布條件。

## 6 Readiness Review 與 Change

### 6.1 依風險選擇審查範圍

**所有進入 Production 的變更都要判斷 readiness，但不必每次重開完整 PRR。** 以下為本流程建議的審查方式，非業界統一名稱。

| 交付方式        | 建議審查方式                                                                                    |
|-----------------|-------------------------------------------------------------------------------------------------|
| Formal Release  | 沿用完整 PRR，確認整體功能、效能、相依性、監控、維運及部署準備                                  |
| Scheduled Patch | 沿用既有 PRR 基線，審查本次修復範圍、影響、回歸測試及部署／恢復方式                             |
| Hotfix          | 加速 readiness review，聚焦不能等的原因、最小修復、必要測試、首批對象、監控與恢復；不等例行會議 |
| Beta            | 針對 UAT／pilot 環境與範圍確認 readiness；涉及 Production 時須符合相應的生產要求                |
| War room 處置   | 依既定 protocol 完成現場判斷與授權，同步留紀錄，儘速補齊未完成的檢查與事後檢討                  |

審查至少回答：改什麼、影響誰、有哪些證據及缺口、何時與哪裡執行、如何判斷成功、失敗如何恢復、誰核准與誰觀察。

涉及 DB schema、資料修正、核心交易、重大相依性或難以回退的變更，應提高審查深度，不能只因標示 Patch／Hotfix 就降低標準。緊急情況需縮短或延後部分檢查時，依預先定義的授權條件記錄例外與補做安排。

### 6.2 三種執行程序

| 程序              | 執行方式                                                                         |
|-------------------|----------------------------------------------------------------------------------|
| Normal Change     | 正常評估與核准後，依核准窗口執行                                                 |
| Urgent Change     | 加速必要評估與核准，於執行前完成適用授權；不等例行審查會議                       |
| War room protocol | 在既定授權範圍內先處置、同步記錄、事後補齊 Change 與檢討；超出授權範圍即現場升級 |

這是本團隊使用的程序名稱與責任安排。Hotfix 不必然等於 War room 處置，Formal Release 也不代表任何時點都能上線；依實際風險、時效與授權選擇程序。

**各產品須在產品聯絡表連結實際適用的 Change／War room protocol，並列明核准者、值班代理與升級管道。** 沿用既有制度即可，不另建一套；本文件不是緊急變更的授權憑證。找不到適用 protocol 或授權人時，立即使用既有值班升級管道確認，不自行擴張權限。同步記錄操作，允許事後補辦的 Change 文件、檢查與檢討須有 Owner 與期限。

**Readiness Review 回答「準備好了沒」；Change 回答「是否授權、何時、如何執行」。** 兩者共用測試、風險與部署證據，可於同一次 Go／No-Go 完成，不要求重複填單或審查。

## 參考資訊

定義、模板與來源，不是規則。

## 7 Type 與關聯紀錄

| 類型             | 定義與處理重點                                                           |
|------------------|--------------------------------------------------------------------------|
| Incident         | 服務中斷、降級或錯誤結果；優先控制影響、恢復服務                         |
| Bug              | 不符合既有規格或承諾功能；確認重現、修復與回歸測試                       |
| Service Request  | 既有服務、權限、設定或操作申請；依標準程序與授權處理                     |
| Enhancement      | 新增能力或改變預期行為；釐清價值、範圍與驗收條件                         |
| Problem          | 一個或多個 Incident 的根因、重複模式或長期風險；追蹤根因及永久改善       |
| Operation Change | 對環境、部署、設定或資料的受控變更；記錄風險、授權、執行、驗證與恢復方式 |

Incident、Bug、Problem、Operation Change 可以互相連結，不必把同一筆紀錄反覆改成不同類型。多個 User 回報同一問題或大量相同 Alarm，應建立／連結共同主單，保留各自影響範圍與通知對象。

## 8 流程角色一覽

**分不清時，先記三句：**

- 預設 Triage Owner 由受理 team 的 SM 擔任；Ticket Owner 由 Triage 指派，通常是處理工程師；兩者可同一人。Triage Owner 確保決定做出來，決定本身由 PO＋RM 拍板。
- 對 User 只有一個窗口：Ticket Owner。Incident Owner 只在重大事件期間存在，對內統籌、對管理層通報，不另開 User 溝通線。
- 重大事件由值班依既定條件升級並指定 Incident Owner；沒升級前，值班就是止血的負責人。

| 角色（PO、SM、RM 見第 2 章） | 主要責任                                                                   |
|------------------------------|----------------------------------------------------------------------------|
| Support／值班人員            | 受理、初篩、補資料、查重複及通報；不自行承諾修復版本                       |
| Triage Owner                 | 確保評估與處置決策完成，指派 Ticket Owner，協調爭議、逾期與升級            |
| Ticket Owner                 | 端到端追蹤、協調、User 更新、風險管理、驗證與結案                          |
| Incident Owner               | 重大事件期間統籌恢復、跨團隊協調、決策、升級與對管理層通報                 |
| 執行人                       | 依 Change 授權實際操作環境的工程師或維運；記錄操作、範圍、結果與需補辦項目 |
| 工程師                       | 調查、實作、修復與測試；提供可行性、風險及 readiness 證據                  |
| User                         | 提供問題與影響，確認 workaround 可接受性，參與 UAT 與結果驗證              |

角色可以兼任。轉派必須由新 Owner 明確接受，留下交接時間、目前狀態、未完成事項、風險及下一步；接受前原 Owner 仍負責。升級不等於責任轉移，User 不承擔內部找人與協調責任。

## 9 狀態與回應節奏

| 狀態        | 使用時機                                                     |
|-------------|--------------------------------------------------------------|
| New         | 已收到，尚未完成初篩                                         |
| Triaging    | 正在 Assess Issue 與 Decide Resolution                       |
| Planned     | 已有處置方向，等待排程／班車；未排入版本者須有原因與重審日期 |
| In Progress | 調查、處置、開發、測試、部署或 pilot 中                      |
| Waiting     | 被明確的外部依賴阻擋；填等誰、等什麼、期限及追蹤人           |
| Resolved    | 原問題已驗證，等待確認                                       |
| Closed      | 完成結案並留下正確 Resolution；同一問題未解決可重開          |

重大 Incident 可直接 In Progress，並行補齊 Triage。等待班車使用 Planned；不得用 Waiting 掩蓋未排程或無 Owner。轉派、等工程師或等班車不自行暫停 SLA 時鐘。

以下為建議初始目標；不是修復完成承諾，正式 SLA 與服務時段另定。

| Priority | 首次人工回應              | 初步處置決定                              | 持續更新         |
|----------|---------------------------|-------------------------------------------|------------------|
| P1       | 15 分鐘內，走既有值班通報 | 立即應變；30 分鐘內提出恢復方向或目前阻礙 | 每 30 分鐘至恢復 |
| P2       | 4 工作小時內              | 1 工作日內確認 Owner、下一步與交付評估    | 每工作日         |
| P3       | 1 工作日內                | 3 工作日內完成 Triage 與安排／評估日期    | 每週             |
| P4       | 2 工作日內                | 5 工作日內完成 Triage 與評估安排          | 每月             |

預期失約、P1 無人承接、影響擴大、workaround 失效或風險升高時，立即升級適用的 Triage Owner、Incident Owner、主管或值班管道。沒有新進展也須回覆阻礙與下一步。

Duplicate 須連到主單並保留後續通知。User 未回覆時，依已約定的提醒與結案規則處理，不標成已修復；仍有未控制重大影響者不得因未回覆而關單。跨組爭議由內部 Owner 協調，不將案件退給 User 自行找團隊。

## 10 紀錄模板

### 使用者提單

``` text
標題：
產品／功能與環境／客戶／範圍：
目前版本：
發生時間與時區：
預期結果、實際結果與重現方式：
業務影響、範圍、期限與原因：
已嘗試處理／workaround：
附件／log／截圖與聯絡人：
```

### 每案至少記錄：Triage 與處置決定

以下是最小紀錄的參考格式；環境與版本等已在原單提供的資料直接引用，不重複填寫。正式版號與 readiness 證據可在後續階段補齊。

``` text
Type／Severity／Priority 與依據（不適用者註明）：
Ticket Owner／影響與業務期限：
處置方向：說明／服務處理／Mitigate／修 Bug／新需求／調查／暫緩
決策理由：為什麼選這個處置，而不是其他選項？
下一步、處理人、期限與下次回覆時間：
驗收／結案條件；未定案時的調查與重審時間：
```

### 依情境補充：不用每案全部填

| 何時填                  | 需要補充的紀錄                                                                                                                                                  |
|-------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 有重複或關聯案件        | 主單及相關 Incident／Bug／Problem／Operation Change 連結                                                                                                        |
| Incident／需 Mitigate   | Incident Owner（重大事件）、方式、授權、實際操作與恢復驗證                                                                                                      |
| 需選修復交付路徑        | 最晚解決時間；workaround 可用時間、有效證據、可支撐期限及殘餘風險；最快安全修復時間、信心與未知事項                                                             |
| 需版本交付              | Hotfix／Scheduled Patch／Formal Release；Affected version、候選／確認 Target version；具名 PO 與 Release Manager、負責的 Section Manager；參與 teams 與決策紀錄 |
| 修復延至 Formal Release | 延後原因、等待風險、接受者與重審條件                                                                                                                            |
| Beta                    | 範圍、對象、日期、驗收／停止條件與正式版目標                                                                                                                    |
| 有環境變更              | 適用 Readiness 證據、風險、例外核准；Change／War room protocol 連結、授權及執行紀錄；實際 build／版本、範圍與時間；補做項目、Owner 與期限                       |
| Hotfix                  | 客戶交付驗證、主線整合、後續版本納入，各自的 Owner、期限及結果                                                                                                  |
| 有分歧或逾期            | 未決事項、具名升級主管／代理、期限與決定                                                                                                                        |

產品聯絡表集中維護 PO、Release Manager、Section Manager、升級主管與代理，以及適用 Change／War room protocol；Ticket 引用即可，不需逐單重建。

### User 更新與結案

每次更新交代目前影響、已完成事項、下一步、負責人、目標時間、風險與下次更新時間。結案前確認：

- 原問題或約定交付已在受影響環境驗證。
- 處置、版本／範圍、時間、驗證人與證據完整。
- 剩餘 Bug／Problem／正式 rollout／Operation Change 有具名 Owner 與追蹤。
- 重大事件責任已結束或明確交接。
- User 已確認，或符合已約定的例外結案規則。
- Resolution 正確，不把 workaround、Duplicate、No response 或失敗的 Operation Change 標為已修復／成功。
- 有交接時，新 Owner 已明確接受。

## 11 業界參考與適用範圍

本文件的責任分工、分流、時限與審查分級是團隊流程設計。下列來源支持相關概念，不代表本文全部規則是業界強制標準。

- [GitLab Issue Triage](https://handbook.gitlab.com/handbook/product-development/how-we-work/issue-triage/)：Partial／Complete Triage 與 milestone、Priority。
- [GitLab Bug Prioritization](https://handbook.gitlab.com/handbook/engineering/infrastructure-platforms/developer-experience/bug-prioritization/)：跨職能優先排序與 milestone planning。
- [Microsoft Git Branching Guidance](https://learn.microsoft.com/en-us/azure/devops/repos/git/git-branching-guidance?view=azure-devops)：主線與 release branch 的修復移植。
- [Google SRE PRR](https://sre.google/sre-book/evolving-sre-engagement-model/)：服務可靠性與維運接手準備；不等同每次發布都完整重審。
- [Microsoft Safe Deployment Practices](https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/safe-deployments)：漸進部署、品質檢查與緊急加速 protocol。
- [Atlassian Change Management Types](https://www.atlassian.com/itsm/change-management/types)：風險與時效導向的變更管理。
- [Calendar Versioning](https://calver.org/)：日期版本與 modifier。

## 12 FAQ

- **多個 User 報案或 Alarm 大量發送，該止血、Hotfix、Patch 還是 Formal？** 線上影響持續就先止血；能不能等下一個 Patch 窗口決定 Hotfix 或 Patch；新功能才走 Formal。見 [Step 2](#step-2-一起判斷決定怎麼處理)。
- **UAT 發現問題，另出 Hotfix 還是併入下一版？** 看期限與 workaround，不因還沒上 Production 就降 Priority；已支援版本的修復走 Hotfix／Patch，未發布新功能出下一個 Beta build。不能只為合併簽核而延後。見 [5.2](#section-4)。
- **Release Plan 由誰決定？** PO 決定要什麼，RM 決定能不能上，SM 提供工程評估；PO＋RM 共同確認，沒共識由具名升級主管決定。見 [第 2 章](#section-2)。
