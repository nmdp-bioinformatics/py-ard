import pyard


def before_all(context):
    context.ard = pyard.init("3440", data_dir="/tmp/py-ard")

    # an ard with ping set to True
    my_config = {
        "ping": True,
    }
    context.ard_ping = pyard.init("3440", data_dir="/tmp/py-ard", config=my_config)
