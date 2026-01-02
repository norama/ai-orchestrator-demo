import ReactMarkdown from 'react-markdown'

interface Props {
  content: string
}

export function MarkdownView({ content }: Props) {
  return (
    <div className='prose prose-sm max-w-none not-prose'>
      <ReactMarkdown
        components={{
          h1: (props) => <h1 className='text-lg font-semibold mt-0 mb-0' {...props} />,
          h2: (props) => <h2 className='text-base font-semibold mt-0 mb-0' {...props} />,
          p: (props) => <p className='text-sm leading-snug my-0' {...props} />,
          ul: (props) => <ul className='list-disc pl-5 my-0' {...props} />,
          li: (props) => <li className='leading-snug my-0' {...props} />,
        }}>
        {content}
      </ReactMarkdown>
    </div>
  )
}
