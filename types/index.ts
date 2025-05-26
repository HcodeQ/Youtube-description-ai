// Types pour l'application

export interface VideoPreview {
  title: string
  thumbnail: string
}

export interface UsefulLink {
  id: string
  title: string
  url: string
}

export interface TranscriptionSettings {
  includeTimestamps: boolean
  language: string
}

// Type pour les données envoyées à l'API
export interface FormData {
  video_type: string
  video_url: string
  description_tone: string
  optional_keywords: string
  transcript_format?: string
  transcript?: string
  languages?: string[]
  translation?: string
  hashtags: string
  timestamps_mode: string
  manual_timestamps: string
  useful_links: Record<string, string>[]
}

// Données de test pour simuler une réponse
export const TEST_DATA: FormData = {
  video_type: "Tutoriel",
  video_url: "https://www.youtube.com/watch?v=LgGmaX-l5K8",
  description_tone: "based on the transcript tone",
  optional_keywords: "SEO, IA, LangChain",
  transcript_format: "CHUNKS",
  transcript: "",
  languages: ["fr", "en"],
  translation: "fr",
  hashtags: "#SEO #LangChain",
  timestamps_mode: "automatique",
  manual_timestamps: "",
  useful_links: [{ Github: "https://github.com/" }, { "LangChain Docs": "https://python.langchain.com" }],
}
