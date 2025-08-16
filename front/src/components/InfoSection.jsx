export default function InfoSection() {
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
        onClick={() =>
          alert('More detailed info about the app')
        }
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
        Más info
      </button>
    </section>
  );
}
