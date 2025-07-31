from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import bcrypt
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy import text
from database import engine, SessionLocal, init_database
from models import User, Permission

# تحميل متغيرات البيئة
load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', 'your-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)

# إعداد CORS
CORS(app, origins=[os.getenv('CLIENT_REDIRECT_URL', 'http://localhost:8000')])

# إعداد JWT
jwt = JWTManager(app)

# تهيئة قاعدة البيانات
init_database()

def get_db_session():
    """الحصول على جلسة قاعدة البيانات"""
    return SessionLocal()

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'OK',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'database': 'PostgreSQL on Railway' if os.getenv('DATABASE_URL') else 'SQLite Local',
        'discord': {
            'clientId': 'Configured' if os.getenv('DISCORD_CLIENT_ID') else 'Not configured',
            'redirectUri': os.getenv('DISCORD_REDIRECT_URI')
        }
    })

@app.route('/auth/login', methods=['GET'])
def discord_login():
    """توجيه المستخدم لصفحة مصادقة Discord"""
    client_id = os.getenv('DISCORD_CLIENT_ID')
    redirect_uri = os.getenv('DISCORD_REDIRECT_URI')
    auth_url = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=identify%20email"
    return redirect(auth_url)

@app.route('/auth/callback')
def discord_callback():
    """معالجة callback من Discord"""
    try:
        code = request.args.get('code')
        if not code:
            return redirect(f"{os.getenv('CLIENT_REDIRECT_URL', 'http://localhost:8000')}/#/auth?error=no_code")
        
        print('🔐 Discord OAuth callback received')
        
        # استبدال الكود بـ access token
        token_data = {
            'client_id': os.getenv('DISCORD_CLIENT_ID'),
            'client_secret': os.getenv('DISCORD_CLIENT_SECRET'),
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': os.getenv('DISCORD_REDIRECT_URI')
        }
        
        token_response = requests.post('https://discord.com/api/oauth2/token', data=token_data)
        token_response.raise_for_status()
        
        access_token = token_response.json()['access_token']
        
        # جلب معلومات المستخدم من Discord
        user_response = requests.get('https://discord.com/api/users/@me', 
                                   headers={'Authorization': f'Bearer {access_token}'})
        user_response.raise_for_status()
        
        discord_user = user_response.json()
        print(f'🔐 Discord user data received: {{ id: {discord_user["id"]}, username: {discord_user["username"]} }}')
        
        db = get_db_session()
        
        # التحقق من وجود المستخدم
        existing_user = db.query(User).filter(User.id == discord_user['id']).first()
        
        if existing_user:
            # تحديث المستخدم الموجود
            existing_user.username = discord_user['username']
            existing_user.email = discord_user.get('email')
            existing_user.avatar = discord_user.get('avatar')
            existing_user.discriminator = discord_user.get('discriminator')
            existing_user.lastLogin = datetime.now()
            existing_user.updatedAt = datetime.now()
            
            has_password = bool(existing_user.passwordHash)
            print(f'✅ User updated in database: {discord_user["username"]}')
        else:
            # إنشاء مستخدم جديد
            new_user = User(
                id=discord_user['id'],
                username=discord_user['username'],
                email=discord_user.get('email'),
                avatar=discord_user.get('avatar'),
                discriminator=discord_user.get('discriminator'),
                role='Player',
                hasPassword=0,
                lastLogin=datetime.now()
            )
            db.add(new_user)
            
            has_password = False
            print(f'✅ New user saved to database: {discord_user["username"]}')
        
        db.commit()
        db.close()
        
        # إنشاء JWT token
        token_data = {
            'id': discord_user['id'],
            'username': discord_user['username'],
            'avatar': discord_user.get('avatar'),
            'email': discord_user.get('email'),
            'discriminator': discord_user.get('discriminator'),
            'role': existing_user.role if existing_user else 'Player',
            'hasPassword': has_password
        }
        
        token = create_access_token(identity=token_data)
        
        # التوجيه للواجهة الأمامية
        client_url = os.getenv('CLIENT_REDIRECT_URL', 'http://localhost:8000')
        return redirect(f"{client_url}/#/callback?token={token}")
        
    except Exception as e:
        print(f'🔐 Discord OAuth error: {str(e)}')
        client_url = os.getenv('CLIENT_REDIRECT_URL', 'http://localhost:8000')
        return redirect(f"{client_url}/#/auth?error=unknown")

