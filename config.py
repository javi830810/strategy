import os
mongo_host = os.environ.get('MONGO_HOST', "localhost")
mongo_port = int(os.environ.get('MONGO_PORT', "27017"))
mongo_user = os.environ.get('MONGODB_USERNAME', None)
mongo_password = os.environ.get('MONGODB_PASSWORD', None)