import React, { useState } from 'react';
import { 
  SignedIn, 
  SignedOut, 
  SignInButton, 
  UserButton, 
  useAuth, 
  useUser 
} from '@clerk/clerk-react';
import axios from 'axios';
import { Loader2, Send, FileText, Copy, Check } from 'lucide-react';

const API_URL = "http://localhost:8000";

function HustleForm() {
  const [rawExperience, setRawExperience] = useState('');
  const [cvResult, setCvResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const { getToken } = useAuth();
  const { user } = useUser();

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const token = await getToken();
      const response = await axios.post(`${API_URL}/generate`, {
        full_name: user?.fullName || "Hustle User", 
        email: user?.primaryEmailAddress?.emailAddress || "",
        raw_experience: rawExperience
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setCvResult(response.data.cv);
    } catch (error) {
      console.error("Generation failed", error);
      alert("Something went wrong. Ensure your backend is running.");
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
      <h2 className="text-2xl font-bold mb-4 text-gray-800">
        Hi {user?.firstName || "there"}, turn your Hustle into a CV
      </h2>
      <textarea 
        className="w-full h-40 p-4 border rounded-lg mb-4 text-black focus:ring-2 focus:ring-blue-500 outline-none shadow-sm"
        placeholder="Example: I've been a taxi driver for 5 years. I manage my own routes, handle all cash, and maintain the vehicle..."
        value={rawExperience}
        onChange={(e) => setRawExperience(e.target.value)}
      />
      <button 
        onClick={handleGenerate}
        disabled={loading || !rawExperience}
        className="flex items-center justify-center w-full bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition-all font-semibold"
      >
        {loading ? (
          <>
            <Loader2 className="animate-spin mr-2" />
            Polishing your CV...
          </>
        ) : (
          <>
            <Send className="mr-2" size={18} />
            Generate Professional CV
          </>
        )}
      </button>

      {cvResult && (
        <div className="mt-8 p-6 bg-blue-50 border border-blue-100 rounded-lg shadow-md relative group">
          <div className="flex justify-between items-center mb-4">
            <div className="flex items-center text-blue-700">
              <FileText className="mr-2" />
              <h3 className="font-bold text-lg">Your Professional Experience:</h3>
            </div>
            <button 
              onClick={copyToClipboard}
              className="p-2 hover:bg-blue-100 rounded-md transition-colors text-blue-600"
              title="Copy to clipboard"
            >
              {copied ? <Check size={20} className="text-green-600" /> : <Copy size={20} />}
            </button>
          </div>
          <div className="prose prose-sm max-w-none text-gray-800 bg-white p-4 rounded border border-blue-50 shadow-inner">
            <pre className="whitespace-pre-wrap font-sans leading-relaxed">
              {cvResult}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}

function App() {
  return (
    <div className="min-h-screen bg-gray-50 font-sans">
      <header className="p-4 border-b flex justify-between items-center bg-white sticky top-0 z-10 shadow-sm">
        <h1 className="text-xl font-black text-blue-600 tracking-tight">HUSTLE 2 CV</h1>
        <div className="flex items-center gap-4">
          <SignedOut>
            <SignInButton mode="modal">
              <button className="text-sm font-semibold text-gray-700 hover:text-blue-600 px-4 py-2 rounded-lg border hover:border-blue-600 transition-all">
                Sign In
              </button>
            </SignInButton>
          </SignedOut>
          <SignedIn>
            <UserButton afterSignOutUrl="/" />
          </SignedIn>
        </div>
      </header>
      
      <main className="py-10">
        <SignedOut>
          <div className="text-center py-20 px-4">
            <h2 className="text-4xl font-extrabold mb-4 text-gray-900">Your skills deserve a professional look.</h2>
            <p className="text-lg text-gray-600 mb-8 max-w-lg mx-auto">
              We help taxi drivers, cleaners, and informal workers create world-class CVs from their daily hustle.
            </p>
            <SignInButton mode="modal">
              <button className="bg-blue-600 text-white px-10 py-4 rounded-full font-bold shadow-xl hover:bg-blue-700 transition-all hover:scale-105">
                Get Started Now
              </button>
            </SignInButton>
          </div>
        </SignedOut>
        <SignedIn>
          <HustleForm />
        </SignedIn>
      </main>
    </div>
  );
}

export default App;