export default function Footer() {
  return (
    <footer
      style={{
        width: '37%',
        position: 'fixed',
        bottom: 0,
        padding: '1rem 2rem',
        backgroundColor: '#1e1e2f',
        color: '#bbb',
        textAlign: 'center',
        fontSize: '0.9rem',
        fontFamily: '"Montserrat", sans-serif',
        borderTop: '1px solid #333',
        boxShadow: '0 -2px 6px rgba(0,0,0,0.2)',
      }}
    >
      ⚠️ Disclaimer: AEMET's API may take a long time to respond for large data ranges.
    </footer>
  );
}
