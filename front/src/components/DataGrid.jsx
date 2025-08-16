export default function DataGrid({ data, features }) {
  const columns = ['station', 'fecha', ...(features.length === 0 ? ['temperatura', 'presion', 'viento'] : features)];

  return (
    <table border="1" cellPadding="5" style={{ width: '100%', marginTop: '1rem', borderCollapse: 'collapse' }}>
      <thead style={{ backgroundColor: '#eee' }}>
        <tr>
          {columns.map(col => (
            <th key={col}>{col}</th>
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
