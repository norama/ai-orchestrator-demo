import ReactMarkdown from 'react-markdown'

interface Props {
  content: string
}

export function MarkdownView({ content }: Props) {
  return (
    <div className='prose prose-sm max-w-none not-prose'>
      <ReactMarkdown
        components={{
          h1: (props) => <h1 className='text-lg font-semibold my-2' {...props} />,
          h2: (props) => <h2 className='text-base font-semibold my-1' {...props} />,
          p: (props) => <p className='text-sm leading-snug' {...props} />,
          ul: (props) => <ul className='list-disc pl-5' {...props} />,
          li: (props) => <li className='leading-snug' {...props} />,
        }}>
        {content}
      </ReactMarkdown>
    </div>
  )
}
