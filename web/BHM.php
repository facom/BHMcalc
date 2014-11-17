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
//GLOBAL VARIABLES
//////////////////////////////////////////////////////////////
$CONTENT="";

//PYTHON COMMAND
$PYTHONCMD="PYTHONPATH=. MPLCONFIGDIR=/tmp python";

//LOCATION
if(!isset($RELATIVE)){$RELATIVE=".";}
$ROOTDIR=preg_replace("/BHMcalc/","",rtrim(shell_exec("cd $RELATIVE;pwd")));
$wDIR="/BHMcalc/";
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

$wCSSFILE="web/BHM.css";

$CSSFILE=$DIR."web/BHM.css";

//QUERY STRING
$QUERY_STRING=$_SERVER["QUERY_STRING"];

//QUERYSTRING FOR CONFIGURATION
$PARSE_STRING="";

$DATA_STRUCTURE=array(
	       "binary"=>array(
			       "Pbin"=>array("Pbin",0),
			       "abin"=>array("abin",0.125),
			       "ebin"=>array("ebin",0.0),
			       ),
	       "hz"=>array(
			   "str_incrit_wd"=>array("","'recent venus'"),
			   "str_outcrit_wd"=>array("","'early mars'"),
			   "str_incrit_nr"=>array("","'runaway greenhouse'"),
			   "str_outcrit_nr"=>array("","'maximum greenhouse'"),
			   ),
	       "interaction"=>array(
				    "tauini"=>array("",0.1),
				    "tauref"=>array("taumax",2.5),
				    "str_earlywind"=>array("","'trend'"),
				    "str_refobj"=>array("","'Earth'"),
				    "nM"=>array("",3.0),
				    "nP"=>array("",6.0),
				    "alpha"=>array("",0.3),
				    "muatm"=>array("",44.0),
				    "Mmin"=>array("",0.01),
				    "Mmax"=>array("",10.0),
				    ),
	       "planet"=>array(
			       "M"=>array("Mp",1.0),
			       "fHHe"=>array("",1.0),
			       "CMF"=>array("",0.34),
			       "tau"=>array("",1.0),
			       "Morb"=>array("",2.0),
			       "aorb"=>array("aorb",1.47),
			       "Porb"=>array("Porb",0.0),
			       "eorb"=>array("eorb",0.0167),
			       "worb"=>array("worb",0.0),
			       "Prot"=>array("",1.0),
			       ),
	       "rotation"=>array(
				 "k"=>array("",1),
				 ),
	       "star1"=>array(
			      "M"=>array("M1",1.0),
			      "Z"=>array("Z",0.03),
			      "FeH"=>array("FeH",0.3042),
			      "tau"=>array("taumin",1.0),
			      "taums"=>array("",0.0)
			      ),
	       "star2"=>array(
			      "M"=>array("M2",1.0),
			      "Z"=>array("Z",0.03),
			      "FeH"=>array("FeH",0.3042),
			      "tau"=>array("taumin",1.0),
			      "taums"=>array("",0.0),
			      ),
	       );
$MODULES=array_keys($DATA_STRUCTURE);

//////////////////////////////////////////////////////////////
//CSS
//////////////////////////////////////////////////////////////
if(!file_exists($CSSFILE) or isset($GENCSS)){
  include_once($DIR."web/BHMcss.php");
  $fc=fopen($CSSFILE,"w");
  fwrite($fc,$CSS);
  fclose($fc);
}

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
function mainHeader($refresh="")
{
  global $CSS;
  $refreshcode="";
  if(preg_match("/\d+/",$refresh)){
    $refreshcode="<meta http-equiv='refresh' content='$refresh;URL=?'>";
  }
$HEADER=<<<HEADER
<head>
  $refreshcode
  <script src="web/jquery.js"></script>
  <script src="web/BHM.js"></script>
  <script src="web/tabber.js"></script>
  <link rel="stylesheet" type="text/css" href="web/BHM.css">
  <script type="text/javascript">
  //setInterval("refreshiFrames()",2000);  
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
    $value=$conf[$key];
    $GLOBALS["PARSE_STRING"].="$varname=$value&";
    $GLOBALS[$varname]=$value;
  }
}

