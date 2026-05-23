import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { api } from "../services/api";
import ModelViewer from "../components/ModelViewer";
import styles from "./AvatarEdit.module.css";

interface Avatar {
  id: number;
  model_url: string | null;
  smplx_params: Record<string, number> | null;
}

const SLIDERS: { key: string; label: string; min: number; max: number; step: number }[] = [
  { key: "height", label: "身高 (m)", min: 1.0, max: 2.5, step: 0.01 },
  { key: "weight", label: "体重 (kg)", min: 30, max: 200, step: 1 },
  { key: "shoulder_width", label: "肩宽 (m)", min: 0.3, max: 0.6, step: 0.01 },
  { key: "chest", label: "胸围 (m)", min: 0.5, max: 1.5, step: 0.01 },
  { key: "waist", label: "腰围 (m)", min: 0.4, max: 1.5, step: 0.01 },
  { key: "hip", label: "臀围 (m)", min: 0.5, max: 1.5, step: 0.01 },
  { key: "leg_length", label: "腿长 (m)", min: 0.5, max: 1.2, step: 0.01 },
];

export default function AvatarEdit() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [avatar, setAvatar] = useState<Avatar | null>(null);
  const [params, setParams] = useState<Record<string, number>>({});
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    if (id) api.getAvatar(Number(id)).then((d) => {
      const a = d as Avatar;
      setAvatar(a);
      setParams(a.smplx_params ?? {});
    });
  }, [id]);

  const handleChange = (key: string, value: number) => {
    setParams((prev) => ({ ...prev, [key]: value }));
    setSaved(false);
  };

  const handleSave = async () => {
    if (!id) return;
    try {
      await api.updateAvatarParams(Number(id), params);
      setSaved(true);
    } catch {}
  };

  if (!avatar) return <div className="loading-screen">Loading...</div>;

  return (
    <div className={styles.page}>
      <div className={styles.viewer}>
        <ModelViewer modelUrl={avatar.model_url ?? undefined} />
      </div>
      <div className={styles.panel}>
        <h2 className={styles.title}>调整体型参数</h2>
        <div className={styles.sliders}>
          {SLIDERS.map((s) => (
            <div key={s.key} className={styles.sliderRow}>
              <label>{s.label}</label>
              <div className={styles.sliderInput}>
                <input type="range" min={s.min} max={s.max} step={s.step}
                  value={params[s.key] ?? s.min}
                  onChange={(e) => handleChange(s.key, Number(e.target.value))} />
                <span className={styles.value}>{params[s.key]?.toFixed(2) ?? "-"}</span>
              </div>
            </div>
          ))}
        </div>
        <button className={styles.saveBtn} onClick={handleSave}>
          {saved ? "已保存" : "保存参数"}
        </button>
        <button className={styles.backBtn} onClick={() => navigate(`/avatar/${id}`)}>
          返回查看
        </button>
      </div>
    </div>
  );
}
