FROM node:20-alpine
WORKDIR /app
COPY package-lock.json package.json server.js /app/
COPY daikichi kyo /app/
COPY public/ /app/public
RUN echo "TSGLIVE{REDACTED}" > /flag

RUN adduser -D app-user && chown -R app-user /app
USER app-user

RUN npm install
EXPOSE 3000
CMD ["node", "server.js"]
