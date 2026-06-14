const API_URL = "http://127.0.0.1:8000/lesson-summary";

const form = document.querySelector("#lessonForm");
const generateBtn = document.querySelector("#generateBtn");
const errorMessage = document.querySelector("#errorMessage");
const emptyState = document.querySelector("#emptyState");
const resultCard = document.querySelector("#resultCard");

const shortSummary = document.querySelector("#shortSummary");
const keyConcepts = document.querySelector("#keyConcepts");
const misunderstandings = document.querySelector("#misunderstandings");
const reflectionQuestions = document.querySelector("#reflectionQuestions");
const practiceActivity = document.querySelector("#practiceActivity");
const finalTakeaway = document.querySelector("#finalTakeaway");

function setLoading(isLoading) {
  generateBtn.disabled = isLoading;
  generateBtn.classList.toggle("is-loading", isLoading);
}

function renderList(container, items) {
  container.innerHTML = "";

  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    container.appendChild(li);
  });
}

function renderConcepts(concepts) {
  keyConcepts.innerHTML = "";

  concepts.forEach((item) => {
    const concept = document.createElement("div");
    concept.className = "concept-item";

    const title = document.createElement("h3");
    title.textContent = item.concept;

    const explanation = document.createElement("p");
    explanation.textContent = item.explanation;

    concept.append(title, explanation);
    keyConcepts.appendChild(concept);
  });
}

function renderResult(data) {
  shortSummary.textContent = data.short_summary;
  renderConcepts(data.key_concepts || []);
  renderList(misunderstandings, data.common_misunderstandings || []);
  renderList(reflectionQuestions, data.reflection_questions || []);
  practiceActivity.textContent = data.mini_practice_activity;
  finalTakeaway.textContent = data.final_takeaway;

  emptyState.classList.add("hidden");
  resultCard.classList.remove("hidden");
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorMessage.textContent = "";
  setLoading(true);

  const formData = new FormData(form);
  const payload = {
    lesson_title: formData.get("lessonTitle").trim(),
    output_style: formData.get("outputStyle"),
    raw_notes: formData.get("rawNotes").trim(),
  };

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Something went wrong. Please try again.");
    }

    renderResult(data);
  } catch (error) {
    errorMessage.textContent = error.message;
  } finally {
    setLoading(false);
  }
});
