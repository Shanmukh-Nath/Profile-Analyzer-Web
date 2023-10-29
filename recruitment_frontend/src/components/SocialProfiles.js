// SocialProfiles.js
import React, { useState } from 'react';
import axios from 'axios';

function SocialProfiles({ onNext, email }) {
    const [facebook, setFacebook] = useState('');
    const [instagram, setInstagram] = useState('');
    const [github, setGitHub] = useState('');
    const [linkedin, setLinkedIn] = useState('');
    const [leetcode, setLeetCode] = useState('');
    // ... other social platforms ...

    const handleSubmit = async () => {
        const payload = {
            socials:{facebook,instagram,github,linkedin,leetcode},
            email:email
        };
        try {
            await axios.post('http://localhost:8000/api/submit_socials/', payload);
            onNext();
        } catch (error) {
            console.error("Error saving social profiles:", error);
        }
    };

    return (
        <div>
            <input type="text" placeholder="Facebook" value={facebook} onChange={(e) => setFacebook(e.target.value)} />
            <input type="text" placeholder="Instagram" value={instagram} onChange={(e) => setInstagram(e.target.value)} />
            <input type="text" placeholder="Github" value={github} onChange={(e) => setGitHub(e.target.value)} />
            <input type="text" placeholder="LeetCode" value={leetcode} onChange={(e) => setLeetCode(e.target.value)} />
            <input type="text" placeholder="LinkedIn" value={linkedin} onChange={(e) => setLinkedIn(e.target.value)} />
            {/* ... similar inputs for other platforms ... */}
            <button onClick={handleSubmit}>Next</button>
        </div>
    );
}

export default SocialProfiles;
