import models.schema_pb2 as schema

def obj_to_task_msg(obj):
    message = schema.Task()
    message.id = obj.task_id
    message.containerRef = obj.container_reference
    message.content = obj.content
    if obj.resource is not None:
        resource = schema.Resource()
        resource.cpu = obj.resource.cpu
        resource.memory = obj.resource.memory
        message.resource.CopyFrom(resource)
    if obj.runtime is not None:
        message.runtime = obj.runtime
    if obj.use_gpu is not None:
        message.useGpu = obj.use_gpu
        if obj.use_gpu and obj.gpu_count is not None:
            message.gpuCount = obj.gpu_count
    return message
