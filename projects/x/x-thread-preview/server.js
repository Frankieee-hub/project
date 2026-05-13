const http = require("node:http");
const fs = require("node:fs");
const path = require("node:path");
const { randomUUID } = require("node:crypto");

const root = __dirname;
const generatedDir = path.join(root, "assets", "generated");
const envPath = path.join(root, ".env");
const logPath = path.join(root, "server.log");

process.on("uncaughtException", (error) => {
  log(`uncaughtException: ${error.stack || error.message}`);
  process.exit(1);
});

process.on("unhandledRejection", (error) => {
  log(`unhandledRejection: ${error?.stack || error}`);
  process.exit(1);
});

loadEnv(envPath);
fs.mkdirSync(generatedDir, { recursive: true });

const port = Number(process.env.PORT || 8787);
const imageModel = process.env.OPENAI_IMAGE_MODEL || "gpt-image-1.5";

const mimeTypes = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
};

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, `http://${req.headers.host}`);
    if (req.method === "GET" && url.pathname === "/api/status") {
      sendJson(res, 200, {
        hasKey: Boolean(process.env.OPENAI_API_KEY),
        model: imageModel,
      });
      return;
    }

    if (req.method === "POST" && url.pathname === "/api/generate-image") {
      await handleGenerateImage(req, res);
      return;
    }

    if (req.method === "GET") {
      serveStatic(url.pathname, res);
      return;
    }

    sendJson(res, 405, { error: "Method not allowed" });
  } catch (error) {
    sendJson(res, 500, { error: error.message || "Server error" });
  }
});

server.listen(port, () => {
  log(`X preview server running at http://localhost:${port}`);
  log(`Image model: ${imageModel}`);
});

async function handleGenerateImage(req, res) {
  if (!process.env.OPENAI_API_KEY) {
    sendJson(res, 400, { error: "缺少 OPENAI_API_KEY。请在 .env 中配置后重启服务。" });
    return;
  }

  const body = await readJson(req);
  const prompt = String(body.prompt || "").trim();
  const size = String(body.size || "1536x1024");
  if (!prompt) {
    sendJson(res, 400, { error: "缺少图片提示词。" });
    return;
  }

  const response = await fetch("https://api.openai.com/v1/images/generations", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: imageModel,
      prompt,
      size,
      quality: process.env.OPENAI_IMAGE_QUALITY || "medium",
      n: 1,
    }),
  });

  const data = await response.json();
  if (!response.ok) {
    sendJson(res, response.status, { error: data.error?.message || "OpenAI 图片生成失败。" });
    return;
  }

  const image = data.data?.[0];
  if (!image?.b64_json && !image?.url) {
    sendJson(res, 502, { error: "接口没有返回图片数据。" });
    return;
  }

  const filename = `${new Date().toISOString().slice(0, 10)}-${randomUUID()}.png`;
  const absolutePath = path.join(generatedDir, filename);

  if (image.b64_json) {
    fs.writeFileSync(absolutePath, Buffer.from(image.b64_json, "base64"));
  } else {
    const imageResponse = await fetch(image.url);
    if (!imageResponse.ok) throw new Error("图片下载失败。");
    fs.writeFileSync(absolutePath, Buffer.from(await imageResponse.arrayBuffer()));
  }

  sendJson(res, 200, {
    path: `/assets/generated/${filename}`,
    absolutePath,
    model: imageModel,
  });
}

function serveStatic(pathname, res) {
  const normalized = pathname === "/" ? "/index.html" : decodeURIComponent(pathname);
  const filePath = path.normalize(path.join(root, normalized));
  if (!filePath.startsWith(root)) {
    sendText(res, 403, "Forbidden");
    return;
  }
  if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
    sendText(res, 404, "Not found");
    return;
  }
  res.writeHead(200, { "Content-Type": mimeTypes[path.extname(filePath)] || "application/octet-stream" });
  fs.createReadStream(filePath).pipe(res);
}

function readJson(req) {
  return new Promise((resolve, reject) => {
    let body = "";
    req.on("data", (chunk) => {
      body += chunk;
      if (body.length > 1_000_000) {
        req.destroy();
        reject(new Error("Request body too large"));
      }
    });
    req.on("end", () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch {
        reject(new Error("Invalid JSON"));
      }
    });
    req.on("error", reject);
  });
}

function sendJson(res, status, data) {
  res.writeHead(status, { "Content-Type": "application/json; charset=utf-8" });
  res.end(JSON.stringify(data));
}

function sendText(res, status, text) {
  res.writeHead(status, { "Content-Type": "text/plain; charset=utf-8" });
  res.end(text);
}

function loadEnv(filePath) {
  if (!fs.existsSync(filePath)) return;
  const lines = fs.readFileSync(filePath, "utf8").split(/\r?\n/);
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const index = trimmed.indexOf("=");
    if (index === -1) continue;
    const key = trimmed.slice(0, index).trim();
    const value = trimmed.slice(index + 1).trim().replace(/^["']|["']$/g, "");
    if (key && !process.env[key]) process.env[key] = value;
  }
}

function log(message) {
  const line = `[${new Date().toISOString()}] ${message}`;
  fs.appendFileSync(logPath, `${line}\n`, "utf8");
  console.log(line);
}
