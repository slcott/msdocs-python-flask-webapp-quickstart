import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

const Email = () => {

    const [emails, setEmails] = useState([]);


    useEffect(() => {
        fetch('/api/emails').then(res => res.json()).then(data => {
            // console.log(data)
            setEmails(data);
        });

    }, [])

    return (
        <div>
            <h1>Email</h1>
            {emails.map((result) => (
                <ul>
                    <li key={result.id}>
                        <h2>{result.contents.slice(0, 200)}</h2>
                        <Link to={`/email/${result['id']}`}>Link</Link>
                        <br />
                        <h3>keywords</h3>
                        <ul>
                            {result.keywords.map((keyword) =>
                                <li key={keyword}>
                                    {`${keyword[0]}`}
                                </li>
                            )}
                        </ul>
                        <br />
                        <h3>Contents</h3>
                        {result.contents.slice(0, 1000)}
                    </li>
                </ul>
            ))}
        </div>
    );
};

export default Email;