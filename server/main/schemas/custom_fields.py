from marshmallow import fields


class TrimmedString(fields.String):
    """
    Marshmallow custom field: Trimmed String
    Used to automatically strip off leading/ trailing white spaces of a string
    """

    def _deserialize(self, value, *args, **kwargs):
        if hasattr(value, 'strip'):
            value = value.strip()
        return super()._deserialize(value, *args, **kwargs)
