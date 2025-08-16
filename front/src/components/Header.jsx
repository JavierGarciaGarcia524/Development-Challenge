import { useState } from 'react';
import logo from '../assets/logo.png';

export default function Header() {
  const [showTooltip, setShowTooltip] = useState(false);

  const toggleTooltip = () => setShowTooltip(!showTooltip);

  return (
    <header
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '1rem 2rem',
        backgroundColor: '#1e1e2f',
        color: '#ffffff',
        boxShadow: '0 2px 6px rgba(0,0,0,0.2)',
      }}
    >
      {/* Logo & Title */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <img
          src={logo}
          alt="Logo"
          style={{
            height: '60px',
            width: '60px',
            objectFit: 'contain',
          }}
        />
        <h1
          style={{
            fontFamily: '"Montserrat", sans-serif',
            fontWeight: 700,
            fontSize: '1.8rem',
            margin: 0,
          }}
        >
          Meteo-Antartica
        </h1>
      </div>

      {/* Toggle menú */}
      <div style={{ position: 'relative' }}>
        <button
          onClick={toggleTooltip}
          style={{
            background: 'transparent',
            border: '2px solid #fff',
            borderRadius: '0.3rem',
            padding: '0.5rem 0.8rem',
            color: '#fff',
            cursor: 'pointer',
            fontSize: '1.2rem',
          }}
        >
          ☰
        </button>

        {/* Tooltip */}
        {showTooltip && (
          <div
            style={{
              position: 'absolute',
              top: '120%',
              right: 0,
              backgroundColor: '#333',
              color: '#fff',
              padding: '0.5rem 1rem',
              borderRadius: '0.3rem',
              whiteSpace: 'nowrap',
              boxShadow: '0 2px 6px rgba(0,0,0,0.3)',
              zIndex: 10,
            }}
          >
            Partial version: other features not available
          </div>
        )}
      </div>
    </header>
  );
}
