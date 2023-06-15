import streamlit as st

# CSS styles
st.markdown(
    """
    <style>
    .main {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin-top: 200px;
    }
    
    body {
        color: #f8f8f8;
        background-color: #1f1f1f;
    }
    
    .container {
        max-width: 400px;
        padding: 20px;
        margin: 0 auto;
        background-color: #333333;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
        text-align: center;
    }
    
    .upload-btn {
        margin-top: 20px;
    }
    
    .upload-btn label {
        display: block;
        width: 100%;
        background-color: #888888;
        color: #f8f8f8;
        padding: 20px;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        font-weight: bold;
    }
    
    .upload-btn label:hover {
        background-color: #aaaaaa;
    }
    
    .upload-btn label:active {
        background-color: #666666;
    }
    
    .download-link {
        margin-top: 20px;
        display: none;
    }
    
    .download-link a {
        color: #f8f8f8;
        text-decoration: none;
        transition: color 0.3s ease;
    }
    
    .download-link a:hover {
        color: #cccccc;
    }
    
    .separator {
        margin-top: 30px;
        border-top: 1px solid #f8f8f8;
        width: 100%;
    }
    
    .new-pdfs {
        margin-top: 30px;
        text-align: center;
    }
    
    .new-pdfs h2 {
        color: #f8f8f8;
        margin-bottom: 10px;
    }
    
    .new-pdfs ul {
        list-style-type: none;
        padding: 0;
    }
    
    .new-pdfs li {
        margin-bottom: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the app content
st.markdown(
    """
    <div class="container">
        <h1 style="margin-bottom: 20px; color: #f8f8f8;">OCR PDF</h1>
        <div class="upload-btn">
            <label for="pdf-file">Choose Files</label>
            <input type="file" id="pdf-file" accept=".pdf" multiple style="display: none;">
        </div>
        <div class="download-link" id="download-link">
            <a href="" download>Download OCR'd PDFs</a>
        </div>
    </div>
    
    <div class="separator"></div>
    
    <div class="new-pdfs" id="new-pdfs" style="display: none;">
        <h2>Newly OCR'd PDFs:</h2>
        <ul id="pdf-list"></ul>
    </div>
    """,
    unsafe_allow_html=True
)

# Add JavaScript code to handle file upload and display downloaded PDFs
st.markdown(
    """
    <script>
    const pdfFile = document.getElementById('pdf-file');
    const downloadLink = document.getElementById('download-link');
    const pdfList = document.getElementById('pdf-list');
    const newPDFsSection = document.getElementById('new-pdfs');

    pdfFile.addEventListener('change', (e) => {
        const files = Array.from(e.target.files);
        const formData = new FormData();

        files.forEach((file) => {
            formData.append('pdf-files', file);
        });

        fetch('/', {
            method: 'POST',
            body: formData
        })
        .then((response) => response.json())
        .then((data) => {
            downloadLink.href = data.downloadLink;
            downloadLink.style.display = 'block';

            // Display the list of newly OCR'd PDFs
            const pdfs = data.pdfs;
            if (pdfs.length > 0) {
                newPDFsSection.style.display = 'block';
                pdfList.innerHTML = '';

                pdfs.forEach((pdf) => {
                    const li = document.createElement('li');
                    li.textContent = pdf;
                    pdfList.appendChild(li);
                });
            }
        })
        .catch((error) => console.error(error));
    });
    </script>
    """,
    unsafe_allow_html=True
)
