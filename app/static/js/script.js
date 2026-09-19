const dropzone = document.getElementById("dropzone");
const audioInput = document.getElementById("audioInput");
const dropzoneText = document.getElementById("dropzoneText");
const audioPreview = document.getElementById("audioPreview");
const predictBtn = document.getElementById("predictBtn");
const uploadForm = document.getElementById("uploadForm");
const loading = document.getElementById("loading");
const errorBox = document.getElementById("errorBox");
const resultCard = document.getElementById("result");
const resultEmoji = document.getElementById("resultEmoji");
const resultLabel = document.getElementById("resultLabel");
const resultConfidence = document.getElementById("resultConfidence");
const breakdownEl = document.getElementById("breakdown");

let currentFile = null;

function setFile(file) {
    currentFile = file;
    dropzoneText.textContent = file.name;
    audioPreview.src = URL.createObjectURL(file);
    audioPreview.style.display = "block";
    predictBtn.disabled = false;
    resultCard.style.display = "none";
    errorBox.style.display = "none";
}

audioInput.addEventListener("change", (e) => {
    if (e.target.files.length) {
        setFile(e.target.files[0]);
    }
});

["dragenter", "dragover"].forEach((evt) => {
    dropzone.addEventListener(evt, (e) => {
        e.preventDefault();
        dropzone.classList.add("dragover");
    });
});

["dragleave", "drop"].forEach((evt) => {
    dropzone.addEventListener(evt, (e) => {
        e.preventDefault();
        dropzone.classList.remove("dragover");
    });
});

dropzone.addEventListener("drop", (e) => {
    const file = e.dataTransfer.files[0];
    if (file) setFile(file);
});

// Sample buttons: fetch a bundled sample wav and treat it like an upload
document.querySelectorAll(".sample-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
        const sampleName = btn.dataset.sample;
        const res = await fetch(`/static/sample_audio/${sampleName}`);
        const blob = await res.blob();
        const file = new File([blob], sampleName, { type: "audio/wav" });
        setFile(file);
    });
});

uploadForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!currentFile) return;

    errorBox.style.display = "none";
    resultCard.style.display = "none";
    loading.style.display = "flex";
    predictBtn.disabled = true;

    const formData = new FormData();
    formData.append("audio_file", currentFile);

    try {
        const response = await fetch("/predict", {
            method: "POST",
            body: formData,
        });
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong.");
        }

        renderResult(data);
    } catch (err) {
        errorBox.textContent = err.message;
        errorBox.style.display = "block";
    } finally {
        loading.style.display = "none";
        predictBtn.disabled = false;
    }
});

function renderResult(data) {
    resultEmoji.textContent = data.emoji;
    resultLabel.textContent = data.prediction;
    resultConfidence.textContent = `${data.confidence}% confidence`;

    breakdownEl.innerHTML = "";
    data.breakdown.forEach((row) => {
        const rowEl = document.createElement("div");
        rowEl.className = "breakdown-row";
        rowEl.innerHTML = `
            <span class="breakdown-label">${row.emotion}</span>
            <span class="breakdown-bar-track">
                <span class="breakdown-bar-fill" style="width:${row.probability}%"></span>
            </span>
            <span class="breakdown-value">${row.probability}%</span>
        `;
        breakdownEl.appendChild(rowEl);
    });

    resultCard.style.display = "block";
}
