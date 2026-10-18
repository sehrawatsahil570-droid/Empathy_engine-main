async function generateAudio() {
    const text = document.getElementById("textInput").value;
    const loader = document.getElementById("loader");
    const button = document.getElementById("generateBtn");

    if (!text.trim()) {
        alert("Please enter some text!");
        return;
    }

    // 🔥 Show loader + disable button
    loader.style.display = "block";
    button.disabled = true;

    try {
        const response = await fetch("http://127.0.0.1:8000/generate-audio", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text })
        });

        const data = await response.json();

        // 🔹 Emotion analysis
        const analysisDiv = document.getElementById("analysis");
        analysisDiv.innerHTML = "";

        data.analysis.forEach(item => {
            const p = document.createElement("p");
            p.innerText = `${item.emotion} → ${item.confidence}`;
            analysisDiv.appendChild(p);
        });

        // 🔥 FIXED audio path
        const audioPlayer = document.getElementById("audioPlayer");
        audioPlayer.src = "http://127.0.0.1:8000/" + data.audio_file;

    } catch (error) {
        console.error(error);
        alert("Something went wrong!");
    } finally {
        // 🔥 Hide loader + enable button
        loader.style.display = "none";
        button.disabled = false;
    }
}