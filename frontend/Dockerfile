# Angular Dockerfile
# Stage 1: Build the Angular application
FROM node:18 AS build

# Set the working directory
WORKDIR /app

# Install Angular CLI globally
RUN npm install -g @angular/cli

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the Angular application
RUN ng build

# Stage 2: Serve the Angular application with Nginx
FROM nginx:alpine

# Copy the built Angular application from the previous stage
COPY --from=build /app/dist/your-angular-app /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
