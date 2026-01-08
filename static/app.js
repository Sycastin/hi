const statusEl = document.getElementById("status");
const plotButton = document.getElementById("plotButton");
const nameInput = document.getElementById("nameInput");

let calculator;
let currentIds = [];

function setStatus(message, isError = false) {
  statusEl.textContent = message;
  statusEl.style.color = isError ? "#ff9b9b" : "#f4f6fb";
}

function clearExpressions() {
  currentIds.forEach((id) => calculator.removeExpression({ id }));
  currentIds = [];
}

function addExpression(latex, id) {
  calculator.setExpression({
    id,
    latex,
    parametricDomain: { min: 0, max: 1 },
  });
  currentIds.push(id);
}

function equationsToLatex(eq) {
  const pts = eq.points;
  if (eq.type === "line") {
    const [x0, y0, x1, y1] = pts;
    return `((1-t)${x0}+t${x1},(1-t)${y0}+t${y1})`;
  }

  if (eq.type === "quadratic") {
    const [x0, y0, x1, y1, x2, y2] = pts;
    return `((1-t)^2${x0}+2(1-t)t${x1}+t^2${x2},(1-t)^2${y0}+2(1-t)t${y1}+t^2${y2})`;
  }

  if (eq.type === "cubic") {
    const [x0, y0, x1, y1, x2, y2, x3, y3] = pts;
    return `((1-t)^3${x0}+3(1-t)^2t${x1}+3(1-t)t^2${x2}+t^3${x3},(1-t)^3${y0}+3(1-t)^2t${y1}+3(1-t)t^2${y2}+t^3${y3})`;
  }

  return null;
}

async function plotName() {
  const name = nameInput.value.trim();
  if (!name) {
    setStatus("Please type a name first.", true);
    return;
  }

  plotButton.disabled = true;
  setStatus("Generating equations...");

  try {
    const response = await fetch("/api/equations", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    });

    if (!response.ok) {
      const payload = await response.json();
      throw new Error(payload.error || "Failed to convert name.");
    }

    const payload = await response.json();
    clearExpressions();

    payload.equations.forEach((eq, index) => {
      const latex = equationsToLatex(eq);
      if (latex) {
        addExpression(latex, `eq-${index}`);
      }
    });

    setStatus(`Plotted ${payload.equations.length} curve(s).`);
  } catch (error) {
    setStatus(error.message, true);
  } finally {
    plotButton.disabled = false;
  }
}

window.addEventListener("DOMContentLoaded", () => {
  calculator = Desmos.GraphingCalculator(document.getElementById("calculator"), {
    expressions: false,
    settingsMenu: false,
    zoomButtons: true,
    keypad: false,
  });

  plotButton.addEventListener("click", plotName);
  nameInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      plotName();
    }
  });
});
