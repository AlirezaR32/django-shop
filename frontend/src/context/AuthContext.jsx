import { createContext, useContext, useEffect, useState } from "react";
import { authApi } from "../services/api";

const AuthCtx = createContext(null);
export const useAuth = () => useContext(AuthCtx);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const t = localStorage.getItem("access");
    const u = localStorage.getItem("username");
    return t ? { token: t, username: u || "کاربر" } : null;
  });
  const [loading, setLoading] = useState(false);

  const login = async (username, password) => {
    setLoading(true);
    try {
      const data = await authApi.login(username, password);
      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);
      localStorage.setItem("username", username);
      setUser({ token: data.access, username });
      return true;
    } finally {
      setLoading(false);
    }
  };

  const register = async (username, password) => {
    await authApi.register(username, password);
    // auto login
    return login(username, password);
  };

  const logout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("username");
    setUser(null);
  };

  // check token validity on mount - try to fetch cart?
  useEffect(() => {
    const t = localStorage.getItem("access");
    if (t && !user) {
      const u = localStorage.getItem("username") || "کاربر";
      setUser({ token: t, username: u });
    }
  }, []);

  return (
    <AuthCtx.Provider value={{ user, login, register, logout, loading, isAuthed: !!user }}>
      {children}
    </AuthCtx.Provider>
  );
}
