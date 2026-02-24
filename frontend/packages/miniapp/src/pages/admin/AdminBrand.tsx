import { useEffect, useState } from 'react';
import { adminApi } from '@dfc/shared';
import type { BrandSettings } from '@dfc/shared';
import { Palette, Save } from 'lucide-react';
import toast from 'react-hot-toast';

export default function AdminBrand() {
  const [brand, setBrand] = useState<BrandSettings>({
    app_name: '',
    logo_url: '',
    accent_color: '#00BCD4',
  });
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    adminApi.getBrand().then(({ data }) => setBrand(data)).catch(() => {});
  }, []);

  const handleSave = async () => {
    setSaving(true);
    try {
      await adminApi.saveBrand(brand);
      toast.success('Бренд сохранён');
    } catch { toast.error('Ошибка'); } finally { setSaving(false); }
  };

  return (
    <div className="admin-form">
      <div className="card">
        <label className="admin-form-label">Название приложения</label>
        <input
          className="input"
          value={brand.app_name}
          onChange={(e) => setBrand({ ...brand, app_name: e.target.value })}
          placeholder="My VPN Shop"
        />

        <label className="admin-form-label" style={{ marginTop: 12 }}>URL логотипа</label>
        <input
          className="input"
          value={brand.logo_url}
          onChange={(e) => setBrand({ ...brand, logo_url: e.target.value })}
          placeholder="https://..."
        />

        {brand.logo_url && (
          <div style={{ marginTop: 8, textAlign: 'center' }}>
            <img
              src={brand.logo_url}
              alt="Logo preview"
              style={{
                maxWidth: 120,
                maxHeight: 120,
                borderRadius: 12,
                border: '1px solid var(--border)',
              }}
            />
          </div>
        )}

        <label className="admin-form-label" style={{ marginTop: 12 }}>
          <Palette size={14} /> Акцентный цвет
        </label>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <input
            type="color"
            value={brand.accent_color}
            onChange={(e) => setBrand({ ...brand, accent_color: e.target.value })}
            style={{ width: 40, height: 40, border: 'none', background: 'none', cursor: 'pointer' }}
          />
          <input
            className="input"
            value={brand.accent_color}
            onChange={(e) => setBrand({ ...brand, accent_color: e.target.value })}
            style={{ flex: 1 }}
          />
        </div>
      </div>

      <button className="btn btn-primary btn-full btn-glossy" disabled={saving} onClick={handleSave}>
        <Save size={16} /> {saving ? 'Сохранение...' : 'Сохранить'}
      </button>
    </div>
  );
}
