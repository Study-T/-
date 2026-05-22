import { useEffect, useState } from "react";
import { api } from "../services/api";
import styles from "./History.module.css";

interface TryOnTask {
  id: number;
  avatar_id: number;
  garment_id: number;
  result_url: string | null;
  status: string;
  created_at: string;
}

export default function History() {
  const [tasks, setTasks] = useState<TryOnTask[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getTryOnHistory().then((d) => setTasks(d as TryOnTask[])).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading-screen">Loading...</div>;

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>试穿历史</h1>
      {tasks.length === 0 ? (
        <p className={styles.empty}>还没有试穿记录</p>
      ) : (
        <div className={styles.list}>
          {tasks.map((t) => (
            <div key={t.id} className={styles.item}>
              <span>数字人 #{t.avatar_id} × 服装 #{t.garment_id}</span>
              <span className={`${styles.badge} ${styles[t.status]}`}>{t.status}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
