import axios from 'axios'
import { getToken } from './auth'
import { ElMessage } from 'element-plus'

const service = axios.create({ baseURL: import.meta.env.VITE_API_BASE_URL, timeout: 30000 })
//请求拦截
service.interceptors.request.use(
  (config) => {
    const token = getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (err) => Promise.reject(err)
)

//返回拦截器的配置
service.interceptors.response.use(
  (res) => {
    const data = res.data
    //后端约定：HTTP状态码恒为200,业务结果看body里面的code
    if (data.code != 200) {
      ElMessage.error(data.message || '请求失败')
      return Promise.reject(new Error(data.message || '请求失败'))
    }
    return data
  },
  (err) => {
    //网络层错误：后端未启动、 超时、401,402等非2XX响应
    const message = err.response?.data?.message || err.message || '网络异常'
    ElMessage.error(message)
    return Promise.reject(err)
  }
)

export default service
