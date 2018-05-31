import json
from nodes.nodes_tree_generator import NodesTreeGenerator
from dialog_manager.dialog_manager import DialogManager
from django.http import JsonResponse
import base64

from helpers.speech_kit import speech2text

from logger.bot_logger import BotLogger
import logger.log_db_adapter



# logic_config = 'json_configs/smart_home_example.json'
# logic_config = 'json_configs/iptv_example_search.json'
logic_config = 'json_configs/caller.json'
tree_generator = NodesTreeGenerator(
    logic_config)
nodes_tree = tree_generator.gen_full_tree()
dialog_manager = DialogManager(nodes_tree)
db_path = 'db/ai_api.db'
sql_debug = False
db_adapter = logger.log_db_adapter.LogDBAdapter(
    db_path=db_path,
    create_tables=True,
    sql_debug=sql_debug
)
logger = BotLogger(
    db_adapter=db_adapter,
    storage_type='sqlite',
    logs_on=True
)


class UserMessage:
    class UserInfo:
        def __init__(self, user_id=None, first_name=None, last_name=None):
            self.id = user_id
            self.first_name = first_name
            self.last_name = last_name

    def __init__(
            self,
            text=None,
            user_id=None,
            first_name=None,
            last_name=None
    ):
        self.from_user = UserMessage.UserInfo(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name
        )
        self.text = text
        self.entities = []


def bot_base_api(request, **kwargs):
    print(request)
    if request.method == 'POST':
        req = (json.loads(request.body))
        print(req)
        if 'voice' in req:
            txt = speech2text(data=base64.decodebytes(req['voice']))
            if len(txt):
                req['text'] = txt[0][0]
            else:
                req['text'] = '[Голосовое сообщение не распознано]'
        msg = UserMessage(
            text=req['text'],
            user_id=req['user_id'],
            first_name=req['first_name'],
            last_name=req['last_name']
        )
        logger.add_user_message(msg)
        answer, current_node_name = dialog_manager.parse_message(
            msg
        )
        data = {
            'request': req['text'],
            'user_id': req['user_id'],
            'first_name': req['first_name'],
            'last_name': req['last_name'],
            'answer.text': answer.text,
            'answer.command': ''
        }
        if current_node_name == 'root node':
            data['answer.command'] = 'hang_up'
        logger.add_classification(current_node_name)
        logger.add_bot_answer(answer.text)
    return JsonResponse(data)
