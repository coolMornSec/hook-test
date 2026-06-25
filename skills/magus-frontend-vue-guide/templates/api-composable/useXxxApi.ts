import { useAxios } from '@magustek/framework-core'
import type { XxxDTO, XxxPageReq, XxxSaveReq } from '@/api/xxx/types'

export const useXxxApi = () => {
  const { get, post } = useAxios()
  const baseUrl = '/magus-service/xxx'

  return {
    page: (params: XxxPageReq) => post<MgPageResponse<XxxDTO>>(`${baseUrl}/page`, params),
    detail: (id: string) => get<MgDataResponse<XxxDTO>>(`${baseUrl}/find-by-id/${id}`),
    create: (data: XxxSaveReq) => post<MgBaseResponse>(`${baseUrl}/create`, data),
    update: (data: XxxSaveReq) => post<MgBaseResponse>(`${baseUrl}/update`, data),
    remove: (ids: string[]) => post<MgBaseResponse>(`${baseUrl}/delete`, ids),
  }
}
