#!/bin/bash

# 使用 GitHub API 创建 secret
WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/b8c0c513-ecd0-46a3-8789-8343562a678d"

# 对 webhook URL 进行 base64 编码
ENCRYPTED_VALUE=$(echo -n "$WEBHOOK_URL" | base64 -w 0)

# 使用 GitHub CLI 创建 secret
gh secret set FEISHU_WEBHOOK_URL --body "$WEBHOOK_URL" --repo zzb13/ai_code

echo "✅ Secret 配置完成"
