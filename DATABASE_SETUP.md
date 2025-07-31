# 🗄️ دليل إعداد قاعدة البيانات - Shining Management System

## 📋 نظرة عامة

هذا الدليل يوفر لك السيطرة الكاملة على قاعدة البيانات وجميع صلاحيات النظام. تم تصميم النظام ليكون مرناً وقابلاً للتخصيص بالكامل.

## 🔐 صلاحيات المدير الأعلى (YOUR CREDENTIALS)

```sql
-- حسابك الأساسي مع جميع الصلاحيات
INSERT INTO users (id, discord_id, username, display_name, role, is_super_admin) VALUES 
('super-admin-001', 'YOUR_DISCORD_ID', 'YasserAlquraishi', 'Yasser - System Creator', 'SuperAdmin', TRUE);

-- منح جميع الصلاحيات
INSERT INTO user_permissions (user_id, permission) VALUES 
('super-admin-001', 'SYSTEM_ADMIN'),
('super-admin-001', 'DATABASE_ADMIN'),
('super-admin-001', 'FULL_ACCESS'),
('super-admin-001', 'CREATE_ADMINS'),
('super-admin-001', 'DELETE_USERS'),
('super-admin-001', 'MODIFY_SYSTEM');
```

## 🏗️ هيكل قاعدة البيانات

### 1. جدول المستخدمين (Users)
```sql
CREATE TABLE users (
    id VARCHAR(50) PRIMARY KEY,
    discord_id VARCHAR(20) UNIQUE NOT NULL,
    username VARCHAR(50) NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    avatar_url TEXT,
    role ENUM('SuperAdmin', 'Leader', 'Co-Leader', 'Manager', 'Staff', 'Helper', 'Player') DEFAULT 'Player',
    is_super_admin BOOLEAN DEFAULT FALSE,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    status ENUM('active', 'inactive', 'banned', 'suspended') DEFAULT 'active',
    
    -- معلومات إضافية
    age INT,
    location VARCHAR(100),
    bio TEXT,
    phone VARCHAR(20),
    email VARCHAR(100),
    
    -- إحصائيات اللعب
    total_playtime INT DEFAULT 0, -- بالدقائق
    level INT DEFAULT 1,
    reputation DECIMAL(2,1) DEFAULT 3.0,
    
    -- إعدادات الحساب
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 2. جدول الأدوار والصلاحيات (Roles & Permissions)
```sql
CREATE TABLE roles (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    color VARCHAR(7) DEFAULT '#6B7280',
    priority INT DEFAULT 10,
    is_default BOOLEAN DEFAULT FALSE,
    discord_role_id VARCHAR(20),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE permissions (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50)
);

CREATE TABLE role_permissions (
    role_id VARCHAR(50),
    permission_id VARCHAR(50),
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE
);

CREATE TABLE user_permissions (
    user_id VARCHAR(50),
    permission VARCHAR(100),
    granted_by VARCHAR(50),
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, permission),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### 3. جدول التذاكر (Tickets)
```sql
CREATE TABLE tickets (
    id VARCHAR(20) PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    category ENUM('technical', 'account', 'gameplay', 'report', 'general', 'suggestion') NOT NULL,
    priority ENUM('low', 'medium', 'high', 'urgent') DEFAULT 'medium',
    status ENUM('open', 'in_progress', 'resolved', 'closed') DEFAULT 'open',
    
    creator_id VARCHAR(50) NOT NULL,
    assigned_to VARCHAR(50),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    closed_at TIMESTAMP NULL,
    
    FOREIGN KEY (creator_id) REFERENCES users(id),
    FOREIGN KEY (assigned_to) REFERENCES users(id)
);

CREATE TABLE ticket_responses (
    id VARCHAR(50) PRIMARY KEY,
    ticket_id VARCHAR(20) NOT NULL,
    author_id VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    is_admin_response BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (ticket_id) REFERENCES tickets(id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES users(id)
);
```

