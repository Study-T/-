const BASE = "http://localhost:8000/api";

let token: string | null = localStorage.getItem("token");

export function setToken(t: string | null) {
  token = t;
  if (t) localStorage.setItem("token", t);
  else localStorage.removeItem("token");
}

export function getToken() {
  return token;
}

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string>),
  };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${BASE}${path}`, { ...options, headers });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail ?? "Request failed");
  }

  return res.json();
}

export const api = {
  // Auth
  sendCode: (phone: string) =>
    request("/auth/send-code", {
      method: "POST",
      body: JSON.stringify({ phone }),
      headers: { "Content-Type": "application/json" },
    }),

  login: (phone: string, code: string) =>
    request<{ token: string }>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ phone, code }),
      headers: { "Content-Type": "application/json" },
    }),

  // Avatars
  getAvatars: () => request<Array<unknown>>("/avatars"),

  getAvatar: (id: number) => request<unknown>(`/avatars/${id}`),

  createAvatar: (photoUrl: string) =>
    request<unknown>("/avatars", {
      method: "POST",
      body: JSON.stringify({ photo_url: photoUrl }),
      headers: { "Content-Type": "application/json" },
    }),

  updateAvatarParams: (id: number, params: Record<string, number>) =>
    request<unknown>(`/avatars/${id}/params`, {
      method: "PUT",
      body: JSON.stringify(params),
      headers: { "Content-Type": "application/json" },
    }),

  deleteAvatar: (id: number) =>
    request(`/avatars/${id}`, { method: "DELETE" }),

  // Try-on
  tryOn: (avatarId: number, garmentId: number) =>
    request<unknown>("/tryon", {
      method: "POST",
      body: JSON.stringify({ avatar_id: avatarId, garment_id: garmentId }),
      headers: { "Content-Type": "application/json" },
    }),

  getTryOnTask: (id: number) => request<unknown>(`/tryon/${id}`),

  getTryOnHistory: () => request<Array<unknown>>("/tryon"),

  // Garments
  getGarments: () => request<Array<unknown>>("/garments"),

  createGarment: (category: string, imageUrl: string) =>
    request<unknown>("/garments", {
      method: "POST",
      body: JSON.stringify({ category, image_url: imageUrl }),
      headers: { "Content-Type": "application/json" },
    }),

  // Upload
  upload: async (file: File) => {
    const form = new FormData();
    form.append("file", file);
    const headers: Record<string, string> = {};
    if (token) headers["Authorization"] = `Bearer ${token}`;
    const res = await fetch(`${BASE}/upload`, {
      method: "POST",
      body: form,
      headers,
    });
    if (!res.ok) throw new Error("Upload failed");
    return res.json() as Promise<{ url: string }>;
  },
};
