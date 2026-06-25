import type { XxxDTO } from '@/api/xxx/types'

export const useXxx = () => {
  const selectedRows = ref<XxxDTO[]>([])

  const setSelectedRows = (rows: XxxDTO[]) => {
    selectedRows.value = [...rows]
  }

  const clearSelectedRows = () => {
    selectedRows.value = []
  }

  return {
    selectedRows,
    setSelectedRows,
    clearSelectedRows,
  }
}
