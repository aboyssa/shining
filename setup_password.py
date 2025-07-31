import sqlite3
import bcrypt

print('🔧 Setting up password for Leader user...\n')

def setup_password():
    try:
        # Connect to database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        # Leader user details
        leader_id = '651015003843067904'
        password = 'TestPass123!'
        
        # Check if user exists
        cursor.execute('SELECT * FROM users WHERE id = ?', (leader_id,))
        user = cursor.fetchone()
        
        if not user:
            print('❌ User not found! Creating user...')
            cursor.execute('''
                INSERT INTO users (id, username, email, role, hasPassword, isActive)
                VALUES (?, 'a_yssa12', 'leader@example.com', 'Leader', 0, 1)
            ''', (leader_id,))
            print('✅ User created!')
        else:
            print(f'✅ User found: {user[1]} (Role: {user[5]})')
        
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
        
        # Update password
        cursor.execute('''
            UPDATE users 
            SET passwordHash = ?, hasPassword = 1, updatedAt = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (hashed_password.decode('utf-8'), leader_id))
        
        conn.commit()
        conn.close()
        
        print('✅ Password set successfully!')
        print(f'📝 Discord ID: {leader_id}')
        print(f'🔑 Password: {password}')
        print('\n🎉 You can now test the login system!')
        
    except Exception as e:
        print(f'❌ Error: {str(e)}')

if __name__ == '__main__':
    setup_password() 