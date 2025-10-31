import { useState } from 'react'
import './App.css'

type Customer = {
  nom: string
  prenom: string
  customers_id: number // adapte ce champ si besoin, selon la réponse de ton backend
}

type Sale = {
  sale_id: number
  date: string
  total: number
  // ajoute d'autres champs selon la réponse réelle de l'API
}

function App() {
  const [nom, setNom] = useState('')
  const [customers, setCustomers] = useState<Customer[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [selectedCustomer, setSelectedCustomer] = useState<Customer | null>(null)
  const [sales, setSales] = useState<Sale[]>([])
  const [salesLoading, setSalesLoading] = useState(false)
  const [salesError, setSalesError] = useState<string | null>(null)

  const apiUrl = import.meta.env.VITE_API_URL

  // Recherche clients
  const handleSearch = async (event: React.FormEvent) => {
    event.preventDefault()
    setLoading(true)
    setError(null)
    setCustomers([])
    setSelectedCustomer(null)
    setSales([])
    try {
      const response = await fetch(`${apiUrl}/customers?nom=${encodeURIComponent(nom)}`)
      if (!response.ok) {
        throw new Error("Erreur lors de la recherche client")
      }
      const result = await response.json()
      setCustomers(result)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  // Sélection d'un client → charge ses ventes
  const handleCustomerClick = async (customer: Customer) => {
    setSelectedCustomer(customer)
    setSales([])
    setSalesError(null)
    setSalesLoading(true)
    try {
      // Adapte le champ customers_id si besoin
      const response = await fetch(`${apiUrl}/customer/${customer.customers_id}/sales`)
      if (!response.ok) {
        throw new Error("Erreur lors du chargement des ventes")
      }
      const result = await response.json()
      setSales(result)
    } catch (err: any) {
      setSalesError(err.message)
    } finally {
      setSalesLoading(false)
    }
  }

  return (
    <div className="App">
      <h1>Recherche de clients</h1>
      <form onSubmit={handleSearch}>
        <input
          type="text"
          value={nom}
          placeholder="Nom du client"
          onChange={e => setNom(e.target.value)}
        />
        <button type="submit" disabled={loading || !nom.trim()}>
          Rechercher
        </button>
      </form>
      {loading && <p>Chargement...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <div>
        <h2>Résultats</h2>
        <ul>
          {customers.length === 0 && !loading && <li>Aucun résultat</li>}
          {customers.map((c, i) => (
            <li key={i}>
              <button onClick={() => handleCustomerClick(c)}>
                {c.prenom} {c.nom}
              </button>
            </li>
          ))}
        </ul>
      </div>

      {selectedCustomer && (
        <div>
          <h2>Ventes pour {selectedCustomer.prenom} {selectedCustomer.nom}</h2>
          {salesLoading && <p>Chargement des ventes...</p>}
          {salesError && <p style={{ color: 'red' }}>{salesError}</p>}
          <ul>
            {sales.length === 0 && !salesLoading && <li>Aucune vente trouvée</li>}
            {sales.map((s, i) => (
              <li key={i}>
                {/* adapte les champs à ta structure */}
                Vente n°{s.sale_id}, date: {s.date}, total: {s.total}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default App