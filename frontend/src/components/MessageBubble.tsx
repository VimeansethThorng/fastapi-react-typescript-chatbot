import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark, oneLight } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Message } from '../types';

// Import KaTeX CSS
import 'katex/dist/katex.min.css';

interface MessageBubbleProps {
  message: Message;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`message-bubble ${isUser ? 'user' : 'assistant'}`}>
      {!isUser && (
        <div className="message-avatar assistant-avatar">
          🤖
        </div>
      )}
      <div className={`message-content ${isUser ? 'user' : 'assistant'}`}>
        <div className="markdown-content">
          <ReactMarkdown 
            remarkPlugins={[remarkGfm, remarkMath]}
            rehypePlugins={[rehypeKatex]}
            skipHtml={false}
            components={{
              code(props: any) {
                const { node, inline, className, children, ...rest } = props;
                const match = /language-(\w+)/.exec(className || '');
                const language = match ? match[1] : '';
                
                return !inline && language ? (
                  <SyntaxHighlighter
                    style={isUser ? oneDark as any : oneLight as any}
                    language={language}
                    PreTag="div"
                    className="code-block"
                    customStyle={{
                      margin: '12px 0',
                      borderRadius: '8px',
                      fontSize: '0.9em',
                    }}
                    {...rest}
                  >
                    {String(children).replace(/\n$/, '')}
                  </SyntaxHighlighter>
                ) : (
                  <code className={`inline-code ${className || ''}`} {...rest}>
                    {children}
                  </code>
                );
              },
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>
      </div>
      {isUser && (
        <div className="message-avatar user-avatar">
          👤
        </div>
      )}
    </div>
  );
};

export default MessageBubble;
