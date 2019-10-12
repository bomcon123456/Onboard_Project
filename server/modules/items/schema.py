from ma import ma


class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'user_id', 'category_id')
