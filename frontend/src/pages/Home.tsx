import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../services/api";
import styles from "./Home.module.css";

interface Avatar {
  id: number;
  photo_url: string;
  model_url: string | null;
  status: string;
}

export default function Home() {
  const navigate = useNavigate();
  const [avatars, setAvatars] = useState<Avatar[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getAvatars().then((d) => setAvatars(d as Avatar[])).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading-screen">Loading...</div>;

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1 className={styles.title}>My Avatars</h1>
      </header>

      {avatars.length === 0 ? (
        <div className={styles.empty}>
          <p className={styles.emptyText}>还没有数字人</p>
          <button className={styles.createBtn} onClick={() => navigate("/avatar/create")}>
            创建数字人
          </button>
        </div>
      ) : (
        <div className={styles.grid}>
          {avatars.map((a) => (
            <div key={a.id} className={styles.card} onClick={() => navigate(`/avatar/${a.id}`)}>
              <div className={styles.cardPreview}>
                {a.model_url ? <span>3D 预览</span> : <span className={styles.status}>{a.status}</span>}
              </div>
            </div>
          ))}
          <div className={styles.card} onClick={() => navigate("/avatar/create")}>
            <div className={styles.cardPreview} style={{ color: "var(--color-primary)", fontSize: 32 }}>+</div>
          </div>
        </div>
      )}
    </div>
  );
}
