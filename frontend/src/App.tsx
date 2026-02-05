import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ChatInterface from './components/ChatInterface';
import AdminUpload from './components/AdminUpload';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100 font-sans text-gray-900">
        <header className="bg-white shadow-sm sticky top-0 z-10">
          <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
            <h1 className="text-xl font-bold text-blue-600 flex items-center gap-2">
              ProductDocs Agent
            </h1>
            <nav className="flex gap-6">
              <Link to="/" className="text-gray-600 hover:text-blue-600 font-medium">Chat</Link>
              <Link to="/admin" className="text-gray-600 hover:text-blue-600 font-medium">Upload Docs</Link>
            </nav>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={
              <div className="max-w-3xl mx-auto">
                <div className="mb-6 text-center">
                  <h2 className="text-3xl font-bold mb-2">How can I help you today?</h2>
                  <p className="text-gray-600">Ask questions about our product documentation.</p>
                </div>
                <ChatInterface />
              </div>
            } />
            <Route path="/admin" element={<AdminUpload />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
