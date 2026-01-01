export function BottomFixedLayout({ children }: React.PropsWithChildren) {
  return <div className='sticky bottom-0 border-t bg-white px-6 py-4 shadow-sm'>{children}</div>
}
