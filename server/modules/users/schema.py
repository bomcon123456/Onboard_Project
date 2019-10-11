from ma import ma


class CategorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')
