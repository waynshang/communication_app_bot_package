def get_object_by_keys(dictionary, keys):
  if not keys: return None
  if type(keys)==list:
    key = keys.pop(0)
    result = dictionary.get(key)
    if not result: return result
    if not keys: return result
    return get_object_by_keys(result, keys)
  else:
    return dictionary.get(keys)
