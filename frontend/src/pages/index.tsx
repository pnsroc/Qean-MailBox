import { useState, useEffect } from "react";
import api, { setToken } from "../lib/api";
import { useRouter } from "next/router";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // 检查是否需要初始化管理员
  useEffect(() => {
    api.get("/auth/need-init").then(res => {
      if (res.data.need_init) {
        router.push("/init-admin");
      }
    });
  }, []);

  const login = async () => {
    const res = await api.post("/auth/login", { email, password });
    setToken(res.data.access_token);
    router.push("/mail");
  };

  return (
    <div style={{ padding: 40 }}>
      <h1>Qean-MailBox 登录</h1>

      <input
        placeholder="Email"
        value={email}
        onChange={e => setEmail(e.target.value)}
      /><br/>

      <input
        placeholder="Password"
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
      /><br/>

      <button onClick={login}>登录</button>
    </div>
  );
}
