import { useEffect, useState } from 'react';
import { Save, Eye } from 'lucide-react';
import { adminApi } from '@dfc/shared';

type BrandForm = { name: string; logo: string; slogan: string };

const defaultBrand: BrandForm = { name: '', logo: '', slogan: '' };

export default function AdminBrand() {
  const [brand, setBrand] = useState<BrandForm>(defaultBrand);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [toast, setToast] = useState('');

  useEffect(() => {
    (async () => {
      setLoading(true);
      try {
        const { data } = await adminApi.getBrand();
        setBrand({ name: data.name || '', logo: data.logo || '', slogan: data.slogan || '' });
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const handleChange = (key: keyof BrandForm, value: string) => {
    setBrand((prev) => ({ ...prev, [key]: value }));
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await adminApi.saveBrand(brand as any);
      setToast('Сохранено');
      setTimeout(() => setToast(''), 2500);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="empty-state"><div className="spinner" /></div>
    );
  }

  return (
    <div>
      {/* Form */}
      <div className="card" style={{ marginBottom: 14, display: 'flex', flexDirection: 'column', gap: 14 }}>
        <label style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
          <span className="form-label">Название</span>
          <input className="input" value={brand.name} onChange={(e) => handleChange('name', e.target.value)} placeholder="My VPN" />
        </label>

        <label style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
          <span className="form-label">Логотип (эмодзи или текст)</span>
          <input className="input" value={brand.logo} onChange={(e) => handleChange('logo', e.target.value)} placeholder="🔐" />
        </label>

        <label style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
          <span className="form-label">Слоган</span>
          <input className="input" value={brand.slogan} onChange={(e) => handleChange('slogan', e.target.value)} placeholder="Ваш надёжный VPN" />
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
          <div style={{
            width: 40, height: 40, borderRadius: 10,
            background: 'linear-gradient(135deg, var(--cyan), #1AA3CC)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '1.3rem', flexShrink: 0,
          }}>
            {brand.logo || '🔐'}
          </div>
          <div>
            <div style={{ fontWeight: 700, fontSize: '1rem' }}>{brand.name || 'VPN Shop'}</div>
            {brand.slogan && <div style={{ color: 'var(--text2)', fontSize: '.75rem' }}>{brand.slogan}</div>}
          </div>
        </div>
      </div>

      {/* Toast */}
      {toast && (
        <div className="animate-fade" style={{ position: 'fixed', bottom: 'calc(var(--nav-h) + var(--safe-bottom) + 16px)', left: '50%', transform: 'translateX(-50%)', background: 'var(--green)', color: '#fff', padding: '8px 20px', borderRadius: 'var(--r-pill)', fontSize: '0.88rem', fontWeight: 600, zIndex: 100 }}>
          {toast}
        </div>
      )}
    </div>
  );
}
