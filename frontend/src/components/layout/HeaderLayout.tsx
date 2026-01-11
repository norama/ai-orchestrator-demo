export function HeaderLayout({ children }: React.PropsWithChildren) {
  return (
    <div className='px-3 py-2 text-sm font-medium border-b border-gray-300 text-gray-700 h-12 flex items-center'>
      {children}
    </div>
  )
}
