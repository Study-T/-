import { useNavigate } from "react-router-dom";
import styles from "./Home.module.css";

interface Avatar {
  id: number;
  photo_url: string;
  model_url: string | null;
  status: string;
}

export default function Home() {
  const navigate = useNavigate();
  const avatars: Avatar[] = []; // TODO: fetch from API

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1 className={styles.title}>My Avatars</h1>
      </header>

      {avatars.length === 0 ? (
        <div className={styles.empty}>
          <p className={styles.emptyText}>No avatar yet</p>
          <button
            className={styles.createBtn}
            onClick={() => navigate("/avatar/create")}
          >
            Create Your Digital Human
          </button>
        </div>
      ) : (
        <div className={styles.grid}>
          {avatars.map((a) => (
            <div
              key={a.id}
              className={styles.card}
              onClick={() => navigate(`/avatar/${a.id}`)}
            >
              <div className={styles.cardPreview}>
                {a.model_url ? (
                  <span>3D Preview</span>
                ) : (
                  <span className={styles.status}>{a.status}</span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
