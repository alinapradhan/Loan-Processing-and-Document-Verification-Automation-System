import { useState } from 'react'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api/v1'

export default function App() {
  const [files, setFiles] = useState([])
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const onSubmit = async (event) => {
    event.preventDefault()
    if (!files.length) {
      setError('Please select at least one document.')
      return
    }

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const formData = new FormData()
      files.forEach((file) => formData.append('files', file))

      const response = await axios.post(`${API_BASE}/process-loan-application`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setResult(response.data)
    } catch (e) {
      setError(e?.response?.data?.detail || 'Upload failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="container">
      <h1>Loan Processing & Document Verification</h1>
      <p>Upload Aadhaar, PAN, salary slips, bank statements, and loan form to evaluate eligibility.</p>

      <form onSubmit={onSubmit} className="card">
        <input
          type="file"
          multiple
          accept=".png,.jpg,.jpeg,.pdf"
          onChange={(e) => setFiles(Array.from(e.target.files || []))}
        />
        <button type="submit" disabled={loading}>{loading ? 'Processing...' : 'Process Application'}</button>
      </form>

      {error && <p className="error">{error}</p>}

      {result && (
        <section className="card">
          <h2>Decision</h2>
          <p><strong>Application ID:</strong> {result.application_id}</p>
          <p><strong>Approval Status:</strong> {result.score.approval_status}</p>
          <p><strong>Eligibility Score:</strong> {result.score.score}</p>
          <h3>Extracted Fields</h3>
          <pre>{JSON.stringify(result.consolidated_fields, null, 2)}</pre>
          <h3>Validation Issues</h3>
          <pre>{JSON.stringify(result.validation.issues, null, 2)}</pre>
        </section>
      )}
    </main>
  )
}
