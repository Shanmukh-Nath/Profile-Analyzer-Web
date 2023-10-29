// UploadResume.js
import React, { useState } from 'react';
import axios from 'axios';

function UploadResume({ onNext, email }) {
    const [file, setFile] = useState(null);

    const handleSubmit = async () => {
        const formData = new FormData();
        formData.append('resume', file);
        formData.append('email',email);

        try {
            await axios.post('http://localhost:8000/api/upload_resume/', formData);
            onNext();
        } catch (error) {
            console.error("Error uploading resume:", error);
        }
    };

    return (
        <div>
            <h1>Upload Resume</h1>
            <input type="file" onChange={(e) => setFile(e.target.files[0])} />
            <button onClick={handleSubmit}>Finish</button>
        </div>
    );
}

export default UploadResume;