@app.route('/auth/login-password', methods=['POST'])
def login_with_password():
    """تسجيل الدخول بكلمة المرور"""
    print('🚀 LOGIN-PASSWORD ENDPOINT CALLED!')
    
    try:
        data = request.get_json()
        discord_id = data.get('discordId')
        password = data.get('password')
        
        print(f'🔍 Debug login-password:')
        print(f'   discordId: {discord_id}')
        print(f'   password: {"EXISTS" if password else "MISSING"}')
        
        if not discord_id or not password:
            return jsonify({
                'success': False,
                'message': 'Discord ID وكلمة المرور مطلوبان'
            }), 400
        
        db = get_db_session()
        
        # جلب المستخدم من قاعدة البيانات
        user = db.query(User).filter(User.id == discord_id, User.isActive == 1).first()
        
        print(f'   user from DB: {"FOUND" if user else "NOT FOUND"}')
        if user:
            print(f'   user.id: {user.id}')
            print(f'   user.hasPassword: {user.hasPassword}')
            print(f'   user.passwordHash: {"EXISTS" if user.passwordHash else "NULL"}')
        
        if not user:
            db.close()
            return jsonify({
                'success': False,
                'message': 'المستخدم غير موجود أو غير نشط'
            }), 404
        
        if not user.passwordHash:
            print('❌ passwordHash is NULL!')
            db.close()
            return jsonify({
                'success': False,
                'message': 'المستخدم لم يقم بتعيين كلمة مرور بعد'
            }), 400
        
        print('✅ passwordHash exists, verifying password...')
        
        # التحقق من كلمة المرور
        is_valid = bcrypt.checkpw(password.encode('utf-8'), user.passwordHash.encode('utf-8'))
        print(f'   password valid: {is_valid}')
        
        if not is_valid:
            db.close()
            return jsonify({
                'success': False,
                'message': 'كلمة المرور غير صحيحة'
            }), 401
        
        print('✅ Password verified successfully!')
        
        # تحديث آخر تسجيل دخول
        user.lastLogin = datetime.now()
        db.commit()
        db.close()
        
        # إنشاء JWT token جديد
        token_data = {
            'id': user.id,
            'username': user.username,
            'avatar': user.avatar,
            'email': user.email,
            'discriminator': user.discriminator,
            'role': user.role,
            'hasPassword': True
        }
        
        token = create_access_token(identity=token_data)
        
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role or 'Player',
            'avatar': user.avatar,
            'hasPassword': True
        }
        
        print('✅ Login successful, sending response...')
        
        return jsonify({
            'success': True,
            'token': token,
            'user': user_data
        })
        
    except Exception as e:
        print(f'Error logging in with password: {str(e)}')
        return jsonify({
            'success': False,
            'message': 'حدث خطأ أثناء تسجيل الدخول'
        }), 500

