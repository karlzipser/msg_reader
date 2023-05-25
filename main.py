
from utilz import *
import sqlite3
from msg_reader.format import filtered_to_html, select_people_for_sidebar
import msg_reader.R2dic as R2dic
from msg_reader.get_messages import get_People, select_person_messages
from address_book.Address_book import Address_book

Arguments = get_Arguments2(
    {
        'name' : 'nobody',
        'number' : 0,
        'my_first_name' : 'Karl',
        'start_date' : "1/1/2000",
        'end_date' : "1/1/3000",
        'dst' : opjD('Messages_html'),
        'mode' : '',
        'width' : 550,
        'flip' : False,
        'img_width' : 350,
        'time_gap_between_dates' : 10*minutes,
        'max_wordlength' : 40,
        'msg_count_date_gap' : 5,
        'chat_db' : opjh('Library/Messages/chat_copy.db'),
        #'Address_book' : Address_book, #opjh('address_book.py'),
        'R' : opjD('kMessages','R.pkl'),
        'Attachments' : opjD('kMessages','Attachments'),
        'open' : False,
        'archive_only' : False,
        'current_db_only' : True,
        'min_counts' : 0,
        'force_rewrite' : False,
        'batch' : False,
        'reverse' : False,
        'timing_file' : opjD('kMessages','chat.db-wal'),
        'num_latest' : 10000,
        'save_txt' : True,
    }
)

os_system('mkdir -p',opj( Arguments['dst'], 'counts'  ) )


if not Arguments['batch']:
    if not Arguments['name']:
        Arguments['name'] = input('Enter name or name part: ')
    Arguments['name'] = str(Arguments['name'])
    if Arguments['name']:
        assert not Arguments['number']
    if Arguments['number']:
        assert not Arguments['name']
        Arguments['name'] = str(Arguments['number'])
    assert len(Arguments['name'])


heics = find(opjh('Library/Messages/Attachments'),'*.heic')
heics += find(opjh('Library/Messages/Attachments'),'*.HEIC')
for h in heics:
    j = opj(h+'.jpg')
    if not len(sggo(j)):
        os_system('magick convert',qtd(h),qtd(j),e=1,a=1,r=0)




