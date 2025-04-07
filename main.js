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