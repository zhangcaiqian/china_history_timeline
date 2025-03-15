# 中国历史年表部署指南

本文档详细说明如何将中国历史年表 Python Dash 应用部署到云平台，并通过 Cloudflare 提供服务。

## 部署步骤

我们将采用以下步骤部署应用：

1. 将应用部署到 Render 平台
2. 使用 Cloudflare 作为 CDN 和反向代理

## 一、部署到 Render 平台

[Render](https://render.com/) 是一个现代化的云平台，支持 Python 应用的部署。

### 1. 准备工作

我们已经准备好了以下文件：

- `requirements.txt`：列出项目依赖
- `Procfile`：定义应用启动命令
- `runtime.txt`：指定 Python 版本
- 修改后的 `app.py`：支持从环境变量获取端口

### 2. 创建 Render 账号

1. 访问 [Render 官网](https://render.com/)
2. 点击 "Sign Up" 注册账号
3. 可以使用 GitHub 账号直接登录

### 3. 创建 Web 服务

1. 登录 Render 控制台
2. 点击 "New +" 按钮，选择 "Web Service"
3. 连接你的 GitHub 仓库（需要先将项目推送到 GitHub）
4. 填写服务信息：
   - **Name**：`china-history-timeline`
   - **Environment**：`Python 3`
   - **Build Command**：`pip install -r requirements.txt`
   - **Start Command**：`gunicorn app:server`
   - **Plan**：选择免费计划（Free）

5. 点击 "Create Web Service" 创建服务

### 4. 等待部署完成

Render 会自动部署你的应用。部署完成后，你会获得一个 Render 提供的域名，格式如：
```
https://china-history-timeline.onrender.com
```

## 二、配置 Cloudflare

### 1. 注册 Cloudflare 账号

1. 访问 [Cloudflare 官网](https://www.cloudflare.com/)
2. 点击 "Sign Up" 注册账号

### 2. 添加网站到 Cloudflare

如果你有自己的域名：

1. 登录 Cloudflare 控制台
2. 点击 "添加站点"
3. 输入你的域名（例如 `yourdomain.com`）
4. 选择免费计划
5. 按照指引修改你的域名 DNS 服务器

### 3. 创建 Cloudflare Worker（可选）

如果你想使用 Cloudflare Worker 作为反向代理：

1. 在 Cloudflare 控制台左侧菜单中，点击 "Workers & Pages"
2. 点击 "Create a Worker"
3. 使用以下代码创建一个 Worker：

```javascript
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url)
  
  // 将请求转发到 Render 应用
  const targetUrl = 'https://china-history-timeline.onrender.com' + url.pathname + url.search
  
  return fetch(targetUrl, {
    method: request.method,
    headers: request.headers,
    body: request.body
  })
}
```

4. 点击 "Save and Deploy"
5. 配置自定义域名（如果需要）

### 4. 配置 Cloudflare Pages（替代方案）

如果你想使用 Cloudflare Pages 作为反向代理：

1. 在 Cloudflare 控制台左侧菜单中，点击 "Pages"
2. 点击 "Create a project"
3. 选择 "Direct Upload"
4. 上传一个简单的 HTML 文件，其中包含重定向到 Render 应用的代码
5. 部署完成后，在 "Functions" 选项卡中创建一个 `_routes.json` 文件，配置代理规则

## 三、测试部署

1. 访问你的 Cloudflare 域名（例如 `https://china-history-timeline.yourdomain.com`）
2. 确认应用是否正常运行
3. 测试各项功能是否正常

## 四、维护和更新

当你需要更新应用时：

1. 更新本地代码
2. 提交并推送到 GitHub 仓库
3. Render 会自动检测到更改并重新部署

## 五、监控和日志

1. 在 Render 控制台可以查看应用日志和性能指标
2. 在 Cloudflare 控制台可以查看流量统计和安全事件

## 六、故障排除

如果遇到部署问题：

1. 检查 Render 日志，查找错误信息
2. 确认 `requirements.txt` 中的依赖版本是否兼容
3. 检查 Cloudflare Worker 或 Pages 配置是否正确

## 七、优化建议

1. 启用 Cloudflare 的 APO（Automatic Platform Optimization）功能，提高页面加载速度
2. 配置适当的缓存策略，减少服务器负载
3. 使用 Cloudflare 的 Web Analytics 监控网站性能

## 八、成本估算

- Render 免费计划：每月 750 小时免费使用时间（足够一个服务全天候运行）
- Cloudflare 免费计划：无限流量，基本 DDoS 保护

如有任何问题，请参考 [Render 文档](https://render.com/docs) 和 [Cloudflare 文档](https://developers.cloudflare.com/)。
