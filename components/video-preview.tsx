import type { VideoPreview as VideoPreviewType } from "@/types"

interface VideoPreviewProps {
  preview: VideoPreviewType | null
}

export function VideoPreview({ preview }: VideoPreviewProps) {
  if (!preview) return null

  return (
    <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-md mt-2 animate-fadeIn">
      <img
        src={preview.thumbnail || "/placeholder.svg"}
        alt="Video thumbnail"
        className="w-20 h-12 object-cover rounded"
      />
      <div className="text-sm">
        <p className="font-medium line-clamp-1">{preview.title}</p>
        <p className="text-xs text-gray-500">Vidéo détectée</p>
      </div>
    </div>
  )
}
