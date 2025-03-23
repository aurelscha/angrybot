# Frontend Dockerfile (Svelte)
FROM node:18 as build

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy frontend source code
COPY . .

# Build the Svelte app
RUN npm run build

# Use Nginx to serve the built frontend
FROM nginx:alpine

# Copy built frontend files to Nginx
COPY --from=build /app/build /usr/share/nginx/html

# Expose HTTP port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
