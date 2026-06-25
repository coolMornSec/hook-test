<template>
  <MgLayout v-loading="loading" class="table-search-page h-full min-h-0 bg-[var(--el-bg-color)]">
    <template #header>
      <MgSearch @search="onSearch">
        <template #search>
          <el-form-item label="名称">
            <el-input v-model.trim="searchForm.name" clearable placeholder="请输入名称" />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.state" clearable placeholder="请选择状态" class="w-[200px]">
              <el-option label="启用" value="enabled" />
              <el-option label="停用" value="disabled" />
            </el-select>
          </el-form-item>
        </template>
        <template #buttons>
          <el-button type="primary" :icon="Search" v-auth="['framework:module:resource:find']" @click="onSearch">
            查询
          </el-button>
        </template>
      </MgSearch>
    </template>

    <template #main>
      <MgToolbar :select-length="selectedRows.length" @event-handle="onToolbarEvent">
        <el-button type="primary" v-auth="['framework:module:resource:create']" @click="onAdd">新增</el-button>
        <el-button
          :disabled="!selectedRows.length"
          v-auth="['framework:module:resource:delete']"
          @click="onBatchDelete"
        >
          批量删除
        </el-button>
      </MgToolbar>

      <MgTable
        v-model:page-size="page.size"
        v-model:current-page="page.page"
        class="mg-table-flex"
        stripe
        :data="tableData"
        :total="total"
        @paging-change="fetchList"
        @select="onSelectionChange"
        @select-all="onSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="name" label="名称" min-width="180" show-overflow-tooltip />
        <el-table-column prop="code" label="编码" min-width="160" show-overflow-tooltip />
        <el-table-column prop="state" label="状态" width="120" />
        <el-table-column fixed="right" label="操作" width="160" align="center">
          <template #default="{ row }">
            <el-button
              link
              type="primary"
              :icon="Edit"
              v-auth="['framework:module:resource:update']"
              @click.stop="onEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              link
              type="danger"
              :icon="Delete"
              v-auth="['framework:module:resource:delete']"
              @click.stop="onDelete(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
        <template #empty>
          <div>暂无数据</div>
        </template>
      </MgTable>
    </template>
  </MgLayout>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref, unref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import XxxApi from '@/api/xxx'
import type { XxxDTO, XxxPageReq } from '@/api/xxx/types'
import { Delete, Edit } from '@magustek/icon-svg'
import { useRouter } from 'vue-router'

defineOptions({ name: 'XxxPage' })

type XxxSearchForm = Pick<XxxPageReq, 'name' | 'state'>
type XxxRow = XxxDTO

const router = useRouter()

const searchForm = reactive<XxxSearchForm>({
  name: '',
  state: '',
})

const page = reactive({
  page: 1,
  size: 100,
})

const loading = ref(false)
const total = ref(0)
const tableData = ref<XxxRow[]>([])
const selectedRows = ref<XxxRow[]>([])

const fetchList = async () => {
  loading.value = true
  try {
    const { data } = await XxxApi.page({
      ...searchForm,
      ...page,
    })
    const payload = unref(data)
    tableData.value = payload.list || []
    total.value = payload.totalNum || 0
  } finally {
    loading.value = false
    selectedRows.value = []
  }
}

const onSearch = () => {
  page.page = 1
  void fetchList()
}

const onSelectionChange = (rows: XxxRow[]) => {
  selectedRows.value = [...rows]
}

const onToolbarEvent = (code: string) => {
  if (code === 'add') onAdd()
  if (code === 'batchDelete') void onBatchDelete()
}

const onAdd = () => {
  void router.push({ name: 'XxxAdd' })
}

const onEdit = (row: XxxRow) => {
  void router.push({ name: 'XxxEdit', params: { id: row.id } })
}

const deleteByIds = async (ids: string[]) => {
  await ElMessageBox.confirm('是否确认删除？', '提示', { type: 'warning' })
  await XxxApi.delete(ids)
  ElMessage.success('删除成功')
  await fetchList()
}

const onDelete = (row: XxxRow) => deleteByIds([row.id])

const onBatchDelete = () => deleteByIds(selectedRows.value.map((row) => row.id))

onMounted(() => {
  void fetchList()
})
</script>
