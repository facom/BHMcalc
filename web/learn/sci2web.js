/*
  ////////////////////////////////////////////////////////////////////////////////
  BASIC
  ////////////////////////////////////////////////////////////////////////////////
 */

/*
  OPEN WINDOWS
 */
function Open(url,name,options)
{
    window.open(url,name,options);
}

function openThis(linkid,name,options)
{
    url=$('#'+linkid).attr('url');
    window.open(url,name,options);
}

/*
  CLOSE WINDOWS
 */
function Close()
{
    window.close();
}

/*
 */
function Reload()
{
    window.location.reload();
}

/*
  ////////////////////////////////////////////////////////////////////////////////
  FORMS
  ////////////////////////////////////////////////////////////////////////////////
 */
function clickRow(row)
{
    unchecked=$(row).attr('color_unchecked');
    checked=$(row).attr('color_checked');
    if(!row.checked){
	row.parentNode.parentNode.style.backgroundColor=unchecked;
    }else{
	row.parentNode.parentNode.style.backgroundColor=checked;
    }
}

function clickRow2(row)
{
    unchecked=$(row).attr('color_unchecked');
    checked=$(row).attr('color_checked');
    if(!row.checked){
	$(row.parentNode.parentNode).css('background-color',unchecked);
    }else{
	$(row.parentNode.parentNode).css('background-color',checked);
    }
}

function enableElement(check)
{
    elname=$(check).attr("name").split("_")[0];
    element_enabled=$('[name="'+elname+'"]');
    if(!check.checked){
	element_enabled.attr("disabled",true);
    }else{
	element_enabled.attr("disabled",false);
    }
}

function popOutHidden(field)
{
    var sname=$(field).attr("name")+'_Submit';
    var hfield=$('input[name="'+sname+'"]');
    newvalue=$(field).attr("value");
    if(hfield.length==0){
	var newfield=$(field).clone();
	$(newfield).
	  attr("name",sname).
	  attr("type","hidden").
	  attr("value",newvalue);
	$(field).after(newfield);
    }
    hfield=$('input[name="'+sname+'"]');
    value=hfield.attr("value");
    if($(field).attr("type")=="checkbox"){
      if(field.checked){
	newvalue="on";
 	$(field).attr("value","on"); 
      }else{
	newvalue="off";
 	$(field).attr("value","off"); 
      }
    }
    //alert("Element "+$(hfield).attr("name")+" Changed from "+value+" to "+newvalue);
    hfield.attr("value",newvalue);
}

function popOutHidden2(field)
{
    var sname=$(field).attr("name")+'_Submit';
    var hfield=$('input[name="'+sname+'"]');

    //alert("Name:"+$('input[name="'+sname+'"]').attr('name'));

    newvalue=$(field).attr("value");
    if($(field).attr("type")=="checkbox"){
      if(field.checked){
	newvalue="on";
 	$(field).attr("value","on"); 
      }else{
	newvalue="off";
 	$(field).attr("value","off"); 
      }
    }
    hfield.attr("value",newvalue);
}

/*
  ////////////////////////////////////////////////////////////////////////////////
  DEBUGGING
  ////////////////////////////////////////////////////////////////////////////////
 */

/*
  CHANGE DEBUGGING LINK
 */
function fileDebug(select,fileopts,winprops)
{
  option=select.options[select.selectedIndex];
  value=option.value;
  document.getElementById("server").href="JavaScript:Open('"+fileopts+"&File=phpdb-"+value+"','File','"+winprops+"')";
  document.getElementById("stdout").href="JavaScript:Open('"+fileopts+"&File=phpout-"+value+"','File','"+winprops+"')";
  document.getElementById("stderr").href="JavaScript:Open('"+fileopts+"&File=phperr-"+value+"','File','"+winprops+"')";
  document.getElementById("mysql").href="JavaScript:Open('"+fileopts+"&File=phpsql-"+value+"','File','"+winprops+"')";
}

/*
  CHANGE NEW LINK
 */
function configureNew(select,fileopts,winprops)
{
  option=select.options[select.selectedIndex];
  value=option.value;
  document.getElementById("new").href="JavaScript:Open('"+fileopts+"&Template="+value+"','Configure','"+winprops+"')";
}

