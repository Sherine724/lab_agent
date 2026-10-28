<template>
  <div class="register-container">
    <div class="register-box">
      <h1 style="text-align: center; font-size: 24px; margin-bottom: 10px">
        欢迎注册实验室预约系统
      </h1>

      <el-form ref="formRef" :rules="rules" :model="form" label-width="0px" style="max-width: 100%">
        <el-form-item prop="username">
          <el-input
            size="large"
            v-model="form.username"
            placeholder="请输入账号"
            :prefix-icon="User"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            type="password"
            size="large"
            v-model="form.password"
            placeholder="请输入密码"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>

        <el-form-item prop="confirmPassword">
          <el-input
            type="password"
            size="large"
            v-model="form.confirmPassword"
            placeholder="请确认密码"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>

        <div>
          <el-button type="primary" style="width: 100%" @click="register" :loading="loadingValue"
            >注册</el-button
          >
          <div style="text-align: right; margin-top: 10px">
            已有账号？请<router-link style="color: var(--el-color-primary)" to="/login"
              >登录</router-link
            >
          </div>
        </div>
      </el-form>
    </div>
  </div>
</template>

<!-- const formRef=ref() const form = reactive({ username: '', password: '' }) const rules = { username:
[{ required: true, message: '请输入账号', trigger: 'blur' }], password: [{ required: true, message:
'请输入密码', trigger: 'blur'
}],confirmPassword:[{required:true,message:'请确认密码',trigger:'blur'}] } -->

<script setup>
import { reactive, ref } from 'vue'
import { User, Lock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { registerApi } from '@/api/auth'
const router = useRouter()

const loadingValue = ref(false)

const form = reactive({
  username: '',
  password: '',
  confirmPassword: ''
})

const formRef = ref()
const validatePass = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请确认密码'))
  } else {
    if (value != form.password) {
      callback(new Error('两次密码输入不一致'))
    }
    callback()
  }
}

const rules = {
  username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validatePass, trigger: 'blur' }
  ]
}

const register = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  loadingValue.value = true
  try {
    const res = await registerApi({ username: form.username, password: form.password })
    ElMessage.success(res.message || '注册成功')
    router.push('/login')
  } catch (e) {
    // 4. 空 catch 是有意的：request.js 响应拦截器已经弹过 ElMessage.error 了
  } finally {
    loadingValue.value = false
  }
}
</script>

<style scoped>
.register-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
.register-box {
  width: 380px;
  border-radius: 8px;
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
  padding: 40px;
  text-align: center;
  background-color: white;
}
</style>
