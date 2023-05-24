from utilz import *
import html

if interactive():
  __file__ = opjk('misc/msg_reader/format.py')



def filtered_to_html(
    Person,
    Messages,
    A,
):
    A = limD(A,['my_first_name','dst','width',
            'img_width','time_gap_between_dates','max_wordlength',
            'msg_count_date_gap','Attachments',
            'reverse','num_latest'
        ],)

    import html

    M = Messages

    Dates = {}

    Chat_identifiers = {}

    to_name = Person['name']['first']

    from_name = A['my_first_name']
  
    html_html = ['<html>']


    messages_js_str, raw_txts = messages_to_js_map_str( Person, Messages, A )


    #kprint(messages_js_str)

    head_html = [
        "<head>",

        4*' '+'<link rel="stylesheet" href="file://'+opj(pname(__file__),'style.css')+'">',

        4*' '+'<script>'+'to_name = '+qtd(to_name)+'</script>',

        4*' '+'<script src="file://'+opj(pname(__file__),'script.js')+'"></script>',

        4*' '+'<script src="file:///Users/karlzipser/Desktop/kMessages/Mymap.js"></script>',

        4*' '+'<script src="file:///Users/karlzipser/Desktop/kMessages/setup_people.js"></script>',

        4*' '+'<title>'+to_name+'</title>',

        4*' '+'<link href="file:///Users/karlzipser/favicon.ico" rel="icon" type="image/x-icon">',

        messages_js_str,

        """<script>

        msg_kys = Object.keys(Messages)
        var n = __NUM_LATEST__
        var latest = []
        if ( msg_kys.length >= n ) {
            latest = msg_kys.slice(-n)
        }
        else { latest = msg_kys }

        var Message_lists = {
            'latest' : latest,
            'all' : msg_kys,
        }


        // general function
        function insert_messages_html(Messages,message_list) {
            //if (typeof message_list !== 'undefined') {
            //alert(message_list.length)
            var ms = message_list
            var s = ''
            var i
            for (i = 0; i < ms.length; i++) {
                //s += '<br>'
                s += Messages[ms[i]]
                //s += '<br>'

            }
            document.getElementById('__MESSAGE_LIST__').innerHTML = s
            console.log(s)
            //}
        }
        //alert(1)
        Mymap['Ping Wu']
        //alert(2)
        //alert(Message_lists['all'])
        if ( !(Mymap.includes('__TO_NAME__')) ) {

            Mymap['__TO_NAME__'] = {}
        }
        Mymap['__TO_NAME__']['all'] = Message_lists['all']
        Mymap['__TO_NAME__']['lastest'] = Message_lists['latest']
        //alert(Mymap)

        </script>

        """.replace('__NUM_LATEST__',str(A['num_latest'])).replace('__TO_NAME__',to_name),

        '</head>',
    ]
    

    body_html = [
        '<body id="the_body" onload="insert_messages_html(Messages,Message_lists[\'latest\']);setup_people(); setupToggles(to_name,Mymap,'+qtd(str(A['width'])+'px',1)+');">',
        4*' '+'<a id="TOP">',
        4*' '+"<H1>"+from_name+" to "+to_name+'</H1>',
    ]


    chat_html = ["""
    <div class="chat">

        <div id='__MESSAGE_LIST__'>
            (no messages)
        </div>

    </div>
"""]



    body_html += chat_html

    body_html.append(4*' '+'<div>')
    
    body_html.append(8*' '+'<div style="font-size:125%;">')

    #body_html.append(12*' '+'<br>'+html.escape('• • •').encode('ascii', 'xmlcharrefreplace').decode("utf-8")+'<br>')
    
    body_html.append(8*' '+'<a id="LATEST"><br><br>')

    body_html.append(4*' '+'. . . ' + from_name+" to "+to_name + ', latest<br><br></a>')
    
    if False:
        body_html.append( """
        <a id="abcd" href="#" onclick="insert_messages_html(Messages,Message_lists['all'])"> all </a>
        <br>
        <a id="abcd" href="#" onclick="insert_messages_html(Messages,Message_lists['latest'])"> latest </a>
        """
        )

    body_html.append(8*' '+'</div> <!--dot dot dot-->')

    
    
    body_html.append('</div> <!--body-->')



    html_html = ['<html>'] + head_html + body_html + ['</html>']


    html_str = '\n\n'.join(html_html)


    for d in Dates:
        first_d = Dates[d]['first']
        new_first = '<a id='+qtd(get_safe_name(first_d))+">"+first_d
        html_str = html_str.replace(first_d,new_first)


    html_str += get_sidebar(Messages,Dates,Chat_identifiers,from_name,to_name,A['dst'])

    

    return html_str, raw_txts









