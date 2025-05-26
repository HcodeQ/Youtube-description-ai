import { type FormData, TEST_DATA } from "@/types"

// Fonction pour simuler l'envoi des données de description
export async function submitFormData(data: FormData): Promise<FormData> {
  // Simuler un délai réseau
  await new Promise((resolve) => setTimeout(resolve, 1000))

  // Simuler une réponse avec les données de test
  return {
    ...TEST_DATA,
    // Remplacer certaines valeurs avec celles du formulaire
    video_url: data.video_url,
    optional_keywords: data.optional_keywords || TEST_DATA.optional_keywords,
    hashtags: data.hashtags || TEST_DATA.hashtags,
    timestamps_mode: data.timestamps_mode,
    manual_timestamps: data.manual_timestamps,
    useful_links: data.useful_links.length > 0 ? data.useful_links : TEST_DATA.useful_links,
  }
}

// Fonction pour simuler l'envoi des données de transcription
export async function submitTranscriptionData(data: FormData): Promise<FormData> {
  // Simuler un délai réseau
  await new Promise((resolve) => setTimeout(resolve, 1500))

  // Simuler une réponse avec les données de test
  return {
    ...TEST_DATA,
    video_url: data.video_url,
    transcript:
      "Voici une transcription simulée de la vidéo. Ce texte représente le contenu qui serait extrait de la vidéo YouTube par notre système de transcription automatique. La transcription réelle contiendrait le texte complet de la vidéo avec des horodatages si cette option est activée.",
    languages: data.languages || TEST_DATA.languages,
    timestamps_mode: data.timestamps_mode,
  }
}
