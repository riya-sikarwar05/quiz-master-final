new Vue({
    el: "#appcsv", 
    data: {
        file: null,
        filename: "",
        message: ""
    },
    methods: {
        handleFileUpload(event) {
            const selectedFile = event.target.files[0];
            if (selectedFile && selectedFile.type === "text/csv") {
                this.file = selectedFile;
                this.filename = selectedFile.name;
            } else {
                this.message = "Please select a valid CSV file!";
                this.file = null;
                this.filename = "";
            }
        },
        uploadFile() {
            if (!this.file) {
                this.message = "Please select a file!";
                return;
            }
            let formData = new FormData();
            formData.append("file", this.file);
            fetch("/upload", {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                this.message = data.message;
            })
            .catch(error => {
                this.message = "Error uploading file!";
                console.error("Upload Error:", error);
            });
        }
    }
});