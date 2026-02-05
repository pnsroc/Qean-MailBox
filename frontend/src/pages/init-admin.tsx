import { useState, useEffect } from "react";
import api from "../lib/api";
import { useRouter } from "next/router";

export default function InitAdminPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // 如果管理员已存在，禁止访问
  useEffect(() => {
    api.get("/auth/need-init").then(res => {
      if (!res.data.need_init) {
        router.push("/");
      }
    });
  }, []);

  const submit = async () => {
    await api.post("/auth/init-admin", { email, password });
    alert("管理员初始化成功，请登录");
    router.push("/");
  };

  return (
    <div style={{ padding: 40 }}>
      <h1>初始化管理员账号</h1>

      <input
        placeholder="管理员邮箱"
        value={email}
        onChange={e => setEmail(e.target.value)}
      /><br/>

      <input
        placeholder="管理员密码"
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
      /><br/>

      <button onClick={submit}>保存管理员账号</button>
    </div>
  );
}
