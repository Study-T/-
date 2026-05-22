import { Outlet, NavLink } from "react-router-dom";
import styles from "./Layout.module.css";

const tabs = [
  { to: "/home", label: "Home", icon: "🏠" },
  { to: "/avatar/create", label: "Create", icon: "➕" },
  { to: "/history", label: "History", icon: "📋" },
];

export default function Layout() {
  return (
    <div className={styles.wrapper}>
      <main className={styles.main}>
        <Outlet />
      </main>
      <nav className={styles.tabbar}>
        {tabs.map((tab) => (
          <NavLink
            key={tab.to}
            to={tab.to}
            className={({ isActive }) =>
              `${styles.tab} ${isActive ? styles.active : ""}`
            }
          >
            <span className={styles.icon}>{tab.icon}</span>
            <span className={styles.label}>{tab.label}</span>
          </NavLink>
        ))}
      </nav>
    </div>
  );
}