/*
  ////////////////////////////////////////////////////////////////////////////////
  AJAX
  ////////////////////////////////////////////////////////////////////////////////
 */

/*
  GENERAL LOAD CONTENT
 */
function loadContent(script,elementid,
		     onsuccessfunc,onwaitfunc,onerrorfunc,
		     timeout,async)
{
  var x=new XMLHttpRequest();
  var element=document.getElementById(elementid);
  x.onreadystatechange=function(){
    rtext=x.responseText;
    if(x.readyState==4){
      if(x.status==200){
	onsuccessfunc(element,rtext);
	x.abort();
      }else{
	onerrorfunc(element,rtext);
	x.abort();
      }
    }else{
      onwaitfunc(element,rtext);
    }
  }
  x.open("POST",script,async);
  x.send();
  if(timeout>0){
      callback="loadContent('"+script+"','"+elementid+"',"+onsuccessfunc.toString()+","+onwaitfunc.toString()+","+onerrorfunc.toString()+","+timeout.toString()+","+async.toString()+")";
      setTimeout(callback,timeout);
  }
}

/*
  WRITE FILE
 */
function writeFile(file,msg,writescr)
{
    script=writescr+"?File="+file+"&Content="+msg;
    var x=new XMLHttpRequest();
    x.onreadystatechange=function(){
	if(x.readyState==4){
	    if(x.status==200){
		//alert(x.responseText);
	    }
	}
    }
    x.open("GET",script,true);
    x.send();
}

/*
  TOGGLE ELEMENT
 */
function toggleElement(elementid)
{
  $("#"+elementid).toggle('fast',null);
}

function showElement(elementid)
{
  $("#"+elementid).show('fast',null);
}

/*
  CHANGE TO EDITOR
 */
function toggleToEdition(view,edit,link,color,ckfinder)
{
    $('#'+view).css("display","none");
    CKEDITOR.replace(edit,
    {
    uiColor:color,
    filebrowserBrowseUrl : ckfinder+'/ckfinder.html',
    filebrowserImageBrowseUrl:ckfinder+'/ckfinder.html?Type=Images',
    filebrowserFlashBrowseUrl:ckfinder+'/ckfinder.html?Type=Flash',
    filebrowserUploadUrl:ckfinder+'/core/connector/php/connector.php?command=QuickUpload&type=Files',
    filebrowserImageUploadUrl:ckfinder+'/core/connector/php/connector.php?command=QuickUpload&type=Images',
    filebrowserFlashUploadUrl:ckfinder+'/core/connector/php/connector.php?command=QuickUpload&type=Flash',
    height:'400'
    });
    $('#'+link).html("<input type='submit' name='SaveContent' value='Save'><input type='submit' name='Cancel' value='Cancel'>");
}

/*
  CHANGE TO EDITOR
 */
function toggleHidden(object,hclass,symbols){
    hclassjq="."+hclass;
    if($(object).attr("action").search(/More/i)>=0){
	$(object).attr("action","Less");
	$(object).html(symbols["Less"]);
	$(hclassjq).slideDown('fast',null);
    }else{
	$(object).attr("action","More");
	$(object).html(symbols["More"]);
	$(hclassjq).slideUp('fast',null);
    }
}

/*
  SUBMIT FORM 
 */
function submitForm(formid,script,
		    elementid,onsuccessfunc,onwaitfunc,onerrorfunc)
{
  var x=new XMLHttpRequest();
  var element=document.getElementById(elementid);
  var form=document.getElementById(formid);
  
  //GET SUBMIT FORM ELEMENTS
  i=0;
  qstring="";
  while(formel=form.elements[i]){
      if(esname=$(formel).attr("name")){
	  //alert(esname);
	  if(esname.search("_Submit")>=0){
	      ename=esname.split("_")[0];
	      qstring+=ename+"="+$(formel).attr("value")+"&";
	  }
      }
      i++;
  }
  script=script+"&"+qstring;
  //alert(script);
  
  x.onreadystatechange=function(){
    rtext=x.responseText;
    if(x.readyState==4){
      if(x.status==200){
	onsuccessfunc(element,rtext);
      }else{
	onerrorfunc(element,rtext);
      }
    }else{
      onwaitfunc(element,rtext);
    }
  }

  x.open("GET",script,true);
  x.send();
}

