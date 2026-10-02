# Release Strategy Template

v0.12 ・ 2026-10-02 ・ 草稿，供討論

**一句話：** 每個 package 搭固定班車出版。先在一個點驗收（pilot），通過後再擴散到整廠（fanout）。廠和廠之間照依賴順序走。

| 標記 | 意思 |
|---|---|
| ✅ | 已定 |
| 💡 | 建議，還沒確認 |
| ⏳ | 待決 |
| 🔧 | team 要填 |

---

## 1. 名詞

| 名詞 | 意思 |
|---|---|
| PR | Pull Request：程式碼合併請求，要有人審查才能合併 |
| PRR | Production Readiness Review：上線準備審查，確認可以安全上線 |
| 班車（Release train） | 固定時間出發的出版時段。趕上就上車，趕不上等下一班 |
| package-dc | 部署到各 DC（資料中心）的 package。一個 DC 對應幾個 phase，例如 P123 |
| package-zone | 以 A／B 分區（zone）為部署單位的 package |
| 部署目標（Target） | 一次部署的範圍。dc 可以小到單一 phase，例如 `FAB14-P1`；zone 例如 `FAB14A` |
| Pilot run | 先在一個目標上線試跑。Pilot run 就是 UAT（使用者驗收測試），也就是 staging |
| Beta | Pilot run 用的版本，版號加 `-beta.N`。會上 staging 和 production |
| Fanout | Pilot 通過後，放到同廠其他所有目標 |
| Progressive rollout | 分批、分天上線，不一次全部放 |
| 禁止變更日 | 不能做 change 的日子：週五、放假前一天 |
| Parent／Child fab | Child 要等 parent 達到條件，才能開始 |
| 每廠 pilot | 每個 fab 都先 pilot，再 fanout |
| 首廠 pilot | 只有第一個 fab pilot，其他 fab 直接 fanout |
| 預設路線 | 每個 package 選一種路線，當成平常的做法 |
| Special route | 單一版本不走 package 的預設路線。要和 user 協議 |
| 跳版 | Fab 從舊版直接升到更新的版本，跳過中間版本 |
| Acceptance criteria | 驗收標準。Pilot 開始前和 user 談定 |
| Blocking issue | 擋住上線的問題，包括 incident |

---

## 2. 角色與決策

**責任角色只有兩個：PO 和 RM（沿用 Issue Triage v1.12）。Project lead 和每位 SM 都是 PO，所以 PO 有好幾位。** ✅

每張 ticket、每份 Release Plan 只寫一位 PO，避免「兩個人都以為對方簽了」。💡

**一句話分工：PO 管「做對的事」，tech lead 管「把事做對」，RM 管「安全地放上去」。**

| 決策 | 誰 | 狀態 |
|---|---|---|
| 主持 Triage（Triage Owner） | 受理 team 的 PO | ✅ |
| PR 把關 | Tech lead | ✅ |
| PRR 把關 | RM | ✅ |
| 和 user 談定 acceptance criteria | PO | ✅ |
| Pilot（UAT）sign off | PO ＋ user | ✅ |
| Blocking issue／incident 的 triage | RM | ✅ |
| 跳版 | RM | ✅ |
| 分天時每批放哪些 phase | PO ＋ RM | ✅ |
| 單一版本走 special route | PO 和 user 協議，RM 確認可行 | 💡 |
| 安排部署與 fanout | RM | 💡 |

---

## 3. 版本與班車

### 3.1 版號（沿用 Issue Triage v1.12）

| 規則 | 內容 | 狀態 |
|---|---|---|
| 格式 | CalVer（用日期當版號）：`YYYY.MM.PATCH` | ✅ |
| Hotfix／Patch | 共用同一組遞增的 PATCH 序號 | ✅ |
| Beta | 版號加 `-beta.N`；pilot run 用的就是 Beta | ✅ |
| Beta 轉正式 | Pilot 簽核通過的那個 Beta，直接標成正式版號拿去 fanout，不重新 build（重新 build 的東西等於沒驗收過） | 💡 |
| Merge 回主幹 | Hotfix／Patch 一定 merge 回主線，並納入後續版本 | ✅ |
| 各自編號 | package-dc 和 package-zone 各有自己的版號 | ✅ |
| 標示 package | 版號前加 package 名，避免撞名：`package-dc/2026.10.0` | 💡 |