### 4. جدول تتبع اللاعبين (Player Tracking)
```sql
CREATE TABLE player_tracking (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    
    -- معلومات الشخصية في اللعبة
    character_name VARCHAR(100),
    citizen_id VARCHAR(20),
    job VARCHAR(50) DEFAULT 'unemployed',
    job_grade VARCHAR(50) DEFAULT 'unemployed',
    
    -- الموقع والحالة
    is_online BOOLEAN DEFAULT FALSE,
    current_location_x DECIMAL(10,2),
    current_location_y DECIMAL(10,2),
    current_zone VARCHAR(50),
    last_location VARCHAR(100),
    
    -- المعلومات المالية
    cash INT DEFAULT 0,
    bank INT DEFAULT 5000,
    
    -- إحصائيات النشاط
    session_time INT DEFAULT 0, -- بالدقائق
    afk_time INT DEFAULT 0,
    is_afk BOOLEAN DEFAULT FALSE,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- تحديث البيانات
    last_sync TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- جدول المركبات
CREATE TABLE player_vehicles (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    plate VARCHAR(10) NOT NULL UNIQUE,
    garage VARCHAR(100),
    type ENUM('personal', 'job', 'rental') DEFAULT 'personal',
    purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- جدول العقارات
CREATE TABLE player_properties (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    type ENUM('apartment', 'house', 'garage', 'business') NOT NULL,
    address VARCHAR(200) NOT NULL,
    is_owned BOOLEAN DEFAULT TRUE,
    value INT DEFAULT 0,
    purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### 5. جدول التقديم للوظائف (Job Applications)
```sql
CREATE TABLE job_applications (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    job_type VARCHAR(50) NOT NULL,
    status ENUM('pending', 'approved', 'rejected', 'interview') DEFAULT 'pending',
    
    -- معلومات التقديم
    full_name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    experience TEXT,
    motivation TEXT NOT NULL,
    specialization VARCHAR(100),
    available_hours VARCHAR(20),
    
    -- معلومات المعالجة
    reviewed_by VARCHAR(50),
    interview_date TIMESTAMP NULL,
    notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewed_by) REFERENCES users(id)
);
```

### 6. جدول الانتهاكات والتحذيرات (Violations & Warnings)
```sql
CREATE TABLE violations (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    type ENUM('warning', 'violation', 'ban', 'kick') NOT NULL,
    reason TEXT NOT NULL,
    severity ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    
    issued_by VARCHAR(50) NOT NULL,
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL,
    
    is_active BOOLEAN DEFAULT TRUE,
    notes TEXT,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (issued_by) REFERENCES users(id)
);
```

### 7. جدول السجلات والتدقيق (Audit Logs)
```sql
CREATE TABLE audit_logs (
    id VARCHAR(50) PRIMARY KEY,
    action VARCHAR(100) NOT NULL,
    performed_by VARCHAR(50) NOT NULL,
    target_user VARCHAR(50),
    details JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (performed_by) REFERENCES users(id),
    FOREIGN KEY (target_user) REFERENCES users(id)
);
```

### 8. جدول الإحصائيات (Statistics)
```sql
CREATE TABLE server_statistics (
    id VARCHAR(50) PRIMARY KEY,
    date DATE NOT NULL,
    total_users INT DEFAULT 0,
    active_users INT DEFAULT 0,
    new_registrations INT DEFAULT 0,
    total_playtime INT DEFAULT 0,
    tickets_created INT DEFAULT 0,
    tickets_resolved INT DEFAULT 0,
    violations_issued INT DEFAULT 0,
    job_applications INT DEFAULT 0,
    server_uptime DECIMAL(5,2) DEFAULT 0.0,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_date (date)
);
```

## 🔧 بيانات أساسية للنظام

### إدراج الأدوار الأساسية
```sql
INSERT INTO roles (id, name, display_name, color, priority, description) VALUES
('role-superadmin', 'SuperAdmin', 'المدير الأعلى', '#000000ff', 1000, 'صانع النظام - جميع الصلاحيات'),
('role-leader', 'Leader', '#080019ff', 100, 'القائد الأعلى للسيرفر'),
('role-coleader', 'Co-Leader', '#6b0200ff', 90, 'نائب القائد مع صلاحيات متقدمة'),
('role-manager', 'Manager', 'مدير', '#10B981', 80, 'مدير مع صلاحيات إدارية'),
('role-staff', 'Staff', '#F59E0B', 70, 'موظف مع صلاحيات أساسية'),
('role-player', 'Player', '#6B7280', 10, 'الدور الافتراضي للاعبين');

