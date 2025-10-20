# Build stage
FROM node:22-alpine AS build-stage
WORKDIR /app

ARG VITE_API_GATEWAY_HTTP_BASE
ARG VITE_API_GATEWAY_WS

ENV VITE_API_GATEWAY_HTTP_BASE=${VITE_API_GATEWAY_HTTP_BASE}
ENV VITE_API_GATEWAY_WS=${VITE_API_GATEWAY_WS}

RUN corepack enable
RUN corepack prepare yarn@4 --activate

COPY package*.json yarn.lock .yarnrc.yml ./
COPY .yarn ./.yarn

RUN yarn install --immutable
COPY . .
RUN yarn build

# Production stage
FROM nginx:stable-alpine AS production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
