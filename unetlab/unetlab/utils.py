def db_fields_to_dict(fields):
    output = {}
    for field in fields:
        output[field.name] = field.verbose_name
    return output