-- تحديد الدور الافتراضي
UPDATE roles SET is_default = TRUE WHERE id = 'role-player';
```

### إدراج الصلاحيات
```sql
INSERT INTO permissions (id, name, description, category) VALUES
-- صلاحيات النظام
('perm-system-admin', 'إدارة النظام', 'السيطرة الكاملة على النظام', 'نظام'),
('perm-database-admin', 'إدارة قاعدة البيانات', 'تعديل قاعدة البيانات', 'نظام'),
('perm-full-access', 'وصول كامل', 'جميع الصلاحيات', 'نظام'),

-- إدارة المستخدمين
('perm-users-view', 'عرض المستخدمين', 'عرض قائمة المستخدمين', 'المستخدمون'),
('perm-users-edit', 'تعديل المستخدمين', 'تعديل بيانات المستخدمين', 'المستخدمون'),
('perm-users-ban', 'حظر المستخدمين', 'حظر وإلغاء حظر المستخدمين', 'المستخدمون'),
('perm-users-delete', 'حذف المستخدمين', 'حذف حسابات المستخدمين', 'المستخدمون'),

-- إدارة الأدوار
('perm-roles-view', 'عرض الأدوار', 'عرض قائمة الأدوار', 'الأدوار'),
('perm-roles-create', 'إنشاء الأدوار', 'إنشاء أدوار جديدة', 'الأدوار'),
('perm-roles-edit', 'تعديل الأدوار', 'تعديل الأدوار الموجودة', 'الأدوار'),
('perm-roles-delete', 'حذف الأدوار', 'حذف الأدوار', 'الأدوار'),

-- نظام التذاكر
('perm-tickets-view', 'عرض التذاكر', 'عرض جميع التذاكر', 'التذاكر'),
('perm-tickets-manage', 'إدارة التذاكر', 'إدارة والرد على التذاكر', 'التذاكر'),
('perm-tickets-close', 'إغلاق التذاكر', 'إغلاق التذاكر', 'التذاكر'),

-- تتبع اللاعبين
('perm-tracking-view', 'تتبع اللاعبين', 'عرض بيانات تتبع اللاعبين', 'التتبع'),
('perm-tracking-location', 'تتبع المواقع', 'تتبع مواقع اللاعبين', 'التتبع'),
('perm-tracking-finance', 'تتبع المالية', 'عرض البيانات المالية للاعبين', 'التتبع'),

-- التحليلات
('perm-analytics-view', 'عرض التحليلات', 'عرض تحليلات السيرفر', 'التحليلات'),
('perm-analytics-export', 'تصدير التحليلات', 'تصدير البيانات والتقارير', 'التحليلات');
```

## 🛠️ أوامر الإدارة الكاملة

### 1. منح صلاحيات المدير الأعلى لحسابك
```sql
-- الصلاحيات الاعلى في النظام
UPDATE users SET 
    role = 'SuperAdmin',
    is_super_admin = TRUE 
WHERE discord_id = '651015003843067904';

-- منح جميع الصلاحيات
INSERT IGNORE INTO user_permissions (user_id, permission) 
SELECT id, 'SYSTEM_ADMIN' FROM users WHERE discord_id = '651015003843067904';

-- ليدر الموقع
INSERT IGNORE INTO user_permissions (user_id, permission)
SELECT id, 'Leader' FROM users
WHERE discord_id = '651015003843067904';
```

### 2. إنشاء مدير جديد
```sql
-- إنشاء مدير جديد
INSERT INTO users (id, discord_id, username, display_name, role) VALUES 
('admin-002', 'DISCORD_ID_HERE', 'NewAdmin', 'اسم المدير', 'Leader');

-- منح الصلاحيات
INSERT INTO user_permissions (user_id, permission) VALUES 
('admin-002', 'perm-users-view'),
('admin-002', 'perm-users-edit'),
('admin-002', 'perm-tickets-manage');
```

### 3. حظر مستخدم
```sql
-- حظر مستخدم
UPDATE users SET status = 'banned' WHERE id = 'USER_ID';

