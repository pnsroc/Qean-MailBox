import { useState } from "react";
import api from "../../lib/api";
import { useRouter } from "next/router";

export default function AddAccountPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [imapHost, setImapHost] = useState("");
  const [imapPort, setImapPort] = useState(993);
  const [imapSsl, setImapSsl] = useState(true);
  const [smtpHost, setSmtpHost] = useState("");
  const [smtpPort, setSmtpPort] = useState(465);
  const [smtpSsl, setSmtpSsl] = useState(true);
  const [testing, setTesting] = useState(false);
  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState("");
  const router = useRouter();

  const testConnection = async () => {
    setTesting(true);
    setMsg("");
    try {
      await api.post("/mail/test-connection", {
        email,
        password,
        imap_host: imapHost,
        imap_port: imapPort,
        imap_ssl: imapSsl,
        smtp_host: smtpHost,
        smtp_port: smtpPort,
        smtp_ssl: smtpSsl,
      });
      setMsg("连接成功，可以保存。");
    } catch (e: any) {
      setMsg(e?.response?.data?.detail || "连接失败");
    } finally {
      setTesting(false);
    }
  };

  const saveAccount = async () => {
    setSaving(true);
    setMsg("");
    try {
      await api.post("/mail/add-manual", {
        email,
        password,
        imap_host: imapHost,
        imap_port: imapPort,
        imap_ssl: imapSsl,
        smtp_host: smtpHost,
        smtp_port: smtpPort,
        smtp_ssl: smtpSsl,
      });
      router.push("/mail");
    } catch (e: any) {
      setMsg(e?.response?.data?.detail || "保存失败");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div style={{ padding: 24 }}>
      <h2>手动添加邮箱（IMAP/SMTP）</h2>
      <div>
        <div>邮箱地址</div>
        <input value={email} onChange={e => setEmail(e.target.value)} />
      </div>
      <div>
        <div>密码 / 授权码</div>
        <input
          type="password"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />
      </div>
      <hr />
      <div>
        <div>IMAP 服务器</div>
        <input value={imapHost} onChange={e => setImapHost(e.target.value)} />
      </div>
      <div>
        <div>IMAP 端口</div>
        <input
          type="number"
          value={imapPort}
          onChange={e => setImapPort(Number(e.target.value))}
        />
      </div>
      <div>
        <label>
          <input
            type="checkbox"
            checked={imapSsl}
            onChange={e => setImapSsl(e.target.checked)}
          />
          IMAP SSL
        </label>
      </div>
      <hr />
      <div>
        <div>SMTP 服务器</div>
        <input value={smtpHost} onChange={e => setSmtpHost(e.target.value)} />
      </div>
      <div>
        <div>SMTP 端口</div>
        <input
          type="number"
          value={smtpPort}
          onChange={e => setSmtpPort(Number(e.target.value))}
        />
      </div>
      <div>
        <label>
          <input
            type="checkbox"
            checked={smtpSsl}
            onChange={e => setSmtpSsl(e.target.checked)}
          />
          SMTP SSL
        </label>
      </div>
      <div style={{ marginTop: 16 }}>
        <button disabled={testing} onClick={testConnection}>
          测试连接
        </button>
        <button disabled={saving} onClick={saveAccount} style={{ marginLeft: 8 }}>
          保存
        </button>
      </div>
      {msg && <div style={{ marginTop: 12 }}>{msg}</div>}
    </div>
  );
}
