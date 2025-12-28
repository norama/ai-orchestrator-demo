import type { UITicket } from '@/types/fe'

interface Props {
  ticket: UITicket
}

export function TicketView({ ticket }: Props) {
  return (
    <div className='border border-yellow-200 rounded-md p-4 bg-yellow-50 shadow-sm'>
      <h2 className='text-lg font-semibold mb-2'>Ticket Details</h2>
      <div className='mb-2'>
        <span className='font-medium'>Title:</span> {ticket.title}
      </div>
      <div>
        <span className='font-medium'>Description:</span> {ticket.description}
      </div>
    </div>
  )
}
