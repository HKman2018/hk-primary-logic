# 香港小學邏輯訓練網站 · 靜態 MVP

小四至小六 · 五類：找規律／數列、分類／歸類、條件推理、圖形／空間、真假／矛盾。  
純前端、繁體中文 UI、**唔使登入／後端**。

線上即玩：**https://hkman2018.github.io/hk-primary-logic/**

GitHub Pages 由公開 repo 嘅 `main` 分支根目錄（`/`）發佈。第一次推上或者更新後，頁面可能要等一兩分鐘先更新。

---

## 需要咩

- 電腦有現代瀏覽器（Chrome／Edge／Safari／Firefox）
- （本機試玩先要）已安裝 [Python 3](https://www.python.org/)——用嚟開本機靜態伺服器  
  或者用 VS Code／Cursor 嘅 Live Server 都得

唔使 `npm install`、唔使資料庫。呢個係公開 repo，clone 唔使 Personal Access Token。

---

## 安裝（取得檔案）

```bash
git clone https://github.com/HKman2018/hk-primary-logic.git
cd hk-primary-logic
```

檔案喺 **repo 根目錄**（有 `index.html`），唔使再入子目錄。

目錄內應見到：`index.html`、`css/`、`js/`。

---

## 執行

### 線上

直接開：**https://hkman2018.github.io/hk-primary-logic/**

### 本機

喺專案根目錄（有 `index.html` 嗰層）開本機伺服器：

```bash
python3 -m http.server 8765
```

然後用瀏覽器開：

**http://127.0.0.1:8765/**

停伺服器：喺終端機按 `Ctrl+C`。

### 其他開法

| 方法 | 做法 |
|------|------|
| 另一埠 | `python3 -m http.server 8080` → 開 `http://127.0.0.1:8080/` |
| 直接雙擊 `index.html` | 多數情況可用；若瀏覽器擋本地腳本，改用上面 `http.server` |
| npx（有 Node 時） | `npx --yes serve -p 8765` |

---

## 點玩

1. 開首頁，揀題型（五類之一）。
2. 當日每類會出 **5 題**（同日再開會見到同一組，方便複習）。
3. 揀答案 → 睇啱／錯同提示。
4. 進度存在瀏覽器 `localStorage`（換瀏覽器或清網站資料＝當新用戶）。

首頁分隔線下面有獨立嘅「其他練習」：**看圖學英文單字**。呢個唔係第六類邏輯，亦唔用每日題池。睇圖打英文，前後空白同大小寫唔計，錯咗會顯示正確單字。字庫 v2 有 222 條；每輪隨機抽 10 題。具體圖（牛奶、蜜蜂等）只靠圖；抽象、多義，或者圖載入唔到嗰陣，輸入上面會顯示「意思：」加該詞繁中。答案仍然只接受英文，交中文唔算啱。

---

## 每日唔重複（硬約束）

- 用 **香港時區（HKT）日期**做種子：同日穩定、換日換題。
- 用內容指紋（`contentKey`）記錄已出過嘅題，**禁止跨日重用同一內容**湊滿 5 題。
- 池不夠時當日可以少過 5 題，都唔會用舊題充數。

---

## 專案結構

```
.
├── index.html          # 繁中 UI
├── css/styles.css
├── js/questions.js     # 靜態樣本（後備）
├── js/generators.js    # 日期種子＋參數化出題＋每日組卷（v4-rich-pool）
├── js/app.js           # 邏輯答題流程、localStorage
├── js/vocab-data.js    # 看圖學英文單字表（獨立，222 條）
├── js/vocab.js         # 看圖學英文流程
├── assets/vocab/       # 本地 SVG 插圖、字表、產生腳本
├── docs/題型大綱.md
├── .gitignore          # 擋住 .env、金鑰、憑證同本機雜檔
└── README.md
```

---

## 自測摘要（2026-10-16）

- 五題型：`pattern` / `classify` / `condition` / `spatial` / `truth`
- 生成器種子標籤：`v4-rich-pool`（題目靠規律族同情境參數加深，唔靠選項次序充數，亦無隨機 `-x` id）
- 靜態樣本（`js/questions.js`）每類 7 題
- 由 2026-10-15 起連續 90 日：每日每類 5 題、零 contentKey 重用（每類 450 個唔同內容）
- 無登入、無後端

---

## 已知限制

- 圖形／空間題目前偏文字描述。
- 進度只喺本機瀏覽器；唔會同步到其他裝置。
- 看圖學英文每輪由 222 條本地字表隨機抽 10 題，唔跟邏輯題「每日唔重複」。開始頁顯示嘅「共 10 題」係呢一輪嘅題數。
- 每條只接受字表嗰一個英文（去掉前後空白再轉小寫）。冇同義字、縮寫、發音，亦唔可以重試同一題。答錯會顯示正確英文。
- 同一個英文可以有兩張圖（唔同中文意思，例如兩個 clear）。兩張都要打同一個英文。
- 字數係 222 而唔係片題講嘅 240：清理後核實到嘅係 222 條，冇湊數。
- 星期、月份卡用繁中標籤加圖示，圖入面唔印英文答案。抽象詞（動詞、形容詞）靠比喻圖，有時唔係實物名（例如 book 係預訂印，climb 係上升圖）。停車牌有字母 P，答案係 `park`。
- 圖片係原創扁平 SVG（CC0），可以 `python3 assets/vocab/generate_images.py` 重新畫。唔係影片截圖。載入失敗可以跳過。
