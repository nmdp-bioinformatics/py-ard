from pyard import ARD


def before_all(context):
    context.ard = ARD(verbose=True)
