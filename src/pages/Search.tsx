import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Search.css';


const Search = () => {
    const [text, setText] = useState('');
    const [results, setResults] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

    const handleChange = (event) => {
        setText(event.target.value)
        // console.log(text);
    }

    const handleClick = (event) => {
        event.preventDefault()
        setIsLoading(true);
        fetch('/api/email_search?query=' + text + '&k=' + 5).then(res => res.json()).then(data => {
            setResults(data);
            // console.log(data)
            setIsLoading(false);
        });
        // setText('');
    }

    const listStyle = {
        listStyleType: 'none',
    }

    const convertToBold = (contents: string) => {
        var re = new RegExp(text, 'g');
        return contents.replace(re, `<strong>${text}</strong>`);
    }

    return (
        <div>
            <h1>Search</h1>
            <form>
                <label>
                    Query:
                    <input value={text} onChange={handleChange} type="text" name="name" />
                </label>
                {/* <input type="submit" value="Submit" /> */}
                <button onClick={(e) => handleClick(e)}>Submit</button>
                <br />
                <br />
                {isLoading && "...loading"}
            </form>
            <div>
                {results.map((email) => (
                    <div className='email'>
                        <ul>
                            <li key={email.id} style={listStyle}>
                                <Link to={`/email/${email['id']}`}>
                                    <h2> {email.contents.slice(0, 200)}</h2>
                                </Link>
                                <h3>keywords</h3>
                                {email.keywords.map((keyword) =>
                                    <span key={keyword}>
                                        {`${keyword[0]} | `}
                                    </span>
                                )}
                                <br />
                                <h3>Contents</h3>
                                {/* {email.contents} */}
                                <div dangerouslySetInnerHTML={{ __html: convertToBold(email.contents) }} />
                            </li>
                        </ul>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Search;