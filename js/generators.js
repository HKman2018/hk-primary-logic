/** 參數化出題（靜態站、無需後端）。以日期種子保證同日穩定、跨日唔同。 */
(function (global) {
  function mulberry32(a) {
    return function () {
      let t = (a += 0x6d2b79f5);
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t = t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function hashStr(s) {
    let h = 2166136261;
    for (let i = 0; i < s.length; i++) {
      h ^= s.charCodeAt(i);
      h = Math.imul(h, 16777619);
    }
    return h >>> 0;
  }

  /** 內容指紋：同一題幹＋答案 = 同一 id，唔靠隨機尾。 */
  function normalizeContent(prompt, answer) {
    return String(prompt || "")
      .replace(/\s+/g, " ")
      .trim()
      .toLowerCase() + "||" + String(answer || "").replace(/\s+/g, "").trim().toLowerCase();
  }

  function contentKey(prompt, answer) {
    return "ck-" + hashStr(normalizeContent(prompt, answer)).toString(16);
  }

  function fingerprintId(catId, level, prompt, answer) {
    return `gen-${catId}-${level}-${hashStr(normalizeContent(prompt, answer)).toString(16)}`;
  }

  function stamp(catId, q) {
    const id = fingerprintId(catId, q.level, q.prompt, q.answer);
    const ck = contentKey(q.prompt, q.answer);
    return Object.assign({}, q, { id, contentKey: ck });
  }


  function pick(rng, arr) {
    return arr[Math.floor(rng() * arr.length)];
  }

  function shuffle(rng, arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(rng() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  /** HKT YYYY-MM-DD */
  function hktDateString(d) {
    const fmt = new Intl.DateTimeFormat("en-CA", {
      timeZone: "Asia/Hong_Kong",
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    });
    return fmt.format(d || new Date());
  }

  function genPattern(rng, level) {
    const modes =
      level === "P4"
        ? ["add", "repeat2"]
        : level === "P5"
          ? ["add", "addGrow", "alt"]
          : ["addGrow", "mulAdd", "alt"];
    const mode = pick(rng, modes);
    let seq = [];
    let answer;
    let hint;
    let prompt;

    if (mode === "add") {
      const start = 1 + Math.floor(rng() * 20);
      const step = 1 + Math.floor(rng() * 9);
      seq = [start, start + step, start + 2 * step, start + 3 * step, start + 4 * step];
      answer = String(start + 5 * step);
      hint = `每次加 ${step}。`;
      prompt = `數列：${seq.join("、")}、？\n下一個數係幾多？`;
    } else if (mode === "addGrow") {
      const start = 1 + Math.floor(rng() * 12);
      let n = start;
      seq = [n];
      const diffs = [];
      for (let i = 0; i < 4; i++) {
        const d = i + 1 + Math.floor(rng() * (level === "P6" ? 4 : 2));
        diffs.push(d);
        n += d;
        seq.push(n);
      }
      const nextDiff = diffs[diffs.length - 1] + 1;
      answer = String(n + nextDiff);
      hint = `相差依次係 ${diffs.join("、")}，下一差距再大 1。`;
      prompt = `數列：${seq.join("、")}、？\n下一個數係幾多？`;
    } else if (mode === "repeat2") {
      const a = pick(rng, ["○", "△", "□", "☆"]);
      const b = pick(rng, ["○", "△", "□", "☆"].filter((x) => x !== a));
      seq = [a, b, a, b, a];
      answer = b;
      hint = `${a} 同 ${b} 交替。`;
      prompt = `圖案規律：${seq.join(" ")} ？\n下一個應該係邊個？`;
    } else if (mode === "alt") {
      let n = 2 + Math.floor(rng() * 4);
      seq = [n];
      for (let i = 0; i < 3; i++) {
        n = n * 2;
        seq.push(n);
        n = n - 1;
        seq.push(n);
      }
      // last op was -1; next is *2
      answer = String(n * 2);
      hint = "×2 再 −1，交替進行。";
      prompt = `數列：${seq.slice(0, 5).join("、")}、？\n下一個數係幾多？`;
      // Fix: rebuild clean 5-term then ask 6th
      n = 2 + Math.floor(rng() * 3);
      seq = [n];
      let opMul = true;
      while (seq.length < 5) {
        if (opMul) n = n * 2;
        else n = n - 1;
        seq.push(n);
        opMul = !opMul;
      }
      answer = String(opMul ? n * 2 : n - 1);
      hint = "×2 再 −1，交替進行。";
      prompt = `數列：${seq.join("、")}、？\n下一個數係幾多？`;
    } else {
      // mulAdd
      const start = 1 + Math.floor(rng() * 6);
      const add = 1 + Math.floor(rng() * 5);
      seq = [start];
      let n = start;
      for (let i = 0; i < 4; i++) {
        n = n * 2 + add;
        seq.push(n);
      }
      answer = String(n * 2 + add);
      hint = `每次：×2 再 +${add}。`;
      prompt = `數列：${seq.join("、")}、？\n下一個數係幾多？`;
    }

    const choices =
      mode === "repeat2"
        ? shuffle(rng, [answer, ...shuffle(rng, ["○", "△", "□", "☆"]).filter((x) => x !== answer).slice(0, 3)])
        : null;

    return stamp("pattern", {
      level,
      prompt,
      type: choices ? "choice" : "fill",
      choices: choices || undefined,
      answer: String(answer),
      hint,
      generated: true,
    });
  }

  function genClassify(rng, level) {
    const sets = [
      { items: ["蘋果", "香蕉", "橙", "汽車", "葡萄", "梨"], odd: "汽車", hint: "其餘都係水果。" },
      { items: ["貓", "狗", "兔", "椅", "倉鼠", "鳥"], odd: "椅", hint: "其餘都係動物。" },
      { items: ["圓", "球", "環", "正方形", "橢圓", "盤"], odd: "正方形", hint: "其餘同「圓」有關。" },
      { items: ["書", "報紙", "雜誌", "汽水", "筆記簿", "課本"], odd: "汽水", hint: "其餘都係讀物／紙本。" },
      { items: ["鉛筆", "原子筆", "尺", "足球", "擦膠", "間尺"], odd: "足球", hint: "其餘都係文具。" },
      { items: ["巴士", "的士", "火車", "飛機", "單車", "雪櫃"], odd: "雪櫃", hint: "其餘都係交通工具。" },
      { items: ["恤衫", "褲", "襪", "書包", "外套", "裙"], odd: "書包", hint: "其餘都係衫褲。" },
      { items: ["星期一", "星期二", "星期三", "一月", "星期四", "星期五"], odd: "一月", hint: "其餘都係星期。" },
      { items: ["牛奶", "果汁", "清水", "麵包", "豆漿", "茶"], odd: "麵包", hint: "其餘都係飲料。" },
      { items: ["鋼琴", "結他", "鼓", "電視", "小提琴", "長笛"], odd: "電視", hint: "其餘都係樂器。" },
      { items: ["醫生", "護士", "消防員", "學生", "警察", "教師"], odd: "學生", hint: "其餘都係工作／職業。" },
      { items: ["春", "夏", "秋", "冬", "朝早", "四季"], odd: "朝早", hint: "其餘同季節有關。" },
    ];
    const pack = pick(rng, sets);
    const four = shuffle(rng, pack.items).slice(0, 4);
    if (!four.includes(pack.odd)) {
      four[3] = pack.odd;
    }
    const shown = shuffle(rng, four);
    return stamp("classify", {
      level,
      prompt: `邊個唔屬於同一類？\n${shown.join("、")}`,
      type: "choice",
      choices: shown,
      answer: pack.odd,
      hint: pack.hint,
      generated: true,
    });
  }

  function genCondition(rng, level) {
    const names = shuffle(rng, ["阿明", "小華", "阿美", "阿強", "小美", "阿傑", "小文", "阿珍", "小龍", "阿欣", "小希", "阿樂"]);
    const a = names[0];
    const b = names[1];
    const c = names[2];
    const items = pick(rng, ["書包", "水壺", "學生證", "雨傘", "手套", "筆記簿"]);
    const colors = pick(rng, ["藍色", "紅色", "綠色", "黃色", "紫色"]);
    const days = pick(rng, ["星期一", "星期三", "星期五", "星期六"]);
    const sport = pick(rng, ["足球", "籃球", "游泳", "跑步", "乒乓球"]);
    const pair = pick(rng, [
      ["下雨", "帶傘"],
      ["考試合格", "去旅行"],
      ["完成功課", "睇電視"],
      ["帶水", "去遠足"],
      ["晴天", "去野餐"],
    ]);
    const templates =
      level === "P4"
        ? [
            {
              prompt: `如果今日${pair[0]}，${a}就${pair[1]}。\n今日${pair[0]}。可以得出邊個結論？`,
              choices: [`${a}${pair[1]}`, `${a}唔${pair[1]}`, "唔夠資料"],
              answer: `${a}${pair[1]}`,
              hint: "條件成立，結果就成立。",
            },
            {
              prompt: `班上所有同學都有${items}。${b}係班上同學。\n可以得出？`,
              choices: [`${b}有${items}`, `${b}冇${items}`, "唔夠資料"],
              answer: `${b}有${items}`,
              hint: "「全部」包括呢位同學。",
            },
            {
              prompt: `如果今日係${days}，學校就有體育堂。\n今日係${days}。可以得出？`,
              choices: ["今日有體育堂", "今日冇體育堂", "唔夠資料"],
              answer: "今日有體育堂",
              hint: "條件啱，結果跟住啱。",
            },
            {
              prompt: `盒入面全部係${colors}筆。${b}由盒攞出一支筆。\n可以得出？`,
              choices: [`呢支筆係${colors}`, `呢支筆唔係${colors}`, "唔夠資料"],
              answer: `呢支筆係${colors}`,
              hint: "「全部」包括攞出嚟嗰支。",
            },
            {
              prompt: `隊入面每個隊員都着${colors}衫。${a}係隊員。\n可以得出？`,
              choices: [`${a}着${colors}衫`, `${a}着其他色`, "唔夠資料"],
              answer: `${a}着${colors}衫`,
              hint: "「每個」包括呢位隊員。",
            },
            {
              prompt: `如果${pair[0]}，${b}就${pair[1]}。\n${b}已經遇到「${pair[0]}」呢個條件。可以得出？`,
              choices: [`${b}${pair[1]}`, `${b}唔${pair[1]}`, "唔夠資料"],
              answer: `${b}${pair[1]}`,
              hint: "條件成立就有結果。",
            },
            {
              prompt: `呢盒糖全部係薄荷味。${a}食咗一粒盒入面嘅糖。\n可以得出？`,
              choices: ["嗰粒係薄荷味", "嗰粒唔係薄荷味", "唔夠資料"],
              answer: "嗰粒係薄荷味",
              hint: "「全部」包括食咗嗰粒。",
            },
            {
              prompt: `園裏面所有花都開咗。呢朵係園裏嘅花。\n可以得出？`,
              choices: ["呢朵開咗", "呢朵未開", "唔夠資料"],
              answer: "呢朵開咗",
              hint: "「所有」包括呢朵。",
            },
            {
              prompt: `如果鈴響，${c}就返課室。\n鈴響咗。可以得出？`,
              choices: [`${c}返課室`, `${c}唔返課室`, "唔夠資料"],
              answer: `${c}返課室`,
              hint: "條件成立 → 結果成立。",
            },
            {
              prompt: `盒入面全部係${colors}波。${a}攞出一粒。\n可以得出？`,
              choices: [`嗰粒係${colors}`, `嗰粒唔係${colors}`, "唔夠資料"],
              answer: `嗰粒係${colors}`,
              hint: "全部同色。",
            },
          ]
        : level === "P5"
          ? [
              {
                prompt: `有啲水果係${colors}。蘋果係水果。\n可以肯定蘋果係${colors}嗎？`,
                choices: [`可以肯定係${colors}`, "唔可以肯定", `肯定唔係${colors}`],
                answer: "唔可以肯定",
                hint: "「有啲」唔等於「全部」。",
              },
              {
                prompt: `條件：① ${a}比${b}高 ② ${b}比${c}高\n邊句一定啱？`,
                choices: [`${a}最高`, `${c}最高`, `${b}最矮`, "唔夠資料"],
                answer: `${a}最高`,
                hint: `由①②可得 ${a} > ${b} > ${c}。`,
              },
              {
                prompt: `有啲同學鍾意${sport}。${b}係同學。\n可以肯定${b}鍾意${sport}嗎？`,
                choices: ["可以肯定", "唔可以肯定", "肯定唔鍾意"],
                answer: "唔可以肯定",
                hint: "「有啲」唔代表每一位。",
              },
              {
                prompt: `條件：① ${a}比${b}跑得快 ② ${c}比${a}跑得快\n邊句一定啱？`,
                choices: [`${c}最快`, `${b}最快`, `${a}最慢`, "唔夠資料"],
                answer: `${c}最快`,
                hint: `${c} > ${a} > ${b}。`,
              },
              {
                prompt: `如果唔帶水，就唔可以去遠足。\n${a}去咗遠足。可以得出？`,
                choices: [`${a}有帶水`, `${a}冇帶水`, "唔夠資料"],
                answer: `${a}有帶水`,
                hint: "去到遠足 ⇒ 一定有帶水。",
              },
              {
                prompt: `條件：① 所有熊貓都食竹 ② 豆豆係熊貓\n可以得出？`,
                choices: ["豆豆食竹", "豆豆唔食竹", "唔夠資料"],
                answer: "豆豆食竹",
                hint: "全部＋係其中一個 ⇒ 跟住啱。",
              },
              {
                prompt: `有啲正方形係${colors}。呢個形係正方形。\n可以肯定佢係${colors}嗎？`,
                choices: ["可以肯定", "唔可以肯定", `肯定唔係${colors}`],
                answer: "唔可以肯定",
                hint: "「有啲」唔等於每個正方形都係。",
              },
              {
                prompt: `條件：① ${a}分數高過${b} ② ${b}分數高過${c}\n邊句一定啱？`,
                choices: [`${a}最高分`, `${c}最高分`, `${b}最低分`, "唔夠資料"],
                answer: `${a}最高分`,
                hint: `${a} > ${b} > ${c}。`,
              },
              {
                prompt: `有啲${items}係新嘅。呢個係${items}。\n可以肯定佢係新嘅嗎？`,
                choices: ["可以肯定", "唔可以肯定", "肯定係舊"],
                answer: "唔可以肯定",
                hint: "「有啲」唔等於全部。",
              },
              {
                prompt: `條件：① ${a}早過${b}返到 ② ${b}早過${c}返到\n邊句一定啱？`,
                choices: [`${a}最早`, `${c}最早`, `${b}最遲`, "唔夠資料"],
                answer: `${a}最早`,
                hint: `${a} 早過 ${b} 早過 ${c}。`,
              },
            ]
          : [
              {
                prompt: `只有完成功課，先可以打機。\n${a}而家打緊機。可以得出？`,
                choices: [`${a}已完成功課`, `${a}未完成功課`, "唔夠資料"],
                answer: `${a}已完成功課`,
                hint: "「只有…才…」＝必要條件。",
              },
              {
                prompt: `除非帶齊${items}，否則唔准入場。\n${b}已經入場。可以得出？`,
                choices: [`${b}有帶${items}`, `${b}冇帶${items}`, "唔夠資料"],
                answer: `${b}有帶${items}`,
                hint: "入場 ⇒ 一定帶咗。",
              },
              {
                prompt: `只有晴天先會去野餐。\n今日去咗野餐。可以得出？`,
                choices: ["今日係晴天", "今日一定落雨", "唔夠資料"],
                answer: "今日係晴天",
                hint: "去野餐 ⇒ 必要條件成立。",
              },
              {
                prompt: `如果唔係會員，就唔可以借書。\n${a}借到書。可以得出？`,
                choices: [`${a}係會員`, `${a}唔係會員`, "唔夠資料"],
                answer: `${a}係會員`,
                hint: "借到書 ⇒ 唔可能「唔係會員」。",
              },
              {
                prompt: `只有答啱密語，門先會開。\n門開咗。可以得出？`,
                choices: ["有人答啱密語", "一定冇人答", "唔夠資料"],
                answer: "有人答啱密語",
                hint: "門開 ⇒ 必要條件已滿足。",
              },
              {
                prompt: `唔係週末就唔會去遊樂場。\n${c}去咗遊樂場。可以得出？`,
                choices: ["今日係週末", "今日唔係週末", "唔夠資料"],
                answer: "今日係週末",
                hint: "去咗 ⇒ 唔可能「唔係週末」。",
              },
              {
                prompt: `只有帶${items}先准考試。\n${a}正在考試。可以得出？`,
                choices: [`${a}有帶${items}`, `${a}冇帶${items}`, "唔夠資料"],
                answer: `${a}有帶${items}`,
                hint: "考試中 ⇒ 必要條件已滿足。",
              },
              {
                prompt: `除非完成練習，否則唔准打機。\n${b}打緊機。可以得出？`,
                choices: [`${b}已完成練習`, `${b}未完成練習`, "唔夠資料"],
                answer: `${b}已完成練習`,
                hint: "打機 ⇒ 已完成練習。",
              },
            ];
    const t = pick(rng, templates);
    return stamp("condition", { level, type: "choice", generated: true, ...t });
  }

  function genSpatial(rng, level) {
    const places = ["學校", "公園", "圖書館", "超市", "碼頭", "山頂", "球場", "車站", "博物館", "泳棚", "郵局", "戲院", "醫院", "市場", "社區中心", "游泳池", "禮堂", "科學館", "火車站", "體育館", "書局", "餐廳"];
    const letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"];
    const symLetters = new Set(["A", "H", "I", "M", "O", "T", "U", "V", "W", "X", "Y"]);
    const shapes3 = ["正方形", "圓形", "等邊三角形", "長方形", "菱形"];
    const fromTo = [
      ["教室", "操場"], ["家", "學校"], ["圖書館", "禮堂"], ["車站", "球場"],
      ["超市", "公園"], ["碼頭", "山頂"], ["醫院", "書局"], ["科學館", "游泳池"],
    ];

    const builders = {
      P4: [
        () => {
          const L = pick(rng, letters);
          const sym = symLetters.has(L);
          return {
            prompt: `字母「${L}」左右對稱嗎？`,
            choices: ["係", "唔係", "睇字體先至知"],
            answer: sym ? "係" : "唔係",
            hint: sym ? "左右對摺大致可以重合。" : "左右對摺唔會重合。",
          };
        },
        () => {
          const shape = pick(rng, shapes3);
          const deg = pick(rng, [90, 180, 270, 120, 60]);
          // regular polygons / circle keep outline under these turns for kids' level
          const answer = "外形不變";
          return {
            prompt: `${shape}順時針轉 ${deg}°，外形會唔會變？（只問外形／種類）`,
            choices: ["會變成完全唔同嘅形", "外形不變", "一定變成長方形"],
            answer,
            hint: "題目問外形種類，呢啲形轉完仍然係同一種形。",
          };
        },
        () => {
          const n = 1 + Math.floor(rng() * 5); // 1..5
          return {
            prompt: `一張長方形紙對摺 ${n} 次（每次對半），最多可以分成幾塊一樣大嘅部分？（理想對摺）`,
            choices: shuffle(rng, [String(n), String(2 ** n), String(n * 2), String(n + 2), String(2 ** (n + 1))]).slice(0, 4),
            answer: String(2 ** n),
            hint: `每對摺一次，塊數 ×2，所以係 2^${n} = ${2 ** n}。`,
          };
        },
        () => {
          const a = pick(rng, places);
          const b = pick(rng, places.filter((p) => p !== a));
          return {
            prompt: `路徑：${a}→${b}。\n由${a}去${b}最少幾段路？`,
            choices: ["1", "2", "3", "4"],
            answer: "1",
            hint: "只有一段。",
          };
        },
        () => {
          const n = 3 + Math.floor(rng() * 4); // 3..6 sides
          const map = { 3: "三角形", 4: "四邊形", 5: "五邊形", 6: "六邊形" };
          return {
            prompt: `一個平面圖形有 ${n} 條邊，佢係邊類？`,
            choices: shuffle(rng, [map[n], "圓形", "只有直線", map[((n % 4) + 3)]]),
            answer: map[n],
            hint: `${n} 條邊 → ${map[n]}。`,
          };
        },
        () => {
          const fold = 1 + Math.floor(rng() * 3);
          return {
            prompt: `正方形紙對摺 ${fold} 次（每次對半），摺痕最多將佢分成幾塊一樣大？`,
            choices: shuffle(rng, [String(fold), String(2 ** fold), String(fold * 3), "8"]),
            answer: String(2 ** fold),
            hint: `對摺 ${fold} 次 → ${2 ** fold} 塊。`,
          };
        },
      ],
      P5: [
        () => {
          const n = 3 + Math.floor(rng() * 4); // 3..6 stops
          const route = shuffle(rng, places).slice(0, n);
          const segs = route.length - 1;
          return {
            prompt: `路徑：${route.join("→")}。\n由${route[0]}去${route[route.length - 1]}沿呢條路，經過幾段？`,
            choices: shuffle(rng, [String(segs), String(segs + 1), String(Math.max(1, segs - 1)), String(segs + 2)]),
            answer: String(segs),
            hint: `有 ${route.length} 個站，段數 = 站數 − 1 = ${segs}。`,
          };
        },
        () => {
          const pair = pick(rng, fromTo);
          const shortN = 2 + Math.floor(rng() * 3);
          const longN = shortN + 1 + Math.floor(rng() * 4);
          return {
            prompt: `由${pair[0]}去${pair[1]}有兩條路：A 路 ${shortN} 段、B 路 ${longN} 段。每段一樣長，想最短揀邊條？`,
            choices: ["A 路", "B 路", "一樣長", "唔夠資料"],
            answer: "A 路",
            hint: `段數少嘅較短：${shortN} < ${longN}。`,
          };
        },
        () => {
          const bars = pick(rng, [3, 4, 5, 6, 8]);
          const map = { 3: "三角形", 4: "正方形或菱形", 5: "五邊形", 6: "六邊形", 8: "八邊形" };
          return {
            prompt: `用 ${bars} 條一樣長嘅棒，最容易圍成邊個形？`,
            choices: shuffle(rng, [map[bars], "圓形", "只可以圍成直線", "唔可以圍成形"]),
            answer: map[bars],
            hint: `${bars} 條等長邊，對應正 ${bars} 邊形一類。`,
          };
        },
        () => {
          const fold = 1 + Math.floor(rng() * 4);
          return {
            prompt: `一個正方形對摺 ${fold} 次（每次對半），摺痕會將佢分成幾塊一樣大？`,
            choices: shuffle(rng, [String(fold), String(2 ** fold), String(fold * 3), String(2 ** (fold + 1))]),
            answer: String(2 ** fold),
            hint: `對摺 ${fold} 次 → ${2 ** fold} 塊。`,
          };
        },
        () => {
          const n = 2 + Math.floor(rng() * 4); // 2..5 identical right triangles
          return {
            prompt: `用 ${n} 個一樣嘅直角三角形，最容易拼成邊個形？（可以拼成長方形／正方形）`,
            choices: ["長方形或正方形", "圓形", "五邊形", "只有不規則形"],
            answer: "長方形或正方形",
            hint: "直角三角形兩兩斜邊相對，易拼成矩形。",
          };
        },
        () => {
          const hops = 2 + Math.floor(rng() * 5);
          const route = shuffle(rng, places).slice(0, hops + 1);
          return {
            prompt: `地圖標咗：${route.join(" → ")}。一共經過幾個站？（計起點同終點）`,
            choices: shuffle(rng, [String(route.length), String(hops), String(route.length + 1), String(hops + 2)]),
            answer: String(route.length),
            hint: `路徑上有 ${route.length} 個站名。`,
          };
        },
      ],
      P6: [
        () => {
          const solid = pick(rng, [
            { name: "正方體", faces: 6, edges: 12, verts: 8 },
            { name: "長方體", faces: 6, edges: 12, verts: 8 },
            { name: "三棱柱", faces: 5, edges: 9, verts: 6 },
            { name: "四棱錐", faces: 5, edges: 8, verts: 5 },
            { name: "五棱柱", faces: 7, edges: 15, verts: 10 },
          ]);
          const kind = pick(rng, ["faces", "edges", "vertices"]);
          const label = { faces: "面", edges: "棱（邊）", vertices: "頂點" }[kind];
          const ans = String(solid[kind]);
          const wrong = shuffle(rng, [
            String(solid[kind] + 2),
            String(Math.max(1, solid[kind] - 2)),
            String(solid[kind] + 4),
            String(solid.faces),
            String(solid.edges),
            String(solid.vertices),
          ]).filter((x) => x !== ans);
          return {
            prompt: `一個${solid.name}有幾多個${label}？`,
            choices: shuffle(rng, [ans, ...wrong.slice(0, 3)]),
            answer: ans,
            hint: `${solid.name}有 ${ans} 個${label}。`,
          };
        },
        () => {
          const edge = 2 + Math.floor(rng() * 4); // 2..5
          const small = edge ** 3;
          return {
            prompt: `一個正方體淨係塗咗外面，切成 ${edge}×${edge}×${edge} 共 ${small} 個一樣大細正方體。三面都有色嘅有幾粒？`,
            choices: shuffle(rng, ["8", "12", "6", String(edge * 4), String(edge * edge)]),
            answer: "8",
            hint: "只有八個角位細立方體有三面色。",
          };
        },
        () => {
          const edge = 2 + Math.floor(rng() * 4);
          const small = edge ** 3;
          const faceOnly = edge >= 3 ? 6 * (edge - 2) ** 2 : 0;
          return {
            prompt: `正方體外塗色後切成 ${edge}×${edge}×${edge}（共 ${small} 粒）。只有一面有色嘅約有幾粒？（${edge < 3 ? "細格太少時答案係 0" : "每面中間 (n−2)²"}）`,
            choices: shuffle(rng, [String(faceOnly), "8", String(edge * 6), String(small), "12"]),
            answer: String(faceOnly),
            hint: edge < 3 ? "2×2×2 每粒至少兩面色，單面色=0。" : `6 × (${edge}−2)² = ${faceOnly}。`,
          };
        },
        () => {
          const pair = pick(rng, fromTo);
          const a = 2 + Math.floor(rng() * 4);
          const b = a + 1 + Math.floor(rng() * 5);
          return {
            prompt: `由${pair[0]}去${pair[1]}：C 路 ${a} 段、D 路 ${b} 段（每段一樣長）。最短係邊條？`,
            choices: ["C 路", "D 路", "一樣", "唔夠資料"],
            answer: "C 路",
            hint: `${a} < ${b}，揀 C。`,
          };
        },
        () => {
          const hours = pick(rng, [3, 6, 9, 12]);
          const turns = hours / 3; // 1..4 right angles
          return {
            prompt: `時鐘指針由 12 走到 ${hours === 12 ? 12 : hours}（順時針最短／整圈），轉咗幾多直角？（1 直角 = 90°；走到 12 算 4 個直角）`,
            choices: shuffle(rng, [String(turns), String(turns === 4 ? 2 : turns + 1), "0", String(turns === 1 ? 3 : turns - 1 || 2)]),
            answer: String(turns),
            hint: `每 3 小時 = 1 直角，${hours} 小時 = ${turns} 直角。`,
          };
        },
        () => {
          const n = 3 + Math.floor(rng() * 5);
          const route = shuffle(rng, places).slice(0, n);
          const mid = route[Math.floor(route.length / 2)];
          return {
            prompt: `路徑：${route.join("→")}。中間站（約一半位置）係邊個？`,
            choices: shuffle(rng, [mid, route[0], route[route.length - 1], route[1] || route[0]]),
            answer: mid,
            hint: `中間位置係「${mid}」。`,
          };
        },
      ],
    };

    const pool = builders[level] || builders.P4;
    const t = pick(rng, pool)();
    return stamp("spatial", { level, type: "choice", generated: true, ...t });
  }

  function genTruth(rng, level) {
    const names = shuffle(rng, ["阿文", "阿珍", "小明", "小華", "小美", "阿強", "阿傑", "小龍", "小欣"]);
    const templates =
      level === "P4"
        ? [
            {
              prompt: `${names[0]}話：「我今日冇食糖。」\n${names[1]}話：「${names[0]}食咗糖。」\n已知只有一人講真話。關於「邊個講假」，可以肯定嗎？`,
              choices: [`${names[0]}講假`, `${names[1]}講假`, "兩個都假", "唔夠資料"],
              answer: "唔夠資料",
              hint: "兩句互相矛盾，必定一真一假，但未知邊個真。",
            },
            {
              prompt: "邊兩句互相矛盾？\nA. 今日全日落雨\nB. 今日全日無半滴雨\nC. 今日有人帶傘",
              choices: ["A 同 B", "A 同 C", "B 同 C", "三句都矛盾"],
              answer: "A 同 B",
              hint: "「全日落雨」同「全日無雨」唔可以同時啱。",
            },
            {
              prompt: "邊兩句互相矛盾？\nA. 盒入面全部係紅波\nB. 盒入面有一粒藍波\nC. 盒好重",
              choices: ["A 同 B", "A 同 C", "B 同 C", "三句都矛盾"],
              answer: "A 同 B",
              hint: "「全部紅」同「有藍」矛盾。",
            },
            {
              prompt: `${names[0]}話：「課室冇人。」\n${names[1]}話：「課室有人。」\n已知恰好一人講真話。可以肯定邊個講假嗎？`,
              choices: [`${names[0]}`, `${names[1]}`, "兩個都假", "唔夠資料"],
              answer: "唔夠資料",
              hint: "互相矛盾，未知邊句真。",
            },
            {
              prompt: "邊兩句互相矛盾？\nA. 隊入面全部人空手\nB. 隊入面有人攞住旗\nC. 天氣好熱",
              choices: ["A 同 B", "A 同 C", "B 同 C", "三句都矛盾"],
              answer: "A 同 B",
              hint: "「全部空手」同「有人攞旗」矛盾。",
            },
            {
              prompt: `${names[0]}話：「我完成晒功課。」\n${names[1]}話：「${names[0]}仲有功課未做。」\n已知只有一人講真。可以肯定邊個講假嗎？`,
              choices: [`${names[0]}`, `${names[1]}`, "兩個都假", "唔夠資料"],
              answer: "唔夠資料",
              hint: "一真一假，但未知邊個。",
            },
            {
              prompt: "邊兩句互相矛盾？\nA. 動物園今日休息，冇開放\nB. 今日有人喺動物園入面參觀\nC. 今日星期二",
              choices: ["A 同 B", "A 同 C", "B 同 C", "三句都矛盾"],
              answer: "A 同 B",
              hint: "休息冇開放同有人參觀矛盾。",
            },
            {
              prompt: "邊兩句互相矛盾？\nA. 杯水係凍嘅\nB. 杯水係熱嘅\nC. 杯係玻璃做",
              choices: ["A 同 B", "A 同 C", "B 同 C", "三句都矛盾"],
              answer: "A 同 B",
              hint: "凍同熱唔可以同時成立。",
            },
          ]
        : level === "P5"
          ? [
              {
                prompt: `邊句同「全部同學都交咗功課」矛盾？`,
                choices: ["有同學今日遲到", "有同學未交功課", "有同學交得多過一份"],
                answer: "有同學未交功課",
                hint: "「全部都交」同「有人未交」相反。",
              },
              {
                prompt: `三人中恰好一人講假。\n${names[0]}：「我冇打破杯。」\n${names[1]}：「係${names[0]}打破。」\n${names[2]}：「唔係我打破。」\n如果${names[1]}講真話，邊個講假？`,
                choices: [names[0], names[1], names[2], "無法判斷"],
                answer: names[0],
                hint: `${names[1]}真 ⇒ ${names[0]}打破 ⇒ ${names[0]}句假。`,
              },
              {
                prompt: `邊句同「條河從來冇乾過」矛盾？`,
                choices: ["河水好清", "條河曾經乾過", "河邊有樹"],
                answer: "條河曾經乾過",
                hint: "「從來冇」同「曾經有」矛盾。",
              },
              {
                prompt: `邊句同「盒入面一粒糖都冇」矛盾？`,
                choices: ["盒好輕", "盒入面有一粒薄荷糖", "盒係鐵做"],
                answer: "盒入面有一粒薄荷糖",
                hint: "「一粒都冇」同「有一粒」矛盾。",
              },
              {
                prompt: `邊句同「全班都通過測驗」矛盾？`,
                choices: ["有人滿分", "有人不合格", "測驗好難"],
                answer: "有人不合格",
                hint: "「全部通過」同「有人不合格」矛盾。",
              },
              {
                prompt: `恰好一人講假。\n${names[0]}：「燈熄咗。」\n${names[1]}：「燈亮緊。」\n${names[2]}：「我睇到光。」\n若${names[2]}講真，邊個講假？`,
                choices: [names[0], names[1], names[2], "無法判斷"],
                answer: names[0],
                hint: `${names[2]}真 ⇒ 有光 ⇒ 燈非熄；故${names[0]}假。`,
              },
            ]
          : [
              {
                prompt: `${names[0]}話：「${names[1]}講大話。」\n${names[1]}話：「我同${names[0]}都講真話。」\n邊個一定講大話？`,
                choices: [names[0], names[1], "兩個都假", "兩個都真"],
                answer: names[1],
                hint: `若${names[1]}真則兩人都真，但${names[0]}又話佢假，矛盾；故${names[1]}假。`,
              },
              {
                prompt: `${names[0]}：「${names[1]}同我都講大話。」\n${names[1]}：「${names[0]}講真話。」\n邊個一定講大話？`,
                choices: [names[0], names[1], "兩個都假", "無法判斷"],
                answer: names[0],
                hint: `${names[0]}若真，則自己講大話，矛盾；故${names[0]}假。`,
              },
              {
                prompt: `${names[0]}：「我哋兩個都講真話。」\n${names[1]}：「${names[0]}講大話。」\n邊個一定講大話？`,
                choices: [names[0], names[1], "兩個都假", "兩個都真"],
                answer: names[0],
                hint: `兩句互相矛盾，唔可以同時真；若${names[0]}真則${names[1]}假且兩人都真，矛盾。故${names[0]}假。`,
              },
              {
                prompt: `邊句同「呢條路永遠暢通」矛盾？`,
                choices: ["路上車少", "呢條路曾經封閉過", "路好闊"],
                answer: "呢條路曾經封閉過",
                hint: "「永遠暢通」同「曾經封閉」矛盾。",
              },
              {
                prompt: `${names[0]}：「至少我哋其中一個講假。」\n${names[1]}：「我講真話。」\n若只有呢兩句，邊個可以肯定？`,
                choices: [`${names[0]}一定真`, `${names[1]}一定假`, "兩個都真", "唔夠資料"],
                answer: `${names[0]}一定真`,
                hint: `若${names[0]}假，則「至少一假」為假 ⇒ 兩個都真，矛盾；故${names[0]}真。`,
              },
            ];
    // parametric variants: swap names already; add weather/box variants via rng pick above
    const t = pick(rng, templates);
    return stamp("truth", { level, type: "choice", generated: true, ...t });
  }

  // --- also ensure genCondition still exists; if truncated earlier it may be missing ---
  const GENERATORS = {
    pattern: genPattern,
    classify: genClassify,
    condition: genCondition,
    spatial: genSpatial,
    truth: genTruth,
  };

  const LEVELS = ["P4", "P5", "P6"];

  function buildDailySet(catId, dateStr, usedIds, perDay) {
    const seed = hashStr(`${dateStr}|${catId}|v3-no-reuse`);
    const used = new Set(usedIds || []);
    const out = [];
    const seenContent = new Set();
    let guard = 0;

    function tryPush(q) {
      const ck = q.contentKey || contentKey(q.prompt, q.answer);
      if (used.has(q.id) || used.has(ck) || seenContent.has(ck)) return false;
      out.push(q);
      seenContent.add(ck);
      used.add(q.id);
      used.add(ck);
      return true;
    }

    // 硬約束：禁止放寬跨日重用。池不夠就少過 perDay，唔可以用舊內容湊數。
    while (out.length < perDay && guard < 4000) {
      guard++;
      const level = LEVELS[out.length % LEVELS.length];
      const gen = GENERATORS[catId];
      if (!gen) break;
      const q = gen(mulberry32(seed + guard * 9973), level);
      tryPush(q);
    }
    return out;
  }

  global.LogicDaily = {
    hktDateString,
    buildDailySet,
    hashStr,
    contentKey,
    fingerprintId,
  };
})(window);
