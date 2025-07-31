# 🎮 Discord OAuth2 Setup Guide - Shining Management System

## ✅ What's Been Created

I've successfully implemented a complete Discord OAuth2 infrastructure for your Shining project based on the [GitHub repository](https://github.com/robinvriens/discord-oauth2.git) you referenced. Here's what's been set up:

### 🔧 Backend Infrastructure

1. **`backend/index.js`** - Main server with modular architecture
2. **`backend/routes/auth.js`** - Discord OAuth2 endpoints
3. **`backend/services/discord.js`** - Discord API service
4. **`backend/middleware/auth.js`** - Authentication middleware
5. **`backend/env.template`** - Environment variables template
6. **`backend/README.md`** - Comprehensive documentation

### 🎨 Frontend Integration

1. **`src/lib/auth-service.ts`** - Authentication service
2. **`src/hooks/useAuth.ts`** - React authentication hook

### 📁 File Structure

```
Shining/
├── backend/
│   ├── index.js              # Main server
│   ├── routes/
│   │   └── auth.js           # OAuth routes
│   ├── services/
│   │   └── discord.js        # Discord API service
│   ├── middleware/
│   │   └── auth.js           # Auth middleware
│   ├── package.json          # Dependencies
│   ├── env.template          # Environment template
│   └── README.md            # Setup guide
├── src/
│   ├── lib/
│   │   └── auth-service.ts   # Frontend auth service
│   └── hooks/
│       └── useAuth.ts        # React auth hook
└── DISCORD_OAUTH_SETUP.md   # This guide
```

## 🚀 Quick Setup Steps

### Step 1: Configure Environment Variables

```bash
cd backend
cp env.template .env
```

Edit `.env` file:
```env
DISCORD_CLIENT_ID="your_discord_client_id"
DISCORD_CLIENT_SECRET="your_discord_client_secret"
DISCORD_REDIRECT_URI="http://localhost:5000/auth/callback"
JWT_SECRET="your_jwt_secret_key_here"
CLIENT_REDIRECT_URL="http://localhost:3000"
```

### Step 2: Discord Application Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create new application
3. Go to "OAuth2" section
4. Add redirect URI: `http://localhost:5000/auth/callback`
5. Copy Client ID and Client Secret to `.env`
6. **Important**: Replace `YOUR_SERVER_ID` in `backend/routes/auth.js` with your Discord server ID

### Step 3: Install Dependencies & Start Server

```bash
cd backend
npm install
npm run dev
```

### Step 4: Test the Integration

1. Start your frontend: `npm run dev`
2. Click "تسجيل الدخول بـ Discord" button
3. Complete Discord OAuth flow
4. You should be redirected back with a JWT token

## 🔐 Authentication Flow

```
User clicks login → /auth/login → Discord OAuth → /auth/callback → JWT token → Frontend
```

## 🛡️ Security Features

- ✅ **JWT Token Management** - 7-day expiration
- ✅ **Server Membership Check** - Only Discord server members can login
- ✅ **Rate Limiting** - Protection against abuse
- ✅ **CORS Protection** - Secure cross-origin requests
- ✅ **Error Handling** - Comprehensive error management

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DISCORD_CLIENT_ID` | Discord application client ID | ✅ |
| `DISCORD_CLIENT_SECRET` | Discord application client secret | ✅ |
| `DISCORD_REDIRECT_URI` | OAuth callback URL | ✅ |
| `JWT_SECRET` | Secret key for JWT signing | ✅ |
| `CLIENT_REDIRECT_URL` | Frontend URL for redirects | ✅ |

### Discord Scopes Requested

- `identify` - Get user information
- `guilds` - Get user's servers (for membership check)
- `email` - Get user's email (optional)

## 🎯 Integration with Your Existing Code

Your existing `LoginDialog.tsx` component already works perfectly with this setup:

```typescript
const handleDiscordLogin = () => {
  window.location.href = "http://localhost:5000/auth/login";
};
```

## 🔄 Using the Authentication Hook

```typescript
import useAuth from '../hooks/useAuth';

function MyComponent() {
  const { user, isAuthenticated, isLoading, login, logout } = useAuth();

  if (isLoading) return <div>Loading...</div>;
  
  if (!isAuthenticated) {
    return <button onClick={login}>Login with Discord</button>;
  }

  return (
    <div>
      <h1>Welcome, {user?.username}!</h1>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
```

## 🚨 Important Notes

1. **Server ID**: Replace `YOUR_SERVER_ID` in `backend/routes/auth.js` with your actual Discord server ID
2. **JWT Secret**: Use a strong, random string for `JWT_SECRET`
3. **HTTPS**: For production, use HTTPS URLs
4. **CORS**: Update CORS origins for production domains

## 🔗 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/login` | GET | Redirects to Discord OAuth |
| `/auth/callback` | GET | Handles OAuth callback |
| `/auth/verify` | GET | Verify JWT token |
| `/auth/profile` | GET | Get user profile |
| `/auth/logout` | POST | Logout user |
| `/health` | GET | Health check |

## 🎉 What's Next?

1. **Configure your Discord application** with the credentials
2. **Update the server ID** in the auth routes
3. **Test the authentication flow**
4. **Integrate with your existing dashboard** using the `useAuth` hook
5. **Deploy to production** with proper environment variables

## 📞 Need Help?

If you encounter any issues:

1. Check the backend console for error messages
2. Verify Discord application settings
3. Ensure environment variables are set correctly
4. Check that your Discord server ID is correct

The infrastructure is now complete and ready for use! 🚀 