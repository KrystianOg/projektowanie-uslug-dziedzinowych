import { useFetch, useWebSocket } from "@vueuse/core"

const API_GATEWAY_HTTP = import.meta.env.VITE_API_GATEWAY_HTTP_BASE
const API_GATEWAY_WS = import.meta.env.VITE_API_GATEWAY_WS

export const useAPIGateway = () => {
  const ws = useWebSocket(API_GATEWAY_WS)
  const fetch = useFetch(API_GATEWAY_HTTP + "/health")

  return {
    ws,
    fetch
  }
}
