# Lucky

```
 _
| |   _   _  _ _
| |  | | | || ' |
|_|__|_|___||_|_|
  本地 API 密钥管理
```

## 运行

```bash
python lucky.py
```

零依赖，Python 3.10+ 即可。

## 功能

| 操作 | 方式 |
|------|------|
| 添加密钥 | `[+ 添加]` 或 `Ctrl+N` |
| 编辑密钥 | `[* 编辑]` / 双击行 / `Ctrl+E` |
| 删除密钥 | `[- 删除]` / `Ctrl+D` |
| 复制密钥 | `[> 复制]` / `Ctrl+C` |
| 搜索过滤 | 搜索框输入关键词 |
| 清除搜索 | `Esc` |
| 显示/隐藏密钥 | `[ 显示全部 ]` / `[ 隐藏全部 ]` |

## 存储

数据保存在 `~/.luck/keys.json`：

```json
{
  "name": "OpenAI",
  "api_url": "https://api.openai.com/v1",
  "api_key": "sk-xxxxxxxxxxxx"
}
```

## 打包为 .exe

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name Lucky lucky.py
```

生成的 `dist/Lucky.exe` 可直接运行。

## 设计

- 黑白配色
- 微软雅黑字体
- 半角图标
- 单文件，零依赖