def main(name):
    #cr(name,r=0)

    conn = sqlite3.connect(Arguments['chat_db'])

    cur = conn.cursor()

    if 'Agument Address_book':
        cur.execute("select rowid,chat_identifier from chat")
        chat_row_id = cur.fetchall()
        #chat_row_id = sql('select rowid,chat_identifier from chat')
        chat_identifiers = set()
        for a in chat_row_id:
            chat_identifiers.add(a[1])
        found = []
        for a in Address_book:
            for b in chat_identifiers:
                if a in b:
                    found.append(b)
        chat_identifiers = chat_identifiers - set(found)
        for c in chat_identifiers:
            assert c not in Address_book
            Address_book[c] = c
    #so(opj(pname(Arguments['Address_book']),'Address_book_chat_augmented.pkl'),Address_book)

    People = get_People(Address_book,conn)


    Person = {'chat_identifiers':{},
        'name':{
            'first':name,#Arguments['name'],
            'last':''
        },
    }
    Messages = {}

    #cg('Looking for',name,'. . .')

    if not Arguments['archive_only']:
        if True:#try:
            Person,Messages = select_person_messages(People,inp=name,conn=conn)

            earliest_message_in_db = 10**20
            latest_message_in_db = 0

            for k in Messages:
                if Messages[k]['message.date'] < earliest_message_in_db:
                    earliest_message_in_db = Messages[k]['message.date']
                if Messages[k]['message.date'] > latest_message_in_db:
                    latest_message_in_db = Messages[k]['message.date']

            #cy(earliest_message_in_db)

        else:#except:
            cE('fist failed',r=False)

   
    if Person['name']['last']:
        name = d2s(Person['name']['first'],Person['name']['last'])
    else:
        name = Person['name']['first']
    html_filename = name+'.html'

    try:
        if not Arguments['force_rewrite']:
            t = 0
            t = os.path.getmtime(opj(Arguments['dst'],html_filename))
            #cm(MacTime_to_unixtime(latest_message_in_db/1000000000),t,r=0)
            if MacTime_to_unixtime(latest_message_in_db/1000000000) > t + 8 * hours :
                clp('Updating',html_filename,'. . .','`--rb')
                #cm(time_str('Pretty24',MacTime_to_unixtime(latest_message_in_db/1000000000)+ 8 * hours),time_str('Pretty24',t),r=0)
            else:
                clp(html_filename,'is up to date, exiting . . .','`--rb')
                #cm(0)
                return
                #cm(1)
        else:
            clp(html_filename,'force rewrite','`--rb')
    except:
        clp('Writing',html_filename,'. . .','`--rb')
        #cr(time_str('Pretty24',MacTime_to_unixtime(latest_message_in_db/1000000000)+ 8 * hours),'vs.',time_str('Pretty24',t),r=0)
    #cm(2)
    if not Arguments['current_db_only']:
        Messages_R = R2dic.get_MessageDic_from_R(list(set(kys(Person['chat_identifiers'])+[name])))
        #Messages_R = R2dic.get_MessageDic_from_R(kys(Person['chat_identifiers']))

        for k in Messages_R:
            if Messages_R[k]['message.date'] >= earliest_message_in_db:
                pass
            else:
                Messages[k] = Messages_R[k]
    
    cy(len(Messages),'texts',r=0)

    if not len(Messages):
        #cy('no texts')
        return

    html_str, raw_txts = filtered_to_html(
        Person,
        Messages,
        Arguments,
    )
    
    #cm(raw_txts,r=0,a=0)
    
    text_to_file(
        opj(
            Arguments['dst'],
            html_filename,
        ),
        html_str,
    )


    if Arguments['save_txt']:
        os_system('mkdir -p',qtd(opj(Arguments['dst'],'txt')),e=1)
        text_to_file(
            opj(
                Arguments['dst'],
                'txt',
                html_filename.replace('html','txt'),
            ),
            '\n\n'.join(raw_txts),
        )


    a = qtd(opj(Arguments['dst'],html_filename))
    old_counts = sggo(Arguments['dst'],'counts','*')
    for o in old_counts:
        if html_filename in o:
            os_system('rm',qtd(o),e=1)
    b = qtd(opj(Arguments['dst'],'counts',d2n(len(Messages),'.',html_filename)))
    #cm(a,b,r=1)
    os_system('ln -s', a, b , e=1)

    select_people_for_sidebar(Arguments)
    
    if Arguments['open']:
        os_system('open',qtd(opj(Arguments['dst'],html_filename)))


    




def batch():

    ks = kys(Address_book)

    people = []

    for k in ks:
        p = Address_book[k].replace(';',' ')
        people.append(p)

    people = sorted(list(set(people)))

    #kprint(people,title='Address_book people',r=0)

    for p in people:
        try:
            main( p )
        except KeyboardInterrupt:
            cE('*** KeyboardInterrupt ***')
            sys.exit()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            cE(exc_type,file_name,exc_tb.tb_lineno)
            #time.sleep(1)       




if __name__ == '__main__':

    if not Arguments['batch']:
        main(Arguments['name'])
    else:
        batch()
"""
Done or not needed:
    √--find unique stable identifier for messages which I can copy with click
    √--put in message text word count
    √--have what to mark older messages so they can be assembled
    √--get my name from somewhere, either default arg or from database
    √--get Karl-Karl and Karl-other working
    √--make sidebars for navigation
        √--left, dates
        √--right, people and modes for Karl
    √--convert heic
    √--in page tabs for different modes
    √--keep list of clicked timestamps in js and copy list to clipboard with each click
    √--allow image only and text only modes, as well as images plus associated text only
    √--allow closing of all non-selected messages
    --setup program that looks for database changes and updates .htmls
    --allow for search for patterns in texts
    --allow Karl only or other only outputs
    --put in calendar functionality, record of which entries have been added already
    --allow opening and closing of messages with click, so can locally customize
    --list messages by 100's within each month
    --reverse order mode
    --toggle visibility of id stamps (with hover)
"""

print("""
To do:
    --bring in old archived messages
    --daylight savings time CA
    √--collect chat_identifier's, list count in sidebar with option to choose one or all
    √--put hover enlarge for attatchment timestamps
    --put date and chat_identifier on timestamp line
    √--check for date ordering of rowid's
""")

# magick convert "Library/Messages/Attachments/ef/15/70D3A521-EF04-4883-9C8C-D39C385B553A/IMG_0188 copy-1.HEIC" "Library/Messages/Attachments/ef/15/70D3A521-EF04-4883-9C8C-D39C385B553A/IMG_0188 copy-1.HEIC.jpg"
#EOF
