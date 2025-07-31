import os
import sqlite3
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import pymysql

load_dotenv()

# تحديد نوع قاعدة البيانات
DATABASE_URL = os.getenv('DATABASE_URL')

# إنشاء engine
if DATABASE_URL:
    # استخدام MySQL على Railway
    if DATABASE_URL.startswith('mysql://'):
        # تحويل mysql:// إلى mysql+pymysql:// للتوافق مع SQLAlchemy
        DATABASE_URL = DATABASE_URL.replace('mysql://', 'mysql+pymysql://', 1)
    
    engine = create_engine(DATABASE_URL)
    print('🚀 Using MySQL database on Railway')
else:
    # استخدام SQLite محلياً
    engine = create_engine('sqlite:///users.db')
    print('🚀 Using local SQLite database')

# إنشاء session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# إنشاء base class للنماذج
Base = declarative_base()

def get_db_session():
    """الحصول على جلسة قاعدة البيانات"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """تهيئة قاعدة البيانات"""
    try:
        # إنشاء الجداول
        Base.metadata.create_all(bind=engine)
        
        # إدراج البيانات الأولية
        with engine.connect() as conn:
            # إدراج الصلاحيات الافتراضية
            permissions = [
                ('Player', 'view_profile'),
                ('Staff', 'view_profile'),
                ('Staff', 'moderate_chat'),
                ('Manager', 'view_profile'),
                ('Manager', 'moderate_chat'),
                ('Manager', 'manage_staff'),
                ('Co-Leader', 'view_profile'),
                ('Co-Leader', 'moderate_chat'),
                ('Co-Leader', 'manage_staff'),
                ('Co-Leader', 'manage_roles'),
                ('Leader', 'view_profile'),
                ('Leader', 'moderate_chat'),
                ('Leader', 'manage_staff'),
                ('Leader', 'manage_roles'),
                ('Leader', 'full_access')
            ]
            
            # التحقق من وجود الصلاحيات
            for role, permission in permissions:
                result = conn.execute(text(
                    "SELECT COUNT(*) FROM permissions WHERE role = :role AND permission = :permission"
                ), {"role": role, "permission": permission})
                
                if result.scalar() == 0:
                    conn.execute(text(
                        "INSERT INTO permissions (role, permission) VALUES (:role, :permission)"
                    ), {"role": role, "permission": permission})
            
            # إنشاء المستخدم القائد إذا لم يكن موجوداً
            leader_id = '651015003843067904'
            result = conn.execute(text("SELECT COUNT(*) FROM users WHERE id = :id"), {"id": leader_id})
            
            if result.scalar() == 0:
                conn.execute(text("""
                    INSERT INTO users (id, username, email, role, hasPassword, isActive)
                    VALUES (:id, 'a_yssa12', 'leader@example.com', 'Leader', 0, 1)
                """), {"id": leader_id})
                print(f'✅ Leader user created: {leader_id}')
            else:
                print(f'✅ Leader user already exists: {leader_id}')
            
            conn.commit()
        
        print('✅ Database initialized successfully')
        
    except Exception as e:
        print(f'❌ Error initializing database: {str(e)}')
        raise

def get_sqlite_connection():
    """الحصول على اتصال SQLite (للتوافق مع الكود القديم)"""
    if not DATABASE_URL:
        return sqlite3.connect('users.db')
    else:
        raise Exception("SQLite not available when using MySQL")

# تهيئة قاعدة البيانات عند استيراد الملف
init_database() 