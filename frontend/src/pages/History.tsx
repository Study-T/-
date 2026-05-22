import styles from "./History.module.css";

export default function History() {
  return (
    <div className={styles.page}>
      <h1 className={styles.title}>Try-On History</h1>
      <p className={styles.empty}>No history yet. Try on some clothes!</p>
    </div>
  );
}
