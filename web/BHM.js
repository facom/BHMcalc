/*
###################################################
#  ____  _    _ __  __           _      
# |  _ \| |  | |  \/  |         | |     
# | |_) | |__| | \  / | ___ __ _| | ___ 
# |  _ <|  __  | |\/| |/ __/ _` | |/ __|
# | |_) | |  | | |  | | (_| (_| | | (__ 
# |____/|_|  |_|_|  |_|\___\__,_|_|\___|
# v2.0
###################################################
# 2014 [)] Jorge I. Zuluaga, Viva la BHM!
###################################################
# JAVASCRIPT ROUTINES
###################################################
*/
function changeValues(others,object)
{
    /*
      Change the value of others according to the value of object
    */
    for(var i=0;i<=others.length;i++){
	$(others[i]).attr('value',$(object).val())
    }
}

function loadContent(script,element,
		     onsuccessfunc,onwaitfunc,onerrorfunc,
		     timeout,async)
{
    var x=new XMLHttpRequest();
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

function changeAjax(script,source,target)
{
    loadContent(script+"&val="+$(source).val(),
		$(target),
		function(element,rtext){
		    //element.css('background','yellow');
		    element.val(rtext);
		},
		function(element,rtext){
		    //element.css('background','lightgreen');
		    element.val("Computing...");
		},
		function(element,rtext){
		    //element.css('background','pink');
		    element.val("Error...");
		},
		-1,true);
}

function loadAjax(script,target)
{
    loadContent(script,
		$(target),
		function(element,rtext){
		    //element.css('background','yellow');
		    element.html(rtext);
		},
		function(element,rtext){
		    //element.css('background','lightgreen');
		    element.html("Loading...");
		},
		function(element,rtext){
		    //element.css('background','pink');
		    element.html("Error...");
		},
		-1,true);
}

function forceUpdate(force,qover)
{
    status=$(force).html();
    if(status=="Force"){
	$(force).html("Smart");
	$(qover).attr("value",0);
    }else{
	$(force).html("Force");
	$(qover).attr("value",1);
    }
}

function adjustiFrame(iframe)
{
    height=iframe.contentWindow.document.body.offsetHeight+"px";
    $(iframe).attr("height",height);
}

function refreshiFrame(iframe)
{
    $(iframe).attr("src",$(iframe).attr("src"));
}

function display(element){
    $('#'+element).toggle('fast',null);
}

function refreshiFrames(){
    $(".iframe").each(function() { 
        var src=$(this).attr('src');
        $(this).attr('src',src);  
    });
}

function idSystem(){
    //IT SHOULD BE THE WHOLE FORM
    var forms=["star1_form","star2_form","planet_form","binary_form"];
    var sysid="";
    for(i=0;i<3;i++){
	elements=document.forms[forms[i]].elements;
	for(j=0;j<elements.length;j++){
	    clase=elements[j].getAttribute("class")+"";
	    if(clase.search("sensitive")>=0){
		val=elements[j].value;
		sysid=sysid+val;
	    }
	}
    }
    var sys=calcMD5(sysid);
    $('.sys_input').attr("value","\"\'"+sys+"\'\"");
    //alert($('.sys_input').attr("value"));
}

