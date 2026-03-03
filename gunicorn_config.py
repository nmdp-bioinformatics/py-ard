# Gunicorn configuration for preloading py-ard

# Preload the application
preload_app = True

# Server socket
bind = "0.0.0.0:8080"

# Worker processes
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"

# Timeouts
timeout = 5000

# Logging
loglevel = "info"


def on_starting(server):
    """Called just before the master process is initialized."""
    print("=" * 60)
    print("Preloading py-ard in master process...")
    # Initialize ard in master process - will be shared via fork
    import api

    api.init_pyard()
    print("Done preloading py-ard")
    print("=" * 60)
