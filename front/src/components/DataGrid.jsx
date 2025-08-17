export default function DataGrid({ data, features }) {
  const featureMap = { temp: 'Temperatura', pres: 'Presión', vel: 'Viento' };
  
  const columns = ['nombre', 'fhora', ...(features.length === 0 ? ['temp', 'pres', 'vel'] : features)];

  return (
    <table border="1" cellPadding="5" style={{ width: '100%', marginTop: '1rem', borderCollapse: 'collapse', marginBottom: '5rem'}}>
      <thead style={{ backgroundColor: '#eee' }}>
        <tr>
          {columns.map(col => (
            <th key={col}>
              {col === 'nombre' ? 'Estación' : col === 'fhora' ? 'Fecha' : featureMap[col] || col}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, idx) => (
          <tr key={idx}>
            {columns.map(col => (
              <td key={col}>{row[col]}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
