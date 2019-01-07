'''Update ride record'''

import json
import logging
import os

import boto3

log_level = os.environ.get('LOG_LEVEL', 'INFO')
logging.root.setLevel(logging.getLevelName(log_level))  # type: ignore
_logger = logging.getLogger(__name__)

# DynamoDB
DDB_TABLE_NAME = os.environ.get('DDB_TABLE_NAME')
DDB_TABLE_HASH_KEY = os.environ.get('DDB_TABLE_HASH_KEY')
dynamodb = boto3.resource('dynamodb')
DDT = dynamodb.Table(DDB_TABLE_NAME)


def handler(event, context):
    '''Function entry'''
    _logger.info('Event received: {}'.format(json.dumps(event)))

    key_id = event['pathParameters'].get('Id')

    # XXX: pretend client sends DDB update expressions
    update_expression = json.loads(event.get('body'))

    try:
        DDT.update_item(
            Key=key_id,
            UpdateExpression=update_expression
        )
    except Exception as e:
        _logger.exception(e)
        raise e

    resp = {
        'statusCode': 200,
        'body': json.dumps({'success': True})
    }

    _logger.info('Response: {}'.format(json.dumps(resp)))

    return resp

