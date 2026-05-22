import { useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./Login.module.css";

export default function Login() {
  const [phone, setPhone] = useState("");
  const [code, setCode] = useState("");
  const [codeSent, setCodeSent] = useState(false);
  const navigate = useNavigate();

  const sendCode = async () => {
    // TODO: call API
    setCodeSent(true);
  };

  const login = async () => {
    // TODO: call API
    navigate("/home");
  };

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>Digital Try-On</h1>
      <p className={styles.subtitle}>Create your 3D avatar and try on clothes</p>
      <div className={styles.form}>
        <input
          className={styles.input}
          type="tel"
          placeholder="Phone number"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
        />
        {codeSent && (
          <input
            className={styles.input}
            type="text"
            placeholder="Verification code"
            value={code}
            onChange={(e) => setCode(e.target.value)}
          />
        )}
        {!codeSent ? (
          <button className={styles.btn} onClick={sendCode} disabled={!phone}>
            Send Code
          </button>
        ) : (
          <button className={styles.btn} onClick={login} disabled={!code}>
            Login
          </button>
        )}
      </div>
    </div>
  );
}
