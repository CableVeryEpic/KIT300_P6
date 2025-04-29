async function uploadFile(file) {
    const fileInput = document.getElementById("input");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file first.");
        return;
    }

    try {
        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch("https://kit300-p6.fly.dev/batch-transcription", {
        method: "POST",
        body: formData,
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Failed: ${errorText}`);
        }
  
        const data = await response.json();
        sessionStorage.setItem("transcriptionData", JSON.stringify(data))
        window.location.href = "generate.html";
    } catch (err) {
        alert("Error: " + err.message);
    }
}

async function transcribeSingle(first, last, country) {
    const first = document.getElementById("manual-first").value.trim();
    const last = document.getElementById("manual-last").value.trim();
    const country = document.getElementById("manual-country").value.trim();

    if (!first || !last) {
        alert("Please enter first name, last name and optionally country of origin.");
        return;
    }

    try {
        const formData = {
            First: first,
            Last: last,
            Country: country
        };

        const response = await fetch('https://kit300-p6.fly.dev/transcription', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Failed: ${errorText}`);
        }

        const data = await response.json();
        sessionStorage.setItem("transcriptionData", JSON.stringify(data))
        window.location.href = "generate.html";
    } catch (err) {
        alert("Error: " + err.message);
    }
}

function toggleInput(type) {
    document.getElementById("csv-section").style.display = type === 'csv' ? 'flex' : 'none';
    document.getElementById("manual-section").style.display = type === 'manual' ? 'flex' : 'none';
}