function trim(s)
{
    return rtrim(ltrim(s));
}

function ltrim(s)
{
    var l=0;
    while(l < s.length && s[l] == ' ')
	{l++; }
    return s.substring(l, s.length);
}

function rtrim(s)
{
    var r=s.length -1;
    while(r > 0 && s[r] == ' ')
	{r-=1;}
    return s.substring(0, r+1);
}

function rtrimc(s,c)
{
    var r=s.length -1;
    while(r > 0 && s[r] == c)
	{r-=1;}
    return s.substring(0, r+1);
}

/*
  SUBMIT FORM 
 */
function multipleAction(formid,script,parameter,winprops)
{
  var form=document.getElementById(formid);

  //GET SUBMIT FORM ELEMENTS
  i=0;
  inputscr="";
  while(formel=form.elements[i]){
      if($(formel).attr("type")=="checkbox" &&
	 $(formel).attr("name")!="objall"){
	  if(formel.checked){
	      obj=$(formel).attr("represent");
	      inputscr+=obj+",";
	  }
      }
      i++;
  }
  if(inputscr!=""){
      subscr=script+"&"+parameter+"="+rtrimc(inputscr,',');
      Open(subscr,'Multiple Action',winprops);
  }else{
      alert("You must select at least one data file");
  }
}

function notDiv(notid,text)
{
    $('#'+notid).html(text);
    $('#'+notid).fadeIn(1000,null);
    setTimeout("$('#"+notid+"').fadeOut(5000,null)",2000);
}

function explainThis(object)
{
  name=$(object).attr("name");
  explanation=$(object).attr("explanation");
  boxclass="explanation";
  boxref='.'+boxclass;

  lexpl=strLength(explanation);
  if(lexpl>1000){
      boxwidth=lexpl/2;
      boxheight=(lexpl/50)*7;
  }else{
      boxwidth=lexpl;
      boxheight=15;
  }
  elheight=$(object).height();
  elwidth=$(object).width();
  if(elheight>15) elheight=15;

  boxtop=-elheight;
  winwidth=$(window).width();
  posexpl=$(object).offset().left;
  if(posexpl<winwidth/2){
      boxleft=elwidth+5;
  }else{
      boxleft=-lexpl-5;
  }
  
  unheight="px";
  unwidth="px";
  $.openDOMWindow({
        height:boxheight+unheight,
	width:boxwidth+unwidth,
	positionType:'anchored', 
	anchoredClassName:boxclass, 
	anchoredSelector:object,
	positionTop:boxtop,
	positionLeft:boxleft,
	borderSize:1,
	loader:0,
	windowBGColor:"lightgray",
	windowPadding:2
	}
    );

  $(boxref).css("font-size","12px");
  $(boxref).html(explanation);

  $(this).
    mouseout(function(){$.closeDOMWindow({anchoredClassName:boxclass});});
}

function check()
{
  alert('Hola');
}

function strLength(string)
{
  var ruler=$("#RULER");
  ruler.html(string);
  return ruler.width();
}

function updateSlider(varid)
{
    input=$("#"+varid);
    value=input.attr("value");
    valueSlider(varid,0,0,value);
}

