// import React, { useState } from 'react';
// import axios from 'axios';
// import './App.css';

// function App() {
//   const [query, setQuery] = useState('');
//   const [results, setResults] = useState([]);

//   const handleSearch = async () => {
//     try {
//       const response = await axios.post('http://localhost:5000/search', { query });
//       setResults(response.data);
//     } catch (error) {
//       console.error('Error fetching data', error);
//     }
//   };

//   return (
//     <div className="App">
//       <header className="App-header">
//         <h1>Restaurant Cuisine Finder</h1>
//         <input
//           type="text"
//           placeholder="Find restaurants in ____ miles"
//           value={query}
//           onChange={(e) => setQuery(e.target.value)}
//         />
//         <button onClick={handleSearch}>Search</button>
//         <div className="results">
//           {results.map((result, index) => (
//             <div key={index} className="result">
//               <h2>{result.name}</h2>
//               <p>{result.address}</p>
//               <p>Rating: {result.rating}</p>
//               <p>Price Level: {result.price_level}</p>
//             </div>
//           ))}
//         </div>
//       </header>
//     </div>
//   );
// }

// export default App;






// import React, { useState } from 'react';
// import axios from 'axios';
// import './App.css';

// function App() {
//   const [query, setQuery] = useState('');
//   const [radius, setRadius] = useState('');
//   const [results, setResults] = useState([]);
//   const [message, setMessage] = useState('');

//   const handleSearch = async () => {
//     try {
//       // Send the radius to the backend to fetch and preprocess the data
//       const locationResponse = await axios.post('http://localhost:5000/get_location_and_restaurants', { radius });
//       setMessage(locationResponse.data.message);

//       // Send the query to the backend to search in the preprocessed data
//       const searchResponse = await axios.post('http://localhost:5000/search', { query });
//       setResults(searchResponse.data);
//     } catch (error) {
//       console.error('Error fetching data', error);
//       setMessage('Error fetching data');
//     }
//   };

//   return (
//     <div className="App">
//       <header className="App-header">
//         <h1>Restaurant Cuisine Finder</h1>
//         <input
//           type="text"
//           className="input-large" /* to make the input box larger, in src/App.css */
//           placeholder="Find restaurants in ____ miles"
//           value={radius}
//           onChange={(e) => setRadius(e.target.value)}
//         />
//         {/* add questions */}
//         {/* <input
//           type="text"
//           placeholder="Enter your query..."
//           value={query}
//           onChange={(e) => setQuery(e.target.value)}
//         /> */}
//         <button onClick={handleSearch}>Search</button>
//         {message && <p>{message}</p>}
//         <div className="results">
//           {results.map((result, index) => (
//             <div key={index} className="result">
//               <h2>{result.name}</h2>
//               <p>{result.address}</p>
//               <p>Rating: {result.rating}</p>
//               <p>Price Level: {result.price_level}</p>
//             </div>
//           ))}
//         </div>
//       </header>
//     </div>
//   );
// }

// export default App;




import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import SignUp from './SignUp';
import CheckoutForm from './CheckoutForm';

function App() {
  const [query, setQuery] = useState('');
  const [radius, setRadius] = useState('');
  const [results, setResults] = useState([]);
  const [message, setMessage] = useState('');

  const handleSearch = async () => {
    try {
      console.log('Sending radius:', radius);
      // Send the radius to the backend to fetch and preprocess the data
      const locationResponse = await axios.post('http://localhost:5000/get_location_and_restaurants', { radius });
      console.log('Location response:', locationResponse.data);
      setMessage(locationResponse.data.message);

      // Send the query to the backend to search in the preprocessed data
      console.log('Sending query:', query);
      const searchResponse = await axios.post('http://localhost:5000/search', { query });
      console.log('Search response:', searchResponse.data);
      setResults(searchResponse.data);
    } catch (error) {
      console.error('Error fetching data:', error.response ? error.response.data : error.message);
      setMessage('Error fetching data');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Restaurant Cuisine Finder</h1>
        <input
          type="text"
          className="input-large"
          placeholder="Find restaurants in ____ miles"
          value={radius}
          onChange={(e) => setRadius(e.target.value)}
        />
        <input
          type="text"
          className="input-large" /* to make the input box larger, in src/App.css */
          placeholder="Find restaurants in ____ miles"
          value={radius}
          onChange={(e) => setRadius(e.target.value)}
        />
        {/* add questions */}
        {/* <input
          type="text"
          placeholder="Enter your query..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        /> */}
        <button onClick={handleSearch}>Search</button>
        {message && <p>{message}</p>}
        <div className="results">
          {results.map((result, index) => (
            <div key={index} className="result">
              <h2>{result.name}</h2>
              <p>{result.address}</p>
              <p>Rating: {result.rating}</p>
              <p>Price Level: {result.price_level}</p>
            </div>
          ))}
        </div>
        <SignUp />
        <CheckoutForm />
      </header>
    </div>
  );
}

export default App;
