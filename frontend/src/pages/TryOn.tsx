import { useParams } from "react-router-dom";
import { useState } from "react";
import ModelViewer from "../components/ModelViewer";
import styles from "./TryOn.module.css";

export default function TryOn() {
  const { garmentId } = useParams<{ garmentId: string }>();
  const [loading, setLoading] = useState(false);
  const [resultUrl, setResultUrl] = useState<string | null>(null);

  const handleTryOn = async () => {
    setLoading(true);
    // TODO: call FASHN VTON API
    setTimeout(() => setLoading(false), 5000);
  };

  return (
    <div className={styles.page}>
      <div className={styles.viewer}>
        <ModelViewer modelUrl={resultUrl ?? undefined} />
        {loading && (
          <div className={styles.overlay}>
            <div className={styles.spinner} />
            <p>Trying on...</p>
          </div>
        )}
      </div>

      <div className={styles.panel}>
        <h2 className={styles.garmentTitle}>Garment #{garmentId}</h2>
        <button
          className={styles.tryonBtn}
          onClick={handleTryOn}
          disabled={loading}
        >
          {loading ? "Processing..." : "Try On"}
        </button>
      </div>
    </div>
  );
}
