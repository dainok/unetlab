const API_BASE = "/api";

export const api = {
  async get(url) {
    const res = await fetch(API_BASE + url);
    if (!res.ok) throw new Error(res.statusText);
    return res.json();
  },
  async post(url, body) {
    return this._send("POST", url, body);
  },
  async put(url, body) {
    return this._send("PUT", url, body);
  },
  async delete(url) {
    return this._send("DELETE", url);
  },
  async _send(method, url, body) {
    const res = await fetch(API_BASE + url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    if (!res.ok) throw new Error(res.statusText);
    return res.json();
  }
};
