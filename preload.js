const { contextBridge, ipcRenderer } = require("electron");
const fs = require("fs");
const path = require("path");
const os = require("os");

contextBridge.exposeInMainWorld("electronAPI", {
    generateContent: (prompt) => ipcRenderer.invoke("generate-content", prompt),
    updateCSV: (content) => ipcRenderer.invoke("update-csv", content),
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
      
        const blob = await response.blob();
        const arrayBuffer = await blob.arrayBuffer();
        const buffer = Buffer.from(arrayBuffer);
    
        const downloadsDir = path.join(os.homedir(), "Documents/Uni\ Study/KIT300");
        const outputPath = path.join(downloadsDir, "phonetic_results.csv");
    
        fs.writeFileSync(outputPath, buffer);
    
        return outputPath; // For confirmation
    }
});