from pyard import ARD


def before_all(context):
    context.ard = ARD('3440', data_dir='/tmp/py-ard')
