import { useState } from 'react';

export default function InfoSection() {
  const [showModal, setShowModal] = useState(false);
  return (
    <section
      style={{
        padding: '2rem',
        backgroundColor: '#f5f5f5',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        textAlign: 'center',
        gap: '1rem',
        fontFamily: '"Oswald", sans-serif',
      }}
    >
      <p style={{ fontSize: '1.2rem', maxWidth: '700px', lineHeight: '1.6', margin: 0 }}>
        This app allows you to view historical data from weather stations.
        Select dates, seasons, and features to view the results.
      </p>
      <button
        onClick={() => setShowModal(true)}
        style={{
          padding: '0.6rem 1.2rem',
          border: 'none',
          borderRadius: '0.3rem',
          backgroundColor: '#1e1e2f',
          color: '#fff',
          cursor: 'pointer',
          fontSize: '1rem',
          fontWeight: '600',
          transition: 'background-color 0.3s',
        }}
        onMouseEnter={e => (e.currentTarget.style.backgroundColor = '#33334d')}
        onMouseLeave={e => (e.currentTarget.style.backgroundColor = '#1e1e2f')}
      >
        Detailed Info
      </button>
      {showModal && (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            backgroundColor: 'rgba(0,0,0,0.5)',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            zIndex: 1000,
          }}
          onClick={() => setShowModal(false)}
        >
          <div
            style={{
              backgroundColor: '#fff',
              padding: '2rem',
              borderRadius: '0.5rem',
              maxWidth: '700px',
              maxHeight: '80vh',
              overflowY: 'auto',
              textAlign: 'left',
              position: 'relative',
            }}
            onClick={e => e.stopPropagation()}
          >
            <div
              style={{
                padding: '2rem',
                fontFamily: '"Oswald", sans-serif',
                lineHeight: 1.7,
                color: '#333',
              }}
            >
              <h3
                style={{
                  marginTop: 0,
                  fontSize: '1.8rem',
                  color: '#1e1e2f',
                  borderBottom: '2px solid #1e1e2f',
                  paddingBottom: '0.3rem',
                }}
              >
                Detailed Information
              </h3>

              <p style={{ margin: '1rem 0', fontSize: '1rem' }}>
                This API retrieves and processes historical weather data from Antarctic stations provided by AEMET (Spanish Meteorological Agency).
              </p>

              <p style={{ margin: '1rem 0', fontSize: '1rem' }}>
                It includes temperature, atmospheric pressure, and wind speed, with customizable time aggregation for analysis.
              </p>

              <p style={{ margin: '1rem 0', fontSize: '1rem' }}>
                When selecting time aggregation, the mean for said period of time (hourly, daily, or monthly) is calculated, taking into account that period's registers.
              </p>

              <p style={{ margin: '1rem 0', fontSize: '1rem' }}>
                To ensure data consistency when interacting with the AEMET API while maintaining user interpretability, the solution converts input timestamps (in Madrid timezone, CET/CEST) to their UTC equivalent before making the AEMET API request, eliminating timezone ambiguities and daylight saving time variations. The UTC timestamps from AEMET are then converted back to Madrid timezone (including proper CET/CEST offsets: +01:00 or +02:00) in the final output, ensuring accurate local time representation that matches the operational context of the Antarctic stations while maintaining traceability to the original UTC reference.
              </p>

              <p style={{ margin: '1rem 0', fontSize: '1rem' }}>
                "Aggregation" and "Features" fields can be left blank, in which case the default values will be used: 10-minute aggregation (default AEMET's values) and all three features.
              </p>

              <p style={{ margin: '1rem 0', fontSize: '0.95rem', color: '#666' }}>
                Recomendation: Try with 1st and 2nd January 2024 for assured results (Unless AEMET's API considers that too many requests/minute were done)
              </p>

              <p style={{ margin: '1rem 0', fontSize: '0.95rem', color: '#666' }}>
                Note: Some recent data may not be available immediately from the API, and large date ranges may take a few seconds to load.
              </p>
            </div>

            <button
              onClick={() => setShowModal(false)}
              style={{
                position: 'absolute',
                top: '1rem',
                right: '1rem',
                background: 'transparent',
                border: 'none',
                fontSize: '1.2rem',
                cursor: 'pointer',
              }}
            >
              ✖
            </button>
          </div>
        </div>
      )}
    </section>
  );
}
