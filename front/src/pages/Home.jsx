import { useState } from 'react';
import Header from '../components/Header';
import InfoSection from '../components/InfoSection';
import SearchBar from '../components/SearchBar';
import DataGrid from '../components/DataGrid';
import Footer from '../components/Footer';

export default function Home() {
  const [searchParams, setSearchParams] = useState({
    startDate: '',
    endDate: '',
    station: 'Juan Carlos I',
    features: [],
    aggregation: 'Default',
  });

  const historicalData = [
    { station: 'Juan Carlos I', fecha: '2025-08-10', temperatura: 20, presion: 1015, viento: 5 },
    { station: 'Juan Carlos I', fecha: '2025-08-11', temperatura: 22, presion: 1012, viento: 4 },
    { station: 'Gabriel de Castilla', fecha: '2025-08-10', temperatura: 18, presion: 1018, viento: 6 },
  ];

  const filteredData = historicalData.filter(row => {
    const afterStart = searchParams.startDate ? row.fecha >= searchParams.startDate : true;
    const beforeEnd = searchParams.endDate ? row.fecha <= searchParams.endDate : true;
    const correctStation = row.station === searchParams.station;
    return afterStart && beforeEnd && correctStation;
  });

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
        <SearchBar setSearchParams={setSearchParams} />
        <DataGrid data={filteredData} features={searchParams.features} />
        <Footer />
        </div>
    );
}
