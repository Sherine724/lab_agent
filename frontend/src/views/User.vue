<template>
  <div>
    <el-card>
      <template #header>
        <div style="font-size: 16px; font-weight: bold">
          <span>用户管理</span>
        </div>
      </template>
      <div style="margin-bottom: 10px">
        <el-input
          placeholder="请输入账号查询"
          v-model="params.keywords"
          style="width: 200px; margin-right: 8px"
          clearable
          @keyup.enter="handleSearch"
        >
        </el-input>
        <el-button type="primary" :icon="Search" @click="handleSearch">查询</el-button>
        <el-button style="margin-left: 30px" type="success" :icon="Plus" @click="openCreateDialog"
          >新增用户</el-button
        >
      </div>
      <el-table
        :header-cell-style="{ backgroundColor: '#f5f5f5', color: '#444' }"
        :data="tableData"
        style="width: 100%"
        v-loading="loading"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="账号" width="150" />
        <el-table-column prop="name" label="姓名" width="150" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="avatar" label="头像">
          <template #default="{ row }">
            <div style="min-height: 50px">
              <img
                v-if="row.avatar"
                style="display: block; width: 50px; height: 50px; border-radius: 50%"
                :src="row.avatar"
                alt=""
              />
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="role" label="角色" width="100">
          <template #default="{ row }">
            {{ row.role === 'admin' ? '管理员' : '学生' }}
          </template>
        </el-table-column>
        <el-table-column prop="phone" label="手机号" width="150" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'error'">
              {{ row.status === 1 ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button link type="primary" @click="openEditDialog(row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div>
        <el-pagination
          background
          layout="prev,pager,next,total"
          :total="total"
          :page-size="params.pageSize"
          :current-page="params.page"
          @current-change="handlePageChange"
        ></el-pagination>
      </div>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="400">
      <el-form
        ref="formRef"
        :rules="rules"
        :model="form"
        label-width="100px"
        style="width: 100%; padding-right: 50px"
      >
        <el-form-item label="账号" prop="username">
          <el-input :disabled="!!form.id" v-model="form.username" placeholder="请输入账号" />
        </el-form-item>
        <el-form-item v-if="!form.id" label="密码" prop="password">
          <el-input
            type="password"
            show-password
            v-model="form.password"
            placeholder="请输入密码"
          />
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入名称" />
        </el-form-item>

        <el-form-item label="角色" prop="role">
          <el-select v-model="form.role">
            <el-option label="学生" value="student"></el-option>
            <el-option label="管理员" value="admin"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入手机号" />
        </el-form-item>

        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio :value="1">正常</el-radio>
            <el-radio :value="0">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { Search, Plus } from '@element-plus/icons-vue'
import { ref, reactive, computed, nextTick, onMounted } from 'vue'
import { getUserPageList, createUserApi, updateUserApi } from '@/api/user'
import { ElMessage } from 'element-plus'

const params = reactive({
  page: 1,
  pageSize: 5,
  keywords: ''
})
const tableData = ref([])
const total = ref(0)
const loading = ref(false)
const submitting = ref(false)

const dialogVisible = ref(false)
const formRef = ref()
// 每次打开弹窗都从这份默认值开始，避免残留上一次的输入
const defaultForm = () => ({
  id: null,
  username: '',
  password: '123456',
  name: '',
  email: '',
  phone: '',
  role: 'student',
  status: 1
})
const form = reactive(defaultForm())
const dialogTitle = computed(() => (form.id ? '编辑用户' : '新增用户'))

//bcrypt 只处理前72个字节，和注册接口的规则保持一致
const validatePassword = (rule, value, callback) => {
  if (new TextEncoder().encode(value).length > 72) {
    callback(new Error('密码不能超过72字节'))
  } else {
    callback()
  }
}

const rules = {
  username: [
    { required: true, message: '请输入账号', trigger: 'blur' },
    { max: 50, message: '账号不能超过50个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { validator: validatePassword, trigger: 'blur' }
  ],
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  email: [{ type: 'email', message: '邮箱格式错误', trigger: 'blur' }],
  phone: [{ pattern: /^1[3-9]\d{9}$/, message: '手机号格式错误', trigger: 'blur' }]
}

const load = async () => {
  loading.value = true
  try {
    const res = await getUserPageList({
      page: params.page,
      page_size: params.pageSize,
      keywords: params.keywords
    })
    tableData.value = res.data?.list
    total.value = res.data?.total
  } catch (e) {
    // 错误提示已由 request 拦截器统一处理
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  params.page = 1
  load()
}

const handlePageChange = (page) => {
  params.page = page
  load()
}

// 弹窗打开后再清校验，首次打开时表单节点还没渲染出来
const openDialog = () => {
  dialogVisible.value = true
  nextTick(() => formRef.value?.clearValidate())
}

const openCreateDialog = () => {
  Object.assign(form, defaultForm())
  openDialog()
}

const openEditDialog = (row) => {
  Object.assign(form, defaultForm(), row)
  openDialog()
}

const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  // update 接口不接收 username/password，只提交可修改的字段，空串统一转成 null
  const data = {
    name: form.name,
    email: form.email || null,
    phone: form.phone || null,
    role: form.role,
    status: form.status
  }
  submitting.value = true
  try {
    if (form.id) {
      await updateUserApi(form.id, data)
      ElMessage.success('修改成功')
    } else {
      await createUserApi({ ...data, username: form.username, password: form.password })
      ElMessage.success('新增成功')
    }
    dialogVisible.value = false
    load()
  } catch (e) {
    // 错误提示已由 request 拦截器统一处理
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  load()
})
</script>
