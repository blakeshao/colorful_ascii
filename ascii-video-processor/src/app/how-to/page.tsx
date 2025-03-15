'use client'

import Link from 'next/link'
import { HowTo } from './HowTo'

export default function HowToPage() {
  return (
    <main className="min-h-screen p-20">
      <Link href="/" className="text-md hover:opacity-80 underline">
              colorful_ascii <span className="text-xs">by Blake S.</span>
            </Link>
      <div className="w-full mx-auto my-8">
        <HowTo />
      </div>
    </main>
  )
} 