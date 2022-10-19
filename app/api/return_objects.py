def return_object_by_id(id, model):
    return model.objects.get(id=id)
