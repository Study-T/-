import { useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./AvatarCreate.module.css";

export default function AvatarCreate() {
  const navigate = useNavigate();
  const [step, setStep] = useState<"upload" | "generating" | "done">("upload");
  const [preview, setPreview] = useState<string | null>(null);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setPreview(URL.createObjectURL(file));
  };

  const handleGenerate = async () => {
    setStep("generating");
    // TODO: upload photo → call LHM API → poll status
    setTimeout(() => {
      setStep("done");
    }, 3000);
  };

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>Create Avatar</h1>

      {step === "upload" && (
        <div className={styles.uploadArea}>
          <label className={styles.uploadLabel}>
            {preview ? (
              <img src={preview} alt="preview" className={styles.preview} />
            ) : (
              <div className={styles.placeholder}>
                <span className={styles.plus}>+</span>
                <span>Upload a full-body photo</span>
              </div>
            )}
            <input
              type="file"
              accept="image/*"
              capture="user"
              onChange={handleUpload}
              hidden
            />
          </label>
          <button
            className={styles.genBtn}
            onClick={handleGenerate}
            disabled={!preview}
          >
            Generate 3D Avatar
          </button>
        </div>
      )}

      {step === "generating" && (
        <div className={styles.generating}>
          <div className={styles.spinner} />
          <p>Generating your digital human...</p>
          <p className={styles.hint}>This usually takes about 5 seconds</p>
        </div>
      )}

      {step === "done" && (
        <div className={styles.done}>
          <p className={styles.success}>Avatar created!</p>
          <button className={styles.genBtn} onClick={() => navigate("/home")}>
            View My Avatar
          </button>
        </div>
      )}
    </div>
  );
}
