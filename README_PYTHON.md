# Shining City - Python Backend

نظام مصادقة Discord مع إدارة كلمات المرور مكتوب بلغة Python باستخدام Flask.

## المتطلبات

- Python 3.8+
- pip

## التثبيت

1. تثبيت المتطلبات:
```bash
pip install -r requirements.txt
```

2. إنشاء ملف `.env`:
```bash
copy env.template .env
```

3. تعديل ملف `.env` بإعدادات Discord الخاصة بك:
```env
DISCORD_CLIENT_ID=your_discord_client_id_here
DISCORD_CLIENT_SECRET=your_discord_client_secret_here
DISCORD_REDIRECT_URI=http://localhost:5000/auth/callback
JWT_SECRET=your_super_secret_jwt_key_here
CLIENT_REDIRECT_URL=http://localhost:8000
```

## تشغيل الخادم

```bash
python app.py
```

الخادم سيعمل على `http://localhost:5000`

## إعداد كلمة المرور للمستخدم القائد

```bash
python setup_password.py
```

## اختبار النظام

```bash
python test_python.py
```

## المسارات المتاحة

### المصادقة
- `GET /auth/login` - توجيه لصفحة مصادقة Discord
- `GET /auth/callback` - معالجة callback من Discord
- `POST /auth/login-password` - تسجيل الدخول بكلمة المرور
- `POST /auth/set-password` - إنشاء كلمة المرور (يتطلب JWT)
- `GET /auth/profile` - جلب بيانات الملف الشخصي (يتطلب JWT)
- `POST /auth/logout` - تسجيل الخروج

### النظام
- `GET /health` - فحص صحة الخادم

## الميزات

- ✅ مصادقة Discord OAuth2
- ✅ إدارة كلمات المرور مع bcrypt
- ✅ JWT tokens للمصادقة
- ✅ قاعدة بيانات SQLite
- ✅ نظام الصلاحيات والرتب
- ✅ CORS للواجهة الأمامية
- ✅ معالجة الأخطاء الشاملة
- ✅ Debug logging مفصل

## قاعدة البيانات

النظام ينشئ تلقائياً:
- جدول `users` للمستخدمين
- جدول `permissions` للصلاحيات
- المستخدم القائد مع Discord ID: `651015003843067904`

## الأمان

- كلمات المرور مشفرة بـ bcrypt مع 12 salt rounds
- JWT tokens منتهية الصلاحية
- التحقق من صحة المدخلات
- حماية من CORS 