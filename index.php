<?PHP
//////////////////////////////////////////////////////////////////////////////////
//STYLE
//////////////////////////////////////////////////////////////////////////////////
include("etc/BHM-style.php");
$HEADER=<<<HEADER
<head>
  <script src="etc/jquery.js"></script>
  $CSS
  <script>
  function display(element){
      $('#'+element).toggle('fast',null);
  }
  </script>
</head>
HEADER;
//////////////////////////////////////////////////////////////////////////////////
//STATISTICS
//////////////////////////////////////////////////////////////////////////////////
if(!isset($_SESSION)){session_start();}
$sessid=session_id();
//echo "<P STYLE=font-size:12px>Session $sessid</P>";

$PYTHONCMD="MPLCONFIGDIR=/tmp python";
$out=shell_exec("hostname");
if($out=="urania"){
  $WEBDIR="facom/pages/binary-habitability.rs/files/binary-habitabilitygovwk/.Interactive/BHMcalc";
  $DIR="/websites/sitios/$WEBDIR";
}else{
  $WEBDIR="BHMcalc";
  $DIR="/var/www/$WEBDIR";
}

function generateFileList($sessid,$suffix){
    $files=array(
		 "output-$sessid.log",
		 "fulloutput-$sessid.log",
		 "cmd-$sessid.log",
		 "config-$sessid.log",
		 "HZ-$suffix.png","HZ-$suffix.png.txt",
		 "HZ+planet-$suffix.png","HZ+planet-$suffix.png.txt",
		 "HZevol-$suffix.png","HZevol-$suffix.png.txt",
		 "StellarOrbits-$suffix.png","StellarOrbits-$suffix.png.txt",
		 "InsolationPhotonDensity-$suffix.png","InsolationPhotonDensity-$suffix.png.txt",
		 "PeriodEvolution-$suffix.png","PeriodEvolution-$suffix.png.txt",
		 "FluxXUV-$suffix.png","FluxXUV-$suffix.png.txt",
		 "FluxSW-$suffix.png","FluxSW-$suffix.png.txt",
		 "RatiosFluxXUV-$suffix.png","RatiosFluxXUV-$suffix.png.txt",
		 "RatiosFluxSW-$suffix.png","RatiosFluxSW-$suffix.png.txt",
		 "IntFXUV-$suffix.png","IntFXUV-$suffix.png.txt",
		 "IntSW-$suffix.png","IntSW-$suffix.png.txt",
		 "MassLoss-$suffix.png","MassLoss-$suffix.png.txt");
    return $files;
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

//////////////////////////////////////////////////////////////////////////////////
//FOOTER
//////////////////////////////////////////////////////////////////////////////////
echo<<<CONTENT
<HTML>
$HEADER
<BODY>
<H1><A HREF="?">Binary Habitability Calculator</A>
<!--<SUP style='color:red;font-size:18px'>v2.0</SUP>-->
<!--<br/><a href=changeslog style=font-size:10px>Changeslog/</a><a href=TODO style=font-size:10px>ToDo</a>-->
</H1>
<a href="?">
  Main
</a> 
| <a href="JavaScript:null(0)" onclick="display('about');">
  About
</a> 
| <a href="?help">
  Help
</a>
<HR/>
<form>
CONTENT;

if(isset($_GET["help"])){
echo<<<CONTENT
Men at work.
CONTENT;
goto footer;
}

if(isset($_GET["admin"])){
  echo "<input type='hidden' name='admin' value=1>";
}

//////////////////////////////////////////////////////////////////////////////////
//DEFAULT VALUES
//////////////////////////////////////////////////////////////////////////////////
$randstr=generateRandomString(5);
$Z=0.0;
$FeH=0.0;
$M1=1.0;
$M2=0.5;
$Pbin=10.0;
$e=0.0;
$Mp=1.0;
$ap=1.5;
$ep=0.1;
$tau=1.0;
$tautot=2.0;
$incrit='recent venus';
$outcrit='early mars';
$confname="Configuration $randstr";
$zsvec="ZSVEC_siblings";
$earlywind="trend";
$qsaved=1;
$preconf="0";

//////////////////////////////////////////////////////////////////////////////////
//COMMON
//////////////////////////////////////////////////////////////////////////////////
foreach(array_keys($_GET) as $field){
    $$field=$_GET[$field];
}
foreach(array_keys($_POST) as $field){
    $$field=$_POST[$field];
}

//////////////////////////////////////////////////////////////////////////////////
//REPORT
//////////////////////////////////////////////////////////////////////////////////
if(isset($submit) and !isset($back)){
  /*
  if(!isset($qstring)){
    $qstring=$_SERVER["QUERY_STRING"];
  }
  echo "QSTRING: $qstring<br/>";
  //*/
  $qstring=$_SERVER["QUERY_STRING"];
  
  if(isset($load)){
    preg_match("/\/([^\/]+$)/",$load,$match);
    $loadsessid=$match[1];
    //echo "LOAD DIRECTORY: $load<br/>";
    //echo "LOAD SESSID: $loadsessid<br/>";
    $suffixt=sprintf("%.2f%.2f%.3f%.2f-%s",$M1,$M2,$e,$Pbin,$sessid);
    $suffixs=sprintf("%.2f%.2f%.3f%.2f-%s",$M1,$M2,$e,$Pbin,$loadsessid);
    $files_source=generateFileList($loadsessid,$suffixs);
    $files_target=generateFileList($sessid,$suffixt);
    $nfiles=count($files_source);
    for($i=0;$i<$nfiles;$i++){
      $fsource=$files_source[$i];
      $ftarget=$files_target[$i];
      //echo "Saving file $fsource as $ftarget...<br/>";
      shell_exec("cp -rf $load/$fsource tmp/$ftarget");
    }
  }

  //SAVE CONFIGURATION
  $fc=fopen("tmp/config-$sessid.log","w");
  fwrite($fc,"URL: $qstring\n\n");
  foreach(array_keys($_GET) as $field){
    $$field=$_GET[$field];
    $value=$$field;
    fwrite($fc,"$field=$value\n");
  }
  fclose($fc);

  //CHECK PRECONFIGURATION
  if($preconf!="0"){
    echo "Configuration loaded: $preconf.<br/>";
    $configuration=file("tmp/conf-$preconf/configuration");
    $i=1;
    $Z=rtrim($configuration[$i++]);
    $M1=rtrim($configuration[$i++]); 
    $M2=rtrim($configuration[$i++]); 
    $e=rtrim($configuration[$i++]);
    $Pbin=rtrim($configuration[$i++]);
    $tau=rtrim($configuration[$i++]);
    $Mp=rtrim($configuration[$i++]);
    $ap=rtrim($configuration[$i++]);
    $tautot=rtrim($configuration[$i++]);
    $qintegration=rtrim($configuration[$i++]);
    $i++;
    $zsvec=rtrim($configuration[$i++]);
    $qchz=rtrim($configuration[$i++]);
    $earlywind=rtrim($configuration[$i++]); 
    $FeH=rtrim($configuration[$i++]);
    $ep=rtrim($configuration[$i++]);
    $incrit=rtrim($configuration[$i++]);
    $outcrit=rtrim($configuration[$i++]);
    $i++;
    $qsaved=rtrim($configuration[$i++]);
    $qstring="?preconf=0&Z=$Z&M1=$M1&M2=$M2&e=$e&Pbin=$Pbin&tau=$tau&Mp=$Mp&ap=$ap&tautot=$tautot&qintegration=$qintegration&zsvec=$zsvec&qchz=$qchz&earlywind=$earlywind&FeH=$FeH&ep=$ep&incrit=$incrit&outcrit=$outcrit&confname=$confname&qsaved=$qsaved";
  }
  
  if(!preg_match("/\w+/",$qintegration)){$qintegration=0;}
  else{$qintegration=1;}
  if(!preg_match("/\w+/",$qchz)){$qchz=0;}
  else{$qchz=1;}
  if($qintegration){$qchz=1;}

  if(!isset($stat) and !isset($back)){access("run");}
  if(!isset($reload) and !isset($load) and !isset($save) and !isset($delete)){
    $cmd="$PYTHONCMD BHMcalc.py $Z $M1 $M2 $e $Pbin $tau $Mp $ap $tautot $qintegration $sessid $zsvec $qchz $earlywind $FeH $ep \"$incrit\" \"$outcrit\" \"$confname\" $qsaved &> tmp/fulloutput-$sessid.log";
    //echo "<p>$cmd</p>";return;
    exec($cmd,$output,$status); 
    shell_exec("echo '$cmd' > tmp/cmd-$sessid.log");
    $qreload="reload&$qstring";
  }else if(isset($reload)){
    $qreload=$qstring;
  }else if(isset($delete)){
    echo "<i>Removing '$confname'...<br/><br/></i>";
    //SAVE DIR
    $savedir=$load;
    shell_exec("rm -rf $savedir");
    //echo("rm -rf $savedir");
    return;
  }else if(isset($save)){
    echo "<i>Result has been saved as '$confname'...<br/><br/></i>";
    //QSTRING
    $qstring_save=preg_replace("/admin=1&/","",$qstring);
    $qstring_save=preg_replace("/&save/","",$qstring_save);
    //LOAD DATA
    $parts=array();
    for($i=0;$i<36;$i++){
      $name="parts_$i";
      $parts[$i]=$$name;
    }
    //SUFFIX	
    $i=0;
    $md5inp=$parts[$i++];
    $g1=$parts[$i++];$T1=$parts[$i++];$R1=$parts[$i++];$L1=$parts[$i++];
    $Rmin1=$parts[$i++];$Rmax1=$parts[$i++];$Pini1=$parts[$i++];$Prot1=$parts[$i++];
    $lin1=$parts[$i++];$aE1=$parts[$i++];$aHZ1=$parts[$i++];$lout1=$parts[$i++];
    $g2=$parts[$i++];$T2=$parts[$i++];$R2=$parts[$i++];$L2=$parts[$i++];
    $Rmin2=$parts[$i++];$Rmax2=$parts[$i++];$Pini2=$parts[$i++];$Prot2=$parts[$i++];
    $lin2=$parts[$i++];$aE2=$parts[$i++];$aHZ2=$parts[$i++];$lout2=$parts[$i++];
    $abin=$parts[$i++];$acrit=$parts[$i++];$nsync=$parts[$i++];$Psync=$parts[$i++];
    $lin=$parts[$i++];$aE=$parts[$i++];$aHZ=$parts[$i++];$lout=$parts[$i++];
    $tsync1=$parts[$i++];$tsync2=$parts[$i++];
    $Z=$parts[$i++];
    $suffix=sprintf("%.2f%.2f%.3f%.2f-%s",$M1,$M2,$e,$Pbin,$sessid);
    //SAVE STRING
    $files_source=generateFileList($sessid,$suffix);
    $savestr=$md5inp;
    $suffixt=sprintf("%.2f%.2f%.3f%.2f-%s",$M1,$M2,$e,$Pbin,$savestr);
    $files_target=generateFileList($savestr,$suffixt);
    //CHECK IF IT IS ADMIN
    if(!isset($admin)){$savedir="repo/users/$sessid/$savestr";}
    else{$savedir="repo/admin/$savestr";}
    //CREATE DIRECTORY
    shell_exec("mkdir -p $savedir");
    //SAVE QSTRING
    shell_exec("echo '$qstring_save' > $savedir/qstring");
    shell_exec("echo '$sessid' > $savedir/sessid");
    shell_exec("echo '$confname' > $savedir/confname");
    shell_exec("echo '$md5inp' > $savedir/md5in");

    //SAVING FILES
    $nfiles=count($files_source);
    for($i=0;$i<$nfiles;$i++){
      $fsource=$files_source[$i];
      $ftarget=$files_target[$i];
      //echo "Saving file $fsource as $ftarget...<br/>";
      shell_exec("cp -rf tmp/$fsource $savedir/$ftarget");
    }
  }//END OF SAVE
  
  ////////////////////////////////////////////////////
  //LOAD A RESULT
  ////////////////////////////////////////////////////
  $result=shell_exec("cat tmp/output-$sessid.log");
  
  //ERROR
  if(preg_match("/ERROR/",$result)){
    echo "<P STYLE='color:red'>An error has occurred while executing the program</P>";
    echo "Executing: $cmd<br/>";
    echo "<pre style='background:yellow;padding:10px'>$result</pre>";
    echo "<a href=?back&$qstring>Back</a>";
    return;
  }

  $parts=preg_split("/\s+/",$result);
  echo "<a href=?back&$qstring>Back</a> - ";
  echo "<a href=?$qreload>Reload</a>";
  echo "<P><a href=tmp/fulloutput-$sessid.log target=_blank>Full Output</a> - <a href=tmp/config-$sessid.log target=_blank>Configuration</a> - <a href=tmp/cmd-$sessid.log target=_blank>Command</a></P>";

  //BASIC INFORMATION ON THE SYSTEM
  $Zinp=$Z;
  $i=0;
  $md5inp=$parts[$i++];
  $g1=$parts[$i++];$T1=$parts[$i++];$R1=$parts[$i++];$L1=$parts[$i++];
  $Rmin1=$parts[$i++];$Rmax1=$parts[$i++];$Pini1=$parts[$i++];$Prot1=$parts[$i++];
  $lin1=$parts[$i++];$aE1=$parts[$i++];$aHZ1=$parts[$i++];$lout1=$parts[$i++];
  $g2=$parts[$i++];$T2=$parts[$i++];$R2=$parts[$i++];$L2=$parts[$i++];
  $Rmin2=$parts[$i++];$Rmax2=$parts[$i++];$Pini2=$parts[$i++];$Prot2=$parts[$i++];
  $lin2=$parts[$i++];$aE2=$parts[$i++];$aHZ2=$parts[$i++];$lout2=$parts[$i++];
  $abin=$parts[$i++];$acrit=$parts[$i++];$nsync=$parts[$i++];$Psync=$parts[$i++];
  $lin=$parts[$i++];$aE=$parts[$i++];$aHZ=$parts[$i++];$lout=$parts[$i++];
  $tsync1=$parts[$i++];$tsync2=$parts[$i++];
  $Z=$parts[$i++];

  $q=$M2/$M1;
  /*
  if($q>0){$type="Binary";}
  else{$type="Single star";}
  */
	
  $suffix=sprintf("%.2f%.2f%.3f%.2f-%s",$M1,$M2,$e,$Pbin,$sessid);

  $zcalc="";
  if($Zinp==0){$zcalc="<sup>*Calculated</sup>";}

  $qstring_save=preg_replace("/reload&/","",$qstring);
  $qstring_del=preg_replace("/reload&/","",$qstring);
  $qstring_del=preg_replace("/Modified/","",$qstring);
  for($i=0;$i<36;$i++){$qstring_save.="&parts_$i=".$parts[$i];}
  $del_button="";
  if(!isset($load)){
    $save_button="<a href=\"?$qstring_save&save\" style=background:lightgray;padding:10px;>Save Result</a>";
  }else{
    $save_button="";
    if(isset($admin)){
      $del_button="<a href=\"?$qstring_del&delete\" style=background:lightgray;padding:10px;>Delete</a>";
    }
  }

echo<<<CONTENT
<p>$save_button $del_button</b>
<H2>Input properties</H2>
<B>Input signature</b>:$md5inp<br/>
<B>Configuration name</b>:$confname
<p></p>
<table>
  <tr><td>[Fe/H]:</td><td>$FeH</td></tr>
  <tr><td>Z:</td><td>$Z$zcalc</td></tr>
  <tr><td>M<sub>1</sub>:</td><td>$M1 M<sub>Sun</sub></td></tr>
  <tr><td>M<sub>2</sub>:</td><td>$M2 M<sub>Sun</sub></td></tr>
  <tr><td>q:</td><td>$q</td></tr>
  <tr><td>P<sub>bin</sub>:</td><td>$Pbin days</td></tr>
  <tr><td>e:</td><td>$e</td></tr>
  <tr><td>&tau;:</td><td>$tau Gyr</td></tr>
  <tr><td>M<sub>p</sub>:</td><td>$Mp M<sub>Earth</sub></td></tr>
  <tr><td>a<sub>p</sub>:</td><td>$ap AU</td></tr>
  <tr><td>e<sub>p</sub>:</td><td>$ep</td></tr>
</table>

<H2>Binary System Properties</H2>
<table>
  <tr><td>a<sub>bin</sub>:</td><td>$abin AU</td></tr>
  <tr><td>a<sub>crit</sub>:</td><td>$acrit AU</td></tr>
  <tr><td>n<sub>sync</sub>=&Omega;/n:</td><td>$nsync</td></tr>
  <tr><td>P<sub>sync</sub>=n<sub>sync</sub>P<sub>bin</sub></td><td>$Psync</td></tr>
  <tr><td>a<sub>in</sub>:</td><td>$lin AU</td></tr>
  <tr><td>a<sub>HZ</sub>:</td><td>$aHZ AU</td></tr>
  <tr><td>a<sub>out</sub>:</td><td>$lout AU</td></tr>
  <tr><td>t<sub>sync1</sub>:</td><td>$tsync1 Gyr</td></tr>
  <tr><td>t<sub>sync2</sub>:</td><td>$tsync2 Gyr</td></tr>
</table>

<H2>Instantaneous Stellar Properties</H2>
<P>The following properties of the stars as measured at &tau;=$tau
Gyr.</P>
<H3>Main Component</H3>
<table>
  <tr><td>M:</td><td>$M1 M<sub>sun</sub></td></tr>
  <tr><td>g:</td><td>$g1 cm/s<sup>2</sup></td></tr>
  <tr><td>T<sub>eff</sub>:</td><td>$T1 K</td></tr>
  <tr><td>R:</td><td>$R1 R<sub>sun</sub> (Range in &tau;=0.01-$tau Gyr: $Rmin1-$Rmax1 R<sub>sun</sub>)</td></tr>
  <tr><td>L:</td><td>$L1 L<sub>sun</sub></td></tr>
  <tr><td>P<sub>rot</sub>:</td><td>$Prot1 days</td></tr>
  <tr><td>HZ:</td><td>[$lin1,$aE1 ($aHZ1),$lout1] AU</td></tr>
</table>
<H3>Secondary Component</H3>
<table>
  <tr><td>M:</td><td>$M2 M<sub>sun</sub></td></tr>
  <tr><td>g:</td><td>$g2 cm/s<sup>2</sup></td></tr>
  <tr><td>T<sub>eff</sub>:</td><td>$T2 K</td></tr>
  <tr><td>R:</td><td>$R2 R<sub>sun</sub> (Range in &tau;=0.01-$tau Gyr: $Rmin2-$Rmax2 R<sub>sun</sub>)</td></tr>
  <tr><td>L:</td><td>$L2 L<sub>sun</sub></td></tr>
  <tr><td>P<sub>rot</sub>:</td><td>$Prot2 days</td></tr>
  <tr><td>HZ:</td><td>[$lin2,$aE2 ($aHZ2),$lout2] AU</td></tr>
</table>
<H3>Cricumbinary Habitable Zone</H3>
<a href="tmp/HZ-$suffix.png.txt" target="_blank"><img src="tmp/HZ-$suffix.png"></a><br/>
<a href="tmp/HZ+planet-$suffix.png.txt" target="_blank"><img src="tmp/HZ+planet-$suffix.png"></a><br/>
CONTENT;

if($qchz){
$tsys=$parts[$i++];
$lincont=$parts[$i++];$loutcont=$parts[$i++];
$slincont=$parts[$i++];$sloutcont=$parts[$i++];
echo<<<CONTENT
<H3>Continuous Habitable Zone</H3>
<table>
  <tr><td>&tau;<sub>sys</sub>:</td><td>$tsys Gyr</td></tr>
  <tr><td>CHZ binary:</td><td>[$lincont,$loutcont] AU</td></tr>
  <tr><td>CHZ single-primary:</td><td>[$slincont,$sloutcont] AU</td></tr>
</table>
<a href="tmp/HZevol-$suffix.png.txt" target="_blank"><img src="tmp/HZevol-$suffix.png"></a><br/>

Orbits of the stellar components with respect to a planet at the inner
and outer edge of the Continuous Habitable Zone:<br/>

<a href="tmp/StellarOrbits-$suffix.png.txt"
target="_blank"><img src="tmp/StellarOrbits-$suffix.png"></a><br/>

Insolation and Photosynthetic Photon Flux Density (PPFD, 400-1400 nm)
at the inner and outer edge of the continuous habitable zone:<br/>

<a href="tmp/InsolationPhotonDensity-$suffix.png.txt"
target="_blank"><img src="tmp/InsolationPhotonDensity-$suffix.png"></a><br/>

CONTENT;
}
if($qintegration){
$suffix1=sprintf("%.2f",$M1);
$suffix2=sprintf("%.2f",$M2);
echo<<<CONTENT
<H3>Evolution Plots</H3>

Evolution of rotational periods with (solid) and without (dashed)
tidal interaction:<br/>

<a href="tmp/PeriodEvolution-$suffix.png.txt" target="_blank"><img src="tmp/PeriodEvolution-$suffix.png"></a><br/>

Evolution of XUV and stellar wind flux within the continuous habitable
zone in Binary with BHM (solid), no BHM (dash-dotted) and
single-primary (dotted): <br/>

<a href="tmp/FluxXUV-$suffix.png.txt" target="_blank"><img src="tmp/FluxXUV-$suffix.png"></a><br/> 

<a href="tmp/FluxSW-$suffix.png.txt" target="_blank"><img src="tmp/FluxSW-$suffix.png"></a><br/>

Ratio of XUV and stellar wind flux in Binaries with BHM, without BHM
and around single-primary systems:<br/>

<a href="tmp/RatiosFluxXUV-$suffix.png.txt" target="_blank"><img src="tmp/RatiosFluxXUV-$suffix.png"></a><br/> 

<a href="tmp/RatiosFluxSW-$suffix.png.txt" target="_blank"><img src="tmp/RatiosFluxSW-$suffix.png"></a><br/>

Integrated XUV and stellar wind fluxes:<br/>

<a href="tmp/IntFXUV-$suffix.png.txt" target="_blank"><img src="tmp/IntFXUV-$suffix.png"></a><br/>
<a href="tmp/IntFSW-$suffix.png.txt" target="_blank"><img src="tmp/IntFSW-$suffix.png"></a><br/>

Mass-loss as a function of planetary mass at the inner edge of the
continuous habitable zone:<br/>

<a href="tmp/MassLoss-$suffix.png.txt" target="_blank"><img src="tmp/MassLoss-$suffix.png"></a><br/>

<!--DEPRECATED
<img src="tmp/PeriodFit-$suffix1.png"><br/>
<img src="tmp/PeriodFit-$suffix2.png"><br/>
<img src="tmp/AccelerationEvolution-$suffix.png"><br/>
-->

CONTENT;
}

echo<<<CONTENT
<p>$save_button $del_button</p>
<a href=?back&$qstring>Back</a> - <a href=?$qreload>Reload</a>
</form>
CONTENT;

 }else{

  //echo "Confname: $confname";
//////////////////////////////////////////////////////////////////////////////////
//INPUT
//////////////////////////////////////////////////////////////////////////////////
   if(!isset($stat) and !isset($back)){access("access");}

   //GLOBAL LIST
   $out=shell_exec("ls -md repo/admin/*");
   $confs=preg_split("/\s*,\s/",$out);
   $preconfs=array();
   foreach($confs as $conf){
     $conf=rtrim($conf);
     $confiname=rtrim(shell_exec("cat $conf/confname"));
     $md5in=rtrim(shell_exec("cat $conf/md5in"));
     $qstring=rtrim(shell_exec("cat $conf/qstring"));
     //echo "Configuration '$conf' ($confiname,$md5in)...<br/>";
     $preconfs_name["$md5in"]="$confiname";
     $preconfs_qstring["$md5in"]="$qstring";
   }
   $global_list="";
   $keys=array_keys($preconfs_name);
   array_multisort($preconfs_name,$keys);
   foreach($keys as $key){
     $qstring=$preconfs_qstring[$key];
     $confiname=$preconfs_name[$key];
     $global_list.="<a href='?load=repo/admin/$key&$qstring'>$confiname</a><br/>";
   }
   if(!preg_match("/\w/",$global_list)){
     $global_list="<i>(No configurations found)</i>";
   }

   //SESSION LIST
   $out=shell_exec("ls -md repo/users/$sessid/*");
   $confs=preg_split("/\s*,\s/",$out);
   $preconfs_name=array();
   $preconfs_qstring=array();
   foreach($confs as $conf){
     $conf=rtrim($conf);
     //echo "User configuration:$conf<br/>";
     $confiname=rtrim(shell_exec("cat $conf/confname"));
     $md5in=rtrim(shell_exec("cat $conf/md5in"));
     $qstring=rtrim(shell_exec("cat $conf/qstring"));
     //echo "$confiname";
     $preconfs_name["$md5in"]="$confiname";
     $preconfs_qstring["$md5in"]="$qstring&admin";
   }
   $this_session="";
   $keys=array_keys($preconfs_name);
   array_multisort($preconfs_name,$keys);
   foreach($keys as $key){
     if(!preg_match("/[\w\d]+/",$key)){continue;}
     $qstring=$preconfs_qstring[$key];
     $confiname=$preconfs_name[$key];
     $this_session.="<a href='?load=repo/users/$sessid/$key&$qstring'>$confiname</a><br/>";
   }
   if($this_session==""){
     $this_session="<i>(No configurations found)</i>";
   }
   
   $ZSVEC=array("ZSVEC_full"=>"Full (35 metallicities, 0.0001-0.06, [Fe/H] -2.30 to 0.62)",
	       "ZSVEC_coarse"=>"Coarse (10 values, 0.0001-0.06, [Fe/H] -2.30 to 0.62)",
	       "ZSVEC_siblings"=>"Near solar (3 values , 0.01-0.02, [Fe/H] -0.197 to 0.117)");
   $zsel=selectFunction("zsvec",$ZSVEC,$zsvec);

   $EARLYWIND=array("trend"=>"Trending","constant"=>"Constant");
   $ewsel=selectFunction("earlywind",$EARLYWIND,$earlywind);

   $YESNO=array("1"=>"Yes","0"=>"No");
   $savedsel=selectFunction("qsaved",$YESNO,$qsaved);

   $check_qchz=checkFunction("qchz",$qchz);
   $check_qintegration=checkFunction("qintegration",$qintegration);

   //DISPLAY
   $displayb="none";
   $displayp="none";
   $displayc="none";
   $displayo="none";
   $displayr="none";
   if(isset($back)){
     $displayo="block";
     $displayb="block";
     $savedsel="Yes";
   }

   //REFERENCES
   $mason2013="http://iopscience.iop.org/2041-8205/774/2/L26";
   $mason2014="http://iopscience.iop.org/2041-8205/774/2/L26";
   $zuluaga2014="http://iopscience.iop.org/2041-8205/774/2/L26";

echo<<<CONTENT
<p>
  Welcome to the <b>Binary Habitability Calculator</b>. Use
  the <a href="#form">form below</a> to configure your system and
  calculate its properties and the effects of the BHM.  To know more
  about this calculator and the Binary Habitability
  Mechanism <a href="JavaScript:null(0)"
  style="text-decoration:underline" onclick="display('about');">click
  here</a>.  For a complete guide to this calculator
  just <a href="?help">ask for help</a>.
</p>
<div id="about" style="display:none">
<p>
  The Binary Habitability Calculator is a web interface to a set of
  programs testing the so called <b>Binary Habitability Mechanism</b>
  (BHM).  The BHM was discovered by Paul Mason, Jorge I. Zuluaga,
  Pablo Cuartas and Joni Clark (<a href="$zuluaga2014">Zuluaga et
  al. 2014</a>, <a href="$mason2013">Mason et al. 2013</a>).
  According to this mechanisms some binaries could offer more suitable
  environments for life than single stars.
</p>

<p>
  Using this interface you will be able to:
  <ul>
    <li>Providing metallicity, stellar mass, binary period and binary
    eccentricity, calculate the full properties of a binary system at
    a given age.  They include:
      <ul>
	<li>Binary semi-major axis.</li>
	<li>Critical distance for stable p-type planetary orbits.</li>
	<li>Limits of the circumbinary habitable zone.</li>
	<li>Instantaneous basic properties of the stellar components
	  (gravity, luminosity, temperature, radius, rotational
	  period, circumstellar habitable zone)
      </ul>
    <li>Continuous circumbinary habitable zone (CHZ).</li>
    <li>Insolation and photon flux at the inner and outer edges of the CHZ.</li>
    <li>Evolution of the rotation period of the binary components as a
    result of their mutual tidal interaction.</li>
    <li>Flux of X-Rays and Extreme Ultraviolet radiation (XUV) at the
    inner and outer edges of the CHZ.</li>
    <li>Stellar wind flux at the inner and outer edges of the
    CHZ.</li>
    <li>Atmospheric mass-loss for unmagnetized terrestrial planets at
    the middle of the CHZ.</li>
  </ul>
</p>
<p>
<b>References</b><br/>
<ul>
  <li>
    <a href="$mason2013">
      Mason, Paul A., et al. "Rotational Synchronization May Enhance
      Habitability for Circumbinary Planets: Kepler Binary Case Studies."
      The Astrophysical Journal Letters 774.2 (2013): L26.
  </li>
  <li>
    <a href="$mason2014">
      Mason, Paul A., et al. "Circumbinary Habitability Niches."
      To appear in the International Journal of Astrobiology.
  </li>
  <li>
    <a href="$zuluaga2014">
      Zuluaga, Jorge I., et al. "The Binary Habitability Mechanism."
      In preparation.
  </li>
  </a>
</ul>
</div>
<a name="form"></a>
<!-- &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& -->
<!-- SUBMIT BUTTON -->
<!-- &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& -->
<div class="title">
<a id="show" href="JavaScript:null(0)" onclick="$('.form').toggle('fast',null);$('#hidden').css('display','block');$('#show').css('display','none');">
Show all
</a>
<a id="hidden" href="JavaScript:null(0)" onclick="$('.form').toggle('fast',null);$('#show').css('display','block');$('#hidden').css('display','none');" style="display:none">
Hidden all
</a>
</div>

<!-- &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& -->
<!-- BINARY INFORMATION -->
<!-- &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& -->

<div id="binary_input" class="title">
<H3>
  <a href="JavaScript:null(0)" onclick="display('binary_input_form')">
  Binary System
  </a>
</H3>
<div id="binary_input_form" class="form" style="display:$displayb">
<p>Choose the basic properties of the binary system here. Optionally,
a test planet may be selected with results displayed on the habitable
zone plots. Most results are given for planets in circular orbits at
the inner and outer edges of the continuous habitable zone. You can
load pre-calculated systems in the <a href="#repo" onclick="display('results_input_form');">Results
Repository</a>.</p>

[Fe/H] : <input type="text" name="FeH" value="$FeH"> or Z : <input type="text" name="Z" value="$Z"><br/> 

<i style="font-size:12px">Metallicity. Leave either [Fe/H] in Z as
zero, if you do not know the exact value of this quantities. The valid
range of Z depends on the isochrone set selected in
the <a href="#options">options section</a>. It typically ranges from
0.0001 to 0.06.</i><br/><br/>

M<sub>1</sub> : <input type="text" name="M1" value="$M1"> M<sub>Sun</sub><br/>
<i style="font-size:12px">Mass of the main component</i><br/><br/>

M<sub>2</sub> : <input type="text" name="M2" value="$M2">
M<sub>Sun</sub><br/>
<i style="font-size:12px">Mass of the secondary component.  Leave 0 to
compute single star properties</i><br/><br/>

P<sub>bin</sub> : <input type="text" name="Pbin" value="$Pbin">
days<br/>
<i style="font-size:12px">Binary period.</i><br/><br/>

e : <input type="text" name="e" value="$e"><br/>
<i style="font-size:12px">Binary eccentricity.</i><br/><br/>

&tau; : <input type="text" name="tau" value="$tau"> Gyr<br/>
<i style="font-size:12px">Age of the system.  Values must be between
0.01 and 12.5 Gyr</i><br/><br/>

<input type="submit" name="submit" value="submit">
</div></div>

<!-- &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& -->
<!-- PLANETARY INFORMATION -->
<!-- &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& -->

<div id="planet_input" class="title">
<H3>
  <a href="JavaScript:null(0)" onclick="display('planet_input_form')">
  Properties of the test planet
  </a>
</H3>

<div id="planet_input_form" class="form" style="display:$displayp">
M<sub>p</sub> : <input type="text" name="Mp" value="$Mp">
M<sub>Earth</sub><br/>
<i style="font-size:12px">Planetary mass. Values must be between 0.5
and 10.0</i><br/><br/>

a<sub>p</sub> : <input type="text" name="ap" value="$ap"> AU<br/>
<i style="font-size:12px">Semimajor axis of planet</i><br/><br/>

e<sub>p</sub> : <input type="text" name="ep" value="$ep"><br/>
<i style="font-size:12px">Eccentricity of the planet</i><br/><br/>

<input type="submit" name="submit" value="submit">
</div></div>

<!-- &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& -->
<!-- CALCULATIONS -->
<!-- &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& -->
<div id="calculations_input"  class="title">
<H3>
  <a href="JavaScript:null(0)" onclick="display('calculations_input_form')">
  Available calculation
  </a>
</H3>
<div id="calculations_input_form" class="form" style="display:$displayc">
<p>Please indicate here which calculation you want to perform.  More
advanced calculations will take considerably more time to be
performed.</p>

Basic binary properties: <input type="checkbox" name="qbasic" checked><br/>

<i style="font-size:12px">Compute the basic properties of the binary
including instantaneous stellar properties, critical distance, binary
semimajor axis, etc.</i><br/><br/>

Binary HZ: <input type="checkbox" name="qhz" checked><br/>
	   <i style="font-size:12px">Compute and plot the Habitable Zone (HZ) of the binary at its present age (see parameter &tau;).</i><br/><br/>

Compute the continuous HZ:$check_qchz<br/>
<i style="font-size:12px">Compute and plot the continuous habitable zone (CHZ).</i><br/><br/>

Integrate properties:$check_qintegration<br/>
<i style="font-size:12px">Calculate the evolution of the interacting
properties between the planet and the stars (XUV flux, stellar wind,
estimated atmospheric mass-loss, etc.)</i><br/><br/>

Total integration time : <input type="text" name="tautot" value="$tautot"> Gyr<br/>
<i style="font-size:12px">Values must be between 0.01 and 12.5 Gyr</i><br/><br/>

<input type="submit" name="submit" value="submit">
</div></div>

<!-- &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& -->
<!-- OPTIONS -->
<!-- &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& -->

<div id="options_input" class="title">
<a name="options"></a>
<H3>
  <a href="JavaScript:null(0)" onclick="display('options_input_form')">
  Options
  </a>
</H3>

<div id="options_input_form" class="form" style="display:$displayo">
Set of isochrones : $zsel<br/>

<i style="font-size:12px">Using the default (solar metalicity) reduces
the execution time considerably.</i><br/><br/>

Type of early stellar wind : $ewsel
<br/>

<i style="font-size:12px">Observations do not provide us information
about the stellar wind before &tau;<0.7 Gyr.  Some observations
suggest there is a saturation of magnetic activity before that.
Select which type of behavior do you want to simulate.</i><br/><br/>

Do you want to retrieve any previous result: $savedsel<br/>

<i style="font-size:12px">Use this option to load results from a
previous calculation performed with exactly the same
parameters.</i><br/><br/>

Configuration name: 
<input type='text' name='confname' value="$confname"><br/>

<i style="font-size:12px">Save a configuration with a given name. Do
not modify if you don't need this option.</i><br/><br/>

<input type="submit" name="submit" value="submit">
</div></div>

<!-- &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& -->
<!-- RESULTS REPOSITORY -->
<!-- &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& -->

<div id="results_input" class="title">
<a name="repo"></a>
<H3>
  <a href="JavaScript:null(0)" onclick="display('results_input_form')">
  Results Repository
  </a>
</H3>

<div id="results_input_form" class="form" style="display:$displayr">
<H4>Global list</H4>

$global_list

<H4>This session (id = $sessid)</H4>

$this_session
</div></div>

<!-- &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& -->
<!-- SUBMIT BUTTON -->
<!-- &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& -->
<div class="title">
<input type="submit" name="submit" value="submit">
</div>
CONTENT;
 }

//////////////////////////////////////////////////////////////////////////////////
//FOOTER
//////////////////////////////////////////////////////////////////////////////////
if(isset($stat)){
echo<<<CONTENT
<h2>Usage statistics</h2>
<a href="http://astronomia.udea.edu.co/sitios/$WEBDIR/access.log" target="_blank">
Full
</a>
 - 
<a href="http://urania.udea.edu.co/sitios/facom/cgi-bin/stat.php?statfile=$DIR/access.log" target="_blank">
Recalculate
</a> - 
<a href="http://astronomia.udea.edu.co/sitios/$WEBDIR/access.html" target="_blank">
Last
</a>
CONTENT;
}

footer:
echo<<<CONTENT
</form>
<hr/>

<i style="font-size:10pt">
Developed by <a href="mailto:jorge.zuluaga@udea.edu.co">Jorge I. Zuluaga</a>
(2014), Instituto de Fisica, Universidad de Antioquia, Viva la BHM!. <br/> 

Last update: 18-August-2014 (Jorge Zuluaga)<br/> 

For references please cite: <a href="$mason2013">Mason, P. A., Zuluaga, J. I., Clark, J. M., &
Cuartas-Restrepo, P. A. (2013). Rotational Synchronization May Enhance
Habitability for Circumbinary Planets: Kepler Binary Case Studies. The
Astrophysical Journal Letters, 774(2), L26.</a>

</i>

</BODY>
</HTML>
CONTENT;
?>
