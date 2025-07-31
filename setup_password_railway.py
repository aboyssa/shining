import bcrypt
from database import get_db_session
from models import User

print('🔧 Setting up password for Leader user...\n')

def setup_password():
    try:
        db = get_db_session()
        
        # Leader user details
        leader_id = '651015003843067904'
        password = 'TestPass123!'
        
        # Check if user exists
        user = db.query(User).filter(User.id == leader_id).first()
        
        if not user:
            print('❌ User not found! Creating user...')
            user = User(
                id=leader_id,
                username='a_yssa12',
                email='leader@example.com',
                role='Leader',
                hasPassword=0,
                isActive=1
            )
            db.add(user)
            print('✅ User created!')
        else:
            print(f'✅ User found: {user.username} (Role: {user.role})')
        
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
        
        # Update password
        user.passwordHash = hashed_password.decode('utf-8')
        user.hasPassword = 1
        
        db.commit()
        db.close()
        
        print('✅ Password set successfully!')
        print(f'📝 Discord ID: {leader_id}')
        print(f'🔑 Password: {password}')
        print('\n🎉 You can now test the login system!')
        
    except Exception as e:
        print(f'❌ Error: {str(e)}')

if __name__ == '__main__':
    setup_password() 