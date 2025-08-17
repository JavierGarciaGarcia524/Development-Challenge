import { useState } from 'react';
import Header from '../components/Header';
import InfoSection from '../components/InfoSection';
import SearchBar from '../components/SearchBar';
import DataGrid from '../components/DataGrid';
import Footer from '../components/Footer';
import { fetchWeather } from '../services/api';

export default function Home() {
  const [searchParams, setSearchParams] = useState({
    startDate: '',
    endDate: '',
    station: 'Juan Carlos I',
    features: [],
    aggregation: 'Default',
  });

  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (params) => {
    setLoading(true);         // show loading
    setError(null);           // reset error
    setSearchParams(params);  // update searchParams to keep inputs in sync

    try {
      const result = await fetchWeather(params);    // call your service
      setData(result);        // save the obtained data
    } catch (err) {
      setError("Error fetching data");
      setData([]);
    } finally {
      setLoading(false);      // stop showing loading
    }
  };

  return (
    <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'stretch',
        gap: '0',
        fontFamily: 'Arial, sans-serif',
        minHeight: '100vh'
        }}>
        <Header />
        <InfoSection />
        <SearchBar setSearchParams={setSearchParams} onSearch={handleSearch} /> {/* Pass params and function to searchbar */}
          {loading && <p style={{ textAlign: 'center' }}>Cargando datos...</p>}
          {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}
        <DataGrid data={data} features={searchParams.features} />
        <Footer />
        </div>
    );
}
