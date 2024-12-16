
import reactLogo from '../assets/react.svg'
// import viteLogo from '/vite.svg'
import React, { useState, useEffect } from 'react';
import './Time.css';

function Time() {
    const [currentTime, setCurrentTime] = useState(0);

    useEffect(() => {
        fetch('/api/time').then(res => res.json()).then(data => {
            setCurrentTime(data.time);
        });
    }, []);

    return (
        <div>

                {/* <a href="https://vite.dev" target="_blank">
                    <img src={viteLogo} className="logo" alt="Vite logo" />
                </a> */}
                {/* <a href="https://react.dev" target="_blank">
                    <img src={reactLogo} className="logo react" alt="React logo" />
                </a> */}

                <p>The current time is {currentTime}.</p>
        </div >
    );
}

export default Time;