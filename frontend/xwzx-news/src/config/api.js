/**
 * API配置文件
 * 包含API基础URL和AI问答功能所需的API参数
 */

// API基础URL配置
export const apiConfig = {
  // 后端API基础URL
  baseURL: 'http://127.0.0.1:8000',
}

export const aiChatConfig = {
  // OpenAI API地址
  apiEndpoint: 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
  
  // API Key (由开发人员指定)
  apiKey: 'sk-ws-H.RPEMPYL.wWK1.MEYCIQDT1ET1X_7NuGSvM7e6E5s0iNc1-ex4iEDzKn3gLKFsegIhANRdxKx4UWKEz1xA3ia2Go4bAsgEulyD62ta0Y9hiOW2',
  
  // 使用的模型
  model: 'qwen3.7-max'
}
