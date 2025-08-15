# ⚛️ React TypeScript Frontend

This is the frontend application for the FastAPI-React TypeScript Chatbot. Built with React 18, TypeScript, and modern dependencies for rich content rendering and real-time chat functionality.

## ✨ Features

### Core Chat Features
- 🎨 **Modern UI**: Custom CSS with responsive design
- 📝 **Rich Content**: Support for tables, code blocks, and math equations
- ⚡ **Real-time Chat**: Seamless communication with FastAPI backend
- 🔄 **Auto-refresh**: Conversation history updates automatically
- 📱 **Responsive**: Works on desktop and mobile devices

### Authentication Features
- 🔐 **JWT Authentication**: Secure user login and registration
- 👤 **User Management**: Personal conversation storage
- 🔑 **Session Management**: Persistent login with token refresh

## 🚀 Quick Start

### 🐳 Docker Development (Recommended)
```bash
# From the project root, start development mode
git checkout docker
docker-compose --profile dev up -d frontend-dev

# Access the application
open http://localhost:3000
```

### Using the Root Script
```bash
# From the project root (local development)
./start.sh
```

### Manual Local Setup
```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

## 🐳 Docker Configuration

### Development Mode
- **Hot Reload**: Live code updates without rebuilding
- **Port 3000**: Dedicated development server
- **Volume Mounting**: Source code changes reflected instantly

### Production Mode
- **Static Build**: Optimized React build served via FastAPI
- **Port 8000**: Integrated with backend
- **Single Container**: Streamlined deployment

## 📦 Dependencies

### Core Framework
- **React 18** with TypeScript
- **Create React App** for build tooling

### Rich Content Rendering
- **react-markdown**: Markdown parsing and rendering
- **react-syntax-highlighter**: Code syntax highlighting
- **katex**: Mathematical equation rendering
- **remark-gfm**: GitHub Flavored Markdown (tables)
- **remark-math** & **rehype-katex**: Math equation support

### Component Architecture
```
src/
├── components/
│   ├── ChatBot.tsx           # Main chat interface
│   ├── MessageBubble.tsx     # Individual message display
│   ├── MessageInput.tsx      # User input component
│   ├── AllConversations.tsx  # Conversation history
│   ├── TypingIndicator.tsx   # Loading animation
│   ├── LoadingDots.tsx       # Loading dots
│   └── ConfirmDialog.tsx     # Confirmation dialogs
├── api.ts                    # API client functions
├── types.ts                  # TypeScript type definitions
└── App.tsx                   # Main application component
```

## 🛠️ Configuration

The frontend is configured to connect to the FastAPI backend at `http://localhost:8000` with CORS enabled for development.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).