function valueSlider(varid,newpos,delsgn,value)
{
    ////////////////////////////////////////////////////
    //COMPONENTS
    ////////////////////////////////////////////////////
    cont=$("#"+varid+"_container");
    button=$("#"+varid+"_button");
    input=$("#"+varid);
    bar=$("#"+varid+"_bar");

    ////////////////////////////////////////////////////
    //PROPERTIES OF VARIABLE
    ////////////////////////////////////////////////////
    val=parseFloat(input.attr("value"));
    pos=parseFloat(bar.css("left"));
    max=parseFloat(input.attr("max"));
    min=parseFloat(input.attr("min"));
    delta=parseFloat(input.attr("delta"));

    ////////////////////////////////////////////////////
    //GEOMETRICAL PROPERTIES OF SLIDER
    ////////////////////////////////////////////////////
    width=parseFloat(cont.css("width"));
    wbut=parseFloat(button.css("width"));
    wbar=parseFloat(bar.css("width"));
    minpos=wbut;
    maxpos=width-wbut-wbar;
    pos2val=(max-min)/(maxpos-minpos);

    ////////////////////////////////////////////////////
    //NEW VALUE
    ////////////////////////////////////////////////////
    if(newpos>0){
	newval=min+pos2val*(newpos-wbut);
    }else{
	if(Math.abs(delsgn)>0){
	    delval=delsgn*delta
	}else{
	    delval=parseFloat(value)-min;
	    val=min;
	    pos=minpos;
	}
	newval=val+delval;
	newpos=pos+delval/pos2val;
	if(newpos>maxpos) newpos=maxpos;
	if(newpos<minpos) newpos=minpos;
	bar.css("left",newpos);
    }
    if(newval<min) newval=min;
    if(newval>max) newval=max;
    newval=Math.round(newval*100)/100;
    //$("#report").html("val:"+val+",pos:"+pos+",delta:"+delta+",deltaval:"+delval+",newval:"+newval+",newpos:"+newpos);
    input.attr("value",newval);
}

function posSlider(varid,newpos)
{
    ////////////////////////////////////////////////////
    //COMPONENTS
    ////////////////////////////////////////////////////
    cont=$("#"+varid+"_container");
    button=$("#"+varid+"_button");
    bar=$("#"+varid+"_bar");

    ////////////////////////////////////////////////////
    //GEOMETRICAL PROPERTIES OF SLIDER
    ////////////////////////////////////////////////////
    width=parseFloat(cont.css("width"));
    wbut=parseFloat(button.css("width"));
    wbar=parseFloat(bar.css("width"));
    minpos=wbut;
    maxpos=width-wbut-wbar;
   
    pos=newpos;
    if(pos<minpos){
	pos=minpos;
	cont.die("mousemove");
    }
    if(pos>maxpos){
	pos=maxpos;
	cont.die("mousemove");
    }

    return pos;
}

function moveSlider(varid)
{
    ////////////////////////////////////////////////////
    //COMPONENTS
    ////////////////////////////////////////////////////
    cont=$("#"+varid+"_container");
    input=$("#"+varid);
    button=$("#"+varid+"_button");
    slider=$("#"+varid+"_slider");
    bar=$("#"+varid+"_bar");

    ////////////////////////////////////////////////////
    //GEOMETRICAL PROPERTIES OF SLIDER
    ////////////////////////////////////////////////////
    width=parseFloat(cont.css("width"));
    wbut=parseFloat(button.css("width"));
    wbar=parseFloat(bar.css("width"));
    wsli=parseFloat(slider.css("width"));
    minpos=wbut;
    maxpos=width-wbut-wbar;
    ////////////////////////////////////////////////////
    //ACTIONS
    ////////////////////////////////////////////////////
    if(slider.attr("dragged").search(/true/)>=0){
	cont.live("mousemove",function(e){
		posx=e.pageX-this.offsetLeft-wsli/2;
		valueSlider(varid,posx,0,0);
		posl=posSlider(varid,posx);
		bar.css("left",posl+"px");
	    });
    }else{
	cont.die("mousemove");
    }
    cont.click(function(e){
	    posx=e.pageX-this.offsetLeft-wsli/2;
	    posl=posSlider(varid,posx);
	    if(posl>minpos && posl<maxpos){
		valueSlider(varid,posx,0,0);
		bar.css("left",posl+"px");
	    }
	});
}

function checkInputValue(id,type,reference)
{
    inpel=$("#"+id);
    value=inpel.attr("value");
    qerror=false;
    if(type.search(/minmax/)>=0){
	min=reference['min'];
	max=reference['max'];
	if(value<min){
	    inpel.attr("value",min);
	    qerror=true;
	}
	if(value>max){
	    inpel.attr("value",max);
	    qerror=true;
	}
	if(qerror)
	    alert("Input value should be in the interval ("+
		  min+","+max+")");
    }
}

