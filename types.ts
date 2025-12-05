export enum Role {
  USER = 'user',
  MODEL = 'model',
}

export interface Message {
  id: string;
  role: Role;
  text: string;
  image?: string; // Base64 string
  timestamp: number;
}

export interface ImageFile {
  data: string; // Base64
  mimeType: string;
}