@app.route('/auth/set-password', methods=['POST'])
@jwt_required()
def set_password():
    """إنشاء كلمة المرور"""
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        password = data.get('password')
        confirm_password = data.get('confirmPassword')
        discord_id = current_user['id']
        
        print(f'🔍 Debug set-password:')
        print(f'   current_user: {current_user}')
        print(f'   discordId: {discord_id}')
        print(f'   password: {"EXISTS" if password else "MISSING"}')
        print(f'   confirmPassword: {"EXISTS" if confirm_password else "MISSING"}')
        
        if not discord_id:
            print('❌ discordId is undefined!')
            return jsonify({
                'success': False,
                'message': 'خطأ في معرف المستخدم'
            }), 400
        
        if not password or not confirm_password:
            return jsonify({
                'success': False,
                'message': 'كلمة المرور وتأكيدها مطلوبان'
            }), 400
        
        if password != confirm_password:
            return jsonify({
                'success': False,
                'message': 'كلمتا المرور غير متطابقتين'
            }), 400
        
        # التحقق من شروط كلمة المرور
        if len(password) < 8:
            return jsonify({
                'success': False,
                'message': 'كلمة المرور يجب أن تكون 8 أحرف على الأقل'
            }), 400
        
        import re
        if not re.search(r'(?=.*[0-9])(?=.*[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?_])', password):
            return jsonify({
                'success': False,
                'message': 'كلمة المرور يجب أن تحتوي على رقم واحد على الأقل ورمز واحد على الأقل'
            }), 400
        
        db = get_db_session()
        
        # التحقق من أن المستخدم لم يضع كلمة مرور من قبل
        user = db.query(User).filter(User.id == discord_id).first()
        
        if user and user.passwordHash:
            db.close()
            return jsonify({
                'success': False,
                'message': 'المستخدم لديه كلمة مرور بالفعل'
            }), 400
        
        # إنشاء كلمة المرور
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
        
        print(f'🔧 Updating password for user: {discord_id}')
        
        # تحديث المستخدم في قاعدة البيانات
        user.passwordHash = hashed_password.decode('utf-8')
        user.hasPassword = 1
        user.updatedAt = datetime.now()
        
        db.commit()
        db.close()
        
        print(f'✅ Password set successfully for user: {discord_id}')
        
        return jsonify({
            'success': True,
            'message': 'تم إنشاء كلمة المرور بنجاح'
        })
        
    except Exception as e:
        print(f'Error setting password: {str(e)}')
        return jsonify({
            'success': False,
            'message': 'حدث خطأ أثناء إنشاء كلمة المرور'
        }), 500

@app.route('/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """جلب بيانات الملف الشخصي"""
    try:
        current_user = get_jwt_identity()
        
        db = get_db_session()
        user = db.query(User).filter(User.id == current_user['id']).first()
        db.close()
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'المستخدم غير موجود'
            }), 404
        
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role or 'Player',
            'avatar': user.avatar,
            'discriminator': user.discriminator,
            'hasPassword': bool(user.passwordHash and len(user.passwordHash) > 0),
            'lastLogin': user.lastLogin.isoformat() if user.lastLogin else None,
            'createdAt': user.createdAt.isoformat() if user.createdAt else None
        }
        
        return jsonify({
            'success': True,
            'user': user_data
        })
        
    except Exception as e:
        print(f'Error getting profile: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'حدث خطأ أثناء جلب بيانات الملف الشخصي'
        }), 500

@app.route('/auth/logout', methods=['POST'])
def logout():
    """تسجيل الخروج"""
    return jsonify({
        'success': True,
        'message': 'تم تسجيل الخروج بنجاح'
    })

if __name__ == '__main__':
    print('🚀 Starting Flask server...')
    print('✅ Database initialized successfully')
    print(f'📡 Discord Client ID: {"Configured" if os.getenv("DISCORD_CLIENT_ID") else "Not configured"}')
    print(f'🔗 Redirect URI: {os.getenv("DISCORD_REDIRECT_URI")}')
    print(f'🌐 Client URL: {os.getenv("CLIENT_REDIRECT_URL", "http://localhost:8000")}')
    print(f'🔒 JWT Secret: {"Configured" if os.getenv("JWT_SECRET") else "Not configured"}')
    print(f'🗄️ Database: {"PostgreSQL on Railway" if os.getenv("DATABASE_URL") else "SQLite Local"}')
    
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port) 