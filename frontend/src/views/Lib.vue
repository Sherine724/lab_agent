<template>
  <div>
    <el-card>
      <template #header>
        <div style="font-size: 16px; font-weight: bold">
          <span>实验室管理</span>
        </div>
      </template>
      <div style="margin-bottom: 10px">
        <el-input
          placeholder="请输入实验室名称查询"
          v-model="params.keywords"
          style="width: 200px; margin-right: 8px"
          clearable
          @keyup.enter="handleSearch"
        >
        </el-input>
        <el-button type="primary" :icon="Search" @click="handleSearch">查询</el-button>
        <el-button style="margin-left: 30px" type="success" :icon="Plus" @click="openCreateDialog"
          >新增实验室</el-button
        >
      </div>
      <el-table
        :header-cell-style="{ backgroundColor: '#f5f5f5', color: '#444' }"
        :data="tableData"
        style="width: 100%"
        v-loading="loading"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="名称" width="200" />
        <el-table-column prop="location" label="位置" />
        <el-table-column prop="image" label="图片" width="100">
          <template #default="{ row }">
            <div style="min-height: 40px">
              <img
                v-if="row.image"
                style="display: block; width: 60px; height: 40px; border-radius: 4px; object-fit: cover"
                :src="row.image"
                alt=""
              />
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="capacity" label="学生容量" width="100" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'error'">
              {{ row.status === 1 ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="140">
          <template #default="{ row }">
            <el-button link type="primary" @click="openEditDialog(row)">编辑</el-button>
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
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
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入实验室名称" />
        </el-form-item>
        <el-form-item label="位置" prop="location">
          <el-input v-model="form.location" placeholder="请输入位置" />
        </el-form-item>
        <el-form-item label="图片" prop="image">
          <el-upload
            class="lab-image-uploader"
            :show-file-list="false"
            accept="image/jpeg,image/png,image/gif,image/webp"
            :http-request="handleImageUpload"
            :before-upload="beforeImageUpload"
          >
            <img v-if="form.image" :src="form.image" class="lab-image" />
            <el-icon v-else class="lab-image-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label="学生容量" prop="capacity">
          <el-input-number v-model="form.capacity" :min="1" :max="9999" />
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
import { getLabPageList, createLabApi, updateLabApi, deleteLabApi } from '@/api/lab'
import { uploadFileApi } from '@/api/file'
import { ElMessage, ElMessageBox } from 'element-plus'

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
  name: '',
  location: '',
  image: null,
  capacity: 1,
  status: 1
})
const form = reactive(defaultForm())
const dialogTitle = computed(() => (form.id ? '编辑实验室' : '新增实验室'))

const rules = {
  name: [
    { required: true, message: '请输入实验室名称', trigger: 'blur' },
    { max: 50, message: '名称不能超过50个字符', trigger: 'blur' }
  ],
  location: [{ max: 100, message: '位置不能超过100个字符', trigger: 'blur' }]
}

const load = async () => {
  loading.value = true
  try {
    const res = await getLabPageList({
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
  // 空串统一转成 null，和后端可空字段的约定保持一致
  const data = {
    name: form.name,
    location: form.location || null,
    image: form.image || null,
    capacity: form.capacity,
    status: form.status
  }
  submitting.value = true
  try {
    if (form.id) {
      await updateLabApi(form.id, data)
      ElMessage.success('修改成功')
    } else {
      await createLabApi(data)
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

//选择文件后先校验，返回false会中断上传
const beforeImageUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  if (!isImage) {
    ElMessage.error('实验室图片只能是图片格式')
    return false
  }
  if (file.size > 10 * 1024 * 1024) {
    ElMessage.error('图片大小不能超过10MB')
    return false
  }
  return true
}

//走自己的请求封装上传，成功拿到url后写进表单，点确定才落库
const handleImageUpload = async ({ file }) => {
  const res = await uploadFileApi(file)
  if (res.code === 200) {
    form.image = res.data.url
  }
}

const handleDelete = async (row) => {
  const confirmed = await ElMessageBox.confirm(`确定删除实验室「${row.name}」吗？`, '提示', {
    type: 'warning'
  }).catch(() => false)
  if (!confirmed) return
  try {
    await deleteLabApi(row.id)
    ElMessage.success('删除成功')
    // 删掉当前页最后一条时回到上一页，避免停在空页
    if (tableData.value.length === 1 && params.page > 1) {
      params.page -= 1
    }
    load()
  } catch (e) {
    // 实验室下还有设备时后端会拒绝，错误提示由拦截器统一弹出
  }
}

onMounted(() => {
  load()
})
</script>

<style scoped>
/* .el-upload是element-plus组件内部的节点，scoped下要用:deep才能命中 */
.lab-image-uploader :deep(.el-upload) {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.lab-image-uploader :deep(.el-upload:hover) {
  border-color: var(--el-color-primary);
}

.lab-image-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 120px;
  height: 90px;
}

.lab-image-uploader .lab-image {
  width: 120px;
  height: 90px;
  display: block;
  object-fit: cover;
}
</style>
