import { useEffect, useState } from "react";
import { api } from "../services/api";
import ModelViewer from "../components/ModelViewer";
import styles from "./TryOn.module.css";

interface Avatar { id: number; model_url: string | null; }
interface Garment { id: number; category: string; image_url: string; }

export default function TryOn() {
  const [avatars, setAvatars] = useState<Avatar[]>([]);
  const [garments, setGarments] = useState<Garment[]>([]);
  const [selectedAvatar, setSelectedAvatar] = useState<number | null>(null);
  const [selectedGarment, setSelectedGarment] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    api.getAvatars().then((d) => setAvatars(d as Avatar[]));
    api.getGarments().then((d) => setGarments(d as Garment[]));
  }, []);

  const handleTryOn = async () => {
    if (!selectedAvatar || !selectedGarment) return;
    setLoading(true);
    setError("");
    try {
      await api.tryOn(selectedAvatar, selectedGarment);
    } catch (e) {
      setError(e instanceof Error ? e.message : "试穿失败");
    }
    setLoading(false);
  };

  return (
    <div className={styles.page}>
      <div className={styles.viewer}>
        <ModelViewer />
        {loading && (
          <div className={styles.overlay}>
            <div className={styles.spinner} />
            <p>正在试穿...</p>
          </div>
        )}
      </div>

      <div className={styles.panel}>
        {error && <p className={styles.error}>{error}</p>}
        <select className={styles.select} value={selectedAvatar ?? ""}
          onChange={(e) => setSelectedAvatar(Number(e.target.value))}>
          <option value="">选择数字人</option>
          {avatars.map((a) => <option key={a.id} value={a.id}>数字人 #{a.id}</option>)}
        </select>
        <select className={styles.select} value={selectedGarment ?? ""}
          onChange={(e) => setSelectedGarment(Number(e.target.value))}>
          <option value="">选择服装</option>
          {garments.map((g) => <option key={g.id} value={g.id}>{g.category} #{g.id}</option>)}
        </select>
        <button className={styles.tryonBtn} onClick={handleTryOn}
          disabled={loading || !selectedAvatar || !selectedGarment}>
          {loading ? "处理中..." : "虚拟试穿"}
        </button>
      </div>
    </div>
  );
}
