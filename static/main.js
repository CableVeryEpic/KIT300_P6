const spinnerOverlay = document.getElementById("overlay-spinner");
const IPAChart = document.getElementById("ipa-chart");
const MobileIPAChart = document.getElementById("ipa-chart-mobile");
const localDevelopment = false;

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
            result = data[0];

            if (window.innerWidth > 600) {
                const table = document.getElementById("phonetics-table");
                const tableBody = table.getElementsByTagName("tbody")[0];

                tableBody.innerHTML = "";
                table.classList.remove("off");

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
            } else {
                const mobile_results_container = document.getElementById("mobile-phonetics-table");
                const mobile_results = document.getElementsByClassName("mob-result");
                const manual_input = document.getElementById("manual-section");
                const back_button = document.getElementById("returnToManual");
                const generate_button = document.getElementById("singleUploadBtn");

                manual_input.classList.add("off");
                generate_button.classList.add("off");

                mobile_results_container.classList.remove("off");
                back_button.classList.remove("off");

                let first_text = mobile_results[0].firstElementChild;
                let last_text = mobile_results[1].firstElementChild;
                let country_text = mobile_results[2].firstElementChild;
                let translation_text = mobile_results[3].firstElementChild;
                let audio_container = mobile_results[4];

                first_text.textContent = "First Name: " + result.First;
                last_text.textContent = "Last Name: " + result.Last;

                country_text.textContent = "Country/Countries: ";
                result.Country.forEach(country => { 
                country_text.textContent += country + ", ";
                });
                country_text.textContent = country_text.textContent.slice(0, -2);

                translation_text.textContent = "Phonetics: ";
                result.Translation.forEach(translation => {
                translation_text.textContent += translation + ", ";
                })
                translation_text.textContent = translation_text.textContent.slice(0, -2);

                result.Filename.forEach(file => {
                    let audioItem = document.createElement("div");
                    audioItem.innerHTML = `<audio controls>
                                        <source src="/audio/${file}" type="audio/mpeg">
                                        Your browser does not support the audio element.
                                        </audio>`;
                    audio_container.appendChild(audioItem);
                });

            }
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
        if (window.innerWidth > 600) {
            IPAChart.classList.remove("off");
        } else {
            MobileIPAChart.classList.remove("off");
        }
    } else {
        if (window.innerWidth > 600) {
            IPAChart.classList.add("off");
        } else {
            MobileIPAChart.classList.remove("off");
        }
    }
}

function isChartOff() {
    if (IPAChart.classList.contains("off")) {
        return true;
    } else {
        return false;
    }
}

function manualBack() {
    const manual_input = document.getElementById("manual-section");
    const mobile_results = document.getElementById("mobile-phonetics-table");

    const generate_button = document.getElementById("singleUploadBtn");
    const back_button = document.getElementById("returnToManual");

    mobile_results.classList.add("off");
    back_button.classList.add("off");

    manual_input.classList.remove("off");
    generate_button.classList.remove("off");
}

const chartButton = document.querySelector('#open-chart');
const chartExit = document.querySelector("#close-chart");
const uploadButton = document.querySelector('#input');
const manualButton = document.querySelector('#singleUploadBtn');
const manualBackButton = document.querySelector("#returnToManual");
const mobileChartExit = document.querySelector("#close-mobile-chart")

if (chartButton) {
    chartButton.addEventListener("click", () => { isChartOff() ? toggleChart(true) : toggleChart(false) });
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

if (manualBackButton) {
    manualBackButton.addEventListener("click", manualBack);
}

if (mobileChartExit) {
    mobileChartExit.addEventListener("click", () => { document.getElementById("ipa-chart-mobile").classList.add("off"); });
}