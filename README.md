# 🌟 Shining Management System

## 🎉 نظام إدارة شامل لسيرفر GTA V Roleplay

نظام متكامل لإدارة سيرفر GTA V Roleplay مع ربط Discord OAuth ونظام صلاحيات متقدم.

## ✨ الميزات الرئيسية

### 🔐 نظام تسجيل الدخول المحسن
- **ربط Discord OAuth**: تسجيل دخول آمن عبر Discord
- **نظام كلمة المرور**: إنشاء وتسجيل دخول بكلمة مرور قوية
- **التحقق المزدوج**: تأكيد كلمة المرور للتأكد من صحتها
- **رسائل خطأ مفصلة**: تجربة مستخدم محسنة

### 🛡️ نظام الأمان والصلاحيات
- **الرتب التلقائية**: Player للمستخدمين الجدد
- **الرتب الإدارية**: Leader, Co-Leader, Manager, Staff
- **إدارة الصلاحيات**: نظام متدرج وآمن
- **حماية لوحة الإدارة**: للأداريين فقط

### 🎮 واجهات المستخدم
- **لوحة اللاعبين**: ملف شخصي، متجر، أداء، وظائف
- **لوحة الإدارة**: إدارة شاملة للمستخدمين والصلاحيات
- **نظام التذاكر**: دعم فني متقدم
- **التواصل مع الدعم**: عبر Discord

## 🚀 الإعداد السريع

### المتطلبات
- Node.js 16+
- npm أو yarn
- حساب Discord Developer

### خطوات الإعداد

1. **استنساخ المشروع**
```bash
git clone <repository-url>
cd Shining
```

2. **إعداد البيئة**
```bash
# في مجلد backend
cp backend/env.template backend/.env
# قم بتعديل .env وأضف بيانات Discord OAuth
```

3. **تثبيت التبعيات**
```bash
# Backend
cd backend && npm install

# Frontend
npm install
```

4. **إعداد قاعدة البيانات**
```bash
cd backend
npm run setup-db
```

5. **إعداد المستخدم Leader**
```bash
# قم بتعديل setup-leader.js وأضف Discord ID الخاص بك
npm run setup-leader
```

6. **تشغيل النظام**
```bash
# Terminal 1 - Backend
cd backend && npm start

# Terminal 2 - Frontend
npm run dev
```

## 🔧 إعداد Discord OAuth

1. اذهب إلى [Discord Developer Portal](https://discord.com/developers/applications)
2. أنشئ تطبيق جديد
3. في OAuth2 أضف Redirect: `http://localhost:5000/auth/callback`
4. انسخ Client ID و Client Secret إلى `.env`

## 📁 هيكل المشروع

```
Shining/
├── backend/                 # خادم Node.js
│   ├── database.js         # إعداد قاعدة البيانات
│   ├── setup-leader.js     # إعداد المستخدم Leader
│   ├── routes/
│   │   └── auth.js         # مسارات المصادقة
│   └── middleware/
│       └── auth.js         # وسيط المصادقة
├── src/
│   ├── pages/
│   │   ├── Home.tsx        # الصفحة الرئيسية
│   │   ├── PlayerDashboard.tsx
│   │   ├── AdminDashboard.tsx
│   │   └── PasswordAuthPage.tsx
│   ├── components/
│   │   ├── auth/
│   │   ├── admin/
│   │   └── player/
│   └── lib/
│       └── auth-service.ts
└── README.md
```

## 🛡️ الأمان

### كلمة المرور
- **الحد الأدنى**: 8 أحرف
- **الأرقام**: رقم واحد على الأقل
- **الرموز**: رمز واحد على الأقل (!@#$%^&*)
- **التشفير**: bcrypt مع salt rounds = 12

### الرتب والصلاحيات
- **Player**: الصلاحيات الأساسية
- **Staff**: إدارة التذاكر والبلاغات
- **Manager**: إدارة الطاقم والإحصائيات
- **Co-Leader**: إدارة الأدوار
- **Leader**: جميع الصلاحيات

## 🎯 تدفق تسجيل الدخول

### للمستخدمين الجدد:
1. ربط Discord
2. إنشاء كلمة المرور
3. تأكيد كلمة المرور
4. الانتقال للصفحة المناسبة

### للمستخدمين الموجودين:
1. ربط Discord
2. تسجيل الدخول بكلمة المرور
3. الانتقال للصفحة المناسبة

## 📝 الملفات المهمة

- `QUICK_SETUP.md` - إعداد سريع
- `SETUP_COMPLETE.md` - دليل شامل
- `backend/setup-leader.js` - إعداد المستخدم Leader
- `backend/env.template` - قالب المتغيرات البيئية

## 🆘 الدعم

في حالة مواجهة أي مشاكل:
1. تحقق من إعدادات Discord OAuth
2. تأكد من صحة المتغيرات البيئية
3. تحقق من سجلات الخادم
4. تواصل مع الدعم الفني

## 📄 الترخيص

هذا المشروع مرخص تحت رخصة MIT.

---

**تم تطوير هذا النظام بواسطة فريق Shining** 🌟 