// Next.js & React Component
import React, { useState } from 'react';
import { Sparkles, Image as ImageIcon, FileText, Mic, Home, DollarSign, Key } from 'lucide-react';

export default function Dashboard() {
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState<'rent' | 'sale'>('rent'); // Kiralık/Satılık Modu
  const [inputText, setInputText] = useState('');
  const [result, setResult] = useState<any>(null);

  // API'ye İstek Atma
  const handleGenerate = async () => {
    setLoading(true);
    
    // Simüle edilen Backend isteği
    // Gerçekte: await fetch('http://localhost:8000/generate', ...)
    setTimeout(() => {
      setResult({
        text: "✨ Wohnen im Herzen von Stuttgart! \n\nBu harika daire yeni sahiplerini bekliyor...",
        image: "https://images.unsplash.com/photo-1502005229762-cf1afd386884?auto=format&fit=crop&w=800&q=80"
      });
      setLoading(false);
    }, 3000);
  };

  return (
    <div className="min-h-screen bg-[#F8FAFC] flex font-sans text-slate-900">
      
      {/* --- SOL TARAFTA GİRİŞ ALANI --- */}
      <div className="flex-1 p-8 max-w-2xl mx-auto">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-[#0F172A]">Immo-Agent Pro</h1>
          <p className="text-slate-500">Exposé'yi yükle, viral ol.</p>
        </header>

        {/* Kart */}
        <div className="bg-white p-6 rounded-3xl shadow-sm border border-slate-200">
          
          {/* MOD SEÇİMİ (TOGGLE) */}
          <div className="flex bg-slate-100 p-1 rounded-xl mb-6">
            <button 
              onClick={() => setMode('rent')}
              className={`flex-1 py-2 rounded-lg font-medium flex items-center justify-center gap-2 transition ${mode === 'rent' ? 'bg-white shadow text-indigo-600' : 'text-slate-500'}`}
            >
              <Key size={18} /> Kiralama (Mieten)
            </button>
            <button 
              onClick={() => setMode('sale')}
              className={`flex-1 py-2 rounded-lg font-medium flex items-center justify-center gap-2 transition ${mode === 'sale' ? 'bg-white shadow text-emerald-600' : 'text-slate-500'}`}
            >
              <DollarSign size={18} /> Satış (Kauf)
            </button>
          </div>

          {/* GİRİŞ TİPLERİ */}
          <div className="grid grid-cols-3 gap-4 mb-4">
            <div className="border border-slate-200 p-4 rounded-xl text-center hover:bg-slate-50 cursor-pointer">
               <FileText className="mx-auto mb-2 text-slate-400"/>
               <span className="text-xs font-bold text-slate-600">PDF Exposé</span>
            </div>
            <div className="border border-slate-200 p-4 rounded-xl text-center hover:bg-slate-50 cursor-pointer">
               <ImageIcon className="mx-auto mb-2 text-slate-400"/>
               <span className="text-xs font-bold text-slate-600">Fotoğraf</span>
            </div>
            <div className="border border-slate-200 p-4 rounded-xl text-center hover:bg-slate-50 cursor-pointer">
               <Mic className="mx-auto mb-2 text-slate-400"/>
               <span className="text-xs font-bold text-slate-600">Ses Kaydı</span>
            </div>
          </div>

          <textarea 
            className="w-full bg-slate-50 border border-slate-200 rounded-xl p-4 text-sm min-h-[150px] focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder={mode === 'rent' ? "Örn: Stuttgart-West, 3 oda, 1200€, öğrenciye uygun değil..." : "Örn: Berlin-Mitte, Yatırımlık bina, ROI %4, tadilatlı..."}
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
          ></textarea>

          {/* SİHİRLİ BUTON */}
          <button 
            onClick={handleGenerate}
            disabled={loading}
            className="mt-6 w-full relative overflow-hidden rounded-xl p-4 font-bold text-white transition hover:scale-[1.01]"
            style={{background: 'linear-gradient(135deg, #6366f1 0%, #a855f7 100%)'}}
          >
            {loading ? "Ajan Çalışıyor..." : "✨ İçerik Oluştur"}
          </button>
        </div>
      </div>

      {/* --- SAĞ TARAFTA IPHONE ÖN İZLEME --- */}
      <div className="hidden lg:flex w-1/3 bg-slate-100 items-center justify-center border-l border-slate-200">
        <div className="w-[300px] bg-black rounded-[40px] p-3 shadow-2xl border-4 border-slate-800">
          <div className="bg-white w-full h-[600px] rounded-[30px] overflow-hidden flex flex-col relative">
            
            {/* Instagram Üst Bar */}
            <div className="h-14 border-b flex items-center justify-center font-bold text-sm">
               Immo_Agent_Pro
            </div>

            {/* İçerik */}
            <div className="flex-1 overflow-y-auto">
              {result ? (
                <>
                  {/* Görsel */}
                  <img src={result.image} className="w-full h-[300px] object-cover" />
                  
                  {/* Etkileşim İkonları */}
                  <div className="flex gap-4 p-3 text-2xl">
                    <span>❤️</span> <span>💬</span> <span>✈️</span>
                  </div>

                  {/* Metin */}
                  <div className="px-3 pb-10 text-sm text-slate-800 whitespace-pre-line">
                    <span className="font-bold mr-2">Immo_Agent_Pro</span>
                    {result.text}
                    <br/><br/>
                    <span className="text-blue-500">#Stuttgart #Immobilien #RealEstate</span>
                  </div>
                </>
              ) : (
                <div className="h-full flex flex-col items-center justify-center text-slate-400 p-10 text-center">
                  <Sparkles size={40} className="mb-4 text-slate-200"/>
                  <p>Ön izleme burada görünecek.</p>
                </div>
              )}
            </div>

          </div>
        </div>
      </div>

    </div>
  );
}