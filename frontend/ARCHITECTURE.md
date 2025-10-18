# 🎨 AI Content Generator - Visual Architecture

## 📊 Application Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     USER JOURNEY                             │
└─────────────────────────────────────────────────────────────┘

    1. LANDING PAGE          2. AUTHENTICATION         3. DASHBOARD
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│                     │  │                     │  │  [Navbar]           │
│   🎯 Hero Section   │  │  📝 Login Form      │  │  ┌───────┬───────┐  │
│                     │  │     - Username      │  │  │Upload │Preview│  │
│  "Convert ideas     │─>│     - Password      │─>│  │       │       │  │
│   into videos"      │  │                     │  │  │ 📤    │ 🎥    │  │
│                     │  │  📝 Signup Form     │  │  │       │       │  │
│  [Get Started] ──┐  │  │     - Username      │  │  └───────┴───────┘  │
│                  │  │  │     - Email         │  │                     │
│  ✨ Features     │  │  │     - Password      │  │  [Generate Video]   │
│  📊 How It Works │  │  │     - Confirm       │  │                     │
│                     │  │                     │  │  [Download] 💾      │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘
```

## 🏗️ Component Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                          App.tsx                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │               ThemeProvider (Dark/Light)                  │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │         AuthProvider (Login/Logout/Token)          │  │  │
│  │  │  ┌──────────────────────────────────────────────┐  │  │  │
│  │  │  │           React Router                        │  │  │  │
│  │  │  │                                               │  │  │  │
│  │  │  │  Routes:                                      │  │  │  │
│  │  │  │  ├─ / ──────────> LandingPage               │  │  │  │
│  │  │  │  ├─ /auth ──────> AuthPage                   │  │  │  │
│  │  │  │  └─ /dashboard -> Dashboard (Protected)      │  │  │  │
│  │  │  │                                               │  │  │  │
│  │  │  └──────────────────────────────────────────────┘  │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

## 🎭 Page Components

### 📄 LandingPage.tsx
```
┌──────────────────────────────┐
│  [Logo]    AI Content Gen    │  <- Navbar
├──────────────────────────────┤
│                              │
│    🎯 HERO SECTION           │
│                              │
│  "Convert your ideas..."     │
│                              │
│     [Get Started] ─────┐     │
│                        │     │
├────────────┬───────────┼────┤
│            │           │    │
│  ✨ Text   │  🎨 Image │ 🎥 │  <- Features
│   to Video │Integration│Pro │
│            │           │Vid │
└────────────┴───────────┴────┘
```

### 🔐 AuthPage.tsx
```
┌──────────────────────────────┐
│    [Logo] AI Content Gen     │
├──────────────────────────────┤
│  ┌────────────────────────┐  │
│  │ 📝 Login / Sign Up     │  │
│  │                        │  │
│  │  👤 Username           │  │
│  │  ┌──────────────────┐  │  │
│  │  │                  │  │  │
│  │  └──────────────────┘  │  │
│  │                        │  │
│  │  📧 Email (Signup)     │  │
│  │  ┌──────────────────┐  │  │
│  │  │                  │  │  │
│  │  └──────────────────┘  │  │
│  │                        │  │
│  │  🔒 Password           │  │
│  │  ┌──────────────────┐  │  │
│  │  │                  │👁│  │
│  │  └──────────────────┘  │  │
│  │                        │  │
│  │    [Sign In] ──────┐   │  │
│  │                    │   │  │
│  │  Demo: demo/demo1234  │  │
│  └────────────────────────┘  │
│                              │
│      [← Back to Home]        │
└──────────────────────────────┘
```

### 📊 Dashboard.tsx
```
┌──────────────────────────────────────────────────────────┐
│ [Logo]  AI Content Generator     🌙 ⚙️ [👤▼]          │  <- Navbar
├──────────────────────────────────────────────────────────┤
│  Welcome back, User!                                     │
│  Upload your content and let AI create amazing videos   │
├───────────────────────┬──────────────────────────────────┤
│                       │                                  │
│  📤 Upload Section    │    🎥 Video Preview             │
│                       │                                  │
│  ┌─────────────────┐  │  ┌────────────────────────────┐ │
│  │                 │  │  │                            │ │
│  │  Drag & Drop    │  │  │      Video Player          │ │
│  │    or Browse    │  │  │                            │ │
│  │                 │  │  │   [Play/Pause/Volume]      │ │
│  │   📄 📷 🎨      │  │  │                            │ │
│  │                 │  │  └────────────────────────────┘ │
│  └─────────────────┘  │                                  │
│                       │  [Download Video] 💾            │
│  Selected:            │                                  │
│  ├─ 📄 file.txt       │  Video ID: abc123               │
│  └─ 2.5 MB            │  Status: ✅ Ready               │
│                       │                                  │
│  [Upload & Generate]  │                                  │
│                       │                                  │
└───────────────────────┴──────────────────────────────────┘
```

## 🧩 Component Breakdown

### Navbar Component
```
┌──────────────────────────────────────────────────────┐
│ [🌟Logo]  AI Content Generator                       │
│                                   🌙  ⚙️  [👤▼]      │
└──────────────────────────────────────────────────────┘
                                           │
                            ┌──────────────┴──────────────┐
                            │ Profile Dropdown            │
                            ├─────────────────────────────┤
                            │ 👤 username                 │
                            │ 📧 user@email.com           │
                            ├─────────────────────────────┤
                            │ 👤 Profile                  │
                            │ ⚙️  Settings                │
                            ├─────────────────────────────┤
                            │ 🚪 Log out                  │
                            └─────────────────────────────┘
