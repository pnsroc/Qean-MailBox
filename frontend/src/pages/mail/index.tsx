import { useEffect, useState } from "react";
import api from "../../lib/api";
import { useRouter } from "next/router";

interface MailItem {
  account_id: string;
  account_email: string;
  msg_id: number;
  subject: string;
  from: string;
  date: string | null;
  is_read: boolean;
  starred: boolean;
  snippet: string;
}

export default function UnifiedInboxPage() {
  const [mails, setMails] = useState<MailItem[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const loadInbox = async () => {
    setLoading(true);
    const res = await api.get("/mail/unified/inbox");
    setMails(res.data.results);
    setLoading(false);
  };

  const doSearch = async () => {
    if (!search) return loadInbox();
    const res = await api.get("/mail/unified/search", { params: { q: search } });
    setMails(res.data.results);
  };

  useEffect(() => {
    loadInbox();
  }, []);

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <div style={{ width: 260, borderRight: "1px solid #eee", padding: 16 }}>
        <h3>统一收件箱</h3>
        <button onClick={() => router.push("/mail/add-account")}>
          添加邮箱
        </button>
      </div>
      <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
        <div style={{ padding: 8, borderBottom: "1px solid #eee" }}>
          <input
            style={{ width: "60%" }}
            placeholder="搜索 / from: / subject: / 等"
            value={search}
            onChange={e => setSearch(e.target.value)}
            onKeyDown={e => e.key === "Enter" && doSearch()}
          />
        </div>
        <div style={{ flex: 1, overflow: "auto" }}>
          {loading && <div>加载中...</div>}
          {!loading &&
            mails.map(m => (
              <div
                key={`${m.account_id}-${m.msg_id}`}
                style={{
                  padding: 12,
                  borderBottom: "1px solid #f0f0f0",
                  cursor: "pointer",
                  background: m.is_read ? "#fff" : "#f7f9ff",
                }}
                onClick={() =>
                  router.push(`/mail/${m.account_id}?open=${m.msg_id}`)
                }
              >
                <div style={{ fontWeight: m.is_read ? 400 : 600 }}>
                  {m.subject}
                </div>
                <div style={{ fontSize: 12, color: "#666" }}>
                  {m.from} · {m.date}
                </div>
                <div style={{ fontSize: 12, color: "#999", marginTop: 4 }}>
                  {m.snippet}
                </div>
                <div style={{ fontSize: 12, color: "#888", marginTop: 4 }}>
                  来自：{m.account_email}
                </div>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
}
