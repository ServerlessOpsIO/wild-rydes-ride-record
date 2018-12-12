'''Put ride record'''

import json
import logging
import os

import boto3

from thundra.thundra_agent import Thundra
THUNDRA_API_KEY = os.environ.get('THUNDRA_API_KEY', '')
thundra = Thundra(api_key=THUNDRA_API_KEY)

from thundra.plugins.log.thundra_log_handler import ThundraLogHandler
log_level = os.environ.get('LOG_LEVEL', 'INFO')
logging.root.setLevel(logging.getLevelName(log_level))  # type: ignore
_logger = logging.getLogger(__name__)
_logger.addHandler(ThundraLogHandler())

# DynamoDB
DDB_TABLE_NAME = os.environ.get('DDB_TABLE_NAME')
DDB_TABLE_HASH_KEY = os.environ.get('DDB_TABLE_HASH_KEY')
dynamodb = boto3.resource('dynamodb')
DDT = dynamodb.Table(DDB_TABLE_NAME)


@thundra
def handler(event, context):
    '''Function entry'''
    _logger.info('Event received: {}'.format(json.dumps(event)))

    ride_record = json.loads(event.get('body'))

    try:
        DDT.put_item(
            TableName=DDB_TABLE_NAME,
            Item=ride_record
        )
    except Exception as e:
        _logger.exception(e)
        raise e

    resp = {
        'statusCode': 201,
        'body': json.dumps({'success': True})
    }

    _logger.info('Response: {}'.format(json.dumps(resp)))

    return resp