function saveConfiguration($dir,$qstring)
{
  $fields=preg_split("/&/",$qstring);
  $data=array();
  foreach($fields as $field){
    if(!preg_match("/_/",$field)){continue;}
    $parts=preg_split("/_/",$field);
    $module=$parts[0];
    preg_match("/${module}_(.+)=(.+)/",$field,$matches);
    $key=$matches[1];
    $value=$matches[2];
    $value=preg_replace("/%27/","'",$value);
    $value=preg_replace("/%20/"," ",$value);
    $data["$module"]["$key"]=$value;
  }
  foreach(array_keys($data) as $module){
    $fmodule="$dir/$module.conf";
    $fm=fopen($fmodule,"w");
    foreach(array_keys($data["$module"]) as $key){
      $value=$data["$module"]["$key"];
      $value=preg_replace("/^'/","\"'",$value);
      $value=preg_replace("/'$/","'\"",$value);
      $entry="$key=$value";
      fwrite($fm,"$entry\n");
    }
    fclose($fm);
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
	      $("#${id}_download").css("display","block");
	      $("#${id}_download").html("<a href=JavaScript:refreshiFrame('#${id}_results_frame')>Refresh</a> | <a href="+data+" target='_blank'>Download</a>");
	      $("#${id}_results_frame").attr("src",data);
	      refreshiFrames();
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

function readCSV($csvfile,$key=""){
  if(($fc=fopen($csvfile,"r"))==FALSE){
    echo "File $cvsfile is not reachable.";
    return;
  }
  $i=0;
  $data=array();
  $keys=array();
  while(($row=fgetcsv($fc,1000,";"))!=FALSE){
    $ncols=count($row);
    if($i==0){
      $col=0;
      $fields=array();
      foreach($row as $field){
	$fields[$col]=$field;
	$col++;
      }
    }else{
      $data[$i]=array();
      for($c=0;$c<$ncols;$c++){
	$value=$row[$c];
	$value=preg_replace("/\*/","",$value);
	if(preg_match("/\d+,\d+/",$value)){
	  $value=preg_replace("/,/",".",$value);
	}
	$data[$i][$fields[$c]]=$value;
      }
      if(preg_match("/\w/",$key)){
	$valkey=$data[$i][$key];
	$keys[$valkey]=$i;
      }else{
	$keys[$i]=$i;
      }
    }
    $i++;
  }
  fclose($fc);
  return array($data,$keys);
}

function loadSystems()
{
  global $DIR;
  $sys_csvfile="$DIR/BHM/data/BHMcat/BHMcat-systems.csv";
  $pla_csvfile="$DIR/BHM/data/BHMcat/BHMcat-planets.csv";

  $data=readCSV($sys_csvfile,"BHMCat");
  $systems=$data[0];
  $sys_keys=$data[1];
  $sys_fields=array_keys($systems[1]);
  $sys_num=count($systems);

  $data=readCSV($pla_csvfile,"BHMCatP");
  $planets=$data[0];
  $pla_keys=$data[1];
  $pla_fields=array_keys($planets[1]);
  $pla_num=count($planets);

  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  //LOAD PLANETS INTO SYSTEMS
  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  for($i=1;$i<=$sys_num;$i++){
    $planetids=$systems[$i]["Planets"];
    $planetids=preg_split("/;/",$planetids);
    $systems[$i]["PlanetsData"]=array();
    $j=0;
    foreach($planetids as $planetid){
      if(!preg_match("/\w/",$planetid)){continue;}
      $planet=$planets[$pla_keys["$planetid"]];
      array_push($systems[$i]["PlanetsData"],$planet);
      $j++;
    }
    if($j==0){
      $systems[$i]["NumPlanets"]=1;
      $planet=$planets[$pla_keys["BHMCatP0000"]];
      array_push($systems[$i]["PlanetsData"],$planet);
      $j=1;
    }
    $systems[$i]["NumPlanets"]=$j;
  }
  return $systems;
}

?>