### 3.2 班車

| Package | 班車 | 狀態 |
|---|---|---|
| package-dc | 季班車 | ✅ |
| package-zone | 月班車 | ✅ |

- Hotfix 不等班車：不能等 Patch → Hotfix（v1.12）。✅
- 目前只有月／季班車，週或雙週不訂規則。✅

### 3.3 dc 與 zone 怎麼配合

**dc 一季一版，zone 一季三版。所以 dc 要先準備好，zone 不能等 dc。**

| 規則 | 內容 | 狀態 |
|---|---|---|
| dc 先提供 | zone 要用的新介面，先跟 dc 季班車上線，zone 之後再用 | 💡 |
| dc 向後相容 | dc 新版上線後，線上現有的 zone 版本要照常運作 | 💡 |
| 同月兩班車 | dc 先上、穩定後 zone 再上 | 💡 |
| 相容表 | 每個 zone 版本寫明「需要 dc 哪一版以上」 | 💡 |
| 需求提前收 | dc 規劃季班車時，收集 zone 未來三個月的需求 | 💡 |

---

## 4. 部署範圍

### 4.1 部署目標 ✅

**package-dc**

| Fab | DC（phase 群組） |
|---|---|
| FAB12 | P123、P456、P789 |
| FAB14 | P123、P456、P78 |
| FAB15 | P123、P456、P7 |
| FAB18 | P123、P456、P78 |
| FAB22 | P12 |
| FAB23 | P12 |

**package-zone**

| Fab | 目標 |
|---|---|
| FAB12 | 🔧 |
| FAB14 | 14A（P1–P4）、14B（P5–P8） |
| FAB15 | 15A（P1–P4）、15B（P5–P7） |
| FAB18 | 18A（P1–P5）、18B（P6–P8） |
| FAB22 | 🔧 |
| FAB23 | 🔧 |

- 每個 fab 都有 dc 和 zone 兩種部署。✅
- dc 部署時，可以只放 DC 裡的部分 phase。✅
- FAB21 只出現在舊表，先視為不在範圍。💡

### 4.2 命名 💡

| 類型 | 寫法 |
|---|---|
| dc 整個 DC | `FAB14-P123` |
| dc 部分 phase | `FAB14-P1`、`FAB14-P12` |
| zone 目標 | `FAB14A` |
| Pilot 目標 | 可以比部署單位小，例如 dc 只在 `f14p1` pilot；zone 在 `f14a` pilot |

### 4.3 產品歸屬 🔧

| 產品 | Package | 預設路線 | 版本上限 |
|---|---|---|---|
| `<填寫>` | package-dc／package-zone | 每廠 pilot／首廠 pilot | 3 |

---

## 5. 上線流程

### 5.1 步驟 ✅

| 步驟 | 做什麼 | 通過條件 |
|---|---|---|
| 1. 前置條件 | 完成 PR、完成 PRR | 見下表 |
| 2. Pilot run（UAT／staging） | 用 Beta 版在一個目標上線試跑，例如 f14p1、f14a | 見第 6 章 |
| 3. Fanout | 分天放到該廠所有 phase（dc）或所有 zone | 自己的 pilot 通過；見 5.5 |

**進入 release 前，兩關都要過。**

| 關卡 | 內容 | 誰把關 | 狀態 |
|---|---|---|---|
| PR 完成 | 程式碼審查通過 | Tech lead | ✅ |
| PRR 完成 | 上線準備審查通過 | RM | ✅ |
| PRR 檢查項目 | 沿用 Package Baseline 四個維度：Test、Deployment Safety、Monitoring、Change Automation | RM | 💡 |

**各出版類型的 PR／PRR：每一種都要 PRR，差別只在深度。** 💡

