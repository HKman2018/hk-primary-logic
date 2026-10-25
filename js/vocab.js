/** 「看圖學英文」— separate from the five logic categories and the HKT daily pool. */
(function () {
  const SESSION_SIZE = 10;

  const bank = (window.VOCAB_PICTURE_BANK || []).filter(function (item) {
    return Boolean(item && item.id && item.image && typeof item.answer === "string" && item.answer.trim());
  });

  const els = {
    home: document.getElementById("home"),
    mode: document.getElementById("vocab-mode"),
    quiz: document.getElementById("vocab-quiz"),
    done: document.getElementById("vocab-done"),
    entry: document.getElementById("btn-vocab-entry"),
    modeHome: document.getElementById("btn-vocab-mode-home"),
    quizHome: document.getElementById("btn-vocab-home"),
    doneHome: document.getElementById("btn-vocab-done-home"),
    start: document.getElementById("btn-vocab-start"),
    retry: document.getElementById("btn-vocab-retry"),
    submit: document.getElementById("btn-vocab-submit"),
    next: document.getElementById("btn-vocab-next"),
    skip: document.getElementById("btn-vocab-skip"),
    modeCount: document.getElementById("vocab-mode-count"),
    progress: document.getElementById("vocab-progress"),
    figure: document.getElementById("vocab-image-wrap"),
    image: document.getElementById("vocab-image"),
    loading: document.getElementById("vocab-image-loading"),
    imageError: document.getElementById("vocab-image-error"),
    input: document.getElementById("vocab-input"),
    feedback: document.getElementById("vocab-feedback"),
    doneSummary: document.getElementById("vocab-done-summary"),
  };

  const state = {
    items: [],
    index: 0,
    correct: 0,
    phase: "empty",
    token: 0,
  };

  function normalizeAnswer(value) {
    return String(value).trim().toLowerCase();
  }

  function shuffle(list) {
    const copy = list.slice();
    for (let i = copy.length - 1; i > 0; i -= 1) {
      const j = Math.floor(Math.random() * (i + 1));
      const swap = copy[i];
      copy[i] = copy[j];
      copy[j] = swap;
    }
    return copy;
  }

  function sessionLength() {
    return Math.min(SESSION_SIZE, bank.length);
  }

  function current() {
    return state.items[state.index] || null;
  }

  function showPanel(panel) {
    document.querySelectorAll(".panel").forEach(function (node) {
      node.classList.toggle("hidden", node !== panel);
    });
  }

  function altFor(item) {
    const fallback = "睇圖學英文題目圖";
    const alt = item && item.altZh ? String(item.altZh) : fallback;
    if (item && alt.toLowerCase().includes(normalizeAnswer(item.answer))) return fallback;
    return alt;
  }

  function applyPhase(phase) {
    switch (phase) {
      case "loading":
      case "image-error":
      case "empty":
      case "typing":
      case "correct":
      case "incorrect":
        break;
      default: {
        const unexpected = phase;
        throw new Error("Unknown vocab phase: " + unexpected);
      }
    }

    state.phase = phase;
    const item = current();
    const answered = phase === "correct" || phase === "incorrect";
    const loading = phase === "loading";
    const imageError = phase === "image-error";
    const canType = phase === "empty" || phase === "typing";

    els.figure.classList.toggle("is-loading", loading);
    els.figure.classList.toggle("is-error", imageError);
    els.figure.classList.toggle("is-ready", canType || answered);
    els.loading.classList.toggle("hidden", !loading);
    els.imageError.classList.toggle("hidden", !imageError);

    els.input.disabled = loading || imageError;
    els.input.readOnly = answered;
    els.input.classList.toggle("is-correct", phase === "correct");
    els.input.classList.toggle("is-incorrect", phase === "incorrect");

    const hasText = els.input.value.trim().length > 0;
    els.submit.classList.toggle("hidden", answered);
    els.submit.disabled = !canType || !hasText;
    els.next.classList.toggle("hidden", !answered);
    els.skip.classList.toggle("hidden", !imageError);

    if (phase === "correct") {
      els.feedback.className = "feedback ok";
      els.feedback.textContent = "啱喇！";
    } else if (phase === "incorrect") {
      els.feedback.className = "feedback bad";
      els.feedback.textContent = "唔啱。正確寫法係：" + (item ? item.answer : "");
    } else {
      els.feedback.className = "feedback hidden";
      els.feedback.textContent = "";
    }

    if (!item || loading || imageError) {
      els.image.alt = "";
      els.image.setAttribute("aria-hidden", "true");
    } else {
      els.image.alt = altFor(item);
      els.image.removeAttribute("aria-hidden");
    }
  }

  function loadPicture(item) {
    const token = (state.token += 1);
    applyPhase("loading");
    const pre = new Image();
    pre.onload = function () {
      if (token !== state.token) return;
      els.image.src = item.image;
      applyPhase(els.input.value.trim() ? "typing" : "empty");
      els.input.focus();
    };
    pre.onerror = function () {
      if (token !== state.token) return;
      els.image.removeAttribute("src");
      applyPhase("image-error");
      els.skip.focus();
    };
    pre.src = item.image;
  }

  function renderQuestion() {
    const item = current();
    const total = state.items.length;
    const n = state.index + 1;
    els.progress.textContent = n + "/" + total;
    els.progress.setAttribute("aria-label", "第 " + n + " 題，共 " + total + " 題");
    els.input.value = "";
    if (item) loadPicture(item);
  }

  function startRound() {
    state.items = shuffle(bank).slice(0, SESSION_SIZE);
    state.index = 0;
    state.correct = 0;
    if (!state.items.length) return;
    showPanel(els.quiz);
    renderQuestion();
  }

  function finishRound() {
    const total = state.items.length;
    els.doneSummary.textContent = "呢輪答啱 " + state.correct + " / " + total + " 題";
    showPanel(els.done);
    els.retry.focus();
  }

  function advance() {
    if (state.index + 1 >= state.items.length) {
      finishRound();
      return;
    }
    state.index += 1;
    renderQuestion();
  }

  function submitAnswer() {
    if (els.submit.disabled) return;
    if (state.phase !== "empty" && state.phase !== "typing") return;
    const item = current();
    if (!item) return;
    const given = normalizeAnswer(els.input.value);
    if (!given) {
      applyPhase("empty");
      return;
    }
    const correct = given === normalizeAnswer(item.answer);
    if (correct) state.correct += 1;
    applyPhase(correct ? "correct" : "incorrect");
    els.next.focus();
  }

  function openMode() {
    const count = sessionLength();
    els.modeCount.textContent = bank.length ? "共 " + count + " 題" : "暫時未有題目。";
    els.start.disabled = bank.length === 0;
    showPanel(els.mode);
    if (!els.start.disabled) els.start.focus();
  }

  function goHome() {
    state.token += 1;
    showPanel(els.home);
  }

  els.entry.addEventListener("click", openMode);
  els.modeHome.addEventListener("click", goHome);
  els.quizHome.addEventListener("click", goHome);
  els.doneHome.addEventListener("click", goHome);
  els.start.addEventListener("click", startRound);
  els.retry.addEventListener("click", startRound);
  els.submit.addEventListener("click", submitAnswer);
  els.next.addEventListener("click", advance);
  els.skip.addEventListener("click", advance);
  els.input.addEventListener("input", function () {
    if (state.phase !== "empty" && state.phase !== "typing") return;
    applyPhase(els.input.value.trim() ? "typing" : "empty");
  });
  els.input.addEventListener("keydown", function (event) {
    if (event.key !== "Enter") return;
    event.preventDefault();
    submitAnswer();
  });
})();
