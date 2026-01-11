type DrawerPlacement = 'left' | 'right' | 'top' | 'bottom'

interface Props extends React.PropsWithChildren {
  open: boolean
  onClose: () => void
  placement?: DrawerPlacement
  className?: string
}

export function Drawer({ open, onClose, placement = 'left', className = '', children }: Props) {
  const baseDrawer =
    'fixed z-50 bg-white flex flex-col transition-transform duration-300 ease-in-out'

  const placementClasses: Record<DrawerPlacement, string> = {
    left: `
      inset-y-0 left-0 max-w-64
      ${open ? 'translate-x-0' : '-translate-x-full'}
    `,
    right: `
      inset-y-0 right-0 max-w-80
      ${open ? 'translate-x-0' : 'translate-x-full'}
    `,
    top: `
      inset-x-0 top-0 max-h-[80vh]
      ${open ? 'translate-y-0' : '-translate-y-full'}
    `,
    bottom: `
      inset-x-0 bottom-0 max-h-[80vh]
      ${open ? 'translate-y-0' : 'translate-y-full'}
    `,
  }

  return (
    <>
      {/* Overlay */}
      <div
        className={[
          'fixed inset-0 z-40 bg-black/30 transition-opacity',
          open ? 'opacity-100' : 'pointer-events-none opacity-0',
        ].join(' ')}
        onClick={onClose}
      />

      {/* Drawer */}
      <div className={[baseDrawer, placementClasses[placement], className].join(' ')}>
        {children}
      </div>
    </>
  )
}
