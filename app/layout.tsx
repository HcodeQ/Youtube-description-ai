import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Youtube Description AI',
  description: 'Youtube Description AI',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
