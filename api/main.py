from fastapi import Body, FastAPI, Response
from enum import Enum
from typing import Any
import yaml
import json

app = FastAPI()

class ConfigType(str, Enum):
    cookies = "cookies",
    priorities = "priorities",
    settings = "settings"
    sources = "sources",
    wrappers = "wrappers",

@app.get("/")
async def home():
    return "Hello world!";
    
@app.get("/config/{config_type}/")
async def read(config_type: ConfigType) -> Response:
    return yaml_to_json(config_type.value);

@app.put("/config/{config_type}/")
async def write(config_type: ConfigType, json_in: Any = Body(None)):
    write_file(config_type.value, json_in);
    return '';

def write_file(config_type: str, json_in):
    with open('./config/%s.yml' % (config_type), 'w') as file:
        file.write(yaml.dump(json_in, default_flow_style=False));

# TODO error handling - for when file not exists?
def yaml_to_json(config_type):
    yaml_in = open("./config/%s.yml" % (config_type), 'r');
    yaml_object = yaml.safe_load(yaml_in);
    json_str = json.dumps(yaml_object, indent=4, default=str);
    return Response(content=json_str, media_type='application/json')
