import { useParams } from "react-router-dom";
import ModelViewer from "../components/ModelViewer";
import styles from "./AvatarDetail.module.css";

export default function AvatarDetail() {
  const { id } = useParams<{ id: string }>();

  return (
    <div className={styles.page}>
      <div className={styles.viewer}>
        <ModelViewer />
      </div>

      <div className={styles.actions}>
        <button className={styles.actionBtn}>Edit Parameters</button>
        <button className={`${styles.actionBtn} ${styles.primary}`}>
          Try On Clothes
        </button>
      </div>
    </div>
  );
}
