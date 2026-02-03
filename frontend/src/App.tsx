import React, { useState } from 'react';
import { SignedIn, SignedOut, SignInButton, UserButton, useAuth, useUser } from '@clerk/clerk-react';
import axios from 'axios';
import { Loader2, Send, FileText, Copy, Check } from 'lucide-react';

const API_URL = "http://127.0.0.1:8080";

function HustleForm() {
  const [rawExperience, setRawExperience] = useState('');
  const [cvResult, setCvResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const { getToken } = useAuth();
  const { user } = useUser();

  const handleGenerate = async () => {
    if (!rawExperience.trim()) return;
    setLoading(true);
    
    try {
      const token = await getToken();
      
      const response = await axios.post(`${API_URL}/generate`, {
        full_name: user?.fullName || "Hustle User", 
        email: user?.primaryEmailAddress?.emailAddress || "guest@hustle.com",
        raw_experience: rawExperience
      }, {
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        timeout: 15000
      });

      setCvResult(response.data.cv);
    } catch (error: any) {
      console.error("Integration Error:", error.response?.data || error.message);
      alert(`Backend Error: ${error.response?.data?.detail || "Could not connect to server"}`);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(cvResult);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Hi {user?.firstName}, build your CV</h2>
      <textarea 
        className="w-full h-40 p-4 border rounded-lg mb-4 text-black focus:ring-2 focus:ring-blue-500 outline-none"
        value={rawExperience}
        onChange={(e) => setRawExperience(e.target.value)}
        placeholder="Describe your hustle here..."
      />
      <button 
        onClick={handleGenerate}
        disabled={loading}
        className="w-full bg-blue-600 text-white p-3 rounded-lg font-bold flex justify-center items-center"
      >
        {loading ? <Loader2 className="animate-spin" /> : "Generate Professional CV"}
      </button>

      {cvResult && (
        <div className="mt-8 p-6 bg-white border rounded-lg shadow-sm">
           <div className="flex justify-between mb-2">
             <span className="font-bold text-blue-600">AI Result:</span>
             <button onClick={copyToClipboard}>{copied ? <Check size={16}/> : <Copy size={16}/>}</button>
           </div>
           <pre className="whitespace-pre-wrap text-sm">{cvResult}</pre>
        </div>
      )}
    </div>
  );
}

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="p-4 bg-white border-b flex justify-between">
        <h1 className="font-black text-blue-600">HUSTLE 2 CV</h1>
        <SignedIn><UserButton /></SignedIn>
        <SignedOut><SignInButton mode="modal" /></SignedOut>
      </header>
      <main className="py-10"><SignedIn><HustleForm /></SignedIn></main>
    </div>
  );
}