<template>
  <div style="width: 50%">
    <el-card>
      <template #header>
        <div style="font-size: 16px; font-weight: bold">
          <span>修改密码</span>
        </div>
      </template>
      <el-form
        ref="formRef"
        :rules="rules"
        :model="form"
        label-width="100px"
        style="width: 100%; padding-right: 50px"
      >
        <el-form-item label="原密码" prop="oldPassword">
          <el-input
            type="password"
            show-password
            v-model="form.oldPassword"
            placeholder="请输入原密码"
          />
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input
            type="password"
            show-password
            v-model="form.newPassword"
            placeholder="请输入新密码"
          />
        </el-form-item>
        <el-form-item label="确认密码" prop="conformPassword">
          <el-input
            type="password"
            show-password
            v-model="form.conformPassword"
            placeholder="请确认新密码"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="submitting" @click="handleSubmit">保存修改</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { updatePassword } from '@/api/user'
import { logout } from '@/utils/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()

const validatePass = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请确认密码'))
  } else {
    if (value != form.newPassword) {
      return callback(new Error('两次密码输入不一致'))
    }
    callback()
  }
}
const submitting = ref(false)
const formRef = ref()
const form = reactive({
  oldPassword: '',
  newPassword: '',
  conformPassword: ''
})

const rules = {
  oldPassword: [{ required: true, message: '请输入原密码', trigger: 'blur' }],
  newPassword: [{ required: true, message: '请输入新密码', trigger: 'blur' }],
  conformPassword: [{ validator: validatePass, message: '请确认新密码', trigger: 'blur' }]
}
const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  submitting.value = true
  try {
    const res = await updatePassword({
      old_password: form.oldPassword,
      new_password: form.newPassword
    })
    if (res.code === 200) {
      ElMessage.success('修改密码成功')
      logout()
      await router.push('/login')
    }
  } finally {
    submitting.value = false
  }
}
</script>
