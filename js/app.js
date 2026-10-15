(function () {
  const bank = window.LOGIC_BANK;
  const Daily = window.LogicDaily;
  const STORAGE_USED = "hk-logic-used-ids-v1";
  const STORAGE_DAY = "hk-logic-day-cache-v1";
  const PER_DAY = 5;

  const els = {
    home: document.getElementById("home"),
    quiz: document.getElementById("quiz"),
    done: document.getElementById("done"),
    categoryList: document.getElementById("category-list"),
    quizCat: document.getElementById("quiz-cat"),
    quizProgress: document.getElementById("quiz-progress"),
    questionBox: document.getElementById("question-box"),
    feedback: document.getElementById("feedback"),
    hintText: document.getElementById("hint-text"),
    btnHome: document.getElementById("btn-home"),
    btnHome2: document.getElementById("btn-home2"),
    btnHint: document.getElementById("btn-hint"),
    btnCheck: document.getElementById("btn-check"),
    btnNext: document.getElementById("btn-next"),
    btnRetry: document.getElementById("btn-retry"),
    btnAgain: document.getElementById("btn-again"),
    doneSummary: document.getElementById("done-summary"),
  };

  let state = {
    catId: null,
    index: 0,
    correct: 0,
    questions: [],
    dateStr: "",
  };

  function loadUsed() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_USED) || "[]");
    } catch {
      return [];
    }
  }

  function saveUsed(ids) {
    const merged = Array.from(new Set([].concat(loadUsed(), ids))).slice(-2000);
    localStorage.setItem(STORAGE_USED, JSON.stringify(merged));
  }

  function getDayCache() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_DAY) || "{}");
    } catch {
      return {};
    }
  }

  function setDayCache(dateStr, catId, questions) {
    const cache = getDayCache();
    // drop other dates to keep storage small
    const next = { date: dateStr, cats: (cache.date === dateStr && cache.cats) || {} };
    next.cats[catId] = questions;
    localStorage.setItem(STORAGE_DAY, JSON.stringify(next));
  }

  function questionsForToday(catId) {
    const dateStr = Daily.hktDateString();
    const cache = getDayCache();
    if (cache.date === dateStr && cache.cats && cache.cats[catId] && cache.cats[catId].length) {
      return { dateStr, questions: cache.cats[catId] };
    }
    const used = loadUsed();
    // seed pool: generators first; static bank as fallback spice
    let questions = Daily.buildDailySet(catId, dateStr, used, PER_DAY);
    if (questions.length < PER_DAY && bank[catId]) {
      const staticQ = bank[catId].questions.filter((q) => !used.includes(q.id));
      for (const q of staticQ) {
        if (questions.length >= PER_DAY) break;
        if (!questions.some((x) => x.id === q.id)) questions.push(q);
      }
    }
    setDayCache(dateStr, catId, questions);
    const keys = [];
    questions.forEach((q) => {
      keys.push(q.id);
      if (q.contentKey) keys.push(q.contentKey);
      else if (window.LogicDaily && LogicDaily.contentKey) keys.push(LogicDaily.contentKey(q.prompt, q.answer));
    });
    saveUsed(keys);
    return { dateStr, questions };
  }

  function show(panel) {
    [els.home, els.quiz, els.done].forEach((p) => p.classList.add("hidden"));
    panel.classList.remove("hidden");
  }

  function renderHome() {
    const dateStr = Daily.hktDateString();
    els.categoryList.innerHTML = "";
    Object.values(bank).forEach((cat) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "cat-btn";
      btn.innerHTML = `<strong>${cat.name}</strong><span>${cat.blurb} · 今日題組（${dateStr}）</span>`;
      btn.addEventListener("click", () => startCategory(cat.id));
      els.categoryList.appendChild(btn);
    });
    show(els.home);
  }

  function startCategory(catId) {
    const pack = questionsForToday(catId);
    state = {
      catId,
      index: 0,
      correct: 0,
      questions: pack.questions,
      dateStr: pack.dateStr,
    };
    if (!pack.questions.length) {
      els.doneSummary.textContent = `今日（${pack.dateStr}）呢類暫時無新題（已出過嘅唔會重複）。換日再試，或清瀏覽器本站資料重置題庫紀錄。`;
      show(els.done);
      return;
    }
    renderQuestion();
    show(els.quiz);
  }

  function currentCat() {
    return bank[state.catId];
  }

  function currentQ() {
    return state.questions[state.index];
  }

  function clearFeedback() {
    els.feedback.className = "feedback hidden";
    els.feedback.textContent = "";
    els.hintText.classList.add("hidden");
    els.hintText.textContent = "";
  }

  function renderQuestion() {
    const cat = currentCat();
    const q = currentQ();
    clearFeedback();
    els.btnCheck.classList.remove("hidden");
    els.btnCheck.disabled = false;
    els.btnNext.classList.add("hidden");
    els.btnRetry.classList.add("hidden");
    els.btnHint.disabled = false;

    els.quizCat.textContent = `${cat.name} · ${state.dateStr}`;
    els.quizProgress.textContent = `第 ${state.index + 1} / ${state.questions.length} 題`;

    let body = `<p class="q-text"><span class="level">${q.level}</span>\n${escapeHtml(q.prompt)}</p>`;
    if (q.type === "choice") {
      body += `<div class="choices" role="radiogroup">`;
      q.choices.forEach((c, i) => {
        const id = `c-${i}`;
        body += `<label class="choice" for="${id}"><input type="radio" name="ans" id="${id}" value="${escapeAttr(c)}" /> <span>${escapeHtml(c)}</span></label>`;
      });
      body += `</div>`;
    } else {
      body += `<div class="fill-row"><label for="fill-ans">你嘅答案：</label><input id="fill-ans" type="text" autocomplete="off" /></div>`;
    }
    els.questionBox.innerHTML = body;
  }

  function getUserAnswer() {
    const q = currentQ();
    if (q.type === "choice") {
      const picked = document.querySelector('input[name="ans"]:checked');
      return picked ? picked.value.trim() : "";
    }
    const input = document.getElementById("fill-ans");
    return input ? input.value.trim() : "";
  }

  function normalize(s) {
    return String(s).replace(/\s+/g, "").toLowerCase();
  }

  function checkAnswer() {
    const q = currentQ();
    const user = getUserAnswer();
    if (!user) {
      els.feedback.className = "feedback bad";
      els.feedback.textContent = "請先揀或填答案。";
      els.feedback.classList.remove("hidden");
      return;
    }
    const ok = normalize(user) === normalize(q.answer);
    els.btnCheck.classList.add("hidden");
    els.btnHint.disabled = true;
    if (ok) {
      state.correct += 1;
      els.feedback.className = "feedback ok";
      els.feedback.textContent = "做得好！答啱喇。";
      els.btnNext.classList.remove("hidden");
    } else {
      els.feedback.className = "feedback bad";
      els.feedback.textContent = "再諗一諗。可以再試一次，或者睇提示。";
      els.btnRetry.classList.remove("hidden");
      els.btnNext.classList.remove("hidden");
      els.btnHint.disabled = false;
    }
    els.feedback.classList.remove("hidden");
  }

  function nextQuestion() {
    if (state.index + 1 >= state.questions.length) {
      els.doneSummary.textContent = `今日（${state.dateStr}）呢類 ${state.questions.length} 題，你核對啱咗 ${state.correct} 題。換日會出另一組，唔會用返今日同一批。`;
      show(els.done);
      return;
    }
    state.index += 1;
    renderQuestion();
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
  function escapeAttr(s) {
    return escapeHtml(s).replace(/'/g, "&#39;");
  }

  els.btnHome.addEventListener("click", renderHome);
  els.btnHome2.addEventListener("click", renderHome);
  els.btnAgain.addEventListener("click", () => {
    // 同日再練：用已 cache 嘅今日題（刻意同一日穩定）；換日先變
    startCategory(state.catId);
  });
  els.btnHint.addEventListener("click", () => {
    const q = currentQ();
    els.hintText.textContent = "提示：" + q.hint;
    els.hintText.classList.remove("hidden");
  });
  els.btnCheck.addEventListener("click", checkAnswer);
  els.btnNext.addEventListener("click", nextQuestion);
  els.btnRetry.addEventListener("click", () => {
    clearFeedback();
    els.btnCheck.classList.remove("hidden");
    els.btnNext.classList.add("hidden");
    els.btnRetry.classList.add("hidden");
    const q = currentQ();
    if (q.type === "choice") {
      document.querySelectorAll('input[name="ans"]').forEach((el) => (el.checked = false));
    } else {
      const input = document.getElementById("fill-ans");
      if (input) input.value = "";
    }
  });

  renderHome();
})();
