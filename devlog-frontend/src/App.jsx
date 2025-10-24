import React, { useEffect, useState } from "react";

/**
 * DevLog Frontend — GitHub‑style UI
 * - Tailwind v4 compatible (uses @tailwindcss/postcss in postcss.config.js)
 * - Dark header, repo list feel, action bar, side nav
 * - Login → token → CRUD Projects
 * - LocalStorage for token + backend URL
 */

const DEFAULT_BASE_URL = "http://localhost:8000";

// ---------- helpers ----------
const cx = (...a) => a.filter(Boolean).join(" ");

function Button({ children, onClick, kind = "primary", size = "md", disabled, className = "" }) {
  const sizes = {
    sm: "px-2 py-1 text-xs",
    md: "px-3 py-1.5 text-sm",
    lg: "px-4 py-2 text-sm",
  }[size];
  const styles =
    kind === "danger"
      ? "bg-red-600 hover:bg-red-700 text-white border border-red-700"
      : kind === "ghost"
      ? "bg-transparent hover:bg-zinc-100/70 dark:hover:bg-zinc-800 border border-zinc-300 dark:border-zinc-700 text-zinc-800 dark:text-zinc-100"
      : "bg-green-600 hover:bg-green-700 text-white border border-green-700"; // GitHub primary vibe
  return (
    <button onClick={onClick} disabled={disabled} className={cx("rounded-md inline-flex items-center gap-2 transition disabled:opacity-50", sizes, styles, className)}>
      {children}
    </button>
  );
}

function TextInput({ label, value, onChange, type = "text", placeholder, className = "", autoFocus }) {
  return (
    <label className={cx("block", className)}>
      {label && <div className="text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">{label}</div>}
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        autoFocus={autoFocus}
        className="w-full rounded-md border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-900 px-3 py-1.5 text-sm outline-none focus:ring-2 focus:ring-blue-500"
      />
    </label>
  );
}

function Card({ children, className = "" }) {
  return (
    <div className={cx("border border-zinc-200 dark:border-zinc-800 rounded-md bg-white dark:bg-zinc-900", className)}>{children}</div>
  );
}

// ---------- API helper ----------
async function callApi(baseUrl, token, path, { method = "GET", body } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  const res = await fetch(`${baseUrl}${path}`, { method, headers, body: body ? JSON.stringify(body) : undefined });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  const ct = res.headers.get("content-type") || "";
  return ct.includes("json") ? res.json() : res.text();
}