| 類型 | PR | PRR | 狀態 |
|---|---|---|---|
| Formal | 要 | 完整版 | ✅ |
| Scheduled Patch | 要 | 完整版，但只審這次改的部分 | 💡 |
| Hotfix | 要；可以加速，品質要求不降 | 快速版（見下表），RM 在 triage 時一起確認 | PR ✅、PRR 💡 |
| Beta | 要 | 要；Beta 進 pilot 前做的 PRR，就是這個版本的 PRR | 要 ✅、合併 💡 |

**Hotfix 快速版 PRR** 💡

| 檢查 | 要回答的問題 |
|---|---|
| 範圍小 | 只修這個問題，沒有夾帶其他修改？ |
| 能退回 | 退回方法確認過了嗎？ |
| 看得到 | 上線後看哪些指標，確認真的修好？ |
| 有測試 | 修正本身有測試；受影響的舊功能有回歸測試（確認舊功能沒被弄壞）？ |

### 5.2 兩種路線

**每個 package 選一種路線當預設。單一版本要改走另一種，就是 special route。**

| 項目 | 每廠 pilot | 首廠 pilot |
|---|---|---|
| 做法 | 每個 fab 都先 pilot 再 fanout ✅ | 只有第一個 fab pilot，其他 fab 直接 fanout ✅ |
| 可以當預設 | 可以 ✅ | 可以 ✅ |
| Child 開始條件 | Parent 第一個 pilot 驗證完成 ✅ | Parent fanout 完成的下一週 ✅ |
| Child fanout 條件 | 自己的 pilot 通過 ✅ | 開始就 fanout ✅ |
| 特點 | 慢，每廠都驗證過 | 快，只驗證一次 |

| 規則 | 內容 | 狀態 |
|---|---|---|
| 預設路線 | 每個 package 在 4.3 選一種 | ✅ |
| 每廠 → 首廠 | 單一版本要少做 pilot，要和 user 協議 | ✅ |
| 首廠 → 每廠 | 單一版本要多做 pilot，RM 可以直接決定（比較保守，不需協議） | 💡 |
| 記錄 | Special route 寫明同意人、日期、理由 | 💡 |

「下一週」：parent 在第 N 週完成 fanout，child 最早第 N+1 週開始。💡

### 5.3 Fab 依賴 ✅

- 所有 fab 都放完，這個版本才算完成。
- 沒有依賴的 fab 可以平行跑。
- 有依賴的 fab，照 5.2 的開始條件。
- Rollout 不用趕在下一班車前完成。

### 5.4 Parent／Child 對照 🔧

> 以下是模擬，等真實資料再改。

| 組 | Parent | Child |
|---|---|---|
| 1 | FAB12 | FAB14 |
| 2 | FAB14 | FAB18 |
| 3 | FAB15 | FAB22 |
| 4 | FAB15 | FAB23 |

模擬時用的假設 💡：

| 假設 | 內容 |
|---|---|
| 首廠 pilot 的其他根廠 | 沒有 parent 的廠（例如 FAB15），也等首廠 fanout 完的下一週才開始 |

### 5.5 Progressive rollout ✅

**同一廠的目標分幾天放。一天放一批，不在同一天全部放。**

| 規則 | 內容 | 狀態 |
|---|---|---|
| dc 分天放 | 一個 fab 的所有 dc 目標，不在同一天部署 | ✅ |
| 例子 | Day 1 P12 → Day 2 P34 → Day 3 P456 | ✅ |
| zone 也分天 | 例如 Day 1 14A → Day 2 14B | 💡 |
| 可以拆開 DC | 一批可以只放 DC 裡的部分 phase，例如 P12 | ✅ |
| 誰決定每批 | PO ＋ RM | ✅ |
| 記錄 | 每天放哪一批，寫在 Release Plan | 💡 |

### 5.6 禁止變更日 ✅

**週五和放假前一天，不能做 change。**

| 規則 | 內容 | 狀態 |
|---|---|---|
| 禁止日 | 週五、放假前一天 | ✅ |
| 可部署日 | 週一到週四，但遇到放假前一天也不行 | ✅ |
| 緊急例外 | Hotfix 或退版遇到禁止日，能不能做 | ⏳ |

---

## 6. Pilot（UAT）驗收 ✅

