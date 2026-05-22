import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { api } from "../services/api";
import ModelViewer from "../components/ModelViewer";
import styles from "./AvatarDetail.module.css";

interface Avatar {
  id: number;
  model_url: string | null;
  status: string;
  smplx_params: Record<string, number> | null;
}

export default function AvatarDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [avatar, setAvatar] = useState<Avatar | null>(null);

  useEffect(() => {
    if (id) api.getAvatar(Number(id)).then((d) => setAvatar(d as Avatar));
  }, [id]);

  if (!avatar) return <div className="loading-screen">Loading...</div>;

  return (
    <div className={styles.page}>
      <div className={styles.viewer}>
        <ModelViewer modelUrl={avatar.model_url ?? undefined} />
      </div>
      <div className={styles.actions}>
        <button className={styles.actionBtn} onClick={() => navigate(`/tryon`)}>
          试穿衣服
        </button>
        <button className={`${styles.actionBtn} ${styles.secondary}`}>
          编辑参数
        </button>
      </div>
    </div>
  );
}
