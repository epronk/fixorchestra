from fixorchestra.orchestration import *

filename = 'fix_repository_4_4.xml'
orchestration = Orchestration(filename)

class Message:

    def __init__(self, name, msg_type, category, references):
        self.name = name
        self.msg_type = msg_type
        self.category = category
        self.references = references
        
class Field:
    
    def __init__(self, id, name, type):
        self.id = id
        self.name = name
        self.type = type

class Code:
    # This class needs to be kept in sync with repository.Enum because fixaudit.py stores 
    # instances of these classes in Sets. Specifically both implementations have to be hashable 
    # and they have to be hashing the same thing.
    def __init__(self, name, value):
        self.name = name
        self.value = value

class CodeSet:
 
    def __init__(self, id, name, type, synopsis, pedigree, codes):
        self.id = id
        self.name = name
        self.type = type
        self.synopsis = synopsis
        self.pedigree = pedigree
        self.codes = codes

class Dictionary:

    fields_by_tag = {}          # Field.id -> Field
    fields_by_name = {}         # Field.name.lower() -> Field
    messages = {}               # Message.id -> Message
    messages_by_msg_type = {}   # Message.msg_type -> Message
    messages_by_name = {}       # Message.name.lower() -> Message

    def __init__(self, filename = None):
        if filename == None:
            return
        self.filename = filename
        tree = ET.parse(filename)
        repository = tree.getroot()
        self.load_fields(repository)
        self.load_messages(repository)

    def load_fields(self, repository):
        fieldsElement = repository.find('fields')
        for fieldElement in fieldsElement.findall('field'):
            name = fieldElement.get('name')
            type = fieldElement.get('type')
            for valueElement in fieldElement.findall('value'):
                #print(valueElement.get('enum'), valueElement.get('description'))
                code = Code(
                    valueElement.get('name'),
                    valueElement.get('value'),
                )
            # todo CodeSet
            field = Field(
                int(fieldElement.get('number')),
                name,
                type
            )
            self.fields_by_tag[field.id] = field
            self.fields_by_name[field.name.lower()] = field
    
    def load_messages(self, repository):
        messagesElement = repository.find('messages')
        for messageElement in messagesElement.findall('message'):
            message = Message(
                messageElement.get('name'),
                messageElement.get('msgtype'),
                messageElement.get('msgcat'),
                self.extract_references(messageElement)
            )
            self.messages[message.msg_type] = message
            self.messages_by_msg_type[message.msg_type] = message
            self.messages_by_name[message.name.lower()] = message

    def extract_references(self, element):
        for messageElement in element: #.findall('field'):
            print(messageElement.tag)


filename = 'FIX44.xml'
dictionary = Dictionary(filename)

    
#for message in orchestration.messages.values():
for message in dictionary.messages.values():
    print(message.name)
    for field in orchestration.message_fields(message):
        print('field', field.field.name)
