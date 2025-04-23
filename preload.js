const { contextBridge, ipcRenderer } = require("electron");
const fs = require("fs");
const path = require("path");
const os = require("os");

contextBridge.exposeInMainWorld("electronAPI", {
    getPhoneticTranscription: async (name, country) => {
        const response = await fetch("http://localhost:8000/transcription", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, country })
        });
      
        return await response.json();
    },
    uploadFile: async (file) => {
        const formData = new FormData();
        formData.append("file", file);
    
        const response = await fetch("http://localhost:8000/batch-transcription", {
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

        return data; // For confirmation
    },
    transcribeSingle: async (first, last, country) => {
        const formData = {
            First: first,
            Last: last,
            Country: country
        };

        const response = await fetch('http://localhost:8000/transcription', {
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

        return data; // For confirmation
    }
});