def messages_to_js_map_str(
    Person,
    Messages,
    A,
):
    A = limD(A,[
        'my_first_name','width',
        'img_width','time_gap_between_dates','max_wordlength',
        'msg_count_date_gap','Attachments',
        ],)

    import html

    M = Messages
    jsMessages = {}

    Dates = {}

    Chat_identifiers = {}

    to_name = Person['name']['first']

    from_name = A['my_first_name']
  
    _t_prev = 0
    _msg_count = 0

    ts = []
    message_rowids = []
    for k in M:
        ts.append(M[k]['message.date'])
        message_rowids.append(M[k]['message.rowid'])

    date_sorted = na(ts).argsort()

    loop_range = rlen(date_sorted)    

    raw_txts = []

    #loop_range = range(2000)

    for j in loop_range:

        i = date_sorted[j]

        rowid = message_rowids[i]

        me = M[rowid]['message.is_from_me']
        
        if i < len(message_rowids) - 1:
            if me == M[message_rowids[i+1]]['message.is_from_me']:
                _last = False
            else:
                _last = True
        else:
            _last = True

        t = M[rowid]['message.date']

        if len(M[rowid]['Attachments']):
            _attachment_modifier = '_with_attachment'
        else:
            _attachment_modifier = ''


        _message_identifier = rowid
        _message_identifier = d2n(to_name,'_',t)


        message_html = [
            '\n'+8*' '+'<!--==================================================================-->',
            d2n(8*' ','<div class="message_div',_attachment_modifier,'" id="',_message_identifier,'">'),
            d2n(12*' ','<div class="',get_safe_name(M[rowid]['chat.chat_identifier']),'">'),
        ]


        date_html = []
        if (t - _t_prev)/1000000000 > A['time_gap_between_dates'] or _msg_count > A['msg_count_date_gap']:
            date_html = [
                12*' '+'<div class="date'+_attachment_modifier+'">',
                d2n(16*' '+'<a id="a_date_',_message_identifier,'">'),
                16*' '+M[rowid]['date'],
                12*' '+'</div>  <!--date-->',
            ]
            _msg_count = -1

        if True:
            #
            if not _t_prev <= t:
                cE('not _t_prev <= t',_t_prev//1000000000, t//1000000000, (_t_prev - t)//(1*1000000000))
                #time.sleep(4)

        _t_prev = t
        _msg_count += 1
        

        message_html += date_html
        

        message_html.append(
            d2n(12*' '+'<div class="timestamp',
                _attachment_modifier+'" id="timestamp_',
                _message_identifier,'">',
                _message_identifier,' ',M[rowid]['chat.chat_identifier'],' ',
                M[rowid]['date'],'</div>'
            )
        )

        if M[rowid]['chat.chat_identifier'] not in Chat_identifiers:
            Chat_identifiers[ M[rowid]['chat.chat_identifier'] ] = 0
        Chat_identifiers[ M[rowid]['chat.chat_identifier'] ] += 1

        if me:

            if 'sms' in M[rowid]['message.service'].lower():
                message_html.append(12*' '+'<div class="mine_sms messages">')
            else:
                message_html.append(12*' '+'<div class="mine messages">')

        else:
            message_html.append(12*' '+'<div class="yours messages">')

        



        for B in M[rowid]['Attachments']:

            f = B['attachment.filename']

            if exname(f).lower() == 'heic':
                f = f +'.jpg'
            if f:
                if 'Attachments' in f:
                    f_s = f.split('Attachments/')
                    f = opj(A['Attachments'],f_s[1])
                    f = 'file://'+f.replace('~/',opjh())
                else:
                    cE(f)
                fn = fname(f)
                if len(fn) > A['max_wordlength']:
                    fn = fn[:A['max_wordlength']]+'...'

                if str(B['attachment.mime_type']) not in [
                    'video/mp4',
                    #'image/heic',
                    'application/pdf',
                    'image/png',
                    'image/gif',
                    #'text/x-python-script',
                    #'text/x-vlocation',
                    'image/jpeg',
                    #'audio/x-m4a',
                    #'application/zip',
                    'None',
                    'video/quicktime',
                    #'text/vcard',
                    #'text/rtf'
                    ]:
                    message_html.append(str(B['attachment.mime_type'])+'<br>')

                message_html += [
                    16*' '+'<!--****************************************************-->',
                    16*' '+'<a href="' + f + '"> <img src="' + f + '" alt="' + fn \
                        + '" style="max-width:'+str(A['img_width'])+'px"></a><br>',
                    16*' '+'<!--****************************************************-->',
                ]


        if _last:
             message_html.append(16*' '+'<div class="message last">')
        else:
            message_html.append(16*' '+'<div class="message">')


        if M[rowid]['message.text']:
            txt = M[rowid]['message.text']
            #txt = html.escape(txt)
            txt = txt.replace('\\','')

            raw_txts.append(txt)
            txt = txt.split(' ')
            
            for j in rlen(txt):
                if len(txt[j]) > A['max_wordlength']:
                    txt[j] = txt[j][:A['max_wordlength']]+'...'
            tx = ' '.join(txt)
            tx = html.escape(tx).encode('ascii', 'xmlcharrefreplace').decode("utf-8")
            tx = tx.replace('\n','\n<br>')

            message_html.append( 20*' '+tx )

        message_html.append(16*' '+'</div> <!--message (last?)-->')
        message_html.append(12*' '+'</div> <!--mine/yours-->')
        message_html.append(12*' '+'</div> <!--chat_identifier-->')
        message_html.append(8*' '+'</div> <!--message_div-->')

        jsMessages[_message_identifier] = message_html



    ks = sorted(kys(jsMessages))
    js = ['var Messages = {']
    for k in ks:
        js.append( d2s( qtd(k,s=1), ': `\n', '\n'.join(jsMessages[k]),'\n`,\n') )
    js.append('}\n')

    messages_js_str = '\n'.join(js)

    #messages_js_str = html.escape(messages_js_str)

    return '<script>\n'+messages_js_str+'\n</script>', raw_txts












def get_sidebar(Messages,Dates,Chat_identifiers,from_name,to_name,dst):
    
    safe_chat_identifiers = []
    for c in Chat_identifiers:
        safe_chat_identifiers.append(get_safe_name(c))

    chat_id_on_str = d2n('chat_id_on(',qtd('_all_',1),',',safe_chat_identifiers)+'); '


    h = """


<div id="mySidenav" class="sidenav">

<a href="javascript:void(0)" class="closebtn" onclick=\""""+chat_id_on_str+"""closeNav()">&times;</a><br><br><br>

<a id="toggleText_link" href="#" onclick=\""""+chat_id_on_str+"""toggleText(1);return false;">Text On</a>/
<a id="toggleText_link" href="#" onclick=\""""+chat_id_on_str+"""toggleText(0);return false;"> Off</a>

<div id="toggleDiv_links">

</div>"""


    for k in Chat_identifiers:
        h += d2s('<a id="abcd" href="#" onclick="chat_id_on(',
            qtd(get_safe_name(k),1),
            ',',
            safe_chat_identifiers,
            ')',';return false;">',k+':',Chat_identifiers[k],'</a><br>')

    h += """
<br>
<a href="#TOP" style="font-size:150%">_FROM_ to _TO_</a><br>
<a href="#LATEST" style="font-size:150%">Latest</a><br>

"""
    total_count = 0
    total_word_count = 0
    kprint(Dates)
    for d in Dates:
        c = Dates[d]['count']
        w = Dates[d]['word_count']
        total_count += c
        total_word_count += w
        first = Dates[d]['first']
        h += d2n("<a href=",qtd('#'+get_safe_name(first)),">",d,' (')+f'{c:,}'+") "+f'{w:,}'+"</a><br>\n"

    h += '<br>'
    #h += d2n("<a>Totals:<br>",f'{total_count:,}',' texts<br>',f'{total_word_count:,}',' words</a><br>\n<br>\n')
    h += d2n("<a>Totals:<br>&ensp;",len(Messages),' texts<br>')#,total_word_count,' words</a><br>\n<br>\n')

    cb(d2n("<a>Totals:<br>",len(Messages),' texts<br>',total_word_count,' words</a><br>\n<br>\n'))

    h += '<div id="people_links">YYY</div>'





    h += """</div>
<span style="font-size:30px;cursor:pointer;position:fixed;left:0px;top:0px;" onclick="openNav()">
  &#9776; 
</span> 
<span style="font-size:100%;cursor:pointer;position:fixed;left:30px;top:15px" onclick="openNav()"></span>
"""
    if False:
        h += """
            <a style="font-size:150%;">

                <br>&#8226; &#8226; &#8226;<br><br><br>

            </a>
    """
    h += "\n</div>\n"


    return h.replace('_FROM_',from_name).replace('_TO_',to_name)



def select_people_for_sidebar(A):
    A = limD(A,['dst','min_counts'])
    people = sggo(A['dst'],'*.html')
    
    if A['min_counts'] > 0:
        cm(len(people),r=0,a=0)
        _counts = sggo(A['dst'],'counts','*.html')
        people_with_counts = []
        for c in _counts:
            count = fname(c).split('.')[0]
            if int(count) >= A['min_counts']:
                people_with_counts += [fname(c).split('.')[1]]
        _people = []
        for p in people:
            for c in people_with_counts:
                if c in p:
                    _people += [p]
                    break
        people = _people
        cy(len(people),r=0)
    
    s = ['function setup_people() {\n    s = \'\';']
    for p in people:
        if p[0] != '_':
            person_name = fnamene(p)
            s += [ '    s += ' + qtd(d2n('<a href="file://',p,'#LATEST", style="font-size:150%">',person_name,'</a><br>'),s=1)+';']
    s += [  '    s += ' + qtd(d2n('<a style=\"align-items: center\"><br>&#8226; &#8226; &#8226;</a><br><br><br>'),s=1)+';' ]
    s += ["""    document.getElementById("people_links").innerHTML = s;""" ]
    s += [    '    /*alert(s);*/\n}']
    js = '\n'.join(s)
    text_to_file(opjD('kMessages','setup_people.js'),js)
#EOF