export default function App() {
  const [baseUrl, setBaseUrl] = useState(() => localStorage.getItem("devlog_base") || DEFAULT_BASE_URL);
  const [token, setToken] = useState(() => localStorage.getItem("devlog_token") || "");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [projects, setProjects] = useState([]);
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("");

  useEffect(() => localStorage.setItem("devlog_base", baseUrl), [baseUrl]);
  useEffect(() => localStorage.setItem("devlog_token", token), [token]);

  async function login() {
    setStatus("");
    try {
      const body = new URLSearchParams();
      body.set("username", username);
      body.set("password", password);
      const res = await fetch(`${baseUrl}/auth/token`, { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body });
      if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
      const data = await res.json();
      setToken(data.access_token);
      setUsername(""); setPassword("");
      await loadProjects();
    } catch (e) {
      setStatus(`Login failed: ${e.message}`);
    }
  }

  async function loadProjects(q = "") {
    if (!token) return;
    try {
      const qs = q ? `?q=${encodeURIComponent(q)}` : "";
      const data = await callApi(baseUrl, token, `/projects${qs}`);
      setProjects(data);
    } catch (e) { setStatus(`Load failed: ${e.message}`); }
  }

  // create / edit / delete
  const [newTitle, setNewTitle] = useState("");
  const [newDesc, setNewDesc] = useState("");
  async function createProject() {
    try {
      await callApi(baseUrl, token, "/projects/", { method: "POST", body: { title: newTitle, description: newDesc } });
      setNewTitle(""); setNewDesc("");
      await loadProjects(search);
      setStatus("Project created.");
    } catch (e) { setStatus(`Create failed: ${e.message}`); }
  }

  const [editingId, setEditingId] = useState(null);
  const [editTitle, setEditTitle] = useState("");
  const [editDesc, setEditDesc] = useState("");
  function startEdit(p) { setEditingId(p.id); setEditTitle(p.title || ""); setEditDesc(p.description || ""); }
  async function saveEdit() {
    try {
      await callApi(baseUrl, token, `/projects/${editingId}`, { method: "PUT", body: { title: editTitle, description: editDesc } });
      setEditingId(null);
      await loadProjects(search);
      setStatus("Project updated.");
    } catch (e) { setStatus(`Update failed: ${e.message}`); }
  }
  async function del(id) {
    if (!confirm("Delete this project?")) return;
    try { await callApi(baseUrl, token, `/projects/${id}`, { method: "DELETE" }); await loadProjects(search); setStatus("Project deleted."); }
    catch (e) { setStatus(`Delete failed: ${e.message}`); }
  }

  useEffect(() => { if (token) loadProjects(); }, [token]);

  function logout() { setToken(""); setProjects([]); }

  // ---------- layout ----------
  return (
    <div className="min-h-screen bg-zinc-100 dark:bg-zinc-950 text-zinc-900 dark:text-zinc-100">
      {/* top nav like GitHub */}
      <header className="bg-zinc-900 text-zinc-100">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center gap-4">
          <div className="font-bold text-lg"> DevLog</div>
          <input
            className="hidden md:block flex-1 bg-zinc-800 border border-zinc-700 rounded-md px-3 py-1.5 text-sm placeholder:text-zinc-400"
            placeholder="Search projects…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && loadProjects(search)}
          />
          <div className="ml-auto flex items-center gap-2">
            <input
              className="w-[240px] bg-zinc-800 border border-zinc-700 rounded-md px-3 py-1.5 text-xs"
              value={baseUrl}
              onChange={(e) => setBaseUrl(e.target.value)}
              placeholder="http://localhost:8000"
              title="Backend URL"
            />
            {token ? (
              <Button kind="ghost" size="sm" onClick={logout}>Sign out</Button>
            ) : null}
          </div>
        </div>
      </header>

      {/* content */}
      <div className="max-w-6xl mx-auto px-4 py-6 grid grid-cols-12 gap-6">
        {/* sidebar like GitHub */}
        <aside className="hidden md:block col-span-3">
          <Card>
            <div className="p-4 border-b border-zinc-200 dark:border-zinc-800 font-semibold">Navigation</div>
            <nav className="p-2 text-sm">
              <a className="block px-3 py-2 rounded hover:bg-zinc-100 dark:hover:bg-zinc-800" href="#">Overview</a>
              <a className="block px-3 py-2 rounded hover:bg-zinc-100 dark:hover:bg-zinc-800" href="#">Projects</a>
              <a className="block px-3 py-2 rounded hover:bg-zinc-100 dark:hover:bg-zinc-800" href="#">Logs</a>
              <a className="block px-3 py-2 rounded hover:bg-zinc-100 dark:hover:bg-zinc-800" href="#">Settings</a>
            </nav>
          </Card>
        </aside>

        {/* main */}
        <main className="col-span-12 md:col-span-9 space-y-6">
          {!token ? (
            <Card>
              <div className="p-4 border-b border-zinc-200 dark:border-zinc-800 font-semibold">Sign in</div>
              <div className="p-4 grid sm:grid-cols-3 gap-3">
                <TextInput label="Username" value={username} onChange={setUsername} autoFocus />
                <TextInput label="Password" type="password" value={password} onChange={setPassword} />
                <div className="flex items-end"><Button onClick={login} disabled={!username || !password}>Sign in</Button></div>
              </div>
              {status && <div className="px-4 pb-4 text-sm text-red-600">{status}</div>}
            </Card>
          ) : (
            <>
              {/* action bar like GitHub repo new */}
              <Card>
                <div className="p-4 flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
                  <div className="w-full md:max-w-md grid grid-cols-1 gap-3">
                    <TextInput label="New project name" value={newTitle} onChange={setNewTitle} placeholder="awesome-project" />
                    <TextInput label="Description" value={newDesc} onChange={setNewDesc} placeholder="Optional description" />
                  </div>
                  <div className="flex gap-2">
                    <Button onClick={createProject} disabled={!newTitle}>Create project</Button>
                    <Button kind="ghost" onClick={() => loadProjects(search)}>Refresh</Button>
                  </div>
                </div>
              </Card>

              {/* repo list style */}
              <Card>
                <div className="p-4 border-b border-zinc-200 dark:border-zinc-800 flex items-center justify-between">
                  <div className="font-semibold">Projects</div>
                  <div className="flex items-center gap-2">
                    <input
                      className="hidden sm:block bg-white dark:bg-zinc-900 border border-zinc-300 dark:border-zinc-700 rounded-md px-3 py-1.5 text-sm"
                      value={search}
                      onChange={(e) => setSearch(e.target.value)}
                      placeholder="Filter projects"
                      onKeyDown={(e) => e.key === 'Enter' && loadProjects(search)}
                    />
                    <Button kind="ghost" size="sm" onClick={() => loadProjects(search)}>Search</Button>
                  </div>
                </div>

                {projects.length === 0 ? (
                  <div className="p-6 text-sm text-zinc-600 dark:text-zinc-300">No projects yet. Create your first one above.</div>
                ) : (
                  <ul>
                    {projects.map((p, i) => (
                      <li key={p.id} className={cx("px-4 py-3 flex items-start justify-between gap-4", i !== projects.length - 1 && "border-b border-zinc-200 dark:border-zinc-800")}> 
                        {editingId === p.id ? (
                          <div className="flex-1 grid sm:grid-cols-2 gap-3">
                            <TextInput value={editTitle} onChange={setEditTitle} />
                            <TextInput value={editDesc} onChange={setEditDesc} />
                          </div>
                        ) : (
                          <div className="flex-1">
                            <div className="font-semibold text-blue-600 dark:text-blue-400 hover:underline cursor-pointer">{p.title}</div>
                            <div className="text-sm text-zinc-600 dark:text-zinc-300">{p.description || "—"}</div>
                            <div className="text-xs text-zinc-400 mt-1">id: {p.id}</div>
                          </div>
                        )}
                        <div className="flex shrink-0 gap-2">
                          {editingId === p.id ? (
                            <>
                              <Button size="sm" onClick={saveEdit}>Save</Button>
                              <Button size="sm" kind="ghost" onClick={() => setEditingId(null)}>Cancel</Button>
                            </>
                          ) : (
                            <>
                              <Button size="sm" kind="ghost" onClick={() => startEdit(p)}>Edit</Button>
                              <Button size="sm" kind="danger" onClick={() => del(p.id)}>Delete</Button>
                            </>
                          )}
                        </div>
                      </li>
                    ))}
                  </ul>
                )}
              </Card>

              {status && <div className="text-sm text-zinc-700 dark:text-zinc-300">{status}</div>}
            </>
          )}
        </main>
      </div>

      <footer className="text-center text-xs text-zinc-500 dark:text-zinc-400 py-6">DevLog • GitHub‑style UI</footer>
    </div>
  );
}
