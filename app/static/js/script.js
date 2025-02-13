(function () {
  // ======================================================
  // GLOBAL SETTINGS & TRANSLATIONS
  // ======================================================
  let currentLanguage = "en";
  const translations = {
    planning: { en: "Planning", fr: "Planification" },
    save: { en: "Save", fr: "Sauvegarder" },
    load: { en: "Load", fr: "Charger" },
    toggleLanguage: { en: "Français", fr: "English" },
    mechanicalAdvice: {
      en: "Always ensure optimal gear alignment and proper lubrication levels to achieve maximum mechanical efficiency and safety during high-load operations.",
      fr: "Assurez-vous toujours d'un alignement optimal des engrenages et d'un niveau de lubrification approprié pour obtenir une efficacité mécanique maximale et une sécurité optimale lors des opérations à forte charge."
    },
    removeSubstring: {
      en: "Remove All Occurrences of a Substring",
      fr: "Supprimer toutes les occurrences d'une sous-chaîne"
    },
    submit: { en: "Submit", fr: "Soumettre" },
    output: { en: "Output", fr: "Résultat" },
    textContext: {
      en: "Welcome to the Platform. Here you can generate structured documents styled like Excel with advanced mechanical insights and planning features.",
      fr: "Bienvenue sur la plateforme. Ici, vous pouvez générer des documents structurés au style Excel avec des informations mécaniques avancées et des fonctionnalités de planification."
    },
    reset: { en: "Reset UI", fr: "Réinitialiser l'interface" },
    saveAlert: { en: "State saved!", fr: "État sauvegardé!" },
    loadAlert: { en: "State loaded!", fr: "État chargé!" },
    noStateAlert: { en: "No saved state found.", fr: "Aucun état sauvegardé trouvé." },
    simulationTitle: {
      en: "Mechanics Automobile IoT Simulation",
      fr: "Simulation IoT de Mécanique Automobile"
    },
    startSimulation: { en: "Start", fr: "Démarrer" },
    stopSimulation: { en: "Stop", fr: "Arrêter" },
    // --- New translations for Nerd Metrics ---
    nerdMetrics: { en: "Metrics", fr: "Mesures" },
    proceed: { en: "Go to Next", fr: "Aller à Suivant" },
    close: { en: "Close", fr: "Fermer" }
  };

  // ======================================================
  // GLOBAL VARIABLES FOR SIMULATION
  // ======================================================
  let simulationIntervalID = null;
  let simulationStep = 0;
  const simulationActions = [
    "Checking engine sensor readings",
    "Calibrating transmission sensors",
    "Adjusting fuel mixture parameters",
    "Activating diagnostic mode",
    "Syncing real-time data with cloud",
    "Running predictive maintenance algorithm",
    "Optimizing gear ratios",
    "Monitoring temperature sensors"
  ];

  // ======================================================
  // VERSATILITY: GLOBAL SAFETY WRAPPER & FALLBACK FUNCTIONS
  // ======================================================
  function safeExecute(fn, alternative, fnName) {
    console.log(`Start: ${fnName}`);
    try {
      fn();
      console.log(`End: ${fnName} succeeded.`);
    } catch (error) {
      console.error(`Error in ${fnName}: ${error}`);
      if (typeof alternative === "function") {
        try {
          alternative();
          console.log(`Alternative for ${fnName} succeeded.`);
        } catch (altError) {
          console.error(`Alternative for ${fnName} failed: ${altError}`);
        }
      }
    }
  }

  // Fallback for Drag & Drop: In case the advanced drag/drop fails, we remove draggable attributes.
  function fallbackDragAndDrop() {
    console.warn("Fallback: Basic Drag & Drop not available. Draggables will remain static.");
    const draggables = document.querySelectorAll(".draggable");
    draggables.forEach((elem) => {
      elem.removeAttribute("draggable");
    });
  }

  // Fallback for Floating Bubbles: If animation fails, we paint a static background on the canvas.
  function fallbackFloatingBubbles() {
    console.warn("Fallback: Floating bubbles animation failed. Using static background.");
    const canvas = document.getElementById("bubbleCanvas");
    if (canvas) {
      const ctx = canvas.getContext("2d");
      ctx.fillStyle = "#e0e0e0";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    }
  }

  // ======================================================
  // INSERT CSS STYLES (SELF-CONTAINED)
  // ======================================================
  function insertStyles() {
    const style = document.createElement("style");
    style.innerHTML = `
      /* Minimal inline fallback styles for basic layout & interactions */
      * { box-sizing: border-box; margin: 0; padding: 0; }
      .modal {
        position: fixed; top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        background: #fff; padding: 20px;
        border: 2px solid #000; border-radius: 8px;
        z-index: 10000; max-width: 90%; max-height: 90%; overflow: auto;
      }
      #customModal {
        background: rgba(0, 0, 0, 0.85); color: #fff;
        transition: opacity 0.3s ease; text-align: center;
      }
      #dropZone {
        position: fixed; top: 0; left: 50%;
        transform: translateX(-50%); border: 2px dashed #ccc;
        padding: 20px; margin: 10px; min-width: 300px;
        text-align: center; background: #f9f9f9; z-index: 9999;
      }
      .bubble-button {
        position: relative; padding: 10px 15px; margin: 5px;
        border: none; background: #007BFF; color: #fff;
        border-radius: 5px; cursor: pointer;
        transition: transform 0.3s ease;
      }
      .bubble-button:hover { transform: scale(1.1); }
      @keyframes buzz {
        0% { transform: translate(0, 0); }
        20% { transform: translate(-2px, 2px); }
        40% { transform: translate(-2px, -2px); }
        60% { transform: translate(2px, 2px); }
        80% { transform: translate(2px, -2px); }
        100% { transform: translate(0, 0); }
      }
      .buzz-effect { animation: buzz 0.5s linear; }
      .excel-table { width: 100%; border-collapse: collapse; }
      .excel-table th, .excel-table td {
        border: 1px solid #999; padding: 8px;
        text-align: center;
      }
      .excel-table th { background: #e0e0e0; }
      #mainContainer { padding: 20px; font-family: sans-serif; }
      #iotSimulation { border: 1px solid #ccc; padding: 10px; margin: 20px 0; }
      #simulationLog {
        background: #f4f4f4; height: 150px;
        overflow-y: auto; padding: 10px; font-size: 14px;
      }
      @media (max-width: 600px) {
        .bubble-button { font-size: 14px; padding: 8px 12px; }
        h1 { font-size: 20px; }
      }
      #bubbleCanvas {
        position: fixed; top: 0; left: 0;
        width: 100%; height: 100%;
        pointer-events: none; z-index: -1;
      }
    `;
    document.head.appendChild(style);
  }

  // ======================================================
  // SECRET INDEX MAPPING (GLOBAL)
  // ======================================================
  function applySecretIndexMapping() {
    const elements = document.querySelectorAll("*");
    const prime = 37;
    elements.forEach((el, index) => {
      const secretIndex = ((index + 1) * prime) % 9973;
      el.setAttribute("data-secret-index", secretIndex);
    });
    console.log("Secret index mapping applied to", elements.length, "elements.");
  }

  // ======================================================
  // UI BUILDER METHODS
  // ======================================================
  function createUI() {
    const mainContainer = document.createElement("div");
    mainContainer.id = "mainContainer";
    document.body.appendChild(mainContainer);

    createHeader(mainContainer);
    createButtons(mainContainer);
    createTextContext(mainContainer);
    createRemoveSubstringSection(mainContainer);
    createDraggableElements(mainContainer);
    createIoTSimulationSection(mainContainer);
    // Add Nerd Metrics toggle button to the header
    initNerdMetricsToggle();
  }

  // Creates a header area with language toggle and reset
  function createHeader(parent) {
    const header = document.createElement("div");
    header.id = "header";
    header.style.display = "flex";
    header.style.justifyContent = "space-between";
    header.style.alignItems = "center";
    header.style.padding = "10px 0";
    parent.appendChild(header);

    const title = document.createElement("h1");
    title.innerText = "Engineering Document SaaS Platform";
    header.appendChild(title);

    const controlsContainer = document.createElement("div");
    header.appendChild(controlsContainer);

    // Language toggle
    const langToggleButton = document.createElement("button");
    langToggleButton.id = "langToggleButton";
    langToggleButton.className = "bubble-button";
    langToggleButton.innerText = translations.toggleLanguage[currentLanguage];
    langToggleButton.addEventListener("click", toggleLanguage);
    controlsContainer.appendChild(langToggleButton);

    // Reset UI
    const resetButton = document.createElement("button");
    resetButton.id = "resetButton";
    resetButton.className = "bubble-button";
    resetButton.innerText = translations.reset[currentLanguage];
    resetButton.addEventListener("click", resetUI);
    controlsContainer.appendChild(resetButton);
  }

  // Adds a row of buttons (e.g., planning)
  function createButtons(parent) {
    const buttonsContainer = document.createElement("div");
    buttonsContainer.id = "buttonsContainer";
    buttonsContainer.style.margin = "20px 0";
    parent.appendChild(buttonsContainer);

    const planningButton = document.createElement("button");
    planningButton.id = "planningButton";
    planningButton.className = "bubble-button";
    planningButton.innerText = translations.planning[currentLanguage];
    planningButton.addEventListener("click", showPlanningDocument);
    buttonsContainer.appendChild(planningButton);
  }

  // Intro text context
  function createTextContext(parent) {
    const textContext = document.createElement("p");
    textContext.id = "textContext";
    textContext.innerText = translations.textContext[currentLanguage];
    parent.appendChild(textContext);
  }

  // Substring removal section
  function createRemoveSubstringSection(parent) {
    const removeContainer = document.createElement("div");
    removeContainer.id = "removeContainer";
    removeContainer.style.border = "1px solid #ccc";
    removeContainer.style.padding = "10px";
    removeContainer.style.margin = "20px 0";
    parent.appendChild(removeContainer);

    const removeTitle = document.createElement("h2");
    removeTitle.innerText = translations.removeSubstring[currentLanguage];
    removeContainer.appendChild(removeTitle);

    const sLabel = document.createElement("label");
    sLabel.innerText = "Main string:";
    removeContainer.appendChild(sLabel);

    const sInput = document.createElement("input");
    sInput.type = "text";
    sInput.id = "sInput";
    sInput.style.display = "block";
    sInput.style.marginBottom = "10px";
    removeContainer.appendChild(sInput);

    const partLabel = document.createElement("label");
    partLabel.innerText = "Substring:";
    removeContainer.appendChild(partLabel);

    const partInput = document.createElement("input");
    partInput.type = "text";
    partInput.id = "partInput";
    partInput.style.display = "block";
    partInput.style.marginBottom = "10px";
    removeContainer.appendChild(partInput);

    const submitButton = document.createElement("button");
    submitButton.innerText = translations.submit[currentLanguage];
    submitButton.className = "bubble-button";
    submitButton.addEventListener("click", processInput);
    removeContainer.appendChild(submitButton);

    const outputTitle = document.createElement("h3");
    outputTitle.innerHTML = translations.output[currentLanguage] + ": <span id='output'></span>";
    removeContainer.appendChild(outputTitle);
  }

  // Draggable elements (for demo)
  function createDraggableElements(parent) {
    for (let i = 1; i <= 3; i++) {
      const draggable = document.createElement("div");
      draggable.id = "draggable" + i;
      draggable.className = "draggable buzz bubble-button";
      draggable.style.padding = "10px";
      draggable.style.margin = "10px";
      draggable.style.background = "#ddd";
      draggable.style.width = "100px";
      draggable.style.textAlign = "center";
      draggable.style.cursor = "move";
      draggable.innerHTML = i % 2 === 0 ? "🔧" : "⚙️";
      parent.appendChild(draggable);
    }
  }

  // IoT Simulation Section
  function createIoTSimulationSection(parent) {
    const simulationSection = document.createElement("div");
    simulationSection.id = "iotSimulation";
    simulationSection.style.border = "1px solid #ccc";
    simulationSection.style.padding = "10px";
    simulationSection.style.margin = "20px 0";
    parent.appendChild(simulationSection);

    const simTitle = document.createElement("h2");
    simTitle.innerText = translations.simulationTitle[currentLanguage];
    simulationSection.appendChild(simTitle);

    const startBtn = document.createElement("button");
    startBtn.innerText = translations.startSimulation[currentLanguage];
    startBtn.className = "bubble-button";
    startBtn.addEventListener("click", startIoTSimulation);
    simulationSection.appendChild(startBtn);

    const stopBtn = document.createElement("button");
    stopBtn.innerText = translations.stopSimulation[currentLanguage];
    stopBtn.className = "bubble-button";
    stopBtn.addEventListener("click", stopIoTSimulation);
    simulationSection.appendChild(stopBtn);

    const logArea = document.createElement("pre");
    logArea.id = "simulationLog";
    logArea.style.marginTop = "10px";
    simulationSection.appendChild(logArea);
  }

  // ======================================================
  // LANGUAGE & UI UPDATE METHODS
  // ======================================================
  function toggleLanguage() {
    currentLanguage = currentLanguage === "en" ? "fr" : "en";
    // Update language text in various elements
    document.getElementById("langToggleButton").innerText = translations.toggleLanguage[currentLanguage];
    document.getElementById("planningButton").innerText = translations.planning[currentLanguage];
    document.getElementById("textContext").innerText = translations.textContext[currentLanguage];
    document.querySelector("#removeContainer h2").innerText = translations.removeSubstring[currentLanguage];
    const submitBtn = document.querySelector("#removeContainer button");
    if (submitBtn) submitBtn.innerText = translations.submit[currentLanguage];
    document.querySelector("#removeContainer h3").innerHTML =
      translations.output[currentLanguage] + ": <span id='output'></span>";
    document.getElementById("resetButton").innerText = translations.reset[currentLanguage];
    document.querySelector("#iotSimulation h2").innerText = translations.simulationTitle[currentLanguage];

    // Update Nerd Metrics button & modal
    const nerdBtn = document.getElementById("nerdMetricsButton");
    if (nerdBtn) {
      nerdBtn.innerText = translations.nerdMetrics[currentLanguage];
    }
    const nerdModal = document.getElementById("nerdMetricsModal");
    if (nerdModal) {
      const header = nerdModal.querySelector("h2");
      if (header) header.innerText = translations.nerdMetrics[currentLanguage];
      const buttons = nerdModal.querySelectorAll("button");
      if (buttons.length >= 2) {
        buttons[0].innerText = translations.close[currentLanguage];
        buttons[1].innerText = translations.proceed[currentLanguage];
      }
    }
  }

  function resetUI() {
    const mainContainer = document.getElementById("mainContainer");
    document.querySelectorAll(".draggable").forEach((draggable) => {
      mainContainer.appendChild(draggable);
      draggable.style.opacity = "1";
    });
    const dropZone = document.getElementById("dropZone");
    if (dropZone) dropZone.style.backgroundColor = "#f9f9f9";
    applySecretIndexMapping();
    console.log("UI reset complete.");
  }

  // ======================================================
  // STRING PROCESSING METHODS
  // ======================================================
  function removeOccurrences(s, part) {
    while (s.includes(part)) {
      s = s.replace(part, "");
    }
    return s;
  }
  function processInput() {
    const s = document.getElementById("sInput").value;
    const part = document.getElementById("partInput").value;
    document.getElementById("output").innerText = removeOccurrences(s, part);
  }

  // ======================================================
  // DOCUMENT GENERATOR (EXCEL-LIKE TABLE WITH ADVICE)
  // ======================================================
  function showPlanningDocument() {
    const modal = document.createElement("div");
    modal.className = "modal";

    const table = document.createElement("table");
    table.className = "excel-table";
    const headerRow = document.createElement("tr");
    ["Task", "Engineer", "Start Date", "End Date", "Status"].forEach((txt) => {
      const th = document.createElement("th");
      th.innerText = txt;
      headerRow.appendChild(th);
    });
    table.appendChild(headerRow);

    const dummyData = [
      ["Review Design", "Alice", "2025-03-01", "2025-03-02", "Completed"],
      ["Prototype Build", "Bob", "2025-03-03", "2025-03-10", "In Progress"],
      ["Test & Validate", "Charlie", "2025-03-11", "2025-03-15", "Pending"]
    ];
    dummyData.forEach((rowData) => {
      const row = document.createElement("tr");
      rowData.forEach((cellData) => {
        const td = document.createElement("td");
        td.innerText = cellData;
        row.appendChild(td);
      });
      table.appendChild(row);
    });

    const advice = document.createElement("p");
    advice.style.marginTop = "20px";
    advice.innerText = translations.mechanicalAdvice[currentLanguage];

    const closeBtn = document.createElement("button");
    closeBtn.innerText = translations.close[currentLanguage] || "Close";
    closeBtn.className = "bubble-button";
    closeBtn.style.marginTop = "10px";
    closeBtn.addEventListener("click", () => {
      document.body.removeChild(modal);
    });

    modal.appendChild(table);
    modal.appendChild(advice);
    modal.appendChild(closeBtn);
    document.body.appendChild(modal);
  }

  // ======================================================
  // POPUP MODAL WITH MECHANICAL ADVICE (OPTIONAL)
  // ======================================================
  function initPopup() {
    const modal = document.createElement("div");
    modal.id = "customModal";
    Object.assign(modal.style, { top: "50%", left: "50%", transform: "translate(-50%, -50%)" });
    modal.innerHTML = `
      <p><strong>Mechanical Advice:</strong> ${translations.mechanicalAdvice[currentLanguage]}</p>
      <button id="closeModal" style="padding: 8px 12px; cursor: pointer;">
        ${translations.close[currentLanguage] || "Close Advice"}
      </button>
    `;
    document.body.appendChild(modal);

    // Show/hide the modal on .popup-trigger
    document.querySelectorAll(".popup-trigger").forEach((trigger) => {
      trigger.addEventListener("click", (e) => {
        e.stopPropagation();
        modal.style.display = "block";
        setTimeout(() => { modal.style.opacity = "1"; }, 100);
      });
    });

    // Close the modal
    document.getElementById("closeModal").addEventListener("click", (e) => {
      e.stopPropagation();
      modal.style.opacity = "0";
      setTimeout(() => { modal.style.display = "none"; }, 300);
    });
    window.addEventListener("click", (e) => {
      if (e.target === modal) {
        modal.style.opacity = "0";
        setTimeout(() => { modal.style.display = "none"; }, 300);
      }
    });
  }

  // ======================================================
  // DRAG & DROP & BUZZ EFFECT METHODS
  // ======================================================
  function initDragAndDrop() {
    const draggables = document.querySelectorAll(".draggable");
    draggables.forEach((item) => {
      item.setAttribute("draggable", true);
      item.addEventListener("dragstart", dragStart);
      item.addEventListener("click", () => {
        buzzElement(item);
      });
    });
    let dropZone = document.getElementById("dropZone");
    if (!dropZone) {
      dropZone = document.createElement("div");
      dropZone.id = "dropZone";
      dropZone.textContent = "Drop items here";
      document.body.appendChild(dropZone);
    }
    dropZone.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropZone.style.backgroundColor = "#e0e0e0";
    });
    dropZone.addEventListener("dragleave", () => {
      dropZone.style.backgroundColor = "#f9f9f9";
    });
    dropZone.addEventListener("drop", (e) => {
      e.preventDefault();
      dropZone.style.backgroundColor = "#f9f9f9";
      const id = e.dataTransfer.getData("text/plain");
      const draggableElem = document.getElementById(id);
      if (draggableElem) {
        dropZone.appendChild(draggableElem);
        draggableElem.style.transition = "opacity 0.5s";
        draggableElem.style.opacity = "0.5";
        setTimeout(() => { draggableElem.style.opacity = "1"; }, 500);
      }
    });
  }
  function dragStart(e) {
    e.dataTransfer.setData("text/plain", e.target.id);
  }
  function initBuzzEffect() {
    document.querySelectorAll(".buzz").forEach((elem) => {
      elem.addEventListener("click", () => {
        buzzElement(elem);
      });
    });
  }
  function buzzElement(elem) {
    elem.classList.add("buzz-effect");
    setTimeout(() => {
      elem.classList.remove("buzz-effect");
    }, 500);
  }

  // ======================================================
  // SAVE / LOAD DRAGGABLE STATE METHODS
  // ======================================================
  function initStateSaveLoad() {
    const saveButton = document.createElement("button");
    saveButton.textContent = translations.save[currentLanguage];
    saveButton.className = "bubble-button";
    Object.assign(saveButton.style, {
      position: "fixed",
      bottom: "20px",
      right: "20px",
      padding: "10px 20px",
      zIndex: "9999",
      cursor: "pointer"
    });
    document.body.appendChild(saveButton);

    const loadButton = document.createElement("button");
    loadButton.textContent = translations.load[currentLanguage];
    loadButton.className = "bubble-button";
    Object.assign(loadButton.style, {
      position: "fixed",
      bottom: "20px",
      right: "150px",
      padding: "10px 20px",
      zIndex: "9999",
      cursor: "pointer"
    });
    document.body.appendChild(loadButton);

    saveButton.addEventListener("click", () => {
      const state = [];
      document.querySelectorAll(".draggable").forEach((elem) => {
        state.push({
          id: elem.id,
          parentId: elem.parentElement.id,
          secretIndex: elem.getAttribute("data-secret-index")
        });
      });
      localStorage.setItem("draggableState", JSON.stringify(state));
      alert(translations.saveAlert[currentLanguage]);
    });
    loadButton.addEventListener("click", () => {
      const stateJSON = localStorage.getItem("draggableState");
      if (stateJSON) {
        const state = JSON.parse(stateJSON);
        state.forEach((item) => {
          const elem = document.getElementById(item.id);
          if (elem) {
            const parent = document.getElementById(item.parentId);
            if (parent) {
              parent.appendChild(elem);
            }
          }
        });
        alert(translations.loadAlert[currentLanguage]);
      } else {
        alert(translations.noStateAlert[currentLanguage]);
      }
    });
  }

  // ======================================================
  // PERIODIC UPDATES
  // ======================================================
  function periodicSecretMappingUpdate() {
    setInterval(applySecretIndexMapping, 60000);
  }

  // ======================================================
  // FLOATING BUBBLES (BACKGROUND ANIMATION)
  // ======================================================
  function initFloatingBubbles() {
    const canvas = document.createElement("canvas");
    canvas.id = "bubbleCanvas";
    canvas.style.position = "fixed";
    canvas.style.top = "0";
    canvas.style.left = "0";
    canvas.style.width = "100%";
    canvas.style.height = "100%";
    canvas.style.pointerEvents = "none";
    canvas.style.zIndex = "-1";
    document.body.appendChild(canvas);

    const ctx = canvas.getContext("2d");
    function resizeCanvas() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    resizeCanvas();
    window.addEventListener("resize", resizeCanvas);

    const bubbles = [];
    const bubbleCount = 15;
    for (let i = 0; i < bubbleCount; i++) {
      const radius = Math.random() * 20 + 10;
      bubbles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: radius,
        dx: (Math.random() - 0.5) * 2,
        dy: (Math.random() - 0.5) * 2,
        color: `hsla(${Math.random() * 360}, 70%, 70%, 0.7)`
      });
    }

    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (let i = 0; i < bubbles.length; i++) {
        const b = bubbles[i];
        b.x += b.dx;
        b.y += b.dy;
        // Bounce off edges
        if (b.x + b.radius > canvas.width || b.x - b.radius < 0) b.dx = -b.dx;
        if (b.y + b.radius > canvas.height || b.y - b.radius < 0) b.dy = -b.dy;

        // Simple collision detection among bubbles
        for (let j = i + 1; j < bubbles.length; j++) {
          const b2 = bubbles[j];
          const dx = b2.x - b.x;
          const dy = b2.y - b.y;
          const distance = Math.sqrt(dx * dx + dy * dy);
          if (distance < b.radius + b2.radius) {
            const tempDx = b.dx;
            const tempDy = b.dy;
            b.dx = b2.dx;
            b.dy = b2.dy;
            b2.dx = tempDx;
            b2.dy = tempDy;
          }
        }
        ctx.beginPath();
        ctx.arc(b.x, b.y, b.radius, 0, Math.PI * 2);
        ctx.fillStyle = b.color;
        ctx.fill();
        ctx.closePath();
      }
      requestAnimationFrame(animate);
    }
    animate();
  }

  // ======================================================
  // MECHANICS AUTOMOBILE IOT SIMULATION METHODS
  // ======================================================
  function startIoTSimulation() {
    if (simulationIntervalID !== null) return; // Already running
    simulationIntervalID = setInterval(simulateIoTProcess, 2000);
  }
  function stopIoTSimulation() {
    clearInterval(simulationIntervalID);
    simulationIntervalID = null;
  }
  function simulateIoTProcess() {
    simulationStep++;
    const action = simulationActions[Math.floor(Math.random() * simulationActions.length)];
    const sensorValue = (Math.random() * 100).toFixed(2);
    const stepMessage = `Step ${simulationStep}: ${action}. Sensor reading: ${sensorValue}`;
    const logArea = document.getElementById("simulationLog");
    if (logArea) {
      logArea.textContent += stepMessage + "\n";
      logArea.scrollTop = logArea.scrollHeight;
    }
    // Mimic sensor feedback by changing background color of a random draggable
    const draggables = document.querySelectorAll(".draggable");
    if (draggables.length) {
      const randomIndex = Math.floor(Math.random() * draggables.length);
      const elem = draggables[randomIndex];
      elem.style.background = sensorValue > 50 ? "#cfc" : "#fcc";
      setTimeout(() => { elem.style.background = "#ddd"; }, 500);
    }
  }

  // ======================================================
  // NERD METRICS TOGGLE & MODAL
  // ======================================================
  function initNerdMetricsToggle() {
    const nerdButton = document.createElement("button");
    nerdButton.id = "nerdMetricsButton";
    nerdButton.className = "bubble-button";
    nerdButton.innerText = translations.nerdMetrics[currentLanguage];
    const header = document.getElementById("header");
    if (header) {
      header.appendChild(nerdButton);
    } else {
      document.body.appendChild(nerdButton);
    }
    nerdButton.addEventListener("click", toggleNerdMetricsModal);
  }
  
  function toggleNerdMetricsModal() {
    let modal = document.getElementById("nerdMetricsModal");
    if (modal) {
      // Toggle display if modal already exists
      modal.style.display = (modal.style.display === "none" || modal.style.display === "") ? "block" : "none";
    } else {
      // Create new modal
      modal = document.createElement("div");
      modal.id = "nerdMetricsModal";
      Object.assign(modal.style, {
        position: "fixed",
        top: "50%",
        left: "50%",
        transform: "translate(-50%, -50%)",
        background: "#fff",
        padding: "20px",
        border: "2px solid #000",
        borderRadius: "8px",
        zIndex: "10000",
        maxWidth: "90%",
        maxHeight: "90%",
        overflow: "auto"
      });
      
      const modalHeader = document.createElement("h2");
      modalHeader.innerText = translations.nerdMetrics[currentLanguage];
      modal.appendChild(modalHeader);
      
      const metricsContainer = document.createElement("div");
      metricsContainer.id = "metricsContainer";
      metricsContainer.style.margin = "10px 0";
      modal.appendChild(metricsContainer);
      
      // Periodically update metrics
      function updateMetrics() {
        const currentTime = new Date().toLocaleTimeString();
        const cpuUsage = (Math.random() * 100).toFixed(2);
        const gpuUsage = (Math.random() * 100).toFixed(2);
        const powerConsumption = (Math.random() * 50 + 50).toFixed(2);
        const dataConsumption = (Math.random() * 500).toFixed(2);
        const timeToday = new Date().toLocaleString();
        
        metricsContainer.innerHTML = `
          <p>Current Time: ${currentTime}</p>
          <p>CPU Usage: ${cpuUsage}%</p>
          <p>GPU Usage: ${gpuUsage}%</p>
          <p>Power Consumption: ${powerConsumption}W</p>
          <p>Data Consumption: ${dataConsumption} MB</p>
          <p>Time Today: ${timeToday}</p>
        `;
      }
      updateMetrics();
      const metricsInterval = setInterval(updateMetrics, 5000);
      
      // Close Modal button
      const closeModalBtn = document.createElement("button");
      closeModalBtn.innerText = translations.close[currentLanguage];
      closeModalBtn.className = "bubble-button";
      closeModalBtn.style.marginRight = "10px";
      closeModalBtn.addEventListener("click", () => {
        modal.style.display = "none";
        clearInterval(metricsInterval);
      });
      modal.appendChild(closeModalBtn);
      
      // Proceed button (example)
      const proceedButton = document.createElement("button");
      proceedButton.innerText = translations.proceed[currentLanguage];
      proceedButton.className = "bubble-button";
      proceedButton.addEventListener("click", () => {
        const confirmed = confirm("Do you want to proceed to base-next.html?");
        if (confirmed) {
          window.location.href = "base-next.html";
        }
      });
      modal.appendChild(proceedButton);
      
      document.body.appendChild(modal);
    }
  }
  
  // ======================================================
  // UTILITY: Toggle Emoji for Draggable Elements
  // ======================================================
  function initEmojiToggle() {
    const draggables = document.querySelectorAll(".draggable");
    draggables.forEach((draggable) => {
      let emojiState = draggable.innerHTML === "🔧";
      setInterval(() => {
        draggable.innerHTML = emojiState ? "⚙️" : "🔧";
        emojiState = !emojiState;
      }, 5000);
    });
  }

  // ======================================================
  // INITIALIZATION (ON DOMCONTENTLOADED) WITH GLOBAL SAFETY LOOP
  // ======================================================
  document.addEventListener("DOMContentLoaded", () => {
    const initFunctions = [
      { fn: insertStyles, name: "insertStyles", fallback: null },
      { fn: createUI, name: "createUI", fallback: null },
      { fn: applySecretIndexMapping, name: "applySecretIndexMapping", fallback: null },
      { fn: initPopup, name: "initPopup", fallback: null },
      { fn: initDragAndDrop, name: "initDragAndDrop", fallback: fallbackDragAndDrop },
      { fn: initEmojiToggle, name: "initEmojiToggle", fallback: null },
      { fn: initBuzzEffect, name: "initBuzzEffect", fallback: null },
      { fn: initStateSaveLoad, name: "initStateSaveLoad", fallback: null },
      { fn: periodicSecretMappingUpdate, name: "periodicSecretMappingUpdate", fallback: null },
      { fn: initFloatingBubbles, name: "initFloatingBubbles", fallback: fallbackFloatingBubbles }
    ];

    initFunctions.forEach(item => safeExecute(item.fn, item.fallback, item.name));
  });
})();
