# دليل النشر على Railway

## الخطوات للنشر على Railway

### 1. إنشاء حساب على Railway
- اذهب إلى [railway.app](https://railway.app)
- سجل حساب جديد أو سجل دخول

### 2. إنشاء مشروع جديد
- اضغط على "New Project"
- اختر "Deploy from GitHub repo"
- اربط حساب GitHub الخاص بك
- اختر repository المشروع
-------------م
### 3. إضافة قاعدة بيانات PostgreSQL
- في مشروعك على Railway، اضغط على "New"
- اختر "Database" → "PostgreSQL"
- Railway سينشئ قاعدة بيانات PostgreSQL تلقائياً

### 4. ربط قاعدة البيانات بالتطبيق
- Railway سيقوم تلقائياً بربط قاعدة البيانات بالتطبيق
- متغير `DATABASE_URL` سيتم تعيينه تلقائياً

### 5. إعداد متغيرات البيئة
في إعدادات المشروع، أضف هذه المتغيرات:

```env
DISCORD_CLIENT_ID=your_discord_client_id_here
DISCORD_CLIENT_SECRET=your_discord_client_secret_here
DISCORD_REDIRECT_URI=https://your-app-name.railway.app/auth/callback
JWT_SECRET=your_super_secret_jwt_key_here
CLIENT_REDIRECT_URL=https://your-frontend-url.com
```

### 6. تحديث Discord OAuth
- اذهب إلى [Discord Developer Portal](https://discord.com/developers/applications)
- اختر تطبيقك
- في OAuth2 → Redirects، أضف:
  ```
  https://your-app-name.railway.app/auth/callback
  ```

### 7. النشر
- Railway سينشر التطبيق تلقائياً عند push للـ repository
- يمكنك مراقبة النشر في لوحة التحكم

### 8. اختبار النظام
بعد النشر، اختبر النظام:

```bash
# اختبار health endpoint
curl https://your-app-name.railway.app/health

# إعداد كلمة المرور للمستخدم القائد (محلياً)
python setup_password_railway.py
```

## الملفات المطلوبة للنشر

- ✅ `requirements.txt` - متطلبات Python
- ✅ `Procfile` - إعدادات Railway
- ✅ `app.py` - التطبيق الرئيسي
- ✅ `database.py` - إعداد قاعدة البيانات
- ✅ `models.py` - نماذج قاعدة البيانات
- ✅ `.env` - متغيرات البيئة (محلياً)

## الميزات الجديدة

- ✅ **قاعدة بيانات سحابية** - PostgreSQL على Railway
- ✅ **نشر تلقائي** - عند push للـ repository
- ✅ **متغيرات بيئة آمنة** - إدارة من Railway
- ✅ **قابلية التوسع** - قاعدة بيانات قوية
- ✅ **نسخ احتياطية** - تلقائية من Railway

## استكشاف الأخطاء

### مشكلة في الاتصال بقاعدة البيانات
```bash
# تحقق من متغير DATABASE_URL
echo $DATABASE_URL
```

### مشكلة في النشر
- تحقق من logs في Railway dashboard
- تأكد من أن جميع المتغيرات معينة بشكل صحيح

### مشكلة في Discord OAuth
- تأكد من أن Redirect URI صحيح
- تحقق من Client ID و Client Secret 