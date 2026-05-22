import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, setToken } from "../services/api";
import styles from "./Login.module.css";

export default function Login() {
  const [phone, setPhone] = useState("");
  const [code, setCode] = useState("");
  const [codeSent, setCodeSent] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const sendCode = async () => {
    setLoading(true);
    setError("");
    try {
      await api.sendCode(phone);
      setCodeSent(true);
    } catch (e) {
      setError(e instanceof Error ? e.message : "发送失败");
    }
    setLoading(false);
  };

  const login = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await api.login(phone, code);
      setToken(res.token);
      navigate("/home");
    } catch (e) {
      setError(e instanceof Error ? e.message : "登录失败");
    }
    setLoading(false);
  };

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>Digital Try-On</h1>
      <p className={styles.subtitle}>Create your 3D avatar and try on clothes</p>
      <div className={styles.form}>
        <input className={styles.input} type="tel" placeholder="手机号"
          value={phone} onChange={(e) => setPhone(e.target.value)} />
        {codeSent && (
          <input className={styles.input} type="text" placeholder="验证码"
            value={code} onChange={(e) => setCode(e.target.value)} />
        )}
        {error && <p className={styles.error}>{error}</p>}
        {!codeSent ? (
          <button className={styles.btn} onClick={sendCode} disabled={!phone || loading}>
            {loading ? "发送中..." : "发送验证码"}
          </button>
        ) : (
          <button className={styles.btn} onClick={login} disabled={!code || loading}>
            {loading ? "登录中..." : "登录"}
          </button>
        )}
      </div>
    </div>
  );
}