```

### UploadSection Component States
```
STATE 1: Empty
┌─────────────────────┐
│    📤               │
│                     │
│  Drag & drop here  │
│                     │
│  [Select File]     │
└─────────────────────┘

STATE 2: File Selected
┌─────────────────────┐
│ 📄 document.txt  ❌ │
│ 2.5 MB              │
└─────────────────────┘

STATE 3: Uploading
┌─────────────────────┐
│ Uploading... 67%    │
│ ████████░░░░░░░░    │
└─────────────────────┘
```

### VideoPreview Component States
```
STATE 1: Idle
┌──────────────────────┐
│       🎥             │
│                      │
│   No video yet       │
│                      │
│  Upload to generate  │
└──────────────────────┘

STATE 2: Uploading
┌──────────────────────┐
│       ⏳             │
│                      │
│  Uploading file...   │
│                      │
└──────────────────────┘

STATE 3: Generating
┌──────────────────────┐
│    🎬 + ⏳           │
│                      │
│ Generating video...  │
│  Please wait         │
│ ████████░░░░ 70%     │
└──────────────────────┘

STATE 4: Complete
┌──────────────────────┐
│  ✅ Success!         │
│ ┌──────────────────┐ │
│ │  [Video Player]  │ │
│ │  ▶ ═══◉══ 🔊     │ │
│ └──────────────────┘ │
│  [Download Video]    │
│  ID: abc123          │
└──────────────────────┘
```

## 🔄 Data Flow

```
┌──────────────┐
│   Browser    │
│ (localStorage│
│    theme     │
│    token     │
│    user)     │
└──────┬───────┘
       │
       ↓
┌──────────────────────────────────┐
│      React Context API           │
│  ┌────────────┐  ┌────────────┐  │
│  │ AuthContext│  │ThemeContext│  │
│  │  - user    │  │  - theme   │  │
│  │  - token   │  │  - toggle  │  │
│  │  - login   │  │            │  │
│  │  - logout  │  │            │  │
│  └─────┬──────┘  └────────────┘  │
└────────┼─────────────────────────┘
         │
         ↓
┌──────────────────────────────────┐
│       API Service                │
│   (src/services/api.ts)          │
│                                  │
│  - Axios instance                │
│  - Request interceptor (token)   │
│  - Response interceptor (401)    │
│  - authAPI methods               │
│  - contentAPI methods            │
└────────┬─────────────────────────┘
         │
         ↓
