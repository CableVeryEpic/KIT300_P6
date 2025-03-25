const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("path");
const fs = require("fs");
const dotenv = require("dotenv");
const { Configuration, OpenAI } = require("openai");

dotenv.config();

let mainWindow;

app.whenReady().then(() => {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true, 
            contextIsolation: true,
            enableRemoteModule: false,
            preload: path.join(__dirname, "preload.js"),
        },
    });

    mainWindow.loadFile("index.html");
});

const openai = new OpenAI(process.env.OPENAI_API_KEY);

// Handle OpenAI API Request
ipcMain.handle("generate-content", async (event, prompt) => {
    try {
        const completion = await openai.chat.completions.create({
            model: "gpt-4o-mini",
            messages: [
                {
                    role: "user",
                    content: "translate the chinese name Quan Bai into IPA",
                },
            ],
        });

        return completion.choices[0].text.trim();
    } catch (error) {
        return `Error: ${error.message}`;
    }
});

// Handle CSV File Update
ipcMain.handle("update-csv", async (event, content) => {
    const csvFile = path.join(__dirname, "data.csv");

    try {
        // Append content to CSV
        fs.appendFileSync(csvFile, `"${content}"\n`);
        return "CSV Updated Successfully!";
    } catch (error) {
        return `Error updating CSV: ${error.message}`;
    }
});