import { useEffect, useState } from 'react';
import { Save, Eye } from 'lucide-react';
import { adminApi } from '@dfc/shared';

type BrandSettings = { app_name: string; logo_url: string; accent_color: string; [key: string]: unknown };

const defaultBrand: BrandSettings = { app_name: '', logo_url: '', accent_color: '#24C4F1' };

export default function AdminBrand() {
  const [brand, setBrand] = useState<BrandSettings>(defaultBrand);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [toast, setToast] = useState('');

  useEffect(() => {
    (async () => {
      setLoading(true);
      try {
        const data = await adminApi.getBrand();
        setBrand({ ...defaultBrand, ...data });
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const handleChange = (key: keyof BrandSettings, value: string) => {
    setBrand((prev) => ({ ...prev, [key]: value }));
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await adminApi.saveBrand(brand);
      setToast('Сохранено');
      setTimeout(() => setToast(''), 2500);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div style={{ padding: 16, maxWidth: 'var(--max-w)', margin: '0 auto' }}>
        <h1 className="page-title" style={{ marginBottom: 12 }}>Бренд</h1>
        <div className="loading"><div className="spinner" /><span>Загрузка…</span></div>
      </div>
    );
  }

  return (
    <div style={{ padding: 16, maxWidth: 'var(--max-w)', margin: '0 auto' }}>
      <h1 className="page-title" style={{ marginBottom: 16 }}>Бренд</h1>

      {/* Form */}
      <div className="card" style={{ marginBottom: 14, display: 'flex', flexDirection: 'column', gap: 14 }}>
        <label style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
          <span style={{ fontSize: '0.84rem', color: 'var(--text2)' }}>Название приложения</span>
          <input className="input" value={brand.app_name} onChange={(e) => handleChange('app_name', e.target.value)} placeholder="My App" />
        </label>

        <label style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
          <span style={{ fontSize: '0.84rem', color: 'var(--text2)' }}>URL логотипа</span>
          <input className="input" value={brand.logo_url} onChange={(e) => handleChange('logo_url', e.target.value)} placeholder="https://…" />
        </label>

        <label style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
          <span style={{ fontSize: '0.84rem', color: 'var(--text2)' }}>Акцентный цвет</span>
          <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
            <input className="input" value={brand.accent_color} onChange={(e) => handleChange('accent_color', e.target.value)} style={{ flex: 1 }} />
            <div style={{ width: 36, height: 36, borderRadius: 'var(--r-sm)', background: brand.accent_color, border: '1px solid var(--border)', flexShrink: 0 }} />
          </div>
        </label>

        <button className="btn btn-primary btn-full" onClick={handleSave} disabled={saving} style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6 }}>
          <Save size={16} /> {saving ? 'Сохранение…' : 'Сохранить'}
        </button>
      </div>

      {/* Preview */}
      <div className="card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 10 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6, color: 'var(--text2)', fontSize: '0.84rem' }}>
          <Eye size={15} /> Предпросмотр
        </div>
        <div style={{ width: '100%', background: 'var(--bg)', border: '1px solid var(--border)', borderRadius: 'var(--r)', padding: 16, display: 'flex', alignItems: 'center', gap: 12 }}>
          {brand.logo_url ? (
            <img src={brand.logo_url} alt="logo" style={{ width: 40, height: 40, borderRadius: 'var(--r-sm)', objectFit: 'cover' }} />
          ) : (
            <div style={{ width: 40, height: 40, borderRadius: 'var(--r-sm)', background: brand.accent_color, opacity: 0.3 }} />
          )}
          <span style={{ fontWeight: 600, fontSize: '1.05rem', color: brand.accent_color || 'var(--text)' }}>
            {brand.app_name || 'App Name'}
          </span>
        </div>
      </div>

      {/* Toast */}
      {toast && (
        <div className="animate-fade" style={{ position: 'fixed', bottom: 24, left: '50%', transform: 'translateX(-50%)', background: 'var(--green)', color: '#fff', padding: '8px 20px', borderRadius: 'var(--r-pill)', fontSize: '0.88rem', fontWeight: 600, zIndex: 100 }}>
          {toast}
        </div>
      )}
    </div>
  );
}