┌──────────────────────────────────┐
│     Backend API                  │
│   (http://localhost:9000)        │
│                                  │
│  /users/login                    │
│  /users/register                 │
│  /upload                         │
│  /generate-video                 │
│  /stream/:id                     │
│  /download/:id                   │
└──────────────────────────────────┘
```

## 🎨 Theme System

```
┌────────────────────────────────────┐
│     ThemeContext                   │
│  ┌──────────────┐                  │
│  │ theme: light │ ←→ localStorage  │
│  │    or dark   │                  │
│  └──────────────┘                  │
│         ↓                          │
│  document.documentElement          │
│  .classList.toggle('dark', ...)    │
└────────────────────────────────────┘
         ↓
┌────────────────────────────────────┐
│  TailwindCSS Dark Mode             │
│                                    │
│  Light: bg-white text-gray-900    │
│  Dark:  bg-gray-900 text-gray-100 │
│                                    │
│  Usage: className="              │
│    bg-white dark:bg-gray-900      │
│  "                                 │
└────────────────────────────────────┘
```

## 🔐 Authentication Flow

```
┌──────────┐       ┌──────────┐       ┌──────────┐
│  Login   │──1──→ │  Axios   │──2──→ │ Backend  │
│  Form    │       │  POST    │       │   API    │
└──────────┘       └──────────┘       └────┬─────┘
                                            │
                                          3 │ JWT Token
                                            ↓
┌──────────┐       ┌──────────┐       ┌──────────┐
│Dashboard │←─6──  │localStorage─5──  │AuthContext│
│          │       │  token    │       │  setUser │
└──────────┘       └──────────┘       └──────────┘
     │                                      ↑
     │                                      │
     └───────────7 All API requests────────┘
              include: Authorization: Bearer {token}
```

## 📤 Upload & Generation Flow

```
User Action          Frontend                  Backend
    │                    │                        │
    │ 1. Select File     │                        │
    ├─────────────────→ │                        │
    │                    │                        │
    │ 2. Click Upload    │                        │
    ├─────────────────→ │                        │
    │                    │ 3. POST /upload        │
    │                    ├──────────────────────→ │
    │                    │                        │
    │                    │ 4. content_id          │
    │                    │←────────────────────── │
    │                    │                        │
    │                    │ 5. POST /generate-video │
    │                    ├──────────────────────→ │
    │                    │     {content_id}       │
    │                    │                        │
    │                    │ 6. Processing...       │
    │ 7. Show Progress   │                        │
    │←─────────────────  │                        │
    │                    │                        │
    │                    │ 8. Video ready         │
    │                    │←────────────────────── │
    │                    │                        │
    │ 9. GET /stream/:id │                        │
    │                    ├──────────────────────→ │
    │                    │                        │
    │                    │ 10. Video stream       │
    │ 11. Show Player    │←────────────────────── │
    │←─────────────────  │                        │
```

## 🎯 Key Features Map

```
Landing Page              Auth Page              Dashboard
    │                        │                       │
    ├─ Hero Section         ├─ Login Form          ├─ Navbar
    │  └─ CTA Button        │  ├─ Username         │  ├─ Logo
    │                       │  ├─ Password         │  ├─ Theme Toggle
    ├─ Features Grid        │  └─ Submit           │  ├─ Settings
    │  ├─ Text to Video     │                      │  └─ Profile Menu
    │  ├─ Image Support     ├─ Signup Form         │
    │  └─ Pro Videos        │  ├─ Username         ├─ Upload Section
    │                       │  ├─ Email            │  ├─ Drag & Drop
    ├─ How It Works         │  ├─ Password         │  ├─ File Browser
    │  ├─ Step 1            │  ├─ Confirm          │  ├─ Validation
    │  ├─ Step 2            │  └─ Submit           │  └─ Progress
    │  └─ Step 3            │                      │
    │                       ├─ Form Validation     ├─ Video Preview
    └─ Footer               │                      │  ├─ States
                            └─ Error Handling      │  ├─ Player
                                                   │  ├─ Download
                                                   │  └─ Info
```

## 🛠️ Technology Stack Visualization

```
┌─────────────────────────────────────────────────┐
│              PRESENTATION LAYER                  │
│  ┌───────────────────────────────────────────┐  │
│  │  React Components + TypeScript            │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐     │  │
│  │  │ Pages   │ │Component│ │Context  │     │  │
│  │  │         │ │         │ │         │     │  │
│  │  └─────────┘ └─────────┘ └─────────┘     │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
            │                      │
            ↓                      ↓
┌─────────────────────┐ ┌─────────────────────┐
│   STYLING LAYER     │ │   STATE MANAGEMENT  │
│                     │ │                     │
│  TailwindCSS        │ │  Context API        │
│  - Dark Mode        │ │  - AuthContext      │
│  - Responsive       │ │  - ThemeContext     │
│  - Animations       │ │  - localStorage     │
└─────────────────────┘ └─────────────────────┘
            │
            ↓
┌─────────────────────────────────────────────────┐
│              API LAYER                           │
│  ┌───────────────────────────────────────────┐  │
│  │  Axios HTTP Client                        │  │
│  │  - Request Interceptors                   │  │
│  │  - Response Interceptors                  │  │
│  │  - Error Handling                         │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
            │
            ↓
┌─────────────────────────────────────────────────┐
│         BACKEND API (Existing)                   │
│       FastAPI Server (Port 9000)                 │
│  - Authentication                                │
│  - File Upload                                   │
│  - Video Generation                              │
│  - Content Management                            │
└─────────────────────────────────────────────────┘
```

---

**Visual Architecture Complete!** 🎨

This diagram shows the complete structure and flow of the AI Content Generator frontend application.