function queryResultsDatabase(form,resultsid,script)
{
    results=document.getElementById(resultsid);
    querytxt=form.elements[0].value;
    scripturl=script+"Query="+querytxt;
    loadContent(scripturl,resultsid,
		function(element,rtext){
		    element.innerHTML=rtext;
		    $('#DIVBLANKET').css('display','none');
		    $('#DIVOVER').css('display','none');
		},
		function(element,rtext){
		    $('#DIVBLANKET').css('display','block');
		    $('#DIVOVER').css('display','block');
		},
		function(element,rtext){
		    $('#DIVBLANKET').css('display','none');
		    $('#DIVOVER').css('display','none');
		    element.innerHTML="ERROR";
		},
		-1,
		true
		);
}

function selectAll(formid,object)
{
    form=document.getElementById(formid);
    valueall=object.value;
    checkall=object.checked;
    i=0;
    while(formel=form.elements[i]){
	if(formel.type.search("checkbox")>=0){
	    formel.checked=checkall;
	    formel.value=valueall;
	    namel=formel.name;
	    valel=formel.value;
	    subel=$("input[name="+namel+"_Submit]");
	    subel.attr("value",valel);
	    subel.checked=checkall;
	}
	i++;
    }
}

function deselectAll(allname)
{
    $('input[name='+allname+']').attr('checked',false);
    $('input[name='+allname+'_Submit]').attr('checked',false);
    $('input[name='+allname+'_Submit]').attr('value','off');
}

function toggleBug(elementid,referer)
{
  delement=document.getElementById(elementid);
  element=$("#"+elementid);
  wbox=element.width();
  poslft=referer.offsetLeft;
  postop=referer.offsetTop;
  element.css("top",postop);
  element.css("left",poslft);
  element.toggle('fast',null);
}

function setValue(elementid,value)
{
  element=document.getElementById(elementid);
  $(element).attr("value",value);
}

function downloadFile(url)
{
    window.open(url,'Download');
}

function randomStr(size)
{
    var text="";
    var possible="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    for(var i=0;i<size;i++)
        text+=possible.charAt(Math.floor(Math.random()*possible.length));
    return text;
}

/*
  SHORT CUTS
*/
var isCtrl=false;
$(document).keyup(function(e){
	if(e.which==17) isCtrl=false;
    }).keydown(function(e){
	    if(e.which==17) isCtrl=true;
	    /*CTRL+RIGHT*/
	    if(e.which==39 && isCtrl == true) {
		tabid=$("#CtrlTabId").attr("value");
		tabnum=$("#CtrlTabNum").attr("value");
		tabnext=(parseInt(tabid)+1)%(tabnum+1);
		if(tabnext>tabnum) tabnext=1;
		document.location.href="?TabId="+tabnext;
		return false;
	    }
	    /*CTRL+LEFT*/
	    if(e.which==37 && isCtrl == true) {
		tabid=$("#CtrlTabId").attr("value");
		tabnum=$("#CtrlTabNum").attr("value");
		tabnext=(parseInt(tabid)-1)%(tabnum+1);
		if(tabnext<=0) tabnext=tabnum;
		document.location.href="?TabId="+tabnext;
		return false;
	    }
	});

/*
KEYS CODES:
Backspace:8
Tab:9
Enter:13
Shift:16
Ctrl:17
Alt:18
Pause:19
Capslock:20
Esc:27
Page up:33
Page down:34
End:35
Home:36
Left arrow:37
Up arrow:38
Right arrow:39
Down arrow:40
Insert:45
Delete:46
0:48
1:49
2:50
3:51
4:52
5:53
6:54
7:55
8:56
9:57
a:65
b:66
c:67
d:68
e:69
f:70
g:71
h:72
i:73
j:74
k:75
l:76
m:77
n:78
o:79
p:80
q:81
r:82
s:83
t:84
u:85
v:86
w:87
x:88
y:89
z:90
0 (numpad):96
1 (numpad):97
2 (numpad):98
3 (numpad):99
4 (numpad):100
5 (numpad):101
6 (numpad):102
7 (numpad):103
8 (numpad):104
9 (numpad):105
*:106
+:107
-:109
.:110
/:111
F1:112
F2:113
F3:114
F4:115
F5:116
F6:117
F7:118
F8:119
F9:120
F10:121
F11:122
F12:123
=:187
Coma:188
Slash /:191
Backslash \:220
*/
