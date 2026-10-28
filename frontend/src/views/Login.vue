<template>
  <div class="login-container">
    <div class="login-box">
      <h1 style="text-align: center; font-size: 24px">实验室预约系统</h1>
      <div style="margin-top: 10px; margin-bottom: 10px">基于AI Agent智能预约系统</div>

      <el-form ref="formRef" :rules="rules" :model="form" style="max-width: 600px">
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

        <div>
          <el-button type="primary" style="width: 100%" @click="login" :loading="loadingValue"
            >登录</el-button
          >
          <div style="text-align: right; margin-top: 10px">
            还没有账号？请<router-link style="color: var(--el-color-primary)" to="/register"
              >注册</router-link
            >
          </div>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { loginApi } from '@/api/auth'
import { useUser } from '@/utils/user'

const router = useRouter()
const { saveLoginData } = useUser()
const formRef = ref()

const form = reactive({
  username: '',
  password: ''
})

const loadingValue = ref(false)

const rules = {
  username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const login = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) {
    return
  }
  loadingValue.value = true
  try {
    const res = await loginApi(form)
    //loadingValue.value = false
    console.log(res)
    if (res.code == 200) {
      ElMessage.success('登录成功')
      saveLoginData(res.data)
      await router.push('/manager/home')
    }
    //
  } catch (e) {
  } finally {
    loadingValue.value = false
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
.login-box {
  width: 380px;
  border-radius: 8px;
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
  padding: 40px;
  text-align: center;
  background-color: white;
}
</style>
