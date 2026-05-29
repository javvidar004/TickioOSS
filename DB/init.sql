-- TickioOSS — Initial schema seed
-- FastAPI + SQLAlchemy create tables automatically; this file seeds the admin user.

-- Insert default admin (password: admin123 — change immediately in production!)
-- Password hash generated with bcrypt rounds=12 for "admin123"
INSERT INTO users (username, email, password_hash, role, is_active, created_at)
VALUES (
    'admin',
    'admin@tickio.local',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TiGPB.mKZKnDHfyOEMhm8y3gvmsi',
    'admin',
    true,
    NOW()
) ON CONFLICT (username) DO NOTHING;
