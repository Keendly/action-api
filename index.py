import reader_api.reader_api

def handle(event, context):
    """Lambda function entry point """
    reader_api.reader_api.handle(event)
