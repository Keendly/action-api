import reader_api.reader_api

def handle(event, context):
    print event
    """Lambda function entry point """
    return reader_api.reader_api.handle(event)
