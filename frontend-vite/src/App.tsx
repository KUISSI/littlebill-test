import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [nom, setNom] = useState('')
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const apiUrl = import.meta.env.VITE_API_URL

  // Fonction appelée lors de la soumission du formulaire
  const handleSearch = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true)
    setError(null)
    setData([])

    try {
      const response = await fetch(`${apiUrl}/customers?nom=${encodeURIComponent(nom)}`)
      if (!response.ok) {
        throw new Error("Error during API request")
      }
      const result = await response.json()
      setData(result)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="App">
      <h1>Recherche de customers</h1>
      <form onSubmit={handleSearch}>
        <input
          type="text"
          value={nom}
          placeholder="seek name"
          onChange={e => setNom(e.target.value)}
        />
        <button type="submit" disabled={loading || !nom}>
          Search
        </button>
      </form>
      {loading && <p>Loading...</p>}
      {error && <p style={{color: 'red'}}>{error}</p>}
      <div>
        <h2>Results</h2>
        <pre>{JSON.stringify(data, null, 2)}</pre>
      </div>
    </div>
  )
}

export default App