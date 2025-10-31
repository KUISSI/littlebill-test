import { useState } from "react";
import axios from "axios";
import "./App.css";

type Customer = {
  id: number;
  first_name: string;
  last_name: string;
};

type Sale = {
  sale_id: number;
  created_at: Date;
  total: number;
  currency: string;
};

function App() {
  const [query, setQuery] = useState("");
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [sales, setSales] = useState<Sale[]>([]);

  const searchCustomers = async () => {
    try {
      const response = await axios.get(
        "http://localhost:8000/customers/search",
        {
          params: { query },
        }
      );
      setCustomers(response.data);
    } catch (error) {
      console.error("Error searching customers: ", error);
    }
  };

  const getSales = async (customerId: number) => {
    try {
      const response = await axios.get(`http://localhost:8000/sales`, {
        params: { customer_id: customerId },
      });
      setSales(response.data);
    } catch (error) {
      console.error("Error getting sales", error);
    }
  };

  return (
    <>
      <h1>Customer search</h1>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search customers..."
      />
      <button onClick={searchCustomers}>Search</button>
      <ul>
        {customers.map((customer) => (
          <li id="customer" key={customer.id} onClick={() => getSales(customer.id)}>
            {customer.first_name} {customer.last_name}
          </li>
        ))}
      </ul>

      <h2>Sales</h2>
      <ul>
        {sales.map((sale) => (
          <li key={sale.sale_id}>
            <strong>Sale ID:</strong> {sale.sale_id} <br />
            <strong>Date:</strong>{" "}
            {new Date(sale.created_at).toLocaleDateString()} <br />
            <strong>Total:</strong> €{sale.total} <br />
            <strong>Currency:</strong> {sale.currency}
            <hr />
          </li>
        ))}
      </ul>
    </>
  );
}

export default App;
