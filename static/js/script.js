
document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("fileInput");
    const uploadMessage = document.getElementById("uploadMessage");
    const selectedFilesSection = document.getElementById("selectedFilesSection");
    const selectedFilesList = document.getElementById("selectedFilesList");
    const documentList = document.getElementById("documentList");
    const totalFiles = document.getElementById("totalFiles");
    const storageUsed = document.getElementById("storageUsed");
    const clearFilesButton = document.getElementById("clearFiles");
    const searchInput = document.getElementById("searchInput");
    const uploadButton = document.getElementById("uploadButton");
    const categorySelect = document.getElementById("categorySelect");
    const categoryFilter = document.getElementById("categoryFilter");

    const MAX_FILE_SIZE = 10 * 1024 * 1024;

    const allowedExtensions = [
        "pdf", "doc", "docx", "txt",
        "jpg", "jpeg", "png"
    ];

    const allowedCategories = ["Documents", "Images", "Others"];

    let selectedFiles = [];
    let cloudFiles = [];

    // Format file sizes
    function formatSize(bytes) {
        if (!bytes || bytes === 0) return "0 Bytes";

        const units = ["Bytes", "KB", "MB", "GB"];
        const index = Math.min(
            Math.floor(Math.log(bytes) / Math.log(1024)),
            units.length - 1
        );

        return (
            (bytes / Math.pow(1024, index)).toFixed(2) +
            " " +
            units[index]
        );
    }

    // Display messages
    function showMessage(message, type = "success") {
        uploadMessage.textContent = message;
        uploadMessage.className = "message " + type;
    }

    // Validate file extension
    function isAllowedFile(file) {
        const extension = file.name.split(".").pop().toLowerCase();
        return allowedExtensions.includes(extension);
    }

    // Handle file selection
    fileInput.addEventListener("change", (event) => {
        const files = Array.from(event.target.files);

        if (files.length === 0) return;

        let accepted = 0;
        const rejected = [];

        files.forEach(file => {
            if (!isAllowedFile(file)) {
                rejected.push(file.name + " (unsupported format)");
                return;
            }

            if (file.size > MAX_FILE_SIZE) {
                rejected.push(file.name + " (exceeds 10 MB)");
                return;
            }

            const alreadyExists = selectedFiles.some(
                existing =>
                    existing.name === file.name &&
                    existing.size === file.size &&
                    existing.lastModified === file.lastModified
            );

            if (!alreadyExists) {
                selectedFiles.push(file);
                accepted++;
            }
        });

        if (rejected.length > 0) {
            showMessage(
                accepted + " accepted. Rejected: " + rejected.join(", "),
                "error"
            );
        } else if (accepted > 0) {
            showMessage(
                accepted + " file(s) selected successfully.",
                "success"
            );
        } else {
            showMessage("These files are already selected.", "error");
        }

        renderSelectedFiles();
        fileInput.value = "";
    });

    // Display selected files
    function renderSelectedFiles() {
        selectedFilesList.innerHTML = "";

        const totalSize = selectedFiles.reduce(
            (sum, file) => sum + file.size, 0
        );

        totalFiles.textContent = selectedFiles.length;
        storageUsed.textContent = formatSize(totalSize);

        selectedFilesSection.hidden = selectedFiles.length === 0;

        selectedFiles.forEach((file, index) => {
            const row = document.createElement("div");
            row.className = "file-row";

            const details = document.createElement("div");
            details.className = "file-details";

            const name = document.createElement("div");
            name.className = "file-name";
            name.textContent = file.name;

            const size = document.createElement("div");
            size.className = "file-size";
            size.textContent = formatSize(file.size);

            details.append(name, size);

            const removeButton = document.createElement("button");
            removeButton.type = "button";
            removeButton.className = "remove-file";
            removeButton.textContent = "Remove";

            removeButton.addEventListener("click", () => {
                selectedFiles.splice(index, 1);
                renderSelectedFiles();
                showMessage("File removed.", "success");
            });

            row.append(details, removeButton);
            selectedFilesList.appendChild(row);
        });
    }

    // Clear selected files
    clearFilesButton.addEventListener("click", () => {
        selectedFiles = [];
        renderSelectedFiles();
        showMessage("All selected files cleared.", "success");
    });

    // Upload files with selected category
    uploadButton.addEventListener("click", async () => {
        if (selectedFiles.length === 0) {
            showMessage("Please select files first.", "error");
            return;
        }

        const category = categorySelect.value;

        if (!allowedCategories.includes(category)) {
            showMessage("Please select a valid category.", "error");
            return;
        }

        const filesToUpload = [...selectedFiles];
        const failedFiles = [];
        let uploadedCount = 0;

        uploadButton.disabled = true;
        uploadButton.textContent = "Uploading...";

        try {
            for (const file of filesToUpload) {
                const formData = new FormData();

                formData.append("file", file);
                formData.append("category", category);

                try {
                    const response = await fetch("/upload", {
                        method: "POST",
                        body: formData
                    });

                    const result = await response.json();

                    if (!response.ok) {
                        throw new Error(result.error || "Upload failed");
                    }

                    selectedFiles = selectedFiles.filter(
                        selected => selected !== file
                    );

                    uploadedCount++;
                    renderSelectedFiles();

                } catch (error) {
                    failedFiles.push(file.name + ": " + error.message);
                }
            }

            if (uploadedCount > 0) {
                showMessage(
                    uploadedCount + " file(s) uploaded to " +
                    category + " successfully.",
                    "success"
                );

                await loadCloudFiles();
            }

            if (failedFiles.length > 0) {
                showMessage(
                    "Some uploads failed: " + failedFiles.join("; "),
                    "error"
                );
            }

        } finally {
            uploadButton.disabled = false;
            uploadButton.textContent = "Upload to Cloud";
        }
    });

    // Load files stored in Supabase Storage
    async function loadCloudFiles() {
        try {
            const response = await fetch("/files");
            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || "Unable to load files");
            }

            cloudFiles = result;
            renderCloudFiles();

        } catch (error) {
            cloudFiles = [];
            renderCloudFiles();

            const message = document.createElement("p");
            message.className = "file-size";
            message.textContent =
                "Unable to load cloud files. Please refresh the page.";

            documentList.appendChild(message);
            console.error("File loading error:", error);
        }
    }

    // Display cloud files
    function renderCloudFiles() {
        documentList.innerHTML = "";

        const query = searchInput.value.toLowerCase().trim();
        const selectedCategory = categoryFilter.value;

        const filteredFiles = cloudFiles.filter(file => {
            const matchesSearch =
                file.filename.toLowerCase().includes(query);

            const matchesCategory =
                selectedCategory === "all" ||
                file.category === selectedCategory;

            return matchesSearch && matchesCategory;
        });

        if (filteredFiles.length === 0) {
            const empty = document.createElement("div");
            empty.className = "empty-state";

            const heading = document.createElement("h3");
            heading.textContent = cloudFiles.length === 0
                ? "No documents uploaded"
                : "No matching documents found";

            const description = document.createElement("p");
            description.textContent =
                "Your cloud documents will appear here.";

            empty.append(heading, description);
            documentList.appendChild(empty);
            return;
        }

        filteredFiles.forEach(file => {
            const row = document.createElement("div");
            row.className = "file-row document-row";

            const details = document.createElement("div");
            details.className = "file-details";

            const storedName = file.filename.split("/").pop();

            const originalName = storedName.split("_").slice(1).join("_")
                || storedName;

            const name = document.createElement("div");
            name.className = "file-name";
            name.textContent = originalName;

            const size = document.createElement("div");
            size.className = "file-size";
            size.textContent =
                formatSize(file.size) + " · " +
                (file.category || "Uncategorized");

            details.append(name, size);

            const actions = document.createElement("div");
            actions.className = "file-actions";

            // Download button
            const downloadButton = document.createElement("button");
            downloadButton.type = "button";
            downloadButton.className = "remove-file";
            downloadButton.textContent = "Download";

            downloadButton.addEventListener("click", () => {
                window.location.href =
                    "/download/" + encodeURIComponent(file.filename);
            });

            // Delete button
            const deleteButton = document.createElement("button");
            deleteButton.type = "button";
            deleteButton.className = "remove-file";
            deleteButton.textContent = "Delete";

            deleteButton.addEventListener("click", async () => {
                if (!confirm("Are you sure you want to delete this file?")) {
                    return;
                }

                deleteButton.disabled = true;

                try {
                    const response = await fetch(
                        "/delete/" + encodeURIComponent(file.filename),
                        { method: "DELETE" }
                    );

                    const result = await response.json();

                    if (!response.ok) {
                        throw new Error(result.error || "Delete failed");
                    }

                    showMessage("File deleted successfully.", "success");
                    await loadCloudFiles();

                } catch (error) {
                    showMessage(error.message, "error");
                    deleteButton.disabled = false;
                }
            });

            actions.append(downloadButton, deleteButton);
            row.append(details, actions);

            documentList.appendChild(row);
        });
    }

    // Search cloud files
    searchInput.addEventListener("input", renderCloudFiles);

    // Filter cloud files by category
    categoryFilter.addEventListener("change", renderCloudFiles);

    // Initialize dashboard
    renderSelectedFiles();
    loadCloudFiles();

    console.log("CloudVault frontend initialized successfully.");
});
