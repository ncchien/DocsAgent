import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 60000, // 60 seconds timeout
});

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export const uploadDocument = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const sendChatMessage = async (message: string, history: ChatMessage[]) => {
  const response = await api.post('/chat', {
    message,
    history: history.map(h => ({ role: h.role, content: h.content })),
  });
  return response.data;
};
