// ApplicantDetails.js
import './ApplicantDetails.css'
import React, { useState } from 'react';
import axios from 'axios';

function ApplicantDetails({ onNext, setEmail }) {
    const [name, setName] = useState('');
    const [email, setEmail1] = useState('');
    const [mobile, setMobile] = useState('');
    const handleEmailChange = (e) => {
        const newEmail = e.target.value;
        setEmail1(newEmail);
        setEmail(newEmail);
    };


    const handleSubmit = async () => {
        try {
            await axios.post('http://localhost:8000/api/applicant_profile/', { name, email, mobile });
            onNext();
        } catch (error) {
            console.error("Error saving applicant details:", error);
        }
    };

    return (
        <div>
            <h1>Applicant Details</h1>
            <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
            <input type="email" placeholder="Email" value={email} onChange={handleEmailChange} />
            <input type="tel" placeholder="Mobile" value={mobile} onChange={(e) => setMobile(e.target.value)} />
            <button onClick={handleSubmit}>Next</button>
        </div>
    );
}

export default ApplicantDetails;
