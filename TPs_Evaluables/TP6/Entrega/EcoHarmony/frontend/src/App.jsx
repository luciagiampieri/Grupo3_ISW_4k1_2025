
import { useState } from 'react'
import './App.css'
import SimpleForm from './components/SimpleForm.jsx'
import PurchaseDetail from './components/PurchaseDetail.jsx'
import NavBar from './components/NavBar.jsx'

function App() {
  const [currentView, setCurrentView] = useState('form'); // 'form' | 'detail'
  const [purchaseData, setPurchaseData] = useState(null);

  const handleShowDetail = (data) => {
    setPurchaseData(data);
    setCurrentView('detail');
  };

  const handleBackToForm = () => {
    setCurrentView('form');
    setPurchaseData(null);
  };

  return (
    <>
      <NavBar />
      {currentView === 'form' && (
        <SimpleForm onShowDetail={handleShowDetail} />
      )}
      {currentView === 'detail' && purchaseData && (
        <PurchaseDetail 
          purchaseData={purchaseData} 
          onBack={handleBackToForm} 
        />
      )}
    </>
  )
}

export default App
