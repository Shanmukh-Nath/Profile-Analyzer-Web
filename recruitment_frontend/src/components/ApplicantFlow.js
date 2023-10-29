// ApplicantFlow.js
import React, { useState } from 'react';
import ApplicantDetails from './ApplicantDetails';
import QuestionsComponent from './QuestionsComponent';
import SocialProfiles from './SocialProfiles';
import UploadResume from './UploadResume';
import Finish from './Finish';

function ApplicantFlow() {
    const [step, setStep] = useState(1);
    const [email, setEmail] = useState('');

    const handleNext = () => setStep(step + 1);

    return (
        <div>
            {step === 1 && <ApplicantDetails setEmail={setEmail} onNext={handleNext} />}
            {step === 2 && <QuestionsComponent email={email} onNext={handleNext} />}
            {step === 3 && <SocialProfiles email={email} onNext={handleNext} />}
            {step === 4 && <UploadResume email={email} onNext={() => alert("Application submitted!")} />}
            {step === 5 && <Finish onFinish={()=>alert("Successpage")} />}
        </div>
    );
}

export default ApplicantFlow;
