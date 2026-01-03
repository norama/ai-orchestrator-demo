interface Props extends React.PropsWithChildren {
  open: boolean
  onClose: () => void
  className?: string
}

export function Drawer({ open, onClose, className = '', children }: Props) {
  return (
    <>
      {/* Overlay */}
      <div
        className={[
          'fixed inset-0 z-40 bg-black/30 transition-opacity',
          open ? 'opacity-100' : 'pointer-events-none opacity-0',
          className,
        ].join(' ')}
        onClick={onClose}
      />

      {/* Drawer */}
      <div
        className={[
          'fixed inset-y-0 left-0 z-50 w-64 bg-white border-r',
          'flex flex-col transform transition-transform',
          open ? 'translate-x-0' : '-translate-x-full',
          className,
        ].join(' ')}>
        {children}
      </div>
    </>
  )
}
