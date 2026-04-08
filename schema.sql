-- جدول المهام
CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    local_time TEXT,
    tz_id TEXT,
    action TEXT,
    publisher TEXT,
    status TEXT,
    priority TEXT DEFAULT 'Medium'
);

-- جدول التدقيق (Audit Log)
CREATE TABLE IF NOT EXISTS audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT,
    job_id TEXT,
    timestamp TEXT
);

-- جدول محاولات التشغيل
CREATE TABLE IF NOT EXISTS job_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id TEXT,
    status TEXT,
    attempt INTEGER,
    timestamp TEXT
);

-- جدول وضعيات المشروع (presence, absence, death)
CREATE TABLE IF NOT EXISTS modes_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mode TEXT,
    timestamp TEXT
);

-- جدول تحويلات الوقت
CREATE TABLE IF NOT EXISTS time_conversions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT,
    input_time TEXT,
    tz_id TEXT,
    result TEXT,
    timestamp TEXT
);

-- جدول حدود النشر (Rate Limits)
CREATE TABLE IF NOT EXISTS rate_limits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    publisher TEXT,
    timestamp TEXT
);

-- جدول التفاعل (Engagement Logs) لكل المنصات
CREATE TABLE IF NOT EXISTS engagement_logs (
    job_id TEXT,
    platform TEXT,
    timestamp TEXT,
    views INTEGER,
    likes INTEGER,
    comments INTEGER,
    shares INTEGER,
    reposts INTEGER
);