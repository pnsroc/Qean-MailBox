# 使用官方 Node 镜像
FROM node:20-alpine AS builder

WORKDIR /app

# 复制依赖文件
COPY package.json package-lock.json* ./

# 安装依赖
RUN npm install

# 复制全部前端代码
COPY . .

# 构建 Next.js
RUN npm run build

# -----------------------------
# 生产环境镜像
# -----------------------------
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production

# 复制构建产物
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json

# 安装仅生产依赖
RUN npm install --omit=dev

EXPOSE 3000

CMD ["npm", "start"]
