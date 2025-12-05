import React, { useState, useRef, useEffect } from 'react';
import { GoogleGenAI } from "@google/genai";
import { Send, ScrollText, Flame, Sparkles } from 'lucide-react';
import { ChatBubble } from './components/ChatBubble';
import { ImageInput } from './components/ImageInput';
import { Message, Role } from './types';
import { SYSTEM_INSTRUCTION, LOADING_MESSAGES } from './constants';

const SUGGESTED_QUERIES = [
  "How does Collision work?",
  "Explain the Severe Injury table",
  "What are the Butcher's stats?",
  "How do I setup the Hunt Board?",
  "Explain the Intimacy story event",
];

const App: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      role: Role.MODEL,
      text: "**I am the Hand of the Watcher.** \n\nAsk me of the rules, the monsters, or the settlement. I know the darkness well.\n\nI cannot see page numbers without eyes, but speak the *name* of the rule or monster you seek, and I shall answer.",
      timestamp: Date.now(),
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingText, setLoadingText] = useState(LOADING_MESSAGES[0]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Cycle loading messages
  useEffect(() => {
    let interval: any;
    if (isLoading) {
      interval = setInterval(() => {
        setLoadingText(prev => {
          const currentIndex = LOADING_MESSAGES.indexOf(prev);
          const nextIndex = (currentIndex + 1) % LOADING_MESSAGES.length;
          return LOADING_MESSAGES[nextIndex];
        });
      }, 3000);
    }
    return () => clearInterval(interval);
  }, [isLoading]);

  const handleSendMessage = async (textOverride?: string) => {
    const textToSend = textOverride || inputText;
    if ((!textToSend.trim() && !selectedImage) || isLoading) return;

    const newMessage: Message = {
      id: Date.now().toString(),
      role: Role.USER,
      text: textToSend,
      image: selectedImage || undefined,
      timestamp: Date.now(),
    };

    // Update UI immediately
    const updatedMessages = [...messages, newMessage];
    setMessages(updatedMessages);
    setInputText('');
    setSelectedImage(null);
    setIsLoading(true);

    try {
      const apiKey = process.env.API_KEY;
      if (!apiKey) {
        throw new Error("API Key not found. Please ensure process.env.API_KEY is set.");
      }

      const ai = new GoogleGenAI({ apiKey });
      
      // Construct History
      // We map previous messages to the format expected by the API.
      // Optimization: We exclude base64 images from *history* to save bandwidth/tokens, 
      // relying on the text transcript of the previous interaction.
      const historyContents = updatedMessages.slice(0, -1).map(msg => ({
        role: msg.role === Role.USER ? 'user' : 'model',
        parts: [{ text: msg.text }] 
      }));

      // Construct Current Message Content
      const currentParts: any[] = [];
      
      // If there is an image in the CURRENT message, process it
      if (newMessage.image) {
        const base64Data = newMessage.image.split(',')[1];
        currentParts.push({
          inlineData: {
            mimeType: 'image/jpeg', // Assuming jpeg/png/webp
            data: base64Data
          }
        });
      }

      // Add text prompt
      if (newMessage.text) {
        currentParts.push({ text: newMessage.text });
      } else {
        currentParts.push({ text: "Explain this page to me. Identify any specific rules, tables, or events." });
      }

      const contents = [
        ...historyContents,
        {
          role: 'user',
          parts: currentParts
        }
      ];

      const response = await ai.models.generateContent({
        model: 'gemini-2.5-flash',
        contents: contents,
        config: {
          systemInstruction: SYSTEM_INSTRUCTION,
          temperature: 0.4, 
        }
      });

      const responseText = response.text;

      if (responseText) {
        setMessages(prev => [...prev, {
          id: (Date.now() + 1).toString(),
          role: Role.MODEL,
          text: responseText,
          timestamp: Date.now(),
        }]);
      } else {
        throw new Error("The lantern flickered... no response received.");
      }

    } catch (error) {
      console.error("Error communicating with the Watcher:", error);
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        role: Role.MODEL,
        text: "*A cold wind blows through the settlement... I cannot discern the answer at this moment.* (API Error)",
        timestamp: Date.now(),
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-lg mx-auto bg-[#0a0a0a] shadow-2xl border-x border-[#1a1a1a]">
      {/* Header */}
      <header className="flex items-center justify-center p-4 border-b border-yellow-900/30 bg-[#0f0f0f] relative overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-yellow-700 to-transparent opacity-50"></div>
        <Flame className="text-yellow-600 mr-3 animate-pulse" size={20} />
        <h1 className="text-xl font-cinzel text-transparent bg-clip-text bg-gradient-to-b from-yellow-100 to-yellow-600 tracking-widest font-bold">
          Hand of the Watcher
        </h1>
        <div className="absolute -bottom-4 right-10 text-[100px] text-yellow-900/5 font-cinzel pointer-events-none select-none">
          KDM
        </div>
      </header>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-[url('https://www.transparenttextures.com/patterns/dark-matter.png')]">
        {messages.map((msg) => (
          <ChatBubble key={msg.id} message={msg} />
        ))}
        
        {/* Suggested Queries (Only show if few messages or user hasn't typed) */}
        {messages.length < 3 && !isLoading && (
          <div className="flex flex-wrap gap-2 mt-4 px-2">
            {SUGGESTED_QUERIES.map((query, idx) => (
              <button
                key={idx}
                onClick={() => handleSendMessage(query)}
                className="text-xs bg-slate-800/50 hover:bg-yellow-900/30 text-slate-400 hover:text-yellow-500 border border-slate-700 hover:border-yellow-700 px-3 py-1.5 rounded-full transition-all duration-300 flex items-center gap-1.5"
              >
                <Sparkles size={10} />
                {query}
              </button>
            ))}
          </div>
        )}

        {/* Loading Indicator */}
        {isLoading && (
          <div className="flex justify-start w-full mb-6 animate-pulse">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full flex items-center justify-center bg-yellow-900/10 border border-yellow-900/50">
                <ScrollText size={16} className="text-yellow-700" />
              </div>
              <span className="text-xs font-cinzel text-yellow-700/80 tracking-widest">{loadingText}</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-[#0f0f0f] border-t border-yellow-900/30">
        <div className="flex items-end gap-2 bg-[#1a1a1a] p-2 rounded-xl border border-[#333] focus-within:border-yellow-700/50 transition-colors shadow-lg">
          
          <ImageInput currentImage={selectedImage} onImageSelect={setSelectedImage} />

          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask of the rules..."
            className="flex-1 bg-transparent text-slate-200 text-sm p-3 max-h-32 focus:outline-none resize-none scrollbar-hide font-lora placeholder:text-slate-600 placeholder:italic"
            rows={1}
            style={{ minHeight: '44px' }}
          />

          <button
            onClick={() => handleSendMessage()}
            disabled={isLoading || (!inputText.trim() && !selectedImage)}
            className={`
              p-3 rounded-xl transition-all duration-300
              ${isLoading || (!inputText.trim() && !selectedImage)
                ? 'bg-[#222] text-slate-600 cursor-not-allowed'
                : 'bg-yellow-800 text-yellow-100 hover:bg-yellow-700 shadow-lg shadow-yellow-900/20'
              }
            `}
          >
            <Send size={20} />
          </button>
        </div>
        <div className="text-center mt-2">
           <p className="text-[10px] text-slate-600 font-cinzel">Beware the Rule of Death</p>
        </div>
      </div>
    </div>
  );
};

export default App;