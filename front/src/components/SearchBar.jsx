import { useState } from 'react';

export default function SearchBar({ setSearchParams }) {
  const today = new Date().toISOString().split('T')[0];

  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [station, setStation] = useState('Juan Carlos I');
  const [features, setFeatures] = useState([]);
  const [aggregation, setAggregation] = useState('Default');

  const allFeatures = ['temperatura', 'presion', 'viento'];

  const handleStationChange = (e) => {
    const value = e.target.value;
    setStation(value);
    if (value === 'Gabriel de Castilla') {
      alert('⚠️ This station is known to have issues!');
    }
  };

  const handleFeatureToggle = (feature) => {
    setFeatures((prev) =>
      prev.includes(feature) ? prev.filter((f) => f !== feature) : [...prev, feature]
    );
  };

  const handleSearch = () => {
    setSearchParams({
      startDate,
      endDate,
      station,
      features,
      aggregation,
    });
  };

  return (
    <section
      style={{
        width: '93%',
        background: '#fff',
        padding: '1.5rem',
        margin: '1.5rem auto',
        boxShadow: '0 2px 6px rgba(0,0,0,0.15)',
      }}
    >
      <h2
        style={{
          marginBottom: '1rem',
          fontFamily: '"Montserrat", sans-serif',
          fontWeight: '600',
          fontSize: '1.3rem',
          color: '#1e1e2f',
        }}
      >
        Search Parameters
      </h2>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: '1rem',
          alignItems: 'center',
        }}
      >
        {/* Dates */}
        <div>
          <label style={{ fontWeight: 500 }}>Start Date</label>
          <input
            type="date"
            max={today}
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            style={{
              display: 'block',
              width: '200px',
              padding: '0.4rem',
              marginTop: '0.3rem',
              borderRadius: '0.3rem',
              border: '1px solid #ccc',
            }}
          />
        </div>

        <div>
          <label style={{ fontWeight: 500 }}>End Date</label>
          <input
            type="date"
            max={today}
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            style={{
              display: 'block',
              width: '200px',
              padding: '0.4rem',
              marginTop: '0.3rem',
              borderRadius: '0.3rem',
              border: '1px solid #ccc',
            }}
          />
        </div>

        {/* Station */}
        <div>
          <label style={{ fontWeight: 500 }}>Station</label>
          <select
            value={station}
            onChange={handleStationChange}
            style={{
              display: 'block',
              width: '215px',
              padding: '0.4rem',
              marginTop: '0.3rem',
              borderRadius: '0.3rem',
              border: '1px solid #ccc',
            }}
          >
            <option value="Juan Carlos I">Meteo Station Juan Carlos I</option>
            <option value="Gabriel de Castilla">Meteo Station Gabriel de Castilla</option>
          </select>
        </div>

        {/* Aggregation */}
        <div>
          <label style={{ fontWeight: 500 }}>Aggregation</label>
          <select
            value={aggregation}
            onChange={(e) => setAggregation(e.target.value)}
            style={{
              display: 'block',
              width: '215px',
              padding: '0.4rem',
              marginTop: '0.3rem',
              borderRadius: '0.3rem',
              border: '1px solid #ccc',
            }}
          >
            <option value="Default">Default</option>
            <option value="Hourly">Hourly</option>
            <option value="Daily">Daily</option>
            <option value="Monthly">Monthly</option>
          </select>
        </div>
      </div>

      {/* Features */}
      <div style={{ marginTop: '1rem' }}>
        <label style={{ fontWeight: 500, display: 'block', marginBottom: '0.4rem' }}>
          Features
        </label>
        <div style={{ display: 'flex', gap: '1rem' }}>
          {allFeatures.map((f) => (
            <label key={f} style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
              <input
                type="checkbox"
                checked={features.includes(f)}
                onChange={() => handleFeatureToggle(f)}
              />
              {f}
            </label>
          ))}
        </div>
      </div>

      {/* Button */}
      <div style={{ marginTop: '1.5rem', textAlign: 'right' }}>
        <button
          onClick={handleSearch}
          style={{
            backgroundColor: '#1e1e2f',
            color: '#fff',
            border: 'none',
            padding: '0.6rem 1.2rem',
            borderRadius: '0.4rem',
            fontSize: '1rem',
            cursor: 'pointer',
            transition: 'background 0.2s',
          }}
          onMouseOver={(e) => (e.target.style.backgroundColor = '#333')}
          onMouseOut={(e) => (e.target.style.backgroundColor = '#1e1e2f')}
        >
          🔍 Search
        </button>
      </div>
    </section>
  );
}
