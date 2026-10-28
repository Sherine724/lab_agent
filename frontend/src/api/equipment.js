import request from '@/utils/request'

/*分页模糊查询设备列表，可按所属实验室lab_id过滤*/
export function getEquipmentPageList(params) {
  return request({
    url: '/api/equipment/page',
    method: 'get',
    params: {
      page: params.page,
      page_size: params.page_size,
      keywords: params.keywords,
      lab_id: params.lab_id
    }
  })
}

//新增设备
export function createEquipmentApi(data) {
  return request({
    url: '/api/equipment',
    method: 'post',
    data
  })
}

//修改设备
export function updateEquipmentApi(equipmentId, data) {
  return request({
    url: `/api/equipment/${equipmentId}`,
    method: 'put',
    data
  })
}

//删除设备
export function deleteEquipmentApi(equipmentId) {
  return request({
    url: `/api/equipment/${equipmentId}`,
    method: 'delete'
  })
}
