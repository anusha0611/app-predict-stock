# Stage 1: Build the application
FROM node:18 AS builder

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json for dependency installation
COPY package.json package-lock.json ./

# Install dependencies from requirements
RUN npm install

# Copy the remaining app files to the container
COPY . .

# Build the app for production
RUN npm run build

# Stage 2: Serve the built application
FROM nginx:alpine

# Copy the built application files from the builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80 for the app
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
