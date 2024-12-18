import './Repository.css';
import Filters from './Filters';
import { getResources } from '../config/firebase-functions';
import { useState, useEffect } from 'react';
import Navbar from '../Components/Navbar';
import Footer from '../Components/Footer';

function Repository() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch data from Firestore database and set to statea
  useEffect(() => {
    setLoading(true);
    const fetchData = async () => {
      try {
        const dataFromFirestore = await getResources();
        setData(dataFromFirestore || []);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data from Firestore:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div id="body">
      <Navbar />
      <div id='inner-root'>
        <h1 className="text-36ae9a" style={{ fontSize: '3.5em', lineHeight: '1.1', textAlign: 'center', fontWeight: '400', marginTop: '50px' }}>
          The Speech Resource Repository
        </h1>
        <Filters data={data} loading={loading} />
        <Footer />
      </div>
    </div>
  );
}

export default Repository;
