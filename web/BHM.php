<?PHP
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
# Web Interface
###################################################
*/
?>
<?PHP
//////////////////////////////////////////////////////////////
//PACKAGES
//////////////////////////////////////////////////////////////
include_once("web/BHMcss.php");

//////////////////////////////////////////////////////////////
//GLOBAL VARIABLES
//////////////////////////////////////////////////////////////
$CONTENT="";

//PYTHON COMMAND
$PYTHONCMD="MPLCONFIGDIR=/tmp python";

//LOCATION
$ROOTDIR=preg_replace("/BHMcalc/","",rtrim(shell_exec("pwd")));
$wDIR="BHMcalc/";
$DIR=$ROOTDIR.$wDIR;

//OTHER DIRECTORIES
$wSYSDIR=$wDIR."sys/";
$SYSDIR=$ROOTDIR.$wSYSDIR;

$wTMPDIR="tmp/";
$TMPDIR=$ROOTDIR.$wDIR.$wTMPDIR;

//GET VARIABLES
foreach(array_keys($_GET) as $field){
    $$field=$_GET[$field];
}
foreach(array_keys($_POST) as $field){
    $$field=$_POST[$field];
}
$GETSTR=print_r($_GET,true);
$POSTSTR=print_r($_POST,true);
if(isset($VERBOSE)){$VERBOSE=1;}
else{$VERBOSE=0;}

//////////////////////////////////////////////////////////////
//SESSION ID
//////////////////////////////////////////////////////////////
if(!isset($_SESSION)){session_start();}
$SESSID=session_id();
$wSESSDIR=$wSYSDIR."$SESSID/";
$SESSDIR=$ROOTDIR.$wSESSDIR;

//////////////////////////////////////////////////////////////
//ROUTINES
//////////////////////////////////////////////////////////////
function mainHeader()
{
  global $CSS;

$HEADER=<<<HEADER
<head>
  <script src="web/jquery.js"></script>
  <script src="web/BHM.js"></script>
  <script src="web/tabber.js"></script>
  $CSS
  <script>
  function display(element){
      $('#'+element).toggle('fast',null);
  }
  </script>
</head>
HEADER;
 return $HEADER;
}

function selectFunction($name,$selection,$defvalue){
$sel=<<<SELECT
  <select name="$name">
SELECT;
 foreach(array_keys($selection) as $value){
   $option=$selection[$value];
   $selected="";
   if($value=="$defvalue"){$selected="selected";}
   $sel.="<option value='$value' $selected>$option\n";
 }
 $sel.="</select>";
 return $sel;
}

function checkFunction($name,$value){
  $checked="";
  if($value=="on" or $value==1){$checked="checked";}
  $check="<input type='checkbox' name='$name' $checked>";
  return $check;
}

function access($referer){
  global $DIR,$WEBDIR;

  date_default_timezone_set("EST");
  $PhpGlobal["TODAY"]=getdate();
  $PhpGlobal["YEAR"]=$PhpGlobal["TODAY"]['year'];//e.g. 2005
  $PhpGlobal["MONTH"]=100+$PhpGlobal["TODAY"]['mon'];
  $PhpGlobal["MONTH"]=substr($PhpGlobal["MONTH"],1,2);//e.g. 01, 12
  $PhpGlobal["DAY"]=$PhpGlobal["TODAY"]['mday'];//e.g. 12, 31
  $PhpGlobal["DATE"]="$PhpGlobal[DAY]-$PhpGlobal[MONTH]-$PhpGlobal[YEAR]";//e.g. 12-02-2005
  $date=$PhpGlobal["TODAY"]['hours']."-".$PhpGlobal["DATE"];
  $agent=$_SERVER["HTTP_USER_AGENT"];
  $remote=$_SERVER["REMOTE_ADDR"];
  $self=$_SERVER["PHP_SELF"];
  $hitstr="$date**$remote**$referer**$self**$agent\n";
  $logfile="$DIR/access.log";
  if(file_exists($logfile)){
    $fl=fopen($logfile,"a");
  }else{
    $fl=fopen($logfile,"w");
  }
  fwrite($fl,$hitstr);
  fclose($fl);
}

function generateRandomString($length = 10) {
  $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
  $randomString = '';
  for ($i = 0; $i < $length; $i++) {
    $randomString .= $characters[rand(0, strlen($characters) - 1)];
  }
  return $randomString;
}

function loadConfiguration($file,$prefix)
{
  $conf=parse_ini_file($file);
  foreach(array_keys($conf) as $key){
    $varname="${prefix}_$key";
    $GLOBALS[$varname]=$conf[$key];
  }
}

function ajaxMultipleForm($ids,$element)
{
  $code="";
  $i=0;
  foreach($ids as $id){
    $varname="statusidload$i";
    $$varname="${id}_results_status_loader";
    $i++;
  }

$code.=<<<CODE

$("#$element").submit(function(e){
CODE;
 
 $i=0;
  foreach($ids as $id){
    $sname="statusidload$i";
    $sval=$$sname;

$code.=<<<CODE

 //alert("Submit All");
 var postData$i = $("#${id}_form").serializeArray();
 var formURL$i = $("#${id}_form").attr("action");
 $("#${id}_results_status").attr("style","opacity:0.1;background:white");
 $("#$sval").attr("style","background-image:url('web/load.gif');background-position:center top;background-repeat:no-repeat;z-index:100");
 
CODE;
    $i++;
  }

$code.=<<<CODE
e.preventDefault();
 if(!ajaxLoading){
   ajaxLoading=true;
   $.when(

CODE;

  $i=0;
  foreach($ids as $id){
    $sname="statusidload$i";
    $sval=$$sname;
$code.=<<<CODE

      $.ajax({
	url : formURL$i,
	type: "GET",
	data : postData$i,
	success:function(data, textStatus, jqXHR) 
	    {
	      $("#${id}_results_status").attr("style","background-color:white");
	      $("#$sval").attr("style","background-color:white");
	      $("#${id}_results_frame").attr("src",data);
	    },
	error: function(jqXHR, textStatus, errorThrown) 
	    {
	      $("#${id}_results_status").html('<pre><code class="prettyprint">AJAX Request Failed<br/> textStatus='+textStatus+', errorThrown='+errorThrown+'</code></pre>');
	      $("#${id}_results_status").attr("style","background-color:white");
	      $("#$sval").attr("style","background-color:white");
	    }
	}),
CODE;
        $i++;
    }
    $code=trim($code,",");
$code.=<<<CODE
      );
   }else{ajaxLoading=false;}
      e.unbind();
   });
   $("#$element").submit();
CODE;
 return $code;
}

function ajaxFromCode($code,$element,$action)
{
$allcode=<<<CODE
<script>
 var ajaxLoading=false;
 $($element).$action(function(){
     $code
 });
</script>
CODE;
 return $allcode;
}

function echoVerbose($string){
  if($GLOBALS["VERBOSE"]){echo $string;}
}

?>
