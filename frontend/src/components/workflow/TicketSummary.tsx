import type { UITicket } from '@/types/fe'

interface Props {
  ticket: UITicket
}

export function TicketSummary({ ticket }: Props) {
  return (
    <div className='rounded-md bg-yellow-50 border border-yellow-200 px-4 py-3'>
      <div className='text-sm font-bold text-yellow-900'>Ticket</div>

      <div className='mt-1 text-sm text-yellow-800'>
        <span className='font-medium'>{ticket.title}</span>
      </div>

      <div className='mt-1 text-sm text-yellow-700'>{ticket.description}</div>
    </div>
  )
}
