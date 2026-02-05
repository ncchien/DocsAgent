import React, { useState } from 'react';
import { Upload, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import { uploadDocument } from '../lib/api';

export default function AdminUpload() {
    const [file, setFile] = useState<File | null>(null);
    const [status, setStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
    const [message, setMessage] = useState('');

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!file) return;
        setStatus('uploading');
        try {
            const res = await uploadDocument(file);
            setStatus('success');
            setMessage(res.status);
        } catch (e: any) {
            setStatus('error');
            setMessage(e.message || 'Upload failed');
        }
    };

    return (
        <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-md">
            <h2 className="text-2xl font-bold mb-4">Document Upload</h2>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 flex flex-col items-center justify-center cursor-pointer hover:border-blue-500 transition-colors">
                <Upload className="w-12 h-12 text-gray-400 mb-2" />
                <label className="cursor-pointer">
                    <span className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600">Select PDF</span>
                    <input type="file" accept=".pdf" className="hidden" onChange={handleFileChange} />
                </label>
                {file && <p className="mt-2 text-sm text-gray-600">{file.name}</p>}
            </div>

            <button
                onClick={handleUpload}
                disabled={!file || status === 'uploading'}
                className="w-full mt-4 bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400 flex items-center justify-center font-medium"
            >
                {status === 'uploading' && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
                {status === 'uploading' ? 'Uploading...' : 'Upload Document'}
            </button>

            {status === 'success' && (
                <div className="mt-4 p-3 bg-green-50 text-green-700 rounded-md flex items-center">
                    <CheckCircle className="w-5 h-5 mr-2" />
                    {message}
                </div>
            )}

            {status === 'error' && (
                <div className="mt-4 p-3 bg-red-50 text-red-700 rounded-md flex items-center">
                    <AlertCircle className="w-5 h-5 mr-2" />
                    {message}
                </div>
            )}
        </div>
    );
}
