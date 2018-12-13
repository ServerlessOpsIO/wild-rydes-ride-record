'''Put ride record'''

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


def _put_ride_record(ride_record):
    '''Write ride_record to DDB'''
    try:
        DDT.put_item(
            TableName=DDB_TABLE_NAME,
            Item=ride_record
        )
    except Exception as e:
        _logger.exception(e)
        raise e


def handler_http(event, context):
    '''Function entry'''
    _logger.info('Event received: {}'.format(json.dumps(event)))

    ride_record = json.loads(event.get('body'))

    _put_ride_record(ride_record)

    resp = {
        'statusCode': 201,
        'body': json.dumps({'success': True})
    }

    _logger.info('Response: {}'.format(json.dumps(resp)))

    return resp


def handler_sns(event, context):
    '''Function entry'''
    _logger.info('Event received: {}'.format(json.dumps(event)))

    ride_record = json.loads(event.get('Records')[0].get('Sns').get('Message'))

    _put_ride_record(ride_record)


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