-- إضافة سجل في المخالفات
INSERT INTO violations (id, user_id, type, reason, issued_by) VALUES 
(UUID(), 'USER_ID', 'ban', 'سبب الحظر', 'YOUR_USER_ID');
```

### 4. عرض جميع البيانات
```sql
-- عرض جميع المستخدمين مع تفاصيلهم
SELECT 
    u.id,
    u.discord_id,
    u.username,
    u.display_name,
    u.role,
    u.status,
    u.registration_date,
    u.total_playtime,
    COALESCE(pt.cash, 0) as cash,
    COALESCE(pt.bank, 0) as bank
FROM users u
LEFT JOIN player_tracking pt ON u.id = pt.user_id
ORDER BY u.registration_date DESC;

-- عرض إحصائيات شاملة
SELECT 
    COUNT(*) as total_users,
    COUNT(CASE WHEN status = 'active' THEN 1 END) as active_users,
    COUNT(CASE WHEN status = 'banned' THEN 1 END) as banned_users,
    SUM(total_playtime) as total_playtime_minutes
FROM users;
```

## 🔒 إعدادات الأمان

### 1. إنشاء مستخدم قاعدة بيانات منفصل
```sql
-- إنشاء مستخدم لقاعدة البيانات
CREATE USER 'shining_admin'@'localhost' IDENTIFIED BY 'AboYsaq@1426';
GRANT ALL PRIVILEGES ON shining_db.* TO 'shining_admin'@'localhost';
FLUSH PRIVILEGES;
```

### 2. إعدادات النسخ الاحتياطي
```bash
@echo off
REM نسخ احتياطي يومي
set DATE=%DATE:~10,4%%DATE:~7,2%%DATE:~4,2%
mysqldump -u shining_admin -p shining_db > C:\ShiningBackup\backup_%DATE%.sql

REM نسخ احتياطي أسبوعي (يمكنك ضغط الملف يدوياً أو باستخدام برنامج خارجي)
REM لتغيير اسم الملف الأسبوعي، يمكنك إضافة كلمة weekly:
REM mysqldump -u shining_admin -p shining_db > C:\ShiningBackup\weekly_backup_%DATE%.sql
```

## 📊 استعلامات مفيدة للإدارة

### 1. أكثر اللاعبين نشاطاً
```sql
SELECT 
    u.display_name,
    u.total_playtime,
    pt.cash + pt.bank as total_money,
    pt.job
FROM users u
JOIN player_tracking pt ON u.id = pt.user_id
WHERE u.role = 'Player'
ORDER BY u.total_playtime DESC
LIMIT 10;
```

### 2. إحصائيات التذاكر
```sql
SELECT 
    category,
    COUNT(*) as total,
    COUNT(CASE WHEN status = 'resolved' THEN 1 END) as resolved,
    AVG(TIMESTAMPDIFF(HOUR, created_at, COALESCE(closed_at, NOW()))) as avg_resolution_hours
FROM tickets
GROUP BY category;
```

### 3. اللاعبون المتصلون حالياً
```sql
SELECT 
    u.display_name,
    pt.character_name,
    pt.job,
    pt.current_zone,
    pt.session_time
FROM users u
JOIN player_tracking pt ON u.id = pt.user_id
WHERE pt.is_online = TRUE
ORDER BY pt.session_time DESC;
```

## 🎛️ واجهة التحكم الكاملة

 نملك السيطرة الكاملة على:

✅ **إدارة المستخدمين**: إضافة، تعديل، حذف، حظر أي مستخدم
✅ **إدارة الأدوار**: إنشاء أدوار جديدة ومنح صلاحيات
✅ **قاعدة البيانات**: تحكم كامل في جميع البيانات
✅ **النظام**: تعديل أي جانب في النظام
✅ **التقارير**: إنشاء تقارير مخصصة
✅ **النسخ الاحتياطي**: حماية البيانات
✅ **الأمان**: مراقبة جميع الأنشطة

## 📞 معلومات التواصل

**النظام مُطور بواسطة**: Yasser Alquraishi
**Discord ID**: YOUR_DISCORD_ID (قم بتحديثه)
**تاريخ الإنشاء**: $(28-07-2025)

---
