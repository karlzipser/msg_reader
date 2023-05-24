
from utilz import *
#birthday, email name of benefits
my_first_name = 'Karl'

R = lo('/Users/karlzipser/Desktop/kMessages/R.pkl')

if False:
    def get_people_R():
        People = {}
        C = R['correspondent']
        for person in C:
                name = get_safe_name(person)
        for c in Chats:
            if 'first_name' in Chats[c]:
                name = Chats[c]['first_name'],Chats[c]['last_name']
            else:
                name = '<no-name>',c
            if name not in People:
                People[name] = {}
            if c not in People[name]:
                People[name][c] = {'chat_rowids':[]}
            People[name][c]['chat_rowids'] += Chats[c]['chat_rowids']

        return People

def get_MessageDic_from_R(chat_identifiers):

    C = R['correspondent']

    rowid = 0
    M = {}
    for person in chat_identifiers:#list( set(chat_identifiers) | set(kys(C)) ):#C:
        #cm(person,r=1)
        first_to_name = person.split(' ')[0]
        if person not in C:
            #cr(person)
            continue
        ts = sorted(kys(C[person]))
        for t in ts:
            Q = {}
            #kprint(C[person][t],title=t)
            Q['message.rowid'] = rowid
            Q['chat.chat_identifier'] = get_safe_name(person)
            Q['message.date'] = int(t * 1000000000)
            t_ = MacTime_to_unixtime(Q['message.date']/1000000000)
            Q['timestamp'] = int(t_) - 8 * hours
            Q['date'] = time_str('Pretty24',Q['timestamp'])
            Q['timestamp_GMT'] = int(t_)
            Q['Attachments'] = []
            Q['message.is_from_me'] = C[person][t]['me']
            Q['message.service'] = 'unknown'
            Q['message.text'] = C[person][t]['text']
            """
            if C[person][t]['me']:
                Q['from_name'] = my_first_name
                Q['to_name'] = first_to_name
            else:
                Q['from_name'] = first_to_name
                Q['to_name'] = my_first_name
            Q['To:'] = first_to_name
            Q['is_from_me'] = C[person][t]['me']
            Q['text'] = C[person][t]['text']
            Q['service'] = 'unknown'
            #try:
            #    kprint(Q)
            #except:
            #    cE('kprint(Q) failed')
            """
            #Q['rowid'] = d2n(get_safe_name(person),'_',Q['message.date'])
            M[Q['message.rowid']] = Q
            rowid += 1

    return M

#EOF

"""
M[22895] (n=12)
    Attachments (n=2)
        ----. (n=6)
            attachment.created_date 613283070
            attachment.filename ~/Library/Messages/.../IMG_0402.mov
            attachment.mime_type video/quicktime
            attachment.rowid 918
            chat.rowid 220
            message.rowid 22895
        ----. (n=6)
            attachment.created_date 613283070
            attachment.filename ~/Library/Messages/.../IMG_0401.MOV
            attachment.mime_type video/quicktime
            attachment.rowid 919
            chat.rowid 220
            message.rowid 22895
    chat.chat_identifier +15102541747
    chat.last_addressed_handle +15109099328
    chat.rowid 220
    date Sunday, 07 Jun 2020, 21:24
    message.date 613283070010591744
    message.is_from_me 0
    message.rowid 22895
    message.service iMessage
    message.text ￼￼
    timestamp 1591590270
    timestamp_GMT 1591619070.0105917
"""


