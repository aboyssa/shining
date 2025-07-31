# Authentication Flow Documentation

## Overview
This document explains the role-based authentication flow implemented in the Shining Management System.

## Flow Description

### 1. User Authentication
- User clicks "Login with Discord" on the home page
- User is redirected to Discord OAuth
- After successful authentication, Discord redirects back to our backend
- Backend verifies the user and assigns a role based on Discord ID

### 2. Role Assignment
The system assigns roles based on Discord ID:
- **Leader Role**: Assigned to Discord ID `651015003843067904` (your account)
- **Player Role**: Assigned to all other users

### 3. Permission System
- **SuperAdmin & Leader**: Can assign/change any user's role
- **Co-Leader, Manager, Staff**: Can view admin panel but cannot manage roles
- **Players**: Access to player dashboard only

### 4. Routing Logic
After OAuth authentication:
- **Admin Users** (SuperAdmin, Leader, Co-Leader, Manager, Staff): Redirected to `/admin`
- **Player Users**: Redirected to `/player`

### 5. Protected Routes
- `/admin`: Requires admin role (SuperAdmin, Leader, Co-Leader, Manager, Staff)
- `/player`: Requires any authenticated user
- `/callback`: Handles OAuth redirects and role-based routing

## Technical Implementation

### Frontend Components
1. **OAuthCallback**: Handles OAuth redirects and routes users based on role
2. **ProtectedRoute**: Wraps routes and checks authentication/authorization
3. **useAuth Hook**: Manages authentication state

### Backend Routes
1. `/auth/login`: Initiates Discord OAuth
2. `/auth/callback`: Handles OAuth callback and creates JWT token
3. `/auth/verify`: Verifies JWT tokens
4. `/auth/profile`: Gets user profile

### URL Structure
- OAuth redirect: `http://localhost:8000/#/callback?token=...`
- Admin dashboard: `http://localhost:8000/#/admin`
- Player dashboard: `http://localhost:8000/#/player`

## Testing
1. Start the backend server: `cd backend && npm start`
2. Start the frontend: `npm run dev`
3. Click "Login with Discord" on the home page
4. Complete Discord OAuth
5. You should be redirected to the admin dashboard (if you're the leader) or player dashboard

## Troubleshooting
- If you get a 404 error, check that the backend is running on port 5000
- If authentication fails, verify your Discord ID is correctly set in the backend
- If routing doesn't work, check the browser console for errors 