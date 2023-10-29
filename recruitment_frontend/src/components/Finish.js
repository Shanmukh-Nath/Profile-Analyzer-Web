// SocialProfiles.js
import React, { useState } from 'react';
import axios from 'axios';

function Finish({ onFinish }) {
    window.onload(onFinish());

    return (
        <div>
            <h1>Successfully Submitted</h1>
        </div>
    );
}

export default Finish;
