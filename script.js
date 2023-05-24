

function setupToggles(to_name,Mymap,width_px_str) {
  
  document.getElementById("the_body").style.maxWidth = width_px_str;
  s = "";
  Person = Mymap[to_name];
  if (Person) {
    for ( [key, value] of Object.entries(Person)) {
      //(Messages,message_list)
      a = '<a id="toggleDiv_link" href="#" onclick="insert_messages_html(Messages,Mymap[\''+to_name+'\'][\''+key+'\']);return false;">'+key+'</a><br>\n';
      //alert(a)
      s += a
      //s += '<a id="toggleDiv_link" href="#" onclick="toggleDiv(\''+to_name+'\',\''+key+'\');return false;">'+key+'</a><br>\n';
    }
    document.getElementById("toggleDiv_links").innerHTML = s;
  }
}

function toggleText(turn_on) {
  var myStringArray = ["message_div",'message_div_with_attachment','date'];/*,"timestamp",'date'];*/
  var arrayLength = myStringArray.length;
  for (var ii = 0; ii < arrayLength; ii++) {
    c = myStringArray[ii];
    var w = document.getElementsByClassName(c);
    var i;
    for (i = 0; i < w.length; i++) {
      x = w[i]
      x.style.display = "block";
    }
  }
  var myStringArray = ["message_div",'date'];/*,"timestamp",'date'];*/
  var arrayLength = myStringArray.length;
  for (var ii = 0; ii < arrayLength; ii++) {
    c = myStringArray[ii];
    var w = document.getElementsByClassName(c);
    var i;
    for (i = 0; i < w.length; i++) {
      x = w[i]
      if (turn_on) {
        x.style.display = "block";
      } else {
        x.style.display = "none";
      }
    }
  }
}


function chat_id_on(chat_identifier,full_list) {
  for (var ii = 0; ii < full_list.length; ii++) {
    c = full_list[ii];
    var w = document.getElementsByClassName(c);
    
    var i;
    for (i = 0; i < w.length; i++) {
      x = w[i]
      if (c == chat_identifier || chat_identifier == '_all_') {
        x.style.display = "block";
      } else {
        x.style.display = "none";
      }
    }
  }
}


function toggleDiv(to_name,topic) {
  var cs = ["message_div",'message_div_with_attachment'];
  for (var ii = 0; ii < cs.length; ii++) {
    c = cs[ii];
    var w = document.getElementsByClassName(c);
    var i;
    for (i = 0; i < w.length; i++) {
      x = w[i];
      if ( Mymap[to_name][topic].includes(x.id) ) {
        x.style.display = "block";
      } else {
        x.style.display = "none";
      }
    }
  }
}


function openNav() {
  document.getElementById("mySidenav").style.width = "300px";
  document.getElementById("main").style.marginLeft = "300px";
}


function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  document.getElementById("main").style.marginLeft= "0";
}

