import os


os.environ["PYTHONPATH"] = "{}:{}".format("my/addition/to/pythonpath", os.environ.get("PYTHONPATH", ""))
print(os.environ["PYTHONPATH"])
