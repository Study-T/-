import { useEffect, useRef } from "react";

type MessageHandler = (data: Record<string, unknown>) => void;

export function useWebSocket(taskId: number | null, onMessage: MessageHandler) {
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (taskId == null) return;

    const ws = new WebSocket(`ws://localhost:8000/ws/task/${taskId}`);
    wsRef.current = ws;

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessage(data);
    };

    ws.onerror = () => {
      // WebSocket connection lost — fall back to polling if needed
    };

    return () => {
      ws.close();
      wsRef.current = null;
    };
  }, [taskId, onMessage]);

  return wsRef;
}
