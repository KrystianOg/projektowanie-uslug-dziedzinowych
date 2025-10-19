import { useFetch, useWebSocket } from "@vueuse/core"

// TODO: use env variables or some config instead
const API_GATEWAY_WS = 'ws://localhost:8000/ws'
const API_GATEWAY_HTTP = "http://localhost:8000"

export const useAPIGateway = () => {
  const ws = useWebSocket(API_GATEWAY_WS)
  const fetch = useFetch(API_GATEWAY_HTTP)

  return {
    ws,
    fetch
  }
}
