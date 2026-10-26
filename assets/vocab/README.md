# 看圖學英文 · 詞庫同舊圖

練習詞庫係 Google Translate 繁體中文（zh-TW）去重後嘅 **201** 條。每個英文只得一條，題面用該條 `zh`。

來源：

- `wordlist-gt-201.csv`（欄：`id`, `english`, `zh`）
- `wordlist-gt-201.json`

重新產生 `js/vocab-data.js`：

```bash
python3 assets/vocab/generate_vocab_data.py
```

產生出嚟嘅每條只有 `id`、`answer`（英文）、`zh`（繁中）。網站唔讀圖片路徑，亦冇 `zhCue`。玩法係睇「意思：{zh}」，打英文（去掉前後空白再轉小寫）。

## 舊插圖（答題唔用）

`images/` 仍然有 222 張扁平插圖，原創，以 [CC0](https://creativecommons.org/publicdomain/zero/1.0/) 放出，檔名 `w001.svg`–`w222.svg`，對應 `wordlist-v2.json`。呢批圖對住舊字表，同而家嘅 201 條詞庫唔一定同義，練習流程唔會載入。

要重畫舊圖（唔會改詞庫）：

```bash
python3 assets/vocab/generate_images.py
```

網站本身唔依賴呢個腳本。畫布 `viewBox="0 0 640 480"`，靜態、無動畫、無外連字型檔。呢批圖唔係第三方圖庫，亦唔係 YouTube 或課堂影片嘅畫面、截圖、裁切、描摹。

## 舊版

第一版 24 張 WebP（apple 等）收喺 `archive/v1/`，網站已經唔再引用。
