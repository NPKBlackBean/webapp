FROM node:20-bullseye AS development-dependencies-env
COPY package.json package-lock.json /app/
WORKDIR /app
RUN npm ci

FROM node:20-bullseye AS production-dependencies-env
COPY package.json package-lock.json /app/
WORKDIR /app
RUN npm ci --omit=dev

FROM node:20-bullseye AS build-env
ARG VITE_API_URL=http://localhost:8000
ARG TARGETPLATFORM
COPY package.json package-lock.json /app/
WORKDIR /app
# Install dependencies again for build to ensure correct binaries for target platform
RUN npm ci
COPY . /app/
ENV VITE_API_URL=${VITE_API_URL}
RUN npm run build

FROM node:20-bullseye
COPY package.json package-lock.json /app/
COPY --from=production-dependencies-env /app/node_modules /app/node_modules
COPY --from=build-env /app/build /app/build
WORKDIR /app

EXPOSE 3000

CMD ["npm", "run", "start"]
