// import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
// import './App.css'

// function App() {
//   const [count, setCount] = useState(0)

//   return (
//     <>
//       <div>
//         <a href="https://vite.dev" target="_blank">
//           <img src={viteLogo} className="logo" alt="Vite logo" />
//         </a>
//         <a href="https://react.dev" target="_blank">
//           <img src={reactLogo} className="logo react" alt="React logo" />
//         </a>
//       </div>
//       <h1>Vite + React</h1>
//       <div className="card">
//         <button onClick={() => setCount((count) => count + 1)}>
//           count is {count}
//         </button>
//         <p>
//           Edit <code>src/App.tsx</code> and save to test HMR
//         </p>
//       </div>
//       <p className="read-the-docs">
//         Click on the Vite and React logos to learn more
//       </p>
//     </>
//   )
// }

// import React, { useState, useEffect } from 'react';
// // import logo from './logo.svg';
// import './App.css';

// function App() {
//   const [currentTime, setCurrentTime] = useState(0);

//   useEffect(() => {
//     fetch('/api/time').then(res => res.json()).then(data => {
//       setCurrentTime(data.time);
//     });
//   }, []);

//   return (
//     <div className="App">
//       <header className="App-header">

//         <a href="https://vite.dev" target="_blank">
//           <img src={viteLogo} className="logo" alt="Vite logo" />
//         </a>
//         <a href="https://react.dev" target="_blank">
//           <img src={reactLogo} className="logo react" alt="React logo" />
//         </a>

//         <p>The current time is {currentTime}.</p>
//       </header>
//     </div>
//   );
// }

import React from 'react';
import { Routes, Route, BrowserRouter } from "react-router-dom";
import Layout from "./components/Layout";
import Home from './pages/Home';
import NoMatch from './pages/NoMatch';
import Time from './pages/Time';
import Search from './pages/Search';
import EmailDetails from './pages/EmailDetails';
import Email from './pages/Email';

const App = () => {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />} >
            <Route index element={<Home />} />
            <Route path="search" element={<Search />} />
            <Route path="time" element={<Time />} />
            <Route path="email" element={<Email />} />
            <Route path="email/:emailId" element={<EmailDetails />} />
            <Route path="*" element={<NoMatch />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </>

  );
};


export default App;