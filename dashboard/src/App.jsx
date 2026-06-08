import React, { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

const demoAnswers = {
  '1.1': 'PASS', '1.2': 'FAIL', '5.2': 'FAIL', '6.3': 'FAIL', '11.2': 'PASS', '12.2': 'FAIL', '17.4': 'PASS'
}

export default function App() {
  const [data, setData] = useState(null)

  useEffect(() => {
    fetch('/api/assess', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ answers: demoAnswers })
    })
      .then(r => r.json())
      .then(setData)
      .catch(console.error)
  }, [])

  const chartData = data
    ? Object.entries(data.functions).map(([name, values]) => ({ name, maturity: values.maturity_pct }))
    : []

  return (
    <div style={{ fontFamily: 'sans-serif', padding: 24 }}>
      <h1>Audit Dashboard</h1>
      <p>CLI-first project with an optional dashboard companion.</p>
      {data && (
        <>
          <h2>Overall maturity: {data.overall.maturity_pct}%</h2>
          <div style={{ width: '100%', height: 320 }}>
            <ResponsiveContainer>
              <BarChart data={chartData}>
                <XAxis dataKey="name" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Bar dataKey="maturity" fill="#2563eb" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </>
      )}
    </div>
  )
}
