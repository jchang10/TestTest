
import boto3
import os

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, UTCDateTimeAttribute, NumberAttribute

class MyData(Model):
    class Meta:
        table_name = os.environ.get('STAGE', 'dev') + '.mydata'
        region = boto3.Session().region_name
        host = 'http://localhost:8000' \
            if not os.environ.get('LAMBDA_TASK_ROOT') else None
    id = UnicodeAttribute(hash_key=True)
    customer_id = UnicodeAttribute()
    name = UnicodeAttribute()
    date = UTCDateTimeAttribute()
    score = NumberAttribute(null=True)
    weighting = NumberAttribute(null=True)

    def __repr__(self):
        return '<MyData %r>' % self.name

    def to_json(self):
        mydata = {
            'id':self.id,
            'customer_id':self.customer_id,
            'name':self.name,
            'date':self.date,
            'score':self.score,
            'weighting':self.weighting
            }
        return mydata
