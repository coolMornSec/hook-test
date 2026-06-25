<template>
  <MgBackWrap title="编辑资源">
    <XxxForm
      v-if="detailLoaded"
      v-model="formData"
      :submit-loading="submitLoading"
      is-edit
      show-cancel
      @confirm="onConfirm"
      @cancel="onCancel"
    />
  </MgBackWrap>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, unref } from 'vue'
import { ElMessage } from 'element-plus'
import XxxApi from '@/api/xxx'
import type { XxxSaveReq } from '@/api/xxx/types'
import { closeAndToNext } from '@magustek/framework-biz-utils'
import XxxForm from '../components/XxxForm.vue'
import { useRoute } from 'vue-router'

defineOptions({ name: 'XxxEdit' })
definePage({ name: 'XxxEdit' })

const route = useRoute()
const id = computed(() => route.params.id as string)

const submitLoading = ref(false)
const detailLoaded = ref(false)
const formData = ref<Partial<XxxSaveReq>>({})

const fetchDetail = async () => {
  if (!id.value) return
  const { data } = await XxxApi.findOne(id.value)
  formData.value = { ...unref(data) }
  detailLoaded.value = true
}

const onConfirm = async (data: XxxSaveReq) => {
  submitLoading.value = true
  try {
    await XxxApi.update({ ...data, id: id.value })
    ElMessage.success('保存成功')
    closeAndToNext()
  } finally {
    submitLoading.value = false
  }
}

const onCancel = () => {
  closeAndToNext()
}

onMounted(() => {
  void fetchDetail()
})
</script>
