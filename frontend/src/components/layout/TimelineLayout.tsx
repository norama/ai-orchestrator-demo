import { useEffect, useRef } from 'react'

export function TimelineLayout({ children }: React.PropsWithChildren) {
  const bottomRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [children])

  return (
    <div
      className='flex-1 overflow-y-auto px-6'
      style={{ paddingBottom: '16rem' }} // space for solution + input
    >
      <div className='flex flex-col gap-4'>{children}</div>
      <div ref={bottomRef} /> {/* Added ref for scrolling */}
    </div>
  )
}
