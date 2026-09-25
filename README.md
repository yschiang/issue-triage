# Issue Triage 與交付流程

拿到 Issue 時怎麼判斷：Severity／Priority 定級、止血、選 Hotfix／Scheduled Patch／Formal Release、誰決定、版號怎麼給。

## 直接打開

| 檔案 | 給誰 |
|---|---|
| [`index.html`](index.html) | 團隊成員：操作指南 |
| [`executive-summary.html`](executive-summary.html) | 管理層：一頁摘要 |
| [`triage-wizard.html`](triage-wizard.html) | 處理 Issue 的人：點五題，得到路徑和可貼 Ticket 的紀錄 |

三個檔案都是單一 HTML，瀏覽器直接開。開 GitHub Pages（Settings → Pages → 根目錄）就能用網址分享。

## Claude skill

`skills/issue-triage/` 是 Claude skill（給 Claude 讀的使用說明）。安裝：

```bash
python3 scripts/build_skill.py      # 產生 dist/issue-triage-v<版本>.skill
```

把 `.skill` 上傳到 Claude 的 Skills 設定。之後問「這個 issue 怎麼處理」，Claude 會直接開 wizard。

## 改版

1. 改根目錄的 HTML。`index.html` 是內容的唯一來源；規則有變，`triage-wizard.html` 一起改。先看 `skills/issue-triage/references/editing-rules.md`。
2. `python3 scripts/bump_version.py 1.13 "一句話說明"` —— 三個 HTML、SKILL.md、VERSION、CHANGELOG 一起升版。
3. `python3 scripts/build_skill.py` —— 重生 `sop.md` 和 `.skill`（需要 pandoc）。
4. `git commit` → `git tag v1.13` → `git push --tags`。

## 結構

```
index.html  executive-summary.html  triage-wizard.html   ← 內容，改這裡
CHANGELOG.md  VERSION
scripts/        bump_version.py  html_to_md.py  build_skill.py
skills/issue-triage/
  SKILL.md
  references/   sop.md（自動產生）  editing-rules.md
  assets/       （build 時從根目錄複製，不進 git）
```
