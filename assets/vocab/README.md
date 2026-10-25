# 看圖學英文 · 圖片（v2.1）

222 張扁平插圖，原創，以 [CC0](https://creativecommons.org/publicdomain/zero/1.0/) 放出，並符合圖資規格 v2.1。  
檔名係 `w001.svg`–`w222.svg`，對應 `assets/vocab/wordlist-v2.json` 嘅 `id`（同 `js/vocab-data.js` 嘅相對路徑）。  
每張對準該列 `english`＋`zh`；21 組多義詞各有兩張唔同構圖。畫布 `viewBox="0 0 640 480"`，靜態、無動畫、無外連字型檔。

玩網站唔使裝任何嘢，圖由 `js/vocab-data.js` 用相對路徑載入。

呢批圖唔係第三方圖庫，亦唔係 YouTube 或課堂影片嘅畫面、截圖、裁切、描摹。

## 重新產生

```bash
python3 assets/vocab/generate_images.py
```

腳本會跟 `scenes_v2.py` 重畫全部 SVG，並覆寫 `js/vocab-data.js`。  
網站本身唔依賴呢個腳本。

## 點樣對題

- 玩法答案係英文 lemma（`trim` + 小寫）。圖入面唔會印出該英文詞。
- 同一英文、唔同中文（例如兩個 `clear`）係兩條、兩張唔同嘅圖，跟 `image_hint`。
- 星期同月份卡加咗繁中標籤（星期一、一月…）同時有圖示，等日子可以分得清，又唔會直接寫出英文。
- 停車牌用國際符號字母 P；接受嘅答案係 `park`。
- 字母積木（A、B、C）用嚟表示 basic / spell，答案唔係字母本身，亦唔會拼出目標詞。
- `free`（免費的）標價用 `0` 同繁中「免費」；`fine`（夠好的）用繁中「還可以」。兩處都唔寫英文答案。
- 題面繁中提示唔畫入 SVG。`js/vocab-data.js` 嘅 `zhCue` 先決定答題殼係咪顯示「意思：{zh}」。圖載入失敗時，無論 `zhCue`，題面都會改為以繁中做主提示。

## 舊版

第一版 24 張 WebP（apple 等）收喺 `archive/v1/`，網站已經唔再引用。
