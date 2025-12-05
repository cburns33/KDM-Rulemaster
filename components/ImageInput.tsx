import React, { useRef } from 'react';
import { Camera, X, Image as ImageIcon } from 'lucide-react';

interface ImageInputProps {
  currentImage: string | null;
  onImageSelect: (base64: string | null) => void;
}

export const ImageInput: React.FC<ImageInputProps> = ({ currentImage, onImageSelect }) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        onImageSelect(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const clearImage = () => {
    onImageSelect(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="flex items-center gap-2">
      <input
        type="file"
        ref={fileInputRef}
        accept="image/*"
        onChange={handleFileChange}
        className="hidden"
      />
      
      {currentImage ? (
        <div className="relative group">
          <div className="w-12 h-12 rounded border border-yellow-900/50 overflow-hidden bg-black">
            <img src={currentImage} alt="Preview" className="w-full h-full object-cover opacity-70" />
          </div>
          <button 
            onClick={clearImage}
            className="absolute -top-2 -right-2 bg-red-900 text-white rounded-full p-0.5 shadow-md hover:bg-red-700 transition-colors"
          >
            <X size={12} />
          </button>
        </div>
      ) : (
        <button
          onClick={() => fileInputRef.current?.click()}
          className="p-3 text-slate-400 hover:text-yellow-500 hover:bg-yellow-900/10 rounded-full transition-all duration-300 border border-transparent hover:border-yellow-900/30"
          title="Upload Rulebook Page"
        >
          <Camera size={24} />
        </button>
      )}
    </div>
  );
};
