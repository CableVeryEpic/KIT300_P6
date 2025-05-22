const spinnerOverlay = document.getElementById("overlay-spinner");
const IPAChart = document.getElementById("ipa-chart");
const localDevelopment = true;

URLStart = ""
if (localDevelopment) {
    URLStart = "http://localhost:8000"
} else {
    URLStart = "https://kit300-p6.fly.dev"
}

async function uploadFile() {
    const fileInput = document.getElementById("input");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file first.");
        return;
    }

    try {
        spinnerOverlay.style.display = "flex";

        const formData = new FormData();
        formData.append("file", file);

        console.log("Fetching transcription...");

        const response = await fetch(URLStart + "/batch-transcription", {
        method: "POST",
        body: formData,
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Failed: ${errorText}`);
        }
  
        console.log("Awaiting Data...");
        const data = await response.json();
        console.log("Setting Data...");
        sessionStorage.setItem("transcriptionData", JSON.stringify(data))
        console.log("Redirecting...");
        window.location.href = "/generate.html";
    } catch (err) {
        alert("Error: " + err.message);
    } finally {
        spinnerOverlay.style.display = "none";
    }
}

async function transcribeSingle() {
    const first = document.getElementById("manual-first").value.trim();
    const last = document.getElementById("manual-last").value.trim();
    const country = document.getElementById("manual-country").value.trim();

    if (!first || !last) {
        alert("Please enter first name, last name and optionally country of origin.");
        return;
    }

    try {

        spinnerOverlay.style.display = "flex";

        const formData = {
            First: first,
            Last: last,
            Country: country
        };

        const response = await fetch(URLStart + '/transcription', {
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

        if (data) {
            console.log(data);
            const table = document.getElementById("phonetics-table");
            const tableBody = table.getElementsByTagName("tbody")[0];

            tableBody.innerHTML = "";
            table.classList.remove("off");

            data.forEach(result => {
                const row = document.createElement("tr");

                const firstCell = document.createElement("td");
                firstCell.classList.add("first-col");
                firstCell.textContent = result.First;
                row.appendChild(firstCell);

                const lastCell = document.createElement("td");
                lastCell.classList.add("last-col");
                lastCell.textContent = result.Last;
                row.appendChild(lastCell);

                const countryCell = document.createElement("td");
                countryCell.classList.add("country-col");

                const countryList = document.createElement("ul");
                result.Country.forEach(country => {
                    let countryItem = document.createElement("li")
                    countryItem.textContent = country;
                    countryList.appendChild(countryItem);
                });
                countryCell.appendChild(countryList);
                row.appendChild(countryCell);

                const translationCell = document.createElement("td")
                translationCell.classList.add("phonetics-col");

                const transList = document.createElement("ul");
                result.Translation.forEach(translation => {
                    let transItem = document.createElement("li")
                    transItem.textContent = translation;
                    transList.appendChild(transItem);
                }); 
                translationCell.appendChild(transList);
                row.appendChild(translationCell);

                const audioCell = document.createElement("td");
                audioCell.classList.add("audio-col");

                const audioList = document.createElement("ul");
                result.Filename.forEach(file => {
                    let audioItem = document.createElement("li");
                    audioItem.innerHTML = `<audio controls>
                                        <source src="/audio/${file}" type="audio/mpeg">
                                        Your browser does not support the audio element.
                                        </audio>`;
                    audioList.appendChild(audioItem);
                });
                audioCell.appendChild(audioList);
                row.appendChild(audioCell);

                tableBody.appendChild(row);
                });
            } else {
                // Handle the case where data is not available
                alert("No transcription data found.");
            }
    } catch (err) {
        alert("Error: " + err.message);
    } finally {
        spinnerOverlay.style.display = "none";
    }
}

function toggleChart(toggle) {
    if (toggle === true) {
        IPAChart.classList.remove("off");
    } else {
        IPAChart.classList.add("off");
    }
}

const chartButton = document.querySelector('#open-chart');
const chartExit = document.querySelector("#close-chart");
const uploadButton = document.querySelector('#input');
const manualButton = document.querySelector('#singleUploadBtn');

if (chartButton) {
    chartButton.addEventListener("click", () => { toggleChart(true) });
}

if (chartExit) {
    chartExit.addEventListener("click", () => { toggleChart(false) });
}

if (uploadButton) {
    uploadButton.addEventListener("input", uploadFile);
}

if (manualButton) {
    manualButton.addEventListener("click", transcribeSingle);
}