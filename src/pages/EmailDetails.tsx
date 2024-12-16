import React, { Suspense, useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';

const EmailDetails = () => {
    const { emailId } = useParams();
    const [email, setEmail] = useState({ contents: '', keywords: [], id: emailId});
    const [isLoading, setIsLoading] = useState(true);

    

    useEffect(() => {
        fetch('/api/emails/' + emailId).then(res => res.json()).then(data => {
            console.log(data)
            setEmail(data);
            setIsLoading(false);
        });
    }, [])

    const message = (
        <>
            <h2> {email.contents.slice(0, 200)}</h2>
            <h3>keywords</h3>
            <ul>
                {email.keywords.map((keyword) =>
                    <li key={keyword}>
                        {`${keyword[0]}`}
                    </li>
                )}
            </ul>
            <br />
            <h3>Contents</h3>
            {email.contents}
        </>
    );

    return (
        <div>
            <h1>Email Details</h1>
            <div>
                {/* {isLoading
                    ? "loading..."
                    : email && message
                } */}
                <Suspense fallback={"...loading"}>
                    {message}
                </Suspense>
            </div>
        </div >
    );
};

export default EmailDetails;