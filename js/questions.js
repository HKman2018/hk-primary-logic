/** 正式樣本題庫（繁中・港小用語）。每日動態題見 generators.js；本檔作規格示範同離線參考。 */
window.LOGIC_BANK = {
  pattern: {
    id: "pattern",
    name: "找規律／數列",
    blurb: "找出規律，推下一步",
    questions: [
      {
        id: "p1",
        level: "P4",
        prompt: "數列：2、4、6、8、？\n下一個數係幾多？",
        type: "choice",
        choices: ["9", "10", "12", "14"],
        answer: "10",
        hint: "每次加 2。"
      },
      {
        id: "p2",
        level: "P4",
        prompt: "圖案規律：○ □ ○ □ ○ ？\n下一個應該係邊個？",
        type: "choice",
        choices: ["○", "□", "△", "◇"],
        answer: "□",
        hint: "○ 同 □ 交替出現。"
      },
      {
        id: "p3",
        level: "P5",
        prompt: "數列：1、2、4、7、11、？\n下一個數係幾多？",
        type: "fill",
        answer: "16",
        hint: "相差依次係 +1、+2、+3、+4…"
      },
      {
        id: "p4",
        level: "P5",
        prompt: "數列：3、6、5、10、9、18、？\n下一個數係幾多？",
        type: "choice",
        choices: ["17", "20", "27", "36"],
        answer: "17",
        hint: "×2 再 −1，交替進行。"
      },
      {
        id: "p5",
        level: "P6",
        prompt: "數列：2、6、12、20、30、？\n下一個數係幾多？",
        type: "fill",
        answer: "42",
        hint: "相差係連續偶數：+4、+6、+8、+10…"
      }
    ]
  },
  classify: {
    id: "classify",
    name: "分類／歸類",
    blurb: "按屬性歸類，搵異類",
    questions: [
      {
        id: "c1",
        level: "P4",
        prompt: "邊個唔屬於同一類？\n蘋果、香蕉、橙、汽車",
        type: "choice",
        choices: ["蘋果", "香蕉", "橙", "汽車"],
        answer: "汽車",
        hint: "其餘都係水果。"
      },
      {
        id: "c2",
        level: "P4",
        prompt: "邊個同其余形狀唔同？\n圓、球、環、正方形",
        type: "choice",
        choices: ["圓", "球", "環", "正方形"],
        answer: "正方形",
        hint: "前三個都同「圓」有關。"
      },
      {
        id: "c3",
        level: "P5",
        prompt: "要同時滿足「紅色」同「圓形」。邊個啱？",
        type: "choice",
        choices: ["紅方塊", "藍圓形", "紅圓形", "黃三角形"],
        answer: "紅圓形",
        hint: "兩個條件一齊要啱。"
      },
      {
        id: "c4",
        level: "P5",
        prompt: "邊組分類最合理？\n貓、狗、麻雀、金魚",
        type: "choice",
        choices: [
          "貓狗｜麻雀金魚（陸上／其他）",
          "貓狗麻雀｜金魚（寵物／非寵物）",
          "全部一樣，唔使分"
        ],
        answer: "貓狗｜麻雀金魚（陸上／其他）",
        hint: "可用「會唔會飛／游」等屬性想。"
      },
      {
        id: "c5",
        level: "P6",
        prompt: "邊樣唔屬於「可以摺疊」？\n紙、布、膠紙、玻璃板",
        type: "choice",
        choices: ["紙", "布", "膠紙", "玻璃板"],
        answer: "玻璃板",
        hint: "玻璃板硬而且易碎，唔適宜摺。"
      }
    ]
  },
  condition: {
    id: "condition",
    name: "條件推理",
    blurb: "跟住條件推結論",
    questions: [
      {
        id: "r1",
        level: "P4",
        prompt: "如果今天下雨，阿明就帶傘。\n今天下雨。可以得出邊個結論？",
        type: "choice",
        choices: ["阿明帶傘", "阿明唔帶傘", "唔夠資料"],
        answer: "阿明帶傘",
        hint: "條件成立，結果就成立。"
      },
      {
        id: "r2",
        level: "P4",
        prompt: "班上所有同學都有書包。小華係班上同學。\n可以得出？",
        type: "choice",
        choices: ["小華有書包", "小華冇書包", "唔夠資料"],
        answer: "小華有書包",
        hint: "「全部」包括小華。"
      },
      {
        id: "r3",
        level: "P5",
        prompt: "有啲水果係紅色。蘋果係水果。\n可以肯定蘋果係紅色嗎？",
        type: "choice",
        choices: ["可以肯定係紅色", "唔可以肯定", "肯定唔係紅色"],
        answer: "唔可以肯定",
        hint: "「有啲」唔等於「全部」。"
      },
      {
        id: "r4",
        level: "P5",
        prompt: "條件：① 阿美比阿強高 ② 阿強比阿傑高\n邊句一定啱？",
        type: "choice",
        choices: ["阿美最高", "阿傑最高", "阿強最矮", "唔夠資料"],
        answer: "阿美最高",
        hint: "由①②可得阿美 > 阿強 > 阿傑。"
      },
      {
        id: "r5",
        level: "P6",
        prompt: "只有完成功課，先可以打機。\n小明而家打緊機。可以得出？",
        type: "choice",
        choices: ["小明已完成功課", "小明未完成功課", "唔夠資料"],
        answer: "小明已完成功課",
        hint: "「只有…才…」＝必要條件。"
      }
    ]
  },
  spatial: {
    id: "spatial",
    name: "圖形／空間",
    blurb: "旋轉、對稱、拼合、路徑",
    questions: [
      {
        id: "s1",
        level: "P4",
        prompt: "字母「H」左右對稱嗎？",
        type: "choice",
        choices: ["係", "唔係", "睇旋轉方向"],
        answer: "係",
        hint: "左右對摺可以重合。"
      },
      {
        id: "s2",
        level: "P4",
        prompt: "正方形順時針轉 90°，外形會唔會變？",
        type: "choice",
        choices: ["會變成菱形", "外形不變", "會變成長方形"],
        answer: "外形不變",
        hint: "正方形轉 90° 仍然係正方形。"
      },
      {
        id: "s3",
        level: "P5",
        prompt: "一條路：學校→公園→圖書館。\n由學校去圖書館，最少經過幾段路？（只計上面呢條）",
        type: "choice",
        choices: ["1", "2", "3", "4"],
        answer: "2",
        hint: "學校→公園、公園→圖書館，兩段。"
      },
      {
        id: "s4",
        level: "P5",
        prompt: "用兩個一樣嘅直角三角形，最容易拼成邊個形？",
        type: "choice",
        choices: ["正方形或長方形", "圓形", "五邊形"],
        answer: "正方形或長方形",
        hint: "斜邊對斜邊，可以拼成矩形。"
      },
      {
        id: "s5",
        level: "P6",
        prompt: "一個正方體紙盒展開後，最多可以見到幾個正方形面？",
        type: "choice",
        choices: ["4", "5", "6", "8"],
        answer: "6",
        hint: "正方體有六個面。"
      }
    ]
  },
  truth: {
    id: "truth",
    name: "真假／矛盾",
    blurb: "搵邊句假、邊句互相矛盾",
    questions: [
      {
        id: "t1",
        level: "P4",
        prompt: "阿文話：「我今日冇食糖。」\n阿珍話：「阿文食咗糖。」\n已知只有一人講真話。邊個講假？",
        type: "choice",
        choices: ["阿文講假", "阿珍講假", "兩個都假", "唔夠資料"],
        answer: "唔夠資料",
        hint: "兩句互相矛盾，必定一真一假，但未知邊個真。"
      },
      {
        id: "t2",
        level: "P4",
        prompt: "邊兩句互相矛盾？\nA. 今日全日落雨\nB. 今日全日無半滴雨\nC. 今日有人帶傘",
        type: "choice",
        choices: ["A 同 B", "A 同 C", "B 同 C", "三句都矛盾"],
        answer: "A 同 B",
        hint: "「全日落雨」同「全日無雨」唔可以同時啱；帶傘唔一定矛盾。"
      },
      {
        id: "t3",
        level: "P5",
        prompt: "三人中恰好一人講假。\n小明：「我冇打破杯。」\n小華：「係小明打破。」\n小美：「唔係我打破。」\n如果小華講真話，邊個講假？",
        type: "choice",
        choices: ["小明", "小華", "小美", "無法判斷"],
        answer: "小明",
        hint: "小華真 ⇒ 小明打破 ⇒ 小明句假；小美可以真。"
      },
      {
        id: "t4",
        level: "P5",
        prompt: "邊句同「全部同學都交咗功課」矛盾？",
        type: "choice",
        choices: [
          "有同學今日遲到",
          "有同學未交功課",
          "有同學交得多過一份"
        ],
        answer: "有同學未交功課",
        hint: "「全部都交」同「有人未交」相反。"
      },
      {
        id: "t5",
        level: "P6",
        prompt: "阿強話：「阿傑講大話。」\n阿傑話：「我同阿強都講真話。」\n邊個一定講大話？",
        type: "choice",
        choices: ["阿強", "阿傑", "兩個都假", "兩個都真"],
        answer: "阿傑",
        hint: "若阿傑真，則兩人都真，但阿強又話阿傑假，矛盾；故阿傑假。"
      }
    ]
  }
};
