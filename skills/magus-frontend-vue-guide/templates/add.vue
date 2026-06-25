<template>
  <MgBackWrap title="新增资源">
    <XxxForm :submit-loading="submitLoading" show-cancel show-reset @confirm="onConfirm" @cancel="onCancel" />
  </MgBackWrap>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import XxxApi from '@/api/xxx'
import type { XxxSaveReq } from '@/api/xxx/types'
import { closeAndToNext } from '@magustek/framework-biz-utils'
import XxxForm from '../components/XxxForm.vue'

defineOptions({ name: 'XxxAdd' })
definePage({ name: 'XxxAdd' })

const submitLoading = ref(false)

const onConfirm = async (data: XxxSaveReq) => {
  submitLoading.value = true
  try {
    await XxxApi.create(data)
    ElMessage.success('保存成功')
    closeAndToNext()
  } finally {
    submitLoading.value = false
  }
}

const onCancel = () => {
  closeAndToNext()
}
</script>
