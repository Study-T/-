import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../services/api";
import styles from "./AvatarCreate.module.css";

export default function AvatarCreate() {
  const navigate = useNavigate();
  const [step, setStep] = useState<"upload" | "generating" | "done">("upload");
  const [preview, setPreview] = useState<string | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState("");

  const handleSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (!f) return;
    setFile(f);
    setPreview(URL.createObjectURL(f));
    setError("");
  };

  const handleGenerate = async () => {
    if (!file) return;
    setStep("generating");
    setError("");
    try {
      const { url } = await api.upload(file);
      await api.createAvatar(url);
      setStep("done");
    } catch (e) {
      setError(e instanceof Error ? e.message : "生成失败");
      setStep("upload");
    }
  };

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>创建数字人</h1>
      {error && <p className={styles.error}>{error}</p>}

      {step === "upload" && (
        <div className={styles.uploadArea}>
          <label className={styles.uploadLabel}>
            {preview ? (
              <img src={preview} alt="preview" className={styles.preview} />
            ) : (
              <div className={styles.placeholder}>
                <span className={styles.plus}>+</span>
                <span>上传全身正面照片</span>
              </div>
            )}
            <input type="file" accept="image/*" capture="user" onChange={handleSelect} hidden />
          </label>
          <button className={styles.genBtn} onClick={handleGenerate} disabled={!file}>
            生成 3D 数字人
          </button>
        </div>
      )}

      {step === "generating" && (
        <div className={styles.generating}>
          <div className={styles.spinner} />
          <p>正在生成你的数字人...</p>
          <p className={styles.hint}>通常需要约 5 秒</p>
        </div>
      )}

      {step === "done" && (
        <div className={styles.done}>
          <p className={styles.success}>数字人创建成功!</p>
          <button className={styles.genBtn} onClick={() => navigate("/home")}>
            查看我的数字人
          </button>
        </div>
      )}
    </div>
  );
}
