(function () {
  // ======================================================
  // GLOBAL SETTINGS & TRANSLATIONS (Updated for Mechanisms)
  // ======================================================
  let currentLanguage = "en";
  const translations = {
    planning: {
      en: "Mechanism Analysis",
      fr: "Analyse des Mécanismes"
    },
    save: {
      en: "Save State",
      fr: "Sauvegarder l'état"
    },
    load: {
      en: "Load State",
      fr: "Charger l'état"
    },
    toggleLanguage: {
      en: "Français",
      fr: "English"
    },
    mechanicalAdvice: {
      en: "For optimal performance, ensure that the electric mechanism is calibrated with proper thermal regulation for diesel drives. Always refer to the principles of Newton and Joule.",
      fr: "Pour une performance optimale, assurez-vous que le mécanisme électrique est calibré avec une régulation thermique adéquate pour les motorisations diesel. Référez-vous toujours aux principes de Newton et de Joule."
    },
    removeSubstring: {
      en: "Remove All Occurrences of a Substring",
      fr: "Supprimer toutes les occurrences d'une sous-chaîne"
    },
    submit: {
      en: "Submit",
      fr: "Soumettre"
    },
    output: {
      en: "Output",
      fr: "Résultat"
    },
    textContext: {
      en: "Welcome to our Mechanism Analysis Platform. Here, advanced texts from classical mechanics and electric thermal systems guide you through complex calculations.",
      fr: "Bienvenue sur notre plateforme d'analyse des mécanismes. Ici, des textes avancés de mécanique classique et de systèmes électriques thermiques vous guident à travers des calculs complexes."
    },
    reset: {
      en: "Reset UI",
      fr: "Réinitialiser l'interface"
    },
    saveAlert: {
      en: "State saved!",
      fr: "État sauvegardé!"
    },
    loadAlert: {
      en: "State loaded!",
      fr: "État chargé!"
    },
    noStateAlert: {
      en: "No saved state found.",
      fr: "Aucun état sauvegardé trouvé."
    },
    simulationTitle: {
      en: "Electric & Thermal Mechanism Simulation",
      fr: "Simulation des Mécanismes Électriques et Thermiques"
    },
    startSimulation: {
      en: "Start",
      fr: "Démarrer"
    },
    stopSimulation: {
      en: "Stop",
      fr: "Arrêter"
    },
    nerdMetrics: {
      en: "Performance Metrics",
      fr: "Mesures de Performance"
    },
    proceed: {
      en: "Proceed to Advanced Analysis",
      fr: "Passer à l'Analyse Avancée"
    },
    close: {
      en: "Close",
      fr: "Fermer"
    }
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
    "Syncing real-time data with the cloud",
    "Running predictive maintenance algorithm",
    "Optimizing gear ratios",
    "Monitoring temperature sensors"
  ];

  // ======================================================
  // GLOBAL SAFETY WRAPPER & FALLBACK FUNCTIONS
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
  
  function fallbackDragAndDrop() {
    console.warn("Fallback: Basic Drag & Drop not available. Draggables will remain static.");
    const draggables = document.querySelectorAll(".draggable");
    draggables.forEach(elem => elem.removeAttribute("draggable"));
  }
  
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
  // INSERT INLINE CSS STYLES (for fine-tuning if needed)
  // ======================================================
  function insertStyles() {
    const style = document.createElement("style");
    style.innerHTML = `
      /* Minimal inline fallback styles */
      .hover-light:hover {
        filter: brightness(1.2);
        transition: filter 0.2s ease;
      }
      .zoom-on-hover {
        transition: transform 0.3s ease;
      }
      .zoom-on-hover:hover {
        transform: scale(1.05);
      }
      .particle-effect {
        position: relative;
        overflow: hidden;
      }
      .particle-effect::after {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.5s ease;
      }
      .particle-effect:hover::after {
        opacity: 1;
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
    
    // Build the various UI sections
    createHeader(mainContainer);
    createButtons(mainContainer);
    createTextContext(mainContainer);
    createRemoveSubstringSection(mainContainer);
    createDraggableElements(mainContainer);
    createIoTSimulationSection(mainContainer);
    
    // Optionally, build a horizontal row layout if needed
    createHorizontalRow(mainContainer);
    
    // Initialize Nerd Metrics toggle button
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
    title.innerText = "Classical & Electric Mechanism Analysis";
    header.appendChild(title);
    
    const controlsContainer = document.createElement("div");
    header.appendChild(controlsContainer);
    
    // Language toggle button
    const langToggleButton = document.createElement("button");
    langToggleButton.id = "langToggleButton";
    langToggleButton.className = "bubble-button";
    langToggleButton.innerText = translations.toggleLanguage[currentLanguage];
    langToggleButton.addEventListener("click", toggleLanguage);
    controlsContainer.appendChild(langToggleButton);
    
    // Reset UI button
    const resetButton = document.createElement("button");
    resetButton.id = "resetButton";
    resetButton.className = "bubble-button";
    resetButton.innerText = translations.reset[currentLanguage];
    resetButton.addEventListener("click", resetUI);
    controlsContainer.appendChild(resetButton);
  }
  
  // Creates a row of buttons
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
  
  // Adds a context paragraph
  function createTextContext(parent) {
    const textContext = document.createElement("p");
    textContext.id = "textContext";
    textContext.innerText = translations.textContext[currentLanguage];
    parent.appendChild(textContext);
  }
  
  // Creates a section for substring removal functionality
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
  
  // Creates draggable elements for demonstration
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
      // Alternate emoji icons for variety
      draggable.innerHTML = i % 2 === 0 ? "🔧" : "⚙️";
      parent.appendChild(draggable);
    }
  }
  
  // Creates the IoT simulation section
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
  
  // Creates a horizontal row layout container (if needed)
  function createHorizontalRow(parent) {
    const rowContainer = document.createElement("div");
    rowContainer.className = "horizontal-row";
    // Example items in horizontal layout
    for (let i = 1; i <= 2; i++) {
      const rowItem = document.createElement("div");
      rowItem.className = "row-item";
      rowItem.innerText = `Horizontal Item ${i}`;
      rowContainer.appendChild(rowItem);
    }
    parent.appendChild(rowContainer);
  }
  
  // ======================================================
  // LANGUAGE & UI UPDATE METHODS
  // ======================================================
  function toggleLanguage() {
    currentLanguage = currentLanguage === "en" ? "fr" : "en";
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
    
    // Update Nerd Metrics if present
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
    document.querySelectorAll(".draggable").forEach(draggable => {
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
    ["Task", "Engineer", "Start Date", "End Date", "Status"].forEach(txt => {
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
    dummyData.forEach(rowData => {
      const row = document.createElement("tr");
      rowData.forEach(cellData => {
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
    
    document.querySelectorAll(".popup-trigger").forEach(trigger => {
      trigger.addEventListener("click", e => {
        e.stopPropagation();
        modal.style.display = "block";
        setTimeout(() => { modal.style.opacity = "1"; }, 100);
      });
    });
    
    document.getElementById("closeModal").addEventListener("click", e => {
      e.stopPropagation();
      modal.style.opacity = "0";
      setTimeout(() => { modal.style.display = "none"; }, 300);
    });
    window.addEventListener("click", e => {
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
    draggables.forEach(item => {
      item.setAttribute("draggable", true);
      item.addEventListener("dragstart", dragStart);
      item.addEventListener("click", () => { buzzElement(item); });
    });
    let dropZone = document.getElementById("dropZone");
    if (!dropZone) {
      dropZone = document.createElement("div");
      dropZone.id = "dropZone";
      dropZone.textContent = "Drop items here";
      document.body.appendChild(dropZone);
    }
    dropZone.addEventListener("dragover", e => {
      e.preventDefault();
      dropZone.style.backgroundColor = "#e0e0e0";
    });
    dropZone.addEventListener("dragleave", () => {
      dropZone.style.backgroundColor = "#f9f9f9";
    });
    dropZone.addEventListener("drop", e => {
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
    document.querySelectorAll(".buzz").forEach(elem => {
      elem.addEventListener("click", () => { buzzElement(elem); });
    });
  }
  function buzzElement(elem) {
    elem.classList.add("buzz-effect");
    setTimeout(() => { elem.classList.remove("buzz-effect"); }, 500);
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
      document.querySelectorAll(".draggable").forEach(elem => {
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
        state.forEach(item => {
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
        if (b.x + b.radius > canvas.width || b.x - b.radius < 0) b.dx = -b.dx;
        if (b.y + b.radius > canvas.height || b.y - b.radius < 0) b.dy = -b.dy;
    
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
    if (simulationIntervalID !== null) return;
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
      modal.style.display = (modal.style.display === "none" || modal.style.display === "") ? "block" : "none";
    } else {
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
      
      const closeModalBtn = document.createElement("button");
      closeModalBtn.innerText = translations.close[currentLanguage];
      closeModalBtn.className = "bubble-button";
      closeModalBtn.style.marginRight = "10px";
      closeModalBtn.addEventListener("click", () => {
        modal.style.display = "none";
        clearInterval(metricsInterval);
      });
      modal.appendChild(closeModalBtn);
      
      const proceedButton = document.createElement("button");
      proceedButton.innerText = translations.proceed[currentLanguage];
      proceedButton.className = "bubble-button";
      proceedButton.addEventListener("click", () => {
        const confirmed = confirm("Do you want to proceed to advanced analysis?");
        if (confirmed) {
          window.location.href = "advanced-analysis.html";
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
    draggables.forEach(draggable => {
      let emojiState = draggable.innerHTML === "🔧";
      setInterval(() => {
        draggable.innerHTML = emojiState ? "⚙️" : "🔧";
        emojiState = !emojiState;
      }, 5000);
    });
  }
  
  // ======================================================
  // INITIALIZATION (ON DOMCONTENTLOADED) WITH SAFETY LOOP
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
