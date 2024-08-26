def read_field_from_request(request, field_name: str):
    if request.is_json:
        return request.json.get(field_name, None)
    else:
        return request.form.get(field_name, None)