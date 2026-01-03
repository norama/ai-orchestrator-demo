export function BottomFixedLayout({ children }: React.PropsWithChildren) {
  return (
    <div className='sticky bottom-0 border-t border-gray-300 bg-white px-6 py-4 shadow-sm'>
      {children}
    </div>
  )
}
