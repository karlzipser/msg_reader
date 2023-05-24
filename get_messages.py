
from utilz import *
import sqlite3

def get_People(Address_book,conn):

    AB = Address_book

    cur = conn.cursor()

    cur.execute("select rowid,chat_identifier from chat")

    chat_row_id = cur.fetchall()

    #kprint(chat_row_id)

    Chats = {}

    for row in chat_row_id:
        chat_identifier = row[1]
        rowid = row[0]
        if chat_identifier in Chats:
            pass#cE(chat_identifier)
        else:
            Chats[chat_identifier] = {'chat_rowids':[]}#,'fist_name':'','last_name':''}
        Chats[chat_identifier]['chat_rowids'].append(rowid)

    #kprint(Chats)

    not_found_AB = []
    for p in AB:
        not_found = True
        n = AB[p].split(';')
        first_name = n[0]
        if len(n) > 1:
            last_name = n[1]
        else:
            last_name = ''
        for c in Chats:
            if p in c:
                Chats[c]['first_name'] = first_name
                Chats[c]['last_name'] = last_name
                not_found = False
        if not_found:
            safe_p = p#get_safe_name(p)
            Chats[safe_p] = {}
            Chats[safe_p]['first_name'] = first_name
            Chats[safe_p]['last_name'] = last_name
            Chats[safe_p]['chat_rowids'] = []       
            not_found_AB.append(p)

    for p in not_found_AB:
        #print(p,AB[p])
        pass

    People = {}
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
    #cm(len(People),r=0,a=0)
    #kprint(People,r=0)

    return People


def select_person(People,inp=''):
    """
    if not inp:
        s = input('Enter name or name part: ')
    else:
        s = inp
    """
    s = inp
    l = []
    #spacer = ''
    #if k[1]:
    #    spacer = ' '
    for k in People:
        #cm(k,r=0,a=1)
        #if s.lower() in (k[0]+spacer+k[1]).lower():
        #    l.append(k)
        _first,_last = k[0].lower(),k[1].lower()

        slo = s.lower()

        if False:
            cm(_first,_last,slo,a=0)
            if not _last and slo in _first:#_first[:min(len(slo),len(_first))]:
                cg(s,a=1)
                l.append(k)
            elif _last and ' ' in slo and slo in d2s(_first,_last)[:min(len(slo),1+len(_first)+len(_last))]:
                cy(s,a=1)
                l.append(k)
            else:
                cr(s,a=0)
                pass#cr(s)

        if slo in _first+' '+_last:
            l.append(k)

    pl = []
    for a in l:
        pl.append(a[0] + ' ' + a[1])
    k = select_from_list(l,print_lst=pl)
    if k:
        Person = {'name':{'first':k[0],'last':k[1]},'chat_identifiers':People[k]}
        return Person


def select_person_chats(People,inp='',max_tries=5):
    while True:
        #print('Selecting chats . . .')
        cg('Looking for',inp,'. . .')
        Person = select_person(People,inp=inp)
        if not Person:
            print('Try again.\n')
            max_tries -= 1
            if max_tries == 0:
                return None,None
            continue
        chats = []
        for k in Person['chat_identifiers']:
            for kk in Person['chat_identifiers'][k]['chat_rowids']:
                chats.append((kk,k))
        return Person,chats




def select_person_messages(People,inp='',start_mdy=(1,1,1900),end_mdy=(1,1,3001),conn=None):

    #inp = 'Yy'
    #start_mdy=(1,1,2001)
    #end_mdy=(1,1,3001)

    start_ts = str(month_day_year_to_MacTime(start_mdy[0],start_mdy[1],start_mdy[2]))
    end_ts   = str(month_day_year_to_MacTime(end_mdy[0],end_mdy[1],end_mdy[2]))

    Person,chats = select_person_chats(People,inp)

    qs = []

    cols_str = """
            message.rowid,
            message.text,
            message.service,
            message.date,          
            message.is_from_me,
            chat.rowid,
            chat.chat_identifier,
            chat.last_addressed_handle
    """
    cols = str_to_list(cols_str.replace(',',''))

    q_str = """
        select"""+cols_str+"""
        from
            message
            inner join chat_message_join ON chat_message_join.message_id = message.rowid
            inner join chat ON chat.rowid = chat_message_join.chat_id

        where
            message.date >= _START_
            and
            message.date <= _END_
            and
            chat_id = _CHAT_ID_"""

    print(chats)
    for chat_id,chat_identifier in chats:
        cur = conn.cursor()
        cur.execute(  q_str.replace('_START_',start_ts).replace('_END_',end_ts).replace('_CHAT_ID_',str(chat_id)) )
        qs += cur.fetchall()
        #qs += sql(q_str.replace('_START_',start_ts).replace('_END_',end_ts).replace('_CHAT_ID_',str(chat_id)))

    Messages = {}
    for q in qs:
        M = {}
        for i in rlen(cols):
            M[cols[i]] = q[i]
        Messages[q[0]] = M



    qs = []

    cols_str = """
        attachment.rowid,
        attachment.created_date,
        attachment.filename,
        attachment.mime_type,          
        message.rowid,
        chat.rowid
    """
    cols = str_to_list(cols_str.replace(',',''))

    q_str = """
        select"""+cols_str+"""
        from
            attachment
            inner join message_attachment_join ON message_attachment_join.attachment_id = attachment.rowid
            inner join message ON message.rowid = message_attachment_join.message_id
            inner join chat_message_join ON chat_message_join.message_id = message.rowid
            inner join chat ON chat.rowid = chat_message_join.chat_id
        where
            chat_id = _CHAT_ID_"""

    for chat_id,chat_identifier in chats:
        cur = conn.cursor()
        cur.execute( q_str.replace('_CHAT_ID_',str(chat_id)) )
        #qs += sql(q_str.replace('_CHAT_ID_',str(chat_id)))
        qs += cur.fetchall()


    Attachments = {}
    for q in qs:
        At = {}
        for i in rlen(cols):
            At[cols[i]] = q[i]
        Attachments[q[0]] = At


    for k in Messages:
        Messages[k]['Attachments'] = []
        Messages[k]['timestamp_GMT'] = MacTime_to_unixtime(Messages[k]['message.date']/1000000000)
        Messages[k]['timestamp'] = int( Messages[k]['timestamp_GMT'] - 8 * hours )
        Messages[k]['date'] = time_str('Pretty24',Messages[k]['timestamp'])

    for k in sorted(kys(Attachments)):
        Messages[ Attachments[k]['message.rowid'] ]['Attachments'].append( Attachments[k])


    return Person,Messages

    

###################

if __name__ == '__main__':
    #from bucket.idata.address_book import Address_book
    from address_book.Address_book import Address_book
    print(Address_book)
    #db_path = opjD('kMessages','chat.db')
    conn = sqlite3.connect(opjh('Library/Messages/chat-9-2022.db'))

    People = get_People(Address_book,conn)

    Person,Messages = select_person_messages(People,inp='',conn=conn)

    #kprint(Messages)
    print(Person)
    print(len(Messages),'messages')




#EOF