**Pilot 就是 UAT。兩個條件都滿足，PO 和 user 都簽核，才算通過。**

| 項目 | 內容 |
|---|---|
| 觀察期 | 一般 2 週，可以更長或更短 |
| 條件 1 | 沒有 blocking issue（包括 incident），由 RM triage |
| 條件 2 | 開始前和 user 談定的 acceptance criteria 全部滿足 |
| 簽核 | PO ＋ user |
| 前置 | Acceptance criteria 在 pilot 開始前寫好，並經 user 確認 |

---

## 7. 多版本並存與跳版

### 7.1 版本上限

**線上同一個 package 最多 3 個版本，正在 pilot 的也算。**

| 規則 | 內容 | 狀態 |
|---|---|---|
| 預設上限 | 3 個版本，含正在 pilot 的 Beta 版 | ✅ |
| 是預設值 | 上限可以調整 | ✅ |
| 按 package 調整 | 每個 package 可以設自己的上限 | 💡 |
| 達上限時 | 新版不能開始 pilot，要等最舊版本從線上消失 | 💡 |
| 清掉最舊版 | RM 可以讓還在最舊版的 fab 跳版 | 💡 |

### 7.2 跳版

| 規則 | 內容 | 狀態 |
|---|---|---|
| 可以選 | 跳版是一種可選的升級路徑 | ✅ |
| 盡量不跳 | 預設依序升級 | ✅ |
| 舊版未到、新版已來 | 裝新版 | ✅ |
| 誰決定 | RM | ✅ |
| 前提 1 | 新版包含舊版所有修改 | 💡 |
| 前提 2 | 資料庫或設定的變更，可以一次跳兩版 | 💡 |
| 退版目標 | 退回該 fab 原本的版本，不是中間版本 | 💡 |

---

## 8. 退版 ⏳

**已定的只有「退回舊版」。細節待決，但不擋其他章節。**

| 項目 | 狀態 |
|---|---|
| 出問題時退回舊版 | ✅ |
| 退版方式（重新部署、GitOps 切回或其他） | ⏳ |
| 多久要退完 | ⏳ |
| 誰下決定 | ⏳ |
| 資料相容：新版的資料庫變更，舊版還能不能讀 | ⏳ |

會受影響的章節：6（pilot）、7.1（版本上限）、7.2（跳版）。

---

## 9. 待決與待填

| # | 項目 | 類型 |
|---|---|---|
| 1 | Parent／Child 真實對照（5.4） | 🔧 |
| 2 | 退版規則（第 8 章） | ⏳ |
| 3 | Hotfix 要補到線上哪幾個版本 | ⏳ |
| 4 | PRR 檢查清單（5.1） | 🔧 |
| 5 | 產品歸屬（4.3） | 🔧 |
| 6 | FAB12、FAB22、FAB23 的 zone 目標（4.1） | 🔧 |
| 7 | 緊急 Hotfix 或退版，遇到禁止變更日能不能做（5.6） | ⏳ |
| 8 | 所有 💡 項目逐一確認 | 💡 |

---

## 附錄：Release Plan 必填欄位

**每次出版，照這張表填一份 Release Plan。**

| 欄位 | 說明 |
|---|---|
| Package 與版號 | 例如 `package-zone/2026.11.0` |
| 前置條件 | PR、PRR 完成紀錄與把關人 |
| 出版類型 | Formal／Scheduled Patch／Hotfix／Beta |
| 路線 | 每廠 pilot／首廠 pilot；走 special route 時附 user 同意紀錄 |
| 部署順序 | 每廠 pilot 目標、fanout 目標、parent／child 開始條件 |
| Acceptance criteria | Pilot 前和 user 談定 |
| 每廠升級路徑 | 依序／跳版（跳版附 RM 決定與理由） |
| 每廠退版目標 | 出事時退回哪一版 |
| 相容版本 | zone 版本需要的 dc 最低版本 |
| 時程 | 每廠 pilot 開始、預計 sign off、每天 fanout 哪一批；避開禁止變更日 |
| 負責人 | PO（只寫一位）、RM |
