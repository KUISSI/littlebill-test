import { useState } from 'react';
import axios from 'axios';
import './App.css'

type Customer = {
  first_name: string;
  last_name: string;
};

function App() {
  const [query, setQuery] = useState('');
  const [customers, setCustomers] = useState<Customer[]>([]);

  const searchCustomers = async () => {
    try {
      const response = await axios.get('http://localhost:8000/customers/search', {
        params: { query }
      });
      setCustomers(response.data);
    } catch (error) {
      console.error('Error searching customers: ', error);
      
    }
  };
  return (
    <>
      <h1>Customer search</h1>
      <input 
        type="text"
        value={query}
        onChange={ (e) => setQuery(e.target.value)}
        placeholder='Search customers...' 
        />
      <button onClick={searchCustomers}>Search</button>
      <ul>
        {customers.map((customer, index) => (
          <li key={index}>
            {customer.first_name}. {customer.last_name}
          </li>
        ))}
      </ul>
    </>
  )
}

export default App
