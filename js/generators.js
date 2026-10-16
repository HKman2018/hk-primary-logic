/** 參數化出題（靜態站、無需後端）。
 *  同日穩定、跨日唔同。contentKey = 題幹＋答案，禁止跨日重用；池不夠就少過 5 題。
 *  五類各自有多條互不相干嘅出題族，覆蓋小四至小六。
 */
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

  function irand(rng, lo, hi) {
    return lo + Math.floor(rng() * (hi - lo + 1));
  }

  function pickN(rng, arr, n) {
    return shuffle(rng, arr).slice(0, n);
  }

  function canon(arr) {
    return arr.slice().sort();
  }

  function constDiff(seq) {
    if (seq.length < 2) return null;
    const d = seq[1] - seq[0];
    for (let i = 2; i < seq.length; i++) {
      if (seq[i] - seq[i - 1] !== d) return null;
    }
    return d;
  }

  function secondConst(seq) {
    const d = [];
    for (let i = 1; i < seq.length; i++) d.push(seq[i] - seq[i - 1]);
    return constDiff(d);
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

  function emitFill(prompt, answer, hint) {
    return { prompt, type: "fill", answer: String(answer), hint };
  }

  function emitChoice(rng, prompt, answer, distractors, hint) {
    const ans = String(answer);
    const opts = [];
    const seen = new Set([ans]);
    for (const d of distractors) {
      const s = String(d);
      if (!s || seen.has(s)) continue;
      seen.add(s);
      opts.push(s);
    }
    if (opts.length < 2) return null;
    return {
      prompt,
      type: "choice",
      choices: shuffle(rng, [ans].concat(opts.slice(0, 3))),
      answer: ans,
      hint,
    };
  }

  function finish(catId, level, built) {
    if (!built || !built.prompt || built.answer === undefined || built.answer === null || built.answer === "") {
      return null;
    }
    const answer = String(built.answer);
    if (built.type === "choice") {
      if (!Array.isArray(built.choices)) return null;
      const choices = built.choices.map(String);
      if (new Set(choices).size !== choices.length) return null;
      if (!choices.includes(answer)) return null;
      if (choices.length < 3) return null;
      return stamp(catId, {
        level,
        prompt: built.prompt,
        type: "choice",
        choices,
        answer,
        hint: built.hint || "再睇清楚條件。",
        generated: true,
      });
    }
    return stamp(catId, {
      level,
      prompt: built.prompt,
      type: "fill",
      answer,
      hint: built.hint || "再睇清楚規律。",
      generated: true,
    });
  }

  function fromBuilders(catId, rng, level, builders, fallback) {
    for (let i = 0; i < 80; i++) {
      const q = finish(catId, level, pick(rng, builders)(rng));
      if (q) return q;
    }
    const q = finish(catId, level, fallback(rng));
    if (q) return q;
    return stamp(catId, {
      level,
      prompt: `數列：2、4、6、8、10、？\n下一個數係幾多？`,
      type: "fill",
      answer: "12",
      hint: "每次加 2。",
      generated: true,
    });
  }

  const NAMES = ["阿明", "小華", "阿美", "阿強", "小美", "阿傑", "小文", "阿珍", "小龍", "阿欣", "小希", "阿樂", "小宇", "阿琪", "小童", "阿朗"];
  const SYMS = ["○", "△", "□", "☆", "●", "◆", "▲", "▼", "★", "◇"];
  const POLY = { 3: "三角形", 4: "四邊形", 5: "五邊形", 6: "六邊形", 7: "七邊形", 8: "八邊形", 9: "九邊形", 10: "十邊形" };

  function seqPrompt(seq) {
    return `數列：${seq.join("、")}、？\n下一個數係幾多？`;
  }

  function tooBig(seq, ans) {
    return seq.some((n) => n > 900 || n < 0) || ans > 900 || ans < 0;
  }

  // ---------- 找規律 ----------

  function bAdd(rng) {
    const start = irand(rng, 1, 40);
    const step = irand(rng, 1, 12);
    const seq = [];
    for (let i = 0; i < 5; i++) seq.push(start + i * step);
    const ans = start + 5 * step;
    return emitFill(seqPrompt(seq), ans, `每次加 ${step}。`);
  }

  function bSub(rng) {
    const step = irand(rng, 1, 9);
    const start = step * 5 + 1 + irand(rng, 0, 28);
    const seq = [];
    for (let i = 0; i < 5; i++) seq.push(start - i * step);
    const ans = start - 5 * step;
    if (ans < 1) return null;
    return emitFill(seqPrompt(seq), ans, `每次減 ${step}。`);
  }

  function bAddGrow(rng) {
    const start = irand(rng, 1, 24);
    const d0 = irand(rng, 1, 9);
    const g = irand(rng, 1, 4);
    let n = start;
    const seq = [n];
    const diffs = [];
    for (let i = 0; i < 4; i++) {
      const d = d0 + i * g;
      diffs.push(d);
      n += d;
      seq.push(n);
    }
    const next = d0 + 4 * g;
    const ans = n + next;
    if (constDiff(seq) !== null || tooBig(seq, ans)) return null;
    return emitFill(seqPrompt(seq), ans, `相差依次係 ${diffs.join("、")}，下一個相差係 ${next}。`);
  }

  function bAltAddSub(rng) {
    const a = irand(rng, 2, 12);
    const b = irand(rng, 1, 8);
    if (a === b) return null;
    const start = b + irand(rng, 2, 24);
    let n = start;
    const seq = [n];
    for (let i = 0; i < 4; i++) {
      n = i % 2 === 0 ? n + a : n - b;
      if (n < 1) return null;
      seq.push(n);
    }
    const ans = n + a;
    if (ans < 1 || constDiff(seq) !== null) return null;
    return emitFill(seqPrompt(seq), ans, `加數交替：+${a}、−${b}、+${a}、−${b}…下一個加 ${a}。`);
  }

  function bFib(rng) {
    const a = irand(rng, 1, 12);
    const b = irand(rng, 1, 12);
    let x = a;
    let y = b;
    const seq = [x, y];
    for (let i = 0; i < 3; i++) {
      const z = x + y;
      seq.push(z);
      x = y;
      y = z;
    }
    const ans = x + y;
    if (tooBig(seq, ans) || constDiff(seq) !== null) return null;
    return emitFill(seqPrompt(seq), ans, "每個數係前兩個數相加。");
  }

  function bFibK(rng) {
    const a = irand(rng, 1, 8);
    const b = irand(rng, 1, 8);
    const k = irand(rng, 1, 5);
    let x = a;
    let y = b;
    const seq = [x, y];
    for (let i = 0; i < 3; i++) {
      const z = x + y + k;
      seq.push(z);
      x = y;
      y = z;
    }
    const ans = x + y + k;
    if (tooBig(seq, ans) || constDiff(seq) !== null) return null;
    return emitFill(seqPrompt(seq), ans, `每個數係前兩個數相加，再加 ${k}。`);
  }

  function bInter(rng) {
    const s1 = irand(rng, 1, 15);
    const d1 = irand(rng, 1, 6);
    const s2 = irand(rng, 16, 50);
    const d2 = irand(rng, 1, 9);
    if (d1 === d2) return null;
    const seq = [s1, s2, s1 + d1, s2 + d2, s1 + 2 * d1];
    const ans = s2 + 2 * d2;
    if (constDiff(seq) !== null || secondConst(seq) !== null) return null;
    return emitFill(seqPrompt(seq), ans, `第1、3、5個數每次加 ${d1}；第2、4、6個數每次加 ${d2}。`);
  }

  function bMulSub(rng) {
    const start = irand(rng, 2, 12);
    const k = irand(rng, 1, 5);
    let n = start;
    const seq = [n];
    let mul = true;
    for (let i = 0; i < 4; i++) {
      n = mul ? n * 2 : n - k;
      if (n < 1) return null;
      seq.push(n);
      mul = !mul;
    }
    const ans = mul ? n * 2 : n - k;
    if (ans < 1 || ans > 900 || constDiff(seq) !== null) return null;
    return emitFill(seqPrompt(seq), ans, `運算交替：×2、−${k}、×2、−${k}…下一個係 ×2。`);
  }

  function bMulAdd(rng) {
    const kMul = pick(rng, [2, 3]);
    const start = irand(rng, 1, kMul === 2 ? 7 : 4);
    const add = irand(rng, 1, kMul === 2 ? 8 : 4);
    const steps = kMul === 2 ? 4 : 3;
    let n = start;
    const seq = [n];
    for (let i = 0; i < steps; i++) {
      n = n * kMul + add;
      seq.push(n);
    }
    const ans = n * kMul + add;
    if (tooBig(seq, ans)) return null;
    return emitFill(seqPrompt(seq), ans, `每次 ×${kMul} 再 +${add}。`);
  }

  function bGeo(rng) {
    const k = pick(rng, [2, 3]);
    const start = irand(rng, 1, k === 2 ? 9 : 4);
    const steps = k === 2 ? 5 : 4;
    let n = start;
    const seq = [];
    for (let i = 0; i < steps; i++) {
      seq.push(n);
      n *= k;
    }
    if (tooBig(seq, n)) return null;
    return emitFill(seqPrompt(seq), n, `每次 ×${k}。`);
  }

  function bProd(rng) {
    const s = irand(rng, 1, 10);
    const k = irand(rng, 1, 4);
    const seq = [];
    for (let i = 0; i < 5; i++) seq.push((s + i) * (s + i + k));
    const ans = (s + 5) * (s + 5 + k);
    if (tooBig(seq, ans)) return null;
    return emitFill(seqPrompt(seq), ans, `由 ${s} 起，依次係 n×(n+${k})。`);
  }

  function bSq(rng) {
    const s = irand(rng, 1, 12);
    const seq = [];
    for (let i = 0; i < 5; i++) seq.push((s + i) * (s + i));
    const ans = (s + 5) * (s + 5);
    if (tooBig(seq, ans)) return null;
    return emitFill(seqPrompt(seq), ans, `依次係 ${s}²、${s + 1}²、${s + 2}²…`);
  }

  function bPowGap(rng) {
    const start = irand(rng, 1, 36);
    let n = start;
    const seq = [n];
    let add = 1;
    for (let i = 0; i < 4; i++) {
      n += add;
      seq.push(n);
      add *= 2;
    }
    const ans = n + add;
    return emitFill(seqPrompt(seq), ans, "相差係 1、2、4、8，下一個相差係 16。");
  }

  function bCycle(rng) {
    const a = irand(rng, 1, 7);
    const b = irand(rng, 1, 7);
    const c = irand(rng, 1, 7);
    if (a === b && b === c) return null;
    const start = irand(rng, 1, 18);
    const diffs = [a, b, c, a, b];
    let n = start;
    const seq = [n];
    diffs.forEach((d) => {
      n += d;
      seq.push(n);
    });
    const ans = n + c;
    if (constDiff(seq) !== null || secondConst(seq) !== null) return null;
    return emitFill(seqPrompt(seq), ans, `相差按 ${a}、${b}、${c} 循環。`);
  }

  function bDec(rng) {
    const d0 = irand(rng, 1, 6);
    const g = irand(rng, 1, 4);
    const shown = [0, 1, 2, 3].map((i) => d0 + i * g);
    const next = d0 + 4 * g;
    const offset = irand(rng, 0, 18);
    const ans = 1 + offset;
    let n = ans + next;
    const rev = [n];
    for (let i = shown.length - 1; i >= 0; i--) {
      n += shown[i];
      rev.push(n);
    }
    const seq = rev.reverse();
    if (seq.some((x) => x < 1) || constDiff(seq) !== null) return null;
    return emitFill(seqPrompt(seq), ans, `減少量依次係 ${shown.join("、")}，下一個減少 ${next}。`);
  }

  function bAddMul(rng) {
    const start = irand(rng, 1, 12);
    const a = irand(rng, 1, 9);
    let n = start;
    const seq = [n];
    for (let i = 0; i < 4; i++) {
      n = i % 2 === 0 ? n + a : n * 2;
      seq.push(n);
    }
    const ans = n + a;
    if (tooBig(seq, ans) || constDiff(seq) !== null) return null;
    return emitFill(seqPrompt(seq), ans, `運算交替：+${a}、×2、+${a}、×2…下一個加 ${a}。`);
  }

  function bAbab(rng) {
    const a = irand(rng, 1, 9);
    let b = irand(rng, 1, 9);
    if (b === a) b = a === 9 ? 1 : a + 1;
    const seq = [a, b, a, b, a];
    return emitFill(seqPrompt(seq), b, `數 ${a} 同 ${b} 輪流出現，下一個係 ${b}。`);
  }

  function bDouble(rng) {
    const s = irand(rng, 1, 18);
    const seq = [s, s, s + 1, s + 1, s + 2];
    return emitFill(seqPrompt(seq), s + 2, "同一個數連續出現兩次。");
  }

  function bSym2(rng) {
    const a = pick(rng, SYMS);
    const b = pick(rng, SYMS.filter((x) => x !== a));
    const seq = [a, b, a, b, a];
    const rest = SYMS.filter((x) => x !== b);
    return emitChoice(
      rng,
      `圖案規律：${seq.join(" ")} ？\n下一個應該係邊個？`,
      b,
      rest,
      `${a} 同 ${b} 輪流，下一個係 ${b}。`
    );
  }

  function bSym3(rng) {
    const a = pick(rng, SYMS);
    const b = pick(rng, SYMS.filter((x) => x !== a));
    const c = pick(rng, SYMS.filter((x) => x !== a && x !== b));
    const seq = [a, b, c, a, b, c, a];
    const rest = SYMS.filter((x) => x !== b);
    return emitChoice(
      rng,
      `圖案規律：${seq.join(" ")} ？\n下一個應該係邊個？`,
      b,
      rest,
      `${a}、${b}、${c} 順序循環，下一個係 ${b}。`
    );
  }

  function bCountSym(rng) {
    const sym = pick(rng, SYMS);
    const start = irand(rng, 1, 4);
    const groups = [];
    for (let i = 0; i < 4; i++) groups.push(sym.repeat(start + i));
    const ans = start + 4;
    return emitFill(
      `圖案規律（數吓有幾多個）：${groups.join("、")}、？\n下一組有幾多個？`,
      ans,
      "每組多 1 個。"
    );
  }

  const PATTERN = {
    P4: [bAdd, bSub, bAbab, bDouble, bSym2, bSym3, bCountSym],
    P5: [bAddGrow, bAltAddSub, bFib, bInter, bMulSub, bGeo],
    P6: [bMulAdd, bProd, bSq, bPowGap, bCycle, bDec, bAddMul, bFibK],
  };

  function genPattern(rng, level) {
    return fromBuilders("pattern", rng, level, PATTERN[level] || PATTERN.P4, bAdd);
  }

  // ---------- 分類 ----------

  const GROUPS = [
    { name: "水果", hint: "其餘都係水果。", members: ["蘋果", "香蕉", "橙", "葡萄", "梨", "芒果"], odd: "雪櫃" },
    { name: "蔬菜", hint: "其餘都係蔬菜。", members: ["白菜", "胡蘿蔔", "黃瓜", "茄子", "南瓜", "菠菜"], odd: "鉛筆" },
    { name: "陸上交通", hint: "其餘都係陸上交通工具。", members: ["巴士", "的士", "火車", "單車", "電車", "小巴"], odd: "鯨魚" },
    { name: "文具", hint: "其餘都係文具。", members: ["鉛筆", "原子筆", "擦膠", "間尺", "膠水", "鉛筆刨"], odd: "金魚" },
    { name: "樂器", hint: "其餘都係樂器。", members: ["鋼琴", "結他", "小提琴", "長笛", "鼓", "口琴"], odd: "枕頭" },
    { name: "職業", hint: "其餘都係職業。", members: ["醫生", "護士", "消防員", "警察", "教師", "廚師"], odd: "蘋果" },
    { name: "飲料", hint: "其餘都係飲料。", members: ["牛奶", "果汁", "清水", "豆漿", "檸檬茶", "咖啡"], odd: "波鞋" },
    { name: "星期", hint: "其餘都係星期。", members: ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六"], odd: "芒果" },
    { name: "月份", hint: "其餘都係月份。", members: ["一月", "三月", "五月", "七月", "九月", "十一月"], odd: "鼓" },
    { name: "季節", hint: "其餘都係季節。", members: ["春天", "夏天", "秋天", "冬天"], odd: "星期一" },
    { name: "衫褲", hint: "其餘都係衫褲。", members: ["恤衫", "長褲", "短裙", "外套", "襪子", "領帶"], odd: "飯碗" },
    { name: "球類", hint: "其餘都係球。", members: ["足球", "籃球", "排球", "乒乓球", "羽毛球", "網球"], odd: "球拍" },
    { name: "廚房用具", hint: "其餘都係廚房用具。", members: ["鑊", "鐵鍋", "菜刀", "砧板", "飯勺", "蒸籠"], odd: "單車" },
    { name: "校園地方", hint: "其餘都係校園地方。", members: ["課室", "圖書館", "操場", "禮堂", "音樂室", "電腦室"], odd: "菠蘿包" },
    { name: "讀物", hint: "其餘都係讀物。", members: ["故事書", "報紙", "雜誌", "課本", "字典", "漫畫"], odd: "風扇" },
    { name: "電器", hint: "其餘都係電器。", members: ["雪櫃", "洗衣機", "電視機", "風扇", "冷氣機", "微波爐"], odd: "香蕉" },
    { name: "昆蟲", hint: "其餘都係昆蟲。", members: ["蝴蝶", "蜜蜂", "螞蟻", "蜻蜓", "甲蟲", "蟋蟀"], odd: "鴿子" },
    { name: "鳥類", hint: "其餘都係雀鳥。", members: ["麻雀", "燕子", "鴿子", "老鷹", "鸚鵡", "海鷗"], odd: "鯉魚" },
    { name: "魚類", hint: "其餘都係魚。", members: ["金魚", "鯉魚", "鯊魚", "三文魚", "鰻魚", "鯛魚"], odd: "燕子" },
    { name: "花卉", hint: "其餘都係花。", members: ["玫瑰", "百合", "菊花", "向日葵", "牡丹", "荷花"], odd: "頭盔" },
    { name: "水上工具", hint: "其餘都係水上交通工具。", members: ["渡輪", "潛水艇", "帆船", "獨木舟", "遊艇", "舢舨"], odd: "飛機" },
    { name: "航空工具", hint: "其餘都係航空工具。", members: ["飛機", "直昇機", "熱氣球", "火箭", "滑翔機", "無人機"], odd: "帆船" },
    { name: "運動", hint: "其餘都係運動。", members: ["游泳", "跑步", "跳繩", "體操", "溜冰", "行山"], odd: "字典" },
    { name: "科目", hint: "其餘都係科目。", members: ["中文", "英文", "數學", "常識", "音樂", "體育"], odd: "菊花" },
    { name: "餐具", hint: "其餘都係餐具。", members: ["飯碗", "湯匙", "筷子", "碟子", "叉子", "茶杯"], odd: "外套" },
    { name: "配飾", hint: "其餘都係配飾。", members: ["太陽帽", "眼鏡", "皮帶", "手錶", "頸巾", "耳環"], odd: "筷子" },
    { name: "形狀", hint: "其餘都係形狀。", members: ["圓形", "正方形", "三角形", "長方形", "星形", "心形"], odd: "耳環" },
    { name: "家庭", hint: "其餘都係家人。", members: ["爸爸", "媽媽", "哥哥", "姐姐", "弟弟", "妹妹"], odd: "警察" },
    { name: "節日", hint: "其餘都係節日。", members: ["農曆新年", "中秋節", "端午節", "聖誕節", "復活節", "重陽節"], odd: "星期三" },
    { name: "方向", hint: "其餘都係方向。", members: ["東方", "南方", "西方", "北方", "東南", "西北"], odd: "中秋節" },
    { name: "香港小食", hint: "其餘都係香港小食。", members: ["蛋撻", "菠蘿包", "魚蛋", "腸粉", "格仔餅", "蛋散"], odd: "間尺" },
    { name: "公園設施", hint: "其餘都係公園設施。", members: ["滑梯", "韆鞦", "蹺蹺板", "沙池", "攀登架", "旋轉木馬"], odd: "檸檬茶" },
    { name: "五官", hint: "其餘都係五官。", members: ["眼睛", "耳朵", "嘴巴", "鼻子", "舌頭", "眉毛"], odd: "滑梯" },
    { name: "天氣", hint: "其餘都係天氣。", members: ["晴天", "雨天", "陰天", "颱風", "大霧", "寒流"], odd: "眉毛" },
    { name: "容器", hint: "其餘都係用來裝嘢。", members: ["水樽", "飯盒", "背包", "布袋", "紙箱", "膠盒"], odd: "颱風" },
    { name: "建築物", hint: "其餘都係建築物。", members: ["學校", "醫院", "消防局", "郵政局", "體育館", "火車站"], odd: "水樽" },
    { name: "糖果", hint: "其餘都係糖果。", members: ["朱古力", "棉花糖", "棒棒糖", "果汁糖", "軟糖", "薄荷糖"], odd: "火車站" },
    { name: "哺乳動物", hint: "其餘都係哺乳動物。", members: ["貓", "狗", "兔", "牛", "馬", "羊"], odd: "蜻蜓" },
    { name: "顏色", hint: "其餘都係顏色。", members: ["紅色", "藍色", "綠色", "黃色", "紫色", "黑色"], odd: "馬" },
    { name: "時間單位", hint: "其餘都係時間單位。", members: ["秒鐘", "分鐘", "小時", "星期", "月份", "年份"], odd: "公斤" },
  ];

  function membersNamed(names) {
    const out = [];
    GROUPS.forEach((g) => {
      if (names.indexOf(g.name) >= 0) out.push.apply(out, g.members);
    });
    return out;
  }

  function bOdd(rng) {
    const g = pick(rng, GROUPS);
    const three = pickN(rng, g.members, Math.min(3, g.members.length));
    const shown = canon(three.concat([g.odd]));
    return emitChoice(rng, `邊個唔屬於同一類？\n${shown.join("、")}`, g.odd, three, g.hint);
  }

  function bBelongs(rng) {
    const rules = [
      { ask: "邊個可以食？", yes: membersNamed(["水果", "蔬菜", "香港小食", "糖果"]), no: membersNamed(["文具", "陸上交通", "樂器", "電器", "公園設施", "建築物"]), hint: "淨係得一個可以食。" },
      { ask: "邊個係動物？", yes: membersNamed(["哺乳動物", "鳥類", "魚類", "昆蟲"]), no: membersNamed(["水果", "文具", "電器", "陸上交通", "形狀"]), hint: "淨係得一個係動物。" },
      { ask: "邊個係交通工具？", yes: membersNamed(["陸上交通", "水上工具", "航空工具"]), no: membersNamed(["水果", "文具", "哺乳動物", "餐具"]), hint: "淨係得一個係交通工具。" },
      { ask: "邊個係文具？", yes: membersNamed(["文具"]), no: membersNamed(["哺乳動物", "水果", "陸上交通", "香港小食"]), hint: "淨係得一個係文具。" },
      { ask: "邊個可以穿或者戴？", yes: membersNamed(["衫褲", "配飾"]), no: membersNamed(["餐具", "廚房用具", "球類", "讀物"]), hint: "淨係得一個可以穿或者戴。" },
    ];
    const rule = pick(rng, rules);
    const yes = pick(rng, rule.yes);
    const nos = pickN(rng, rule.no.filter((x) => x !== yes), 3);
    if (nos.length < 3) return null;
    const shown = canon([yes].concat(nos));
    return emitChoice(rng, `${rule.ask}\n${shown.join("、")}`, yes, nos, rule.hint);
  }

  function groupLabel(aName, aItems, bName, bItems) {
    const parts = [
      [aName, canon(aItems).join("、")],
      [bName, canon(bItems).join("、")],
    ].sort((p, q) => (p[0] < q[0] ? -1 : p[0] > q[0] ? 1 : 0));
    return `${parts[0][0]}：${parts[0][1]}｜${parts[1][0]}：${parts[1][1]}`;
  }

  function bGroup(rng) {
    const pool = GROUPS.filter((g) => g.members.length >= 4);
    const A = pick(rng, pool);
    const B = pick(rng, pool.filter((g) => g !== A));
    const aItems = pickN(rng, A.members, 2);
    const bItems = pickN(rng, B.members, 2);
    const shown = canon(aItems.concat(bItems));
    const answer = groupLabel(A.name, aItems, B.name, bItems);
    const wrongMix = groupLabel(A.name, [aItems[0], bItems[0]], B.name, [aItems[1], bItems[1]]);
    const wrongSwap = groupLabel(A.name, bItems, B.name, aItems);
    return emitChoice(
      rng,
      `點樣分組最合理？\n${shown.join("、")}`,
      answer,
      [wrongMix, wrongSwap, "全部同一類，唔使分"],
      `按「${A.name}」同「${B.name}」分開。`
    );
  }

  function bCatName(rng) {
    const g = pick(rng, GROUPS.filter((x) => x.members.length >= 3));
    const three = pickN(rng, g.members, 3);
    const others = pickN(rng, GROUPS.filter((x) => x !== g), 3).map((x) => x.name);
    return emitChoice(
      rng,
      `「${canon(three).join("、")}」最貼切嘅類別係邊個？`,
      g.name,
      others,
      `呢三樣都屬於「${g.name}」。`
    );
  }

  function bAttr(rng) {
    const sizes = ["大", "細"];
    const colors = ["紅", "藍", "綠", "黃", "白", "紫", "橙", "黑"];
    const shapes = ["圓形", "正方形", "三角形", "星形", "心形", "長方形"];
    const things = ["積木", "貼紙", "波", "卡", "盒", "鈕"];
    const size = pick(rng, sizes);
    const color = pick(rng, colors);
    const shape = pick(rng, shapes);
    const thing = pick(rng, things);
    const ans = `${size}${color}色${shape}${thing}`;
    const size2 = size === "大" ? "細" : "大";
    const color2 = colors.find((c) => c !== color);
    const shape2 = shapes.find((s) => s !== shape);
    const thing2 = things.find((t) => t !== thing);
    return emitChoice(
      rng,
      `要同時符合「${size}」、「${color}色」、「${shape}」同「${thing}」。邊個啱？`,
      ans,
      [
        `${size2}${color}色${shape}${thing}`,
        `${size}${color2}色${shape}${thing}`,
        `${size}${color}色${shape2}${thing}`,
        `${size}${color}色${shape}${thing2}`,
      ],
      "四個條件要同時成立。"
    );
  }

  const RULE_PACKS = [
    { rule: "會飛", members: ["麻雀", "蝴蝶", "飛機", "蜜蜂", "直昇機", "蝙蝠"], odd: "烏龜", hint: "烏龜唔識飛。" },
    { rule: "主要住喺水入面", members: ["金魚", "鯨魚", "蝦", "螃蟹", "水母", "海星"], odd: "兔子", hint: "兔子住陸上。" },
    { rule: "用嚟寫字", members: ["鉛筆", "原子筆", "毛筆", "粉筆", "蠟筆", "鋼筆"], odd: "擦膠", hint: "擦膠用嚟擦，唔係用嚟寫。" },
    { rule: "有四條腿", members: ["狗", "貓", "牛", "馬", "象", "老虎"], odd: "鴨", hint: "鴨有兩條腿。" },
    { rule: "屬於天氣現象", members: ["雨", "雪", "霧", "雷", "彩虹", "霜"], odd: "課桌", hint: "課桌唔係天氣。" },
    { rule: "可以飲", members: ["清水", "牛奶", "茶", "果汁", "豆漿", "湯"], odd: "白飯", hint: "白飯係食，唔係飲。" },
    { rule: "係一種球", members: ["足球", "籃球", "排球", "網球", "乒乓球", "羽毛球"], odd: "球拍", hint: "球拍唔係球。" },
    { rule: "係香港常見小食", members: ["蛋撻", "菠蘿包", "魚蛋", "腸粉", "格仔餅", "蛋散"], odd: "間尺", hint: "間尺唔係小食。" },
    { rule: "係節日", members: ["農曆新年", "中秋節", "端午節", "聖誕節", "復活節", "重陽節"], odd: "星期二", hint: "星期二係星期，唔係節日。" },
    { rule: "係月份", members: ["二月", "四月", "六月", "八月", "十月", "十二月"], odd: "秋天", hint: "秋天係季節，唔係月份。" },
    { rule: "有輪而且用嚟載人", members: ["巴士", "的士", "單車", "火車", "電車", "小巴"], odd: "雪櫃", hint: "雪櫃唔係交通工具。" },
    { rule: "係樂器", members: ["鋼琴", "結他", "小提琴", "長笛", "鼓", "口琴"], odd: "電視機", hint: "電視機唔係樂器。" },
    { rule: "係水果", members: ["蘋果", "香蕉", "橙", "葡萄", "梨", "芒果"], odd: "胡蘿蔔", hint: "胡蘿蔔一般當蔬菜。" },
    { rule: "可以穿喺身上", members: ["恤衫", "長褲", "短裙", "外套", "襪子", "領帶"], odd: "飯碗", hint: "飯碗唔可以穿。" },
    { rule: "係昆蟲", members: ["蝴蝶", "蜜蜂", "螞蟻", "蜻蜓", "甲蟲", "蟋蟀"], odd: "海鷗", hint: "海鷗係雀，唔係昆蟲。" },
    { rule: "係建築物", members: ["學校", "醫院", "消防局", "郵政局", "體育館", "火車站"], odd: "蝴蝶", hint: "蝴蝶唔係建築物。" },
    { rule: "用電嘅家電", members: ["雪櫃", "洗衣機", "電視機", "風扇", "冷氣機", "微波爐"], odd: "蠟燭", hint: "蠟燭唔使電。" },
    { rule: "係餐具", members: ["飯碗", "湯匙", "筷子", "碟子", "叉子", "茶杯"], odd: "枕頭", hint: "枕頭唔係餐具。" },
    { rule: "係哺乳動物", members: ["貓", "狗", "兔", "牛", "馬", "羊"], odd: "鯊魚", hint: "鯊魚係魚，唔係哺乳動物。" },
    { rule: "係方向", members: ["東方", "南方", "西方", "北方", "東南", "西北"], odd: "蛋糕", hint: "蛋糕唔係方向。" },
    { rule: "用嚟量度", members: ["間尺", "捲尺", "三角尺", "量角器", "軟尺", "米達尺"], odd: "鉛筆", hint: "鉛筆用嚟寫，唔係用嚟量。" },
    { rule: "常見農場動物", members: ["牛", "馬", "羊", "豬", "雞", "鴨"], odd: "鯊魚", hint: "鯊魚唔係農場動物。" },
    { rule: "可以切或者剪", members: ["菜刀", "鉸剪", "小刀", "界刀", "鋸", "剪紙刀"], odd: "枕頭", hint: "枕頭唔可以切或者剪。" },
    { rule: "係五官", members: ["眼睛", "耳朵", "嘴巴", "鼻子", "舌頭", "眉毛"], odd: "手指", hint: "手指唔算五官。" },
  ];

  function bStated(rng) {
    const g = pick(rng, RULE_PACKS);
    const three = pickN(rng, g.members, 3);
    const shown = canon(three.concat([g.odd]));
    return emitChoice(
      rng,
      `邊個不符合「${g.rule}」？\n${shown.join("、")}`,
      g.odd,
      three,
      g.hint
    );
  }

  const RELATIONS = [
    { name: "工作地點", pairs: [["醫生", "醫院"], ["教師", "學校"], ["廚師", "廚房"], ["圖書管理員", "圖書館"], ["消防員", "消防局"], ["售貨員", "商店"], ["護士", "病房"], ["司機", "車廂"]] },
    { name: "用嚟做", pairs: [["筆", "寫字"], ["刀", "切菜"], ["傘", "遮雨"], ["尺", "量長度"], ["擦膠", "擦走字"], ["眼鏡", "睇得清"], ["水樽", "裝水"], ["鑰匙", "開門"]] },
    { name: "住喺", pairs: [["金魚", "水"], ["雀仔", "巢"], ["蜜蜂", "蜂巢"], ["兔", "草叢"], ["螃蟹", "海邊"], ["駱駝", "沙漠"], ["松鼠", "樹上"], ["蚯蚓", "泥入面"]] },
    { name: "一部分", pairs: [["輪", "單車"], ["頁", "書"], ["窗", "課室"], ["鍵", "鋼琴"], ["葉", "樹"], ["蓋", "壺"], ["帆", "帆船"], ["梯級", "樓梯"]] },
    { name: "相反", pairs: [["大", "細"], ["高", "矮"], ["熱", "凍"], ["快", "慢"], ["開", "關"], ["輕", "重"], ["長", "短"], ["日", "夜"], ["前", "後"], ["左", "右"]] },
    { name: "量度單位", pairs: [["米", "長度"], ["克", "重量"], ["秒", "時間"], ["升", "容量"], ["度", "溫度"]] },
    { name: "保護部位", pairs: [["頭盔", "頭"], ["手套", "手"], ["救生衣", "身體"], ["護膝", "膝頭"], ["口罩", "口鼻"], ["安全帶", "坐車人士"]] },
    { name: "材料", pairs: [["木桌", "木材"], ["玻璃杯", "玻璃"], ["鐵鑊", "鐵"], ["紙袋", "紙"], ["布袋", "布"], ["膠盒", "膠"]] },
    { name: "幼小叫做", pairs: [["狗", "小狗"], ["貓", "小貓"], ["牛", "牛仔"], ["雞", "小雞"], ["馬", "小馬"], ["羊", "小羊"], ["鴨", "小鴨"]] },
    { name: "季節事物", pairs: [["游泳", "夏天"], ["堆雪人", "冬天"], ["賞月", "中秋"], ["賽龍舟", "端午"], ["賞花", "春天"], ["吃湯圓", "元宵節"]] },
  ];

  function bAnalogy(rng) {
    const rel = pick(rng, RELATIONS);
    const i = irand(rng, 0, rel.pairs.length - 1);
    let j = irand(rng, 0, rel.pairs.length - 1);
    if (i === j) j = (j + 1) % rel.pairs.length;
    const a = rel.pairs[i][0];
    const b = rel.pairs[i][1];
    const c = rel.pairs[j][0];
    const d = rel.pairs[j][1];
    const distract = rel.pairs.filter((_, idx) => idx !== j).map((p) => p[1]);
    return emitChoice(rng, `${a} 對於 ${b}，好似 ${c} 對於邊個？`, d, distract, `關係一樣：${rel.name}。`);
  }

  function genClassify(rng, level) {
    const builders = level === "P4" ? [bOdd, bBelongs] : level === "P5" ? [bGroup, bCatName, bAttr] : [bStated, bAnalogy, bCatName];
    return fromBuilders("classify", rng, level, builders, bOdd);
  }

  // ---------- 條件推理 ----------

  const IF_THEN = [
    ["落雨", "帶傘"],
    ["天氣好凍", "穿外套"],
    ["打鈴", "返課室"],
    ["完成功課", "去休息"],
    ["考試合格", "參加旅行"],
    ["天晴", "去野餐"],
    ["肚餓", "食小食"],
    ["圖書館開門", "去借書"],
    ["地面濕滑", "行慢啲"],
    ["老師入課室", "安靜坐下"],
    ["聽到火警鐘", "有序離開"],
    ["到週末", "去公園"],
    ["訓練結束", "飲水"],
    ["做好實驗", "寫報告"],
    ["買到門票", "入閘"],
    ["天色變暗", "開燈"],
  ];

  const ALL_HAVE = [
    ["班上同學", "有書包"],
    ["籃球員", "有球衣"],
    ["合唱團成員", "有歌紙"],
    ["遠足學生", "有水壺"],
    ["游泳隊成員", "有泳帽"],
    ["圖書館義工", "有名牌"],
    ["科學組組員", "有護目鏡"],
    ["畫班學生", "有畫筆"],
    ["管弦樂成員", "有樂譜"],
    ["足球隊隊員", "有波襪"],
    ["升旗隊隊員", "有白手套"],
    ["烘焙組組員", "有廚師帽"],
    ["機械人組組員", "有遙控器"],
    ["合唱比賽選手", "有號碼布"],
    ["單車隊成員", "有頭盔"],
  ];

  const WEEK_CLASS = [
    ["星期一", "中文"],
    ["星期二", "數學"],
    ["星期三", "英文"],
    ["星期四", "常識"],
    ["星期五", "體育"],
    ["星期六", "音樂"],
  ];

  const BOX_OBJS = ["積木", "筆", "波", "貼紙", "鈕", "卡"];
  const BOX_COLORS = ["紅色", "藍色", "綠色", "黃色", "白色", "紫色", "橙色", "黑色"];

  const SOME_CASES = [
    ["同學", "鍾意游泳"],
    ["同學", "鍾意閱讀"],
    ["同學", "戴眼鏡"],
    ["水果", "係紅色"],
    ["筆", "係藍色"],
    ["書", "係中文"],
    ["衫", "有帽"],
    ["動物", "識游水"],
    ["花", "有香味"],
    ["遊戲", "要計時"],
    ["功課", "要畫圖"],
    ["座位", "近窗"],
  ];

  const CMP = [
    { mid: "高", best: "最高", worst: "最矮" },
    { mid: "快", best: "最快", worst: "最慢" },
    { mid: "重", best: "最重", worst: "最輕" },
    { mid: "長", best: "最長", worst: "最短" },
    { mid: "早", best: "最早", worst: "最遲" },
    { mid: "大", best: "最大", worst: "最小" },
    { mid: "多", best: "最多", worst: "最少" },
    { mid: "強", best: "最強", worst: "最弱" },
  ];

  const DID_NEED = [
    { neg: "帶水", ban: "去遠足", did: "去咗遠足", conclude: "有帶水" },
    { neg: "完成功課", ban: "打機", did: "打緊機", conclude: "已完成功課" },
    { neg: "帶學生證", ban: "入圖書館", did: "入咗圖書館", conclude: "有帶學生證" },
    { neg: "穿泳帽", ban: "落水", did: "落咗水", conclude: "有穿泳帽" },
    { neg: "買飛", ban: "入閘", did: "入咗閘", conclude: "有買飛" },
    { neg: "做完實驗", ban: "離開實驗室", did: "離開咗實驗室", conclude: "做完實驗" },
    { neg: "交齊表格", ban: "參加比賽", did: "參加咗比賽", conclude: "交齊表格" },
    { neg: "帶畫筆", ban: "上畫堂", did: "上緊畫堂", conclude: "有帶畫筆" },
    { neg: "通過測驗", ban: "入進階班", did: "入咗進階班", conclude: "通過測驗" },
    { neg: "帶頭盔", ban: "踩單車出場", did: "踩單車出咗場", conclude: "有帶頭盔" },
    { neg: "洗手", ban: "分麵包", did: "分緊麵包", conclude: "洗咗手" },
    { neg: "帶樂譜", ban: "上台演出", did: "上台演出咗", conclude: "有帶樂譜" },
  ];

  const ONLY_IF = [
    { need: "完成功課", done: "已完成功課", act: "打機", acting: "打緊機" },
    { need: "帶學生證", done: "有帶學生證", act: "入圖書館", acting: "入咗圖書館" },
    { need: "穿校服", done: "有穿校服", act: "入校門", acting: "入咗校門" },
    { need: "天晴", done: "今日天晴", act: "去野餐", acting: "去咗野餐" },
    { need: "答啱密語", done: "答啱咗密語", act: "開門", acting: "開咗門" },
    { need: "做會員", done: "係會員", act: "借書", acting: "借到書" },
    { need: "完成練習", done: "已完成練習", act: "打機", acting: "打緊機" },
    { need: "帶水壺", done: "有帶水壺", act: "出發遠足", acting: "出發咗去遠足" },
    { need: "通過初賽", done: "通過咗初賽", act: "入決賽", acting: "入咗決賽" },
    { need: "戴頭盔", done: "有戴頭盔", act: "踩單車", acting: "踩緊單車" },
    { need: "交齊功課", done: "交齊功課", act: "出街玩", acting: "出咗街玩" },
    { need: "買到飛", done: "有買飛", act: "入場", acting: "入咗場" },
    { need: "做完值日", done: "做完值日", act: "返屋企", acting: "返咗屋企" },
    { need: "帶樂譜", done: "有帶樂譜", act: "彩排", acting: "彩排緊" },
  ];

  const UNLESS = [
    { need: "帶齊水壺", done: "有帶水壺", act: "去遠足", did: "去咗遠足" },
    { need: "完成練習", done: "已完成練習", act: "打機", did: "打緊機" },
    { need: "係週末", done: "今日係週末", act: "去遊樂場", did: "去咗遊樂場" },
    { need: "帶學生證", done: "有帶學生證", act: "借器材", did: "借到器材" },
    { need: "預先報名", done: "預先報咗名", act: "參加工作坊", did: "參加咗工作坊" },
    { need: "穿運動鞋", done: "有穿運動鞋", act: "入球場", did: "入咗球場" },
    { need: "交回同意書", done: "交咗同意書", act: "去戶外學習", did: "去咗戶外學習" },
    { need: "通過測驗", done: "通過測驗", act: "升班", did: "升咗班" },
    { need: "帶畫簿", done: "有帶畫簿", act: "上畫堂", did: "上緊畫堂" },
    { need: "洗手", done: "洗咗手", act: "幫手分食物", did: "幫手分緊食物" },
  ];

  const IMPLY = [
    { cond: (n) => `${n}去游泳`, notCond: (n) => `${n}冇去游泳`, result: "件衫濕", notResult: "件衫唔濕" },
    { cond: (n) => `${n}淋到雨`, notCond: (n) => `${n}冇淋到雨`, result: "頭髮濕", notResult: "頭髮唔濕" },
    { cond: (n) => `${n}打開風扇`, notCond: (n) => `${n}冇打開風扇`, result: "風扇轉緊", notResult: "風扇冇轉" },
    { cond: (n) => `${n}按亮燈掣`, notCond: (n) => `${n}冇按亮燈掣`, result: "燈亮", notResult: "燈唔亮" },
    { cond: (n) => `${n}將鹽倒入湯`, notCond: (n) => `${n}冇將鹽倒入湯`, result: "湯變鹹", notResult: "湯冇變鹹" },
    { cond: (n) => `${n}用藍色顏料`, notCond: (n) => `${n}冇用藍色顏料`, result: "幅畫有藍色", notResult: "幅畫冇藍色" },
    { cond: (n) => `${n}踩中水窪`, notCond: (n) => `${n}冇踩中水窪`, result: "對鞋濕", notResult: "對鞋唔濕" },
    { cond: (n) => `${n}打開水龍頭`, notCond: (n) => `${n}冇打開水龍頭`, result: "有水流出", notResult: "冇水流出" },
    { cond: (n) => `${n}撕開糖紙`, notCond: (n) => `${n}冇撕開糖紙`, result: "搵到糖紙屑", notResult: "冇糖紙屑" },
    { cond: (n) => `${n}澆水`, notCond: (n) => `${n}冇澆水`, result: "泥係濕", notResult: "泥唔濕" },
    { cond: (n) => `${n}打開收音機`, notCond: (n) => `${n}冇打開收音機`, result: "聽到廣播", notResult: "聽唔到廣播" },
    { cond: (n) => `${n}撳咗門鈴`, notCond: (n) => `${n}冇撳門鈴`, result: "聽到鈴聲", notResult: "聽唔到鈴聲" },
  ];

  const AND_NEED = [
    { a: "完成功課", b: "帶齊書", act: "打機", acting: "打緊機" },
    { a: "帶水", b: "帶帽", act: "去遠足", acting: "去緊遠足" },
    { a: "穿校服", b: "帶學生證", act: "入校", acting: "入咗校" },
    { a: "買飛", b: "準時到", act: "入場", acting: "入咗場" },
    { a: "交同意書", b: "帶水壺", act: "參加旅行", acting: "參加緊旅行" },
    { a: "通過筆試", b: "通過體能", act: "入校隊", acting: "入咗校隊" },
    { a: "洗手", b: "戴帽", act: "幫手分食物", acting: "幫手分緊食物" },
    { a: "帶樂譜", b: "準時到", act: "上台", acting: "上咗台" },
    { a: "完成值日", b: "關好窗", act: "離開課室", acting: "離開咗課室" },
    { a: "戴頭盔", b: "帶水", act: "出發單車", acting: "出發咗踩單車" },
  ];

  function threeNames(rng) {
    return pickN(rng, NAMES, 3);
  }

  function bIfThen(rng) {
    const pair = pick(rng, IF_THEN);
    const name = pick(rng, NAMES);
    return emitChoice(
      rng,
      `如果${pair[0]}，${name}就${pair[1]}。\n而家${pair[0]}。可以得出？`,
      `${name}${pair[1]}`,
      [`${name}唔會${pair[1]}`, "唔夠資料"],
      "條件成立，結果就成立。"
    );
  }

  function bAllHave(rng) {
    const pair = pick(rng, ALL_HAVE);
    const name = pick(rng, NAMES);
    return emitChoice(
      rng,
      `所有${pair[0]}都${pair[1]}。${name}係${pair[0]}。\n可以得出？`,
      `${name}${pair[1]}`,
      [`${name}冇呢樣`, "唔夠資料"],
      "「所有」包括呢一位。"
    );
  }

  function bWeek(rng) {
    const pair = pick(rng, WEEK_CLASS);
    const name = pick(rng, NAMES);
    return emitChoice(
      rng,
      `如果今日係${pair[0]}，${name}就有${pair[1]}堂。\n今日係${pair[0]}。可以得出？`,
      `${name}今日有${pair[1]}堂`,
      [`${name}今日冇${pair[1]}堂`, "唔夠資料"],
      "條件啱，結果跟住啱。"
    );
  }

  function bBox(rng) {
    const color = pick(rng, BOX_COLORS);
    const obj = pick(rng, BOX_OBJS);
    const name = pick(rng, NAMES);
    return emitChoice(
      rng,
      `盒入面全部係${color}${obj}。${name}攞出一件。\n可以得出？`,
      `攞出嚟嗰件係${color}${obj}`,
      [`攞出嚟嗰件唔係${color}`, "唔夠資料"],
      "「全部」包括攞出嚟嗰件。"
    );
  }

  function bSome(rng) {
    const pair = pick(rng, SOME_CASES);
    const name = pick(rng, NAMES);
    return emitChoice(
      rng,
      `有啲${pair[0]}${pair[1]}。${name}係${pair[0]}。\n可以肯定${name}${pair[1]}嗎？`,
      "唔可以肯定",
      ["可以肯定", "肯定唔係"],
      "「有啲」唔等於「全部」。"
    );
  }

  function bChain(rng) {
    const [a, b, c] = threeNames(rng);
    const cmp = pick(rng, CMP);
    const top = rng() < 0.5;
    const ask = top ? cmp.best : cmp.worst;
    const ans = top ? a : c;
    return emitChoice(
      rng,
      `條件：① ${a}比${b}${cmp.mid} ② ${b}比${c}${cmp.mid}\n邊個一定${ask}？`,
      ans,
      [a, b, c, "唔夠資料"].filter((x) => x !== ans),
      `${a}${cmp.mid}過${b}，${b}${cmp.mid}過${c}。`
    );
  }

  function bOnlyTwo(rng) {
    const [a, b] = pickN(rng, NAMES, 2);
    const cmp = pick(rng, CMP);
    return emitChoice(
      rng,
      `只知道${a}比${b}${cmp.mid}。可以肯定${a}係全班${cmp.best}嗎？`,
      "唔可以肯定",
      ["可以肯定", `一定係${b}${cmp.best}`],
      "仲有其他人未比較。"
    );
  }

  function bDidNeed(rng) {
    const row = pick(rng, DID_NEED);
    const name = pick(rng, NAMES);
    return emitChoice(
      rng,
      `如果唔${row.neg}，就唔可以${row.ban}。\n${name}${row.did}。可以得出？`,
      `${name}${row.conclude}`,
      [`${name}冇${row.neg}`, "唔夠資料"],
      "做到咗，必要條件一定成立。"
    );
  }

  function bScores(rng) {
    const [a, b, c] = threeNames(rng);
    const nums = [];
    while (nums.length < 3) {
      const v = irand(rng, 35, 99);
      if (nums.indexOf(v) < 0) nums.push(v);
    }
    const rows = [
      { n: a, s: nums[0] },
      { n: b, s: nums[1] },
      { n: c, s: nums[2] },
    ];
    const desc = rows.slice().sort((x, y) => y.s - x.s);
    const mode = pick(rng, ["high", "low", "mid"]);
    const ask = mode === "high" ? "最高分" : mode === "low" ? "最低分" : "排第二";
    const ans = mode === "high" ? desc[0].n : mode === "low" ? desc[2].n : desc[1].n;
    return emitChoice(
      rng,
      `分數：${a} ${nums[0]} 分，${b} ${nums[1]} 分，${c} ${nums[2]} 分。\n邊個${ask}？`,
      ans,
      [a, b, c, "唔夠資料"].filter((x) => x !== ans),
      "三個分數都唔同，可以直接排。"
    );
  }

  function bOnlyIf(rng) {
    const row = pick(rng, ONLY_IF);
    const name = pick(rng, NAMES);
    return emitChoice(
      rng,
      `只有${row.need}，先可以${row.act}。\n${name}而家${row.acting}。可以得出？`,
      `${name}${row.done}`,
      [`${name}未${row.need}`, "唔夠資料"],
      "「只有…才…」＝必要條件已經成立。"
    );
  }

  function bUnless(rng) {
    const row = pick(rng, UNLESS);
    const name = pick(rng, NAMES);
    return emitChoice(
      rng,
      `除非${row.need}，否則唔可以${row.act}。\n${name}${row.did}。可以得出？`,
      `${name}${row.done}`,
      [`${name}未${row.need}`, "唔夠資料"],
      "做到咗 ⇒ 除非嗰句條件成立。"
    );
  }

  function bContra(rng) {
    const row = pick(rng, IMPLY);
    const name = pick(rng, NAMES);
    return emitChoice(
      rng,
      `如果${row.cond(name)}，就${row.result}。\n而家${row.notResult}。可以得出？`,
      row.notCond(name),
      [row.cond(name), "唔夠資料"],
      "結果冇發生，條件就冇成立。"
    );
  }

  function bAffirm(rng) {
    const row = pick(rng, IMPLY);
    const name = pick(rng, NAMES);
    return emitChoice(
      rng,
      `如果${row.cond(name)}，就${row.result}。\n而家${row.result}。可以得出？`,
      `唔可以肯定${row.cond(name)}`,
      [`一定係${row.cond(name)}`, `一定係${row.notCond(name)}`],
      "見到結果，唔代表一定係呢個原因。"
    );
  }

  function bDeny(rng) {
    const row = pick(rng, IMPLY);
    const name = pick(rng, NAMES);
    return emitChoice(
      rng,
      `如果${row.cond(name)}，就${row.result}。\n而家${row.notCond(name)}。可以得出？`,
      "唔可以肯定結果",
      [`結果一定係「${row.result}」`, `結果一定係「${row.notResult}」`],
      "條件唔成立，結果仍可能因其他原因出現。"
    );
  }

  function bAndNeed(rng) {
    const row = pick(rng, AND_NEED);
    const name = pick(rng, NAMES);
    return emitChoice(
      rng,
      `只有同時${row.a}同${row.b}，先可以${row.act}。\n${name}${row.acting}。可以得出？`,
      `${name}兩個條件都做到`,
      [`只可以肯定${row.a}`, "唔夠資料"],
      "兩個條件都係必要，缺一不可。"
    );
  }

  function genCondition(rng, level) {
    const builders =
      level === "P4"
        ? [bIfThen, bAllHave, bWeek, bBox]
        : level === "P5"
          ? [bSome, bChain, bOnlyTwo, bDidNeed, bScores]
          : [bOnlyIf, bUnless, bContra, bAffirm, bDeny, bAndNeed];
    return fromBuilders("condition", rng, level, builders, bIfThen);
  }

  // ---------- 圖形／空間 ----------

  const PLACES = ["學校", "公園", "圖書館", "超市", "碼頭", "山頂", "球場", "車站", "博物館", "游泳池", "郵局", "戲院", "醫院", "街市", "社區中心", "禮堂", "科學館", "體育館", "書局", "茶餐廳", "巴士站", "沙灘", "維園", "天星碼頭"];
  const DIRS = ["北", "東", "南", "西"];
  const ARROWS = ["上", "右", "下", "左"];
  const SYM_LETTERS = { A: true, H: true, I: true, M: true, O: true, T: true, U: true, V: true, W: true, X: true, Y: true, B: false, C: false, D: false, E: false, F: false, G: false, J: false, K: false, L: false, N: false, P: false, Q: false, R: false, S: false, Z: false };
  const SYM_SHAPES = [
    ["正方形", "係"],
    ["圓形", "係"],
    ["等邊三角形", "係"],
    ["長方形", "係"],
    ["等腰三角形", "係"],
    ["心形", "係"],
    ["一般平行四邊形", "唔係"],
    ["一般三角形", "唔係"],
    ["字母F", "唔係"],
    ["字母L", "唔係"],
    ["不規則四邊形", "唔係"],
    ["斜箭嘴", "唔係"],
  ];
  const SOLIDS = [
    { name: "正方體", faces: 6, edges: 12, verts: 8 },
    { name: "長方體", faces: 6, edges: 12, verts: 8 },
    { name: "三棱柱", faces: 5, edges: 9, verts: 6 },
    { name: "四棱錐", faces: 5, edges: 8, verts: 5 },
    { name: "三棱錐", faces: 4, edges: 6, verts: 4 },
    { name: "五棱柱", faces: 7, edges: 15, verts: 10 },
    { name: "六棱柱", faces: 8, edges: 18, verts: 12 },
  ];

  function mod4(n) {
    return ((n % 4) + 4) % 4;
  }

  function faceAfter(start, turns) {
    let i = DIRS.indexOf(start);
    turns.forEach((t) => {
      if (t === "右") i += 1;
      else if (t === "左") i -= 1;
      else i += 2;
      i = mod4(i);
    });
    return DIRS[i];
  }

  function paintCount(n, kind) {
    if (kind === "three") return n >= 2 ? 8 : 0;
    if (kind === "two") return n >= 2 ? 12 * (n - 2) : 0;
    if (kind === "one") return n >= 2 ? 6 * (n - 2) * (n - 2) : 0;
    return n >= 2 ? (n - 2) * (n - 2) * (n - 2) : 0;
  }

  function hourPlus(s, delta) {
    return ((s - 1 + delta) % 12) + 1;
  }

  function nearNums(ans, extra) {
    const n = Number(ans);
    return [n + 1, n - 1, n + 2, n * 2, n + 3, n - 2, n + 4, n + 5]
      .concat(extra || [])
      .filter((x) => x !== n && x >= 0)
      .map(String);
  }

  function bLetter(rng) {
    const keys = Object.keys(SYM_LETTERS);
    const L = pick(rng, keys);
    const ans = SYM_LETTERS[L] ? "係" : "唔係";
    return emitChoice(rng, `字母「${L}」左右對稱嗎？`, ans, ["係", "唔係", "睇字體先至知"], ans === "係" ? "左右對摺可以重合。" : "左右對摺唔會重合。");
  }

  function bFold(rng) {
    const n = irand(rng, 1, 6);
    const ans = String(2 ** n);
    return emitChoice(
      rng,
      `一張紙對摺 ${n} 次（每次對半），最多可以分成幾多塊一樣大？`,
      ans,
      nearNums(ans, [n, n * 2, n + 1]),
      `每對摺一次，塊數 ×2，所以係 ${ans}。`
    );
  }

  function bHoles(rng) {
    const n = irand(rng, 1, 6);
    const ans = String(2 ** n);
    return emitChoice(
      rng,
      `紙對摺 ${n} 次（每次對半），用針一次穿過所有層。打開後有幾多個小孔？`,
      ans,
      nearNums(ans, [n, n * 2]),
      `每摺一次層數 ×2，小孔數係 ${ans}。`
    );
  }

  function bPoly(rng) {
    const n = irand(rng, 3, 10);
    const ans = POLY[n];
    const wrong = Object.keys(POLY)
      .map((k) => POLY[k])
      .concat(["圓形"]);
    return emitChoice(rng, `一個平面圖形有 ${n} 條直邊，佢係邊類？`, ans, wrong, `${n} 條直邊 → ${ans}。`);
  }

  function bSticks(rng) {
    const n = irand(rng, 3, 8);
    const ans = POLY[n];
    const wrong = ["圓形", "直線", POLY[n === 8 ? 3 : n + 1], POLY[n === 3 ? 6 : n - 1]];
    return emitChoice(rng, `用 ${n} 條一樣長嘅棒圍一個多邊形，最容易圍成邊類？`, ans, wrong, `${n} 條等長邊可以圍成${ans}。`);
  }

  function bShapeSym(rng) {
    const row = pick(rng, SYM_SHAPES);
    return emitChoice(rng, `「${row[0]}」左右對稱嗎？`, row[1], ["係", "唔係", "一定要轉個角度先知"], row[1] === "係" ? "有一條左右對稱線。" : "一般冇左右對稱線。");
  }

  function bPath(rng, lo, hi) {
    const n = irand(rng, lo, hi);
    const route = pickN(rng, PLACES, n);
    const segs = n - 1;
    return emitChoice(
      rng,
      `路徑：${route.join("→")}。由${route[0]}去${route[n - 1]}沿呢條路行，經過幾段？`,
      String(segs),
      nearNums(segs, [n, 1]),
      `${n} 個地方，段數 = 地方數 − 1 = ${segs}。`
    );
  }

  function bStop(rng) {
    const n = irand(rng, 3, 6);
    const route = pickN(rng, PLACES, n);
    const k = irand(rng, 1, n);
    const ans = route[k - 1];
    const wrong = route.filter((x) => x !== ans).concat(pickN(rng, PLACES.filter((p) => route.indexOf(p) < 0), 2));
    return emitChoice(
      rng,
      `路徑：${route.join("→")}。由起點數起，第 ${k} 個地方係邊度？（起點係第 1 個）`,
      ans,
      wrong,
      `數第 ${k} 個係「${ans}」。`
    );
  }

  function bShort(rng) {
    const [p, q] = pickN(rng, PLACES, 2);
    const mode = pick(rng, ["lt", "gt", "eq"]);
    const a = irand(rng, 2, 9);
    let b = mode === "eq" ? a : irand(rng, 2, 12);
    if (mode === "lt" && b <= a) b = a + 1 + irand(rng, 0, 3);
    if (mode === "gt" && b >= a) b = Math.max(1, a - 1 - irand(rng, 0, 2));
    if (mode !== "eq" && a === b) b = a + 1;
    const ans = a < b ? "A 路" : a > b ? "B 路" : "一樣長";
    return emitChoice(
      rng,
      `由${p}去${q}：A 路 ${a} 段，B 路 ${b} 段，每段一樣長。邊條路最短？`,
      ans,
      ["A 路", "B 路", "一樣長", "唔夠資料"],
      a === b ? "段數一樣。" : `段數少嘅較短（${Math.min(a, b)} 段）。`
    );
  }

  function bArrow(rng) {
    const start = pick(rng, ARROWS);
    const k = irand(rng, 1, 3);
    const ans = ARROWS[mod4(ARROWS.indexOf(start) + k)];
    return emitChoice(
      rng,
      `箭嘴原本指${start}，順時針轉 ${k} 次（每次 90°）。而家指邊？`,
      ans,
      ARROWS,
      `順時針 ${k} 次，由「${start}」去到「${ans}」。`
    );
  }

  function bFace(rng, steps) {
    const start = pick(rng, DIRS);
    const turns = [];
    for (let i = 0; i < steps; i++) turns.push(pick(rng, ["左", "右", "後"]));
    const ans = faceAfter(start, turns);
    const prompt =
      steps === 1
        ? `你面朝${start}，向${turns[0]}轉 1 次（左或右每次 90°，後轉 180°）。而家面朝邊？`
        : `你面朝${start}。動作：${turns.map((t) => "向" + t + "轉").join("，")}（左或右每次 90°，後轉 180°）。而家面朝邊？`;
    return emitChoice(rng, prompt, ans, DIRS, `轉完面朝${ans}。`);
  }

  function bGrid(rng) {
    const r = irand(rng, 1, 12);
    const c = irand(rng, 1, 12);
    const ans = r * c;
    return emitChoice(
      rng,
      `長方形格網有 ${r} 行、每行 ${c} 格。一共有幾多格？`,
      String(ans),
      nearNums(ans, [r + c, r * c + r, r * c - c]),
      `${r} × ${c} = ${ans}。`
    );
  }

  function bManhattan(rng) {
    const x = irand(rng, 1, 12);
    const y = irand(rng, 1, 12);
    const ans = x + y;
    return emitChoice(
      rng,
      `格線上由原點行右 ${x} 格、再行上 ${y} 格。沿格線行，最短一共幾多格？`,
      String(ans),
      nearNums(ans, [x * y, Math.abs(x - y)]),
      `右 ${x} 加 上 ${y}，最短 ${ans} 格。`
    );
  }

  function bCoord(rng) {
    const x = irand(rng, 0, 9);
    const y = irand(rng, 0, 9);
    if (x === 0 && y === 0) return null;
    const ans = `(${1 + x},${1 + y})`;
    return emitChoice(
      rng,
      `方格紙座標（橫,直）。由 (1,1) 向右 ${x} 格、向上 ${y} 格，到達邊個座標？`,
      ans,
      [`(${1 + y},${1 + x})`, `(${x},${y})`, `(${1 + x},${y})`, `(${x},${1 + y})`, `(${2 + x},${1 + y})`],
      `橫 1+${x}，直 1+${y}。`
    );
  }

  function bLine(rng) {
    const names = pickN(rng, NAMES, 4);
    const askLeft = rng() < 0.5;
    const ans = askLeft ? names[0] : names[3];
    return emitChoice(
      rng,
      `由左至右排：${names.join("、")}。${askLeft ? "最左邊" : "最右邊"}係邊個？`,
      ans,
      names,
      askLeft ? "排第一個就係最左。" : "排最後一個就係最右。"
    );
  }

  function bJoin(rng) {
    const iso = rng() < 0.5;
    if (iso) {
      return emitChoice(
        rng,
        "用兩個完全一樣嘅等腰直角三角形，斜邊貼斜邊，可以拼成邊類？",
        "正方形",
        ["圓形", "一般五邊形", "長方形但一定唔係正方形"],
        "等腰直角三角形斜邊相對，可以拼成正方形。"
      );
    }
    return emitChoice(
      rng,
      "用兩個完全一樣嘅直角三角形，斜邊貼斜邊，可以拼成邊類？",
      "長方形",
      ["圓形", "一般五邊形", "只可以拼成三角形"],
      "兩個全等直角三角形斜邊相對，可以拼成長方形。"
    );
  }

  function bDice(rng) {
    const k = irand(rng, 1, 6);
    const ans = 7 - k;
    return emitChoice(
      rng,
      `標準骰仔對面兩數加起係 7。上面係 ${k}，下面係幾多？`,
      String(ans),
      nearNums(ans, [k, 7, 1, 6]),
      `7 − ${k} = ${ans}。`
    );
  }

  function bPaint(rng) {
    const n = irand(rng, 2, 8);
    const kinds = [
      ["three", "三面都有色"],
      ["two", "剛好兩面有色"],
      ["one", "只有一面有色"],
      ["zero", "完全冇色"],
    ];
    const kind = pick(rng, kinds);
    const ans = paintCount(n, kind[0]);
    return emitChoice(
      rng,
      `正方體外面塗滿色，切成 ${n}×${n}×${n} 粒細正方體。${kind[1]}有幾多粒？`,
      String(ans),
      nearNums(ans, [8, 6 * n, n * n, n * n * n, 12 * (n - 2)]),
      kind[0] === "three"
        ? "只有 8 個角有三面色。"
        : kind[0] === "two"
          ? `每條棱中間有 ${n - 2} 粒，12 條棱，共 ${ans}。`
          : kind[0] === "one"
            ? `每面中間有 ${n - 2}×${n - 2} 粒，6 面，共 ${ans}。`
            : `入面 ${(n - 2)}³ = ${ans} 粒冇色。`
    );
  }

  function bSolid(rng) {
    const s = pick(rng, SOLIDS);
    const ask = pick(rng, [
      ["faces", "面"],
      ["edges", "棱"],
      ["verts", "頂點"],
    ]);
    const ans = s[ask[0]];
    return emitChoice(
      rng,
      `一個${s.name}有幾多個${ask[1]}？`,
      String(ans),
      [s.faces, s.edges, s.verts, ans + 1, Math.max(0, ans - 1), ans + 2].map(String),
      `${s.name}有 ${ans} 個${ask[1]}。`
    );
  }

  function bClock(rng) {
    const s = irand(rng, 1, 12);
    const delta = pick(rng, [3, 6, 9]);
    const e = hourPlus(s, delta);
    const ans = delta / 3;
    return emitChoice(
      rng,
      `時鐘短針由 ${s} 點順時針行到 ${e} 點。行咗幾多個直角？（順時針計，1 直角 = 90°）`,
      String(ans),
      nearNums(ans, [delta, 4, 2, 12]),
      `順時針行 ${delta} 小時，每 3 小時一個直角，共 ${ans} 個。`
    );
  }

  function bVolume(rng) {
    const x = irand(rng, 1, 6);
    const y = irand(rng, 1, 6);
    const z = irand(rng, 1, 6);
    const ans = x * y * z;
    return emitChoice(
      rng,
      `用細正方體砌一個長方體，長 ${x} 粒、闊 ${y} 粒、高 ${z} 粒。一共要用幾多粒？`,
      String(ans),
      nearNums(ans, [x + y + z, x * y, x * z]),
      `${x} × ${y} × ${z} = ${ans}。`
    );
  }

  function genSpatial(rng, level) {
    const builders =
      level === "P4"
        ? [bLetter, bFold, bPoly, bShapeSym, () => bPath(rng, 2, 3), bArrow, () => bFace(rng, 1), bGrid, bLine, bJoin]
        : level === "P5"
          ? [() => bPath(rng, 3, 6), bStop, bShort, bSticks, bManhattan, () => bFace(rng, 2), bHoles, bVolume, bCoord, bArrow]
          : [bPaint, bDice, bSolid, () => bFace(rng, 3), bClock, () => bPath(rng, 5, 8), bManhattan, bHoles];
    // wrappers above call rng themselves; fromBuilders also calls builder(rng). Normalize.
    const wrapped = builders.map((fn) => {
      if (fn.length === 0) return function () { return fn(); };
      return fn;
    });
    return fromBuilders("spatial", rng, level, wrapped, () => bPath(rng, 2, 4));
  }

  // ---------- 真假 ----------

  const TALK = [
    { mine: "我今日有帶水壺", other: "今日冇帶水壺" },
    { mine: "我完成晒功課", other: "仲有功課未做" },
    { mine: "我有去圖書館", other: "冇去圖書館" },
    { mine: "我鍾意游泳", other: "唔鍾意游泳" },
    { mine: "我今日穿紅色衫", other: "今日冇穿紅色衫" },
    { mine: "我有交功課", other: "未交功課" },
    { mine: "我識游水", other: "唔識游水" },
    { mine: "我今日食咗水果", other: "今日冇食水果" },
    { mine: "我住喺學校附近", other: "唔住喺學校附近" },
    { mine: "我有參加比賽", other: "冇參加比賽" },
    { mine: "我今日行樓梯", other: "今日冇行樓梯" },
    { mine: "我借咗故事書", other: "冇借故事書" },
    { mine: "我有帶鎖匙", other: "冇帶鎖匙" },
    { mine: "我今朝食早餐", other: "今朝冇食早餐" },
  ];

  const OPEN_SUBJ = ["圖書館", "泳池", "科學館", "課室", "公園", "茶餐廳", "球場", "博物館", "禮堂", "超市", "體育館", "戲院", "醫院", "街市", "社區中心", "書局"];
  const OPEN_PAIRS = [
    ["今日全日開放", "今日全日關閉"],
    ["入面坐滿人", "入面一個人都冇"],
    ["燈全部開", "燈全部熄"],
    ["今日免費入場", "今日一定要買飛"],
    ["而家開住門", "而家鎖住門"],
    ["今日有活動", "今日完全冇活動"],
    ["而家可以入去", "而家禁止入去"],
    ["今日照常開放", "今日休息唔開"],
  ];
  const OPEN_NOISE = ["出面落緊雨", "附近有巴士站", "牆身係白色", "門口有大鐘", "有人喺對面馬路行", "門口有盆栽"];

  const UNIV_ROWS = [
    ["同學", "交咗功課", "未交功課", "今日遲到", "帶咗水樽"],
    ["同學", "返到學", "未返到學", "穿紅色襪", "坐前排"],
    ["球員", "帶咗球衣", "未帶球衣", "今朝跑步", "飲咗水"],
    ["參加者", "交咗報名表", "未交報名表", "帶咗帽", "識唱歌"],
    ["考生", "帶備文具", "未帶備文具", "早到", "坐近窗"],
    ["隊員", "戴上頭盔", "未戴頭盔", "綁好鞋帶", "飲咗水"],
    ["觀眾", "坐低", "未坐低", "拍手", "帶咗袋"],
    ["義工", "簽到", "未簽到", "穿白衫", "識講故事"],
    ["組員", "交回器材", "未交回器材", "寫咗名", "今日開心"],
    ["學生", "交齊閱讀紀錄", "未交閱讀紀錄", "借咗書", "坐校巴"],
    ["選手", "量過體重", "未量體重", "做咗熱身", "帶咗毛巾"],
    ["團員", "交回歌紙", "未交回歌紙", "站好", "飲過水"],
  ];
  const UNIV_WHEN = ["今日", "今朝", "呢一輪", "今個星期"];

  const ACTS = ["打破杯", "打翻水杯", "整污白板", "遺失鎖匙", "踩扁皮球", "畫花牆", "弄壞模型", "忘記關燈", "打翻顏料", "弄散樂譜"];

  const FACT_PLACES = ["圖書館", "課室", "禮堂", "操場", "音樂室", "飯堂", "醫療室", "電腦室", "花園", "走廊"];
  const FACT_THINGS = ["故事書", "水壺", "雨傘", "學生證", "口琴", "足球", "畫簿", "鎖匙", "保溫杯", "名牌"];
  const FACT_COLORS = ["紅色", "藍色", "綠色", "黃色", "白色", "紫色", "橙色", "黑色"];
  const FACT_ITEMS = ["塊布", "個波", "枝筆", "頂帽", "個盒", "張卡", "條絲帶", "隻袋"];

  const ALWAYS_ROWS = [
    ["校巴", "準時開出", "遲到開出"],
    ["呢條路", "暢通", "封閉"],
    ["校門", "準時開", "遲開"],
    ["水機", "有水", "冇水"],
    ["課室鐘", "準時響", "唔響"],
    ["電梯", "正常行", "停用"],
    ["泳池", "開放", "關閉"],
    ["路燈", "會在傍晚亮", "在傍晚唔亮"],
    ["校車冷氣", "開到", "開唔到"],
    ["圖書館", "準時開門", "遲開門"],
    ["飯堂", "準時開飯", "遲開飯"],
    ["朝早廣播", "有播出", "冇播出"],
    ["灑水系統", "按時灑", "冇灑"],
    ["校門燈", "會在天黑亮起", "在天黑仍然唔亮"],
    ["小賣部", "會在小息開門", "在小息關住"],
    ["渡輪", "準時開", "遲開"],
    ["斑馬線燈", "按時轉", "停咗唔轉"],
    ["空調", "會在夏天開到", "在夏天開唔到"],
  ];

  function bCantTell(rng) {
    const [n0, n1] = pickN(rng, NAMES, 2);
    const t = pick(rng, TALK);
    return emitChoice(
      rng,
      `${n0}話：「${t.mine}。」\n${n1}話：「${n0}${t.other}。」\n已知恰好一人講真話。可以肯定邊個講假嗎？`,
      "唔夠資料",
      [`${n0}講假`, `${n1}講假`, "兩個都假"],
      "兩句互相矛盾，一定一真一假，但未知邊句真。"
    );
  }

  function bWhichContradict(rng) {
    const subj = pick(rng, OPEN_SUBJ);
    const pair = pick(rng, OPEN_PAIRS);
    const noise = pick(rng, OPEN_NOISE);
    return emitChoice(
      rng,
      `邊兩句互相矛盾？\nA. ${subj}${pair[0]}\nB. ${subj}${pair[1]}\nC. ${subj}${noise}`,
      "A 同 B",
      ["A 同 C", "B 同 C", "三句都矛盾"],
      `「${pair[0]}」同「${pair[1]}」唔可以同時成立。`
    );
  }

  function bUnivContradict(rng) {
    const row = pick(rng, UNIV_ROWS);
    const when = pick(rng, UNIV_WHEN);
    const stem = `全部${row[0]}${when}都${row[1]}`;
    const ans = `有${row[0]}${when}${row[2]}`;
    return emitChoice(
      rng,
      `邊句同「${stem}」矛盾？`,
      ans,
      [`有${row[0]}${when}${row[3]}`, `有${row[0]}${when}${row[4]}`, "以上都唔矛盾"],
      `「全部都${row[1]}」同「有人${row[2]}」相反。`
    );
  }

  function bAccuse(rng) {
    const [n0, n1, n2] = threeNames(rng);
    const act = pick(rng, ACTS);
    // n1 真 ⇒ n0 做咗 ⇒ n0「我冇做」為假；n2「唔係我」仍可真。恰好 n0 假。
    return emitChoice(
      rng,
      `三人中恰好一人講假。\n${n0}：「我冇${act}。」\n${n1}：「係${n0}${act}。」\n${n2}：「唔係我${act}。」\n如果${n1}講真話，邊個講假？`,
      n0,
      [n1, n2, "無法判斷"],
      `${n1}真 ⇒ 係${n0}${act} ⇒ ${n0}句假。`
    );
  }

  function bFactPlace(rng) {
    const [n0, n1, n2] = threeNames(rng);
    const thing = pick(rng, FACT_THINGS);
    const places = pickN(rng, FACT_PLACES, 3);
    const who = irand(rng, 0, 2);
    const names = [n0, n1, n2];
    const lines = names.map((n, i) => `${n}：「喺${places[i]}。」`).join("\n");
    return emitChoice(
      rng,
      `已知${thing}而家喺${places[who]}。\n${lines}\n邊個講真話？`,
      names[who],
      names.concat(["無法判斷"]).filter((x) => x !== names[who]),
      `事實係喺${places[who]}，所以${names[who]}講啱。`
    );
  }

  function bFactNumber(rng) {
    const [n0, n1, n2] = threeNames(rng);
    const truth = irand(rng, 2, 40);
    const wrongs = [];
    while (wrongs.length < 2) {
      const v = irand(rng, 1, 48);
      if (v !== truth && wrongs.indexOf(v) < 0) wrongs.push(v);
    }
    const who = irand(rng, 0, 2);
    const names = [n0, n1, n2];
    const nums = [0, 0, 0];
    let w = 0;
    for (let i = 0; i < 3; i++) nums[i] = i === who ? truth : wrongs[w++];
    const lines = names.map((n, i) => `${n}話：「有 ${nums[i]} 粒。」`).join("\n");
    return emitChoice(
      rng,
      `已知糖有 ${truth} 粒。\n${lines}\n邊個講真話？`,
      names[who],
      names.concat(["無法判斷"]).filter((x) => x !== names[who]),
      `只有講 ${truth} 粒嗰位先啱。`
    );
  }

  function bFactColor(rng) {
    const [n0, n1, n2] = threeNames(rng);
    const item = pick(rng, FACT_ITEMS);
    const colors = pickN(rng, FACT_COLORS, 3);
    const who = irand(rng, 0, 2);
    const names = [n0, n1, n2];
    const lines = names.map((n, i) => `${n}：「係${colors[i]}。」`).join("\n");
    return emitChoice(
      rng,
      `已知${item}係${colors[who]}。\n${lines}\n邊個講真話？`,
      names[who],
      names.concat(["無法判斷"]).filter((x) => x !== names[who]),
      `事實係${colors[who]}，${names[who]}講啱。`
    );
  }

  function bLiarB(rng) {
    const [a, b] = pickN(rng, NAMES, 2);
    // 若 b 真則兩人都真，但 a 話 b 假，矛盾。故 b 假、a 真。
    return emitChoice(
      rng,
      `${a}話：「${b}講大話。」\n${b}話：「我同${a}都講真話。」\n邊個一定講大話？`,
      b,
      [a, "兩個都假", "兩個都真"],
      `若${b}真，就同${a}句矛盾；所以${b}講大話。`
    );
  }

  function bLiarA(rng) {
    const [a, b] = pickN(rng, NAMES, 2);
    // 若 a 真則兩人都真，但 b 話 a 假，矛盾。故 a 假、b 真。
    return emitChoice(
      rng,
      `${a}話：「我哋兩個都講真話。」\n${b}話：「${a}講大話。」\n邊個一定講大話？`,
      a,
      [b, "兩個都假", "兩個都真"],
      `若${a}真，${b}就唔可以話${a}假；所以${a}講大話。`
    );
  }

  function bAtLeast(rng) {
    const [a, b] = pickN(rng, NAMES, 2);
    // 若 a 假，則「至少一人假」為假 ⇒ 兩人都真，矛盾。故 a 真（同時 b 必假，但選項只問 a）。
    return emitChoice(
      rng,
      `${a}：「至少我哋其中一個講假。」\n${b}：「我講真話。」\n邊句可以肯定？`,
      `${a}一定講真話`,
      [`${a}一定講假`, "兩個都講真話", "兩個都講假"],
      `若${a}假，就變成兩個都真，同佢句矛盾；所以${a}真。`
    );
  }

  function bAlways(rng) {
    const row = pick(rng, ALWAYS_ROWS);
    const ans = `${row[0]}曾經有一次${row[2]}`;
    return emitChoice(
      rng,
      `邊句同「${row[0]}每次都${row[1]}」矛盾？`,
      ans,
      [`${row[0]}多數都${row[1]}`, `${row[0]}附近好熱鬧`, "以上都唔矛盾"],
      `「每次都」同「曾經有一次相反」矛盾。`
    );
  }

  function genTruth(rng, level) {
    const builders =
      level === "P4"
        ? [bCantTell, bWhichContradict]
        : level === "P5"
          ? [bUnivContradict, bAccuse, bFactPlace, bFactNumber]
          : [bLiarB, bLiarA, bAtLeast, bAlways, bFactColor];
    return fromBuilders("truth", rng, level, builders, bCantTell);
  }

  function assertBanks() {
    const seen = new Map();
    if (GROUPS.length < 30) throw new Error("classify groups thin");
    GROUPS.forEach((g) => {
      if (!g.name || g.members.length < 4) throw new Error("short group " + g.name);
      const set = new Set(g.members);
      if (set.size !== g.members.length) throw new Error("dup in " + g.name);
      if (set.has(g.odd)) throw new Error("odd in " + g.name);
      g.members.forEach((m) => {
        if (seen.has(m)) throw new Error("cross " + m + " " + seen.get(m) + "/" + g.name);
        seen.set(m, g.name);
      });
    });
    RULE_PACKS.forEach((g) => {
      const set = new Set(g.members);
      if (set.size !== g.members.length || set.has(g.odd)) throw new Error("rule " + g.rule);
    });
    RELATIONS.forEach((rel) => {
      const left = new Set();
      const right = new Set();
      rel.pairs.forEach((p) => {
        if (left.has(p[0]) || right.has(p[1])) throw new Error("rel " + rel.name + " " + p.join("-"));
        left.add(p[0]);
        right.add(p[1]);
      });
    });
    if (paintCount(3, "one") !== 6 || paintCount(3, "two") !== 12 || paintCount(3, "three") !== 8 || paintCount(3, "zero") !== 1) {
      throw new Error("paint");
    }
    if (paintCount(2, "one") !== 0 || paintCount(4, "zero") !== 8) throw new Error("paint2");
    if (faceAfter("北", ["右"]) !== "東" || faceAfter("北", ["左"]) !== "西" || faceAfter("北", ["後"]) !== "南") {
      throw new Error("face");
    }
    if (faceAfter("東", ["右", "右"]) !== "西") throw new Error("face2");
    if (hourPlus(12, 3) !== 3 || hourPlus(10, 6) !== 4 || hourPlus(11, 9) !== 8) throw new Error("hour");
  }

  assertBanks();

  const GENERATORS = {
    pattern: genPattern,
    classify: genClassify,
    condition: genCondition,
    spatial: genSpatial,
    truth: genTruth,
  };

  const LEVELS = ["P4", "P5", "P6"];

  function buildDailySet(catId, dateStr, usedIds, perDay) {
    const seed = hashStr(`${dateStr}|${catId}|v4-rich-pool`);
    const used = new Set(usedIds || []);
    const out = [];
    const seenContent = new Set();
    let guard = 0;

    function tryPush(q) {
      if (!q) return false;
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
      const q = gen(mulberry32((seed + guard * 9973) >>> 0), level);
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
})(typeof window !== "undefined" ? window : globalThis);
