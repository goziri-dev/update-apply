// lib/api/client.ts
// Base fetch wrapper — single source of truth for all backend API calls.

type RequestOptions = {
  method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  body?: unknown;
  headers?: Record<string, string>;
};

type ApiError = {
  status: number;
  message: string;
  details?: unknown;
};

export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000") {
    this.baseUrl = baseUrl;
  }

  async request<T>(path: string, options: RequestOptions = {}): Promise<T> {
    const { method = "GET", body, headers = {} } = options;

    const fetchHeaders: Record<string, string> = {
      "Content-Type": "application/json",
      ...headers,
    };

    // If running on the client, attach Clerk auth token.
    // On the server, tokens are injected by the calling code.
    if (typeof window !== "undefined") {
      try {
        const { getToken } = await import("@clerk/nextjs");
        const token = await getToken();
        if (token) {
          fetchHeaders["Authorization"] = `Bearer ${token}`;
        }
      } catch {
        // Clerk not available — caller must handle auth themselves
      }
    }

    const response = await fetch(`${this.baseUrl}${path}`, {
      method,
      headers: fetchHeaders,
      body: body ? JSON.stringify(body) : undefined,
    });

    if (!response.ok) {
      const error: ApiError = {
        status: response.status,
        message: await response.text().catch(() => "Unknown error"),
      };
      throw error;
    }

    return response.json() as Promise<T>;
  }

  get<T>(path: string): Promise<T> {
    return this.request<T>(path, { method: "GET" });
  }

  post<T>(path: string, body?: unknown): Promise<T> {
    return this.request<T>(path, { method: "POST", body });
  }

  put<T>(path: string, body?: unknown): Promise<T> {
    return this.request<T>(path, { method: "PUT", body });
  }

  patch<T>(path: string, body?: unknown): Promise<T> {
    return this.request<T>(path, { method: "PATCH", body });
  }

  delete<T>(path: string): Promise<T> {
    return this.request<T>(path, { method: "DELETE" });
  }
}

export const apiClient = new ApiClient();
