# 🚀 الإعداد السريع - نظام تسجيل الدخول المحسن

## ⚡ خطوات سريعة

### 1. إعداد البيئة
```bash
# في مجلد backend
cp env.template .env
# قم بتعديل .env وأضف بيانات Discord OAuth
```

### 2. تثبيت التبعيات
```bash
# في مجلد backend
npm install

# في المجلد الرئيسي
npm install
```

### 3. إعداد قاعدة البيانات
```bash
# في مجلد backend
npm run setup-db
```

### 4. إعداد المستخدم Leader
```bash
# في مجلد backend
# قم بتعديل setup-leader.js وأضف Discord ID الخاص بك
npm run setup-leader
```

### 5. تشغيل النظام
```bash
# Terminal 1 - Backend
cd backend && npm start

# Terminal 2 - Frontend
npm run dev
```

## 🔑 إعداد Discord OAuth

1. اذهب إلى [Discord Developer Portal](https://discord.com/developers/applications)
2. أنشئ تطبيق جديد
3. في OAuth2 أضف Redirect: `http://localhost:5000/auth/callback`
4. انسخ Client ID و Client Secret إلى `.env`

## 🎯 الميزات الجديدة

- ✅ **نظام كلمة المرور**: إنشاء وتسجيل دخول آمن
- ✅ **الرتب التلقائية**: Player للمستخدمين الجدد
- ✅ **حماية لوحة الإدارة**: للأداريين فقط
- ✅ **رسائل خطأ مفصلة**: تجربة مستخدم محسنة
- ✅ **زر التواصل مع الدعم**: عبر الديسكورد

## 🛡️ الأمان

- **كلمة المرور**: 8+ أحرف، رقم + رمز
- **التشفير**: bcrypt مع salt rounds = 12
- **الرتب**: نظام صلاحيات متدرج
- **JWT**: tokens آمنة ومشفرة

---

**جاهز للاستخدام!** 🎉 