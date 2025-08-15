# 👤 Demo User Accounts

## Test User Credentials

For testing the authentication system, you can use any of the following demo accounts:

### Account 1
- **Username**: `testuser`
- **Password**: `testpass123`

### Account 2
- **Username**: `newuser2`
- **Email**: `newuser2@example.com`
- **Password**: `testpassword123`

### Account 3
- **Username**: `newuser3`
- **Email**: `newuser3@example.com`
- **Password**: `testPassword123`

### Account 4
- **Username**: `freshuser`
- **Email**: `freshuser@example.com`
- **Password**: `testpassword123`

### Account 5
- **Username**: `seth`
- **Email**: `seth@lol.com`
- **Password**: `sethTest123`

## Usage Notes

- These accounts are for **testing purposes only**
- All accounts have the same basic user permissions
- Conversations are isolated per user account
- You can create new accounts through the registration interface
- Account data is stored in the SQLite database (`chatbot.db`)

## Creating New Test Accounts

You can register new accounts directly through the application interface:

1. Navigate to the login page
2. Click "Register" or "Sign Up"
3. Fill in the registration form
4. Start chatting with your new account

## Development Notes

- User authentication is handled via JWT tokens
- Passwords are hashed using bcrypt
- Session persistence depends on token storage
- User IDs are used to associate conversations

## Security Reminder

⚠️ **Important**: These are demo credentials for development and testing. Do not use these accounts or passwords in production environments.
