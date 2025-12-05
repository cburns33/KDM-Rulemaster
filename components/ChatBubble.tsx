import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Message, Role } from '../types';
import { User, Skull } from 'lucide-react';

interface ChatBubbleProps {
  message: Message;
}

export const ChatBubble: React.FC<ChatBubbleProps> = ({ message }) => {
  const isUser = message.role === Role.USER;

  return (
    <div className={`flex w-full mb-6 ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`flex max-w-[85%] md:max-w-[75%] ${isUser ? 'flex-row-reverse' : 'flex-row'} gap-3`}>
        
        {/* Avatar */}
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center border ${isUser ? 'bg-slate-800 border-slate-600' : 'bg-yellow-900/20 border-yellow-700'}`}>
          {isUser ? <User size={16} className="text-slate-300" /> : <Skull size={16} className="text-yellow-600" />}
        </div>

        {/* Message Content */}
        <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
          <div 
            className={`
              px-4 py-3 rounded-lg shadow-lg text-sm leading-relaxed
              ${isUser 
                ? 'bg-slate-800 text-slate-200 border border-slate-700 rounded-tr-none' 
                : 'bg-[#121212] text-slate-300 border border-yellow-900/30 rounded-tl-none'}
            `}
          >
            {message.image && (
              <div className="mb-3 rounded-md overflow-hidden border border-slate-700">
                <img src={message.image} alt="User upload" className="max-w-full h-auto max-h-64 object-contain" />
              </div>
            )}
            <div className="markdown-content">
              <ReactMarkdown 
                components={{
                  strong: ({node, ...props}) => <span className="font-bold text-yellow-600/90" {...props} />,
                  em: ({node, ...props}) => <span className="italic text-slate-400" {...props} />,
                  h1: ({node, ...props}) => <h1 className="text-lg font-cinzel text-yellow-500 mt-2 mb-1" {...props} />,
                  h2: ({node, ...props}) => <h2 className="text-base font-cinzel text-yellow-600/80 mt-2 mb-1" {...props} />,
                  ul: ({node, ...props}) => <ul className="list-disc list-inside my-2 pl-2" {...props} />,
                  li: ({node, ...props}) => <li className="my-1" {...props} />,
                  blockquote: ({node, ...props}) => <blockquote className="border-l-2 border-yellow-800 pl-3 py-1 my-2 italic text-slate-500 bg-black/20" {...props} />,
                }}
              >
                {message.text}
              </ReactMarkdown>
            </div>
          </div>
          <span className="text-[10px] text-slate-600 mt-1 font-mono uppercase tracking-wider">
            {isUser ? 'Survivor' : 'The Hand'}
          </span>
        </div>
      </div>
    </div>
  );
};
