<?
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
# Stellar evolution interface
###################################################
*/
include_once("web/BHM.php");
if(preg_match("/template/",$SESSDIR)){
  $SESSID=session_id();
  $wSESSDIR=$wSYSDIR."$SESSID/";
  $SESSDIR=$ROOTDIR.$wSESSDIR;
  shell_exec("mkdir -p $SESSDIR");
  shell_exec("cp -rf $SYSDIR/template/* $SESSDIR/");
}
?>

<?PHP
//////////////////////////////////////////////////////////////
//CREATE CONFIGURATION FILE
//////////////////////////////////////////////////////////////
$confile=$SESSDIR."$object.conf";
$fc=fopen($confile,"w");
foreach(array_keys($_GET) as $key){
  if(!preg_match("/${object}_(.+)/",$key,$matches)){continue;}
  $var=$matches[1];
  $val=$$key;
  if(preg_match('/str_/',$key)){
    preg_match('/([^\'^\"]+)/',$val,$matches);
    $string=$matches[1];
    $val="\"'$string'\"";
  }
  fwrite($fc,"$var = $val\n");
}
fclose($fc);

//////////////////////////////////////////////////////////////
//SUBMIT EXECUTION
//////////////////////////////////////////////////////////////
//COMMAND
$cmd="$PYTHONCMD BHMrun.py BHM${module}.py $SESSDIR $object.conf $pipepos $qover";

//OUTPUT
$stdout="BHMrun-stdout-$SESSID-${module}";
$stderr="BHMrun-stderr-$SESSID-${module}";

//EXCECUTE COMMAND
$out=shell_exec($cmd." 2> $TMPDIR/$stderr |tee $TMPDIR/$stdout");
$parts=preg_split("/--sig--\s*/",$out);

//GET OBJECT HASH
$hash=rtrim(end($parts));
$src_file="objs/$module-$hash/$module.html";

if(file_exists($DIR.$src_file)){
  //RETURN OUTPUT
  echo $src_file;
}else{
  //GENERATE REPORT
  $err_file=$wSESSDIR."error-report.hml";
  $fe=fopen($ROOTDIR.$err_file,"w");
$error=<<<ERROR
  <head>
  <link rel="stylesheet" type="text/css" href="web/BHM.css">
  </head>
  <i>An error has been raised when executing the calculator scripts.
  Check the standard and error outputs of the scripts:</i>
  <p>
  <a href="$wDIR/$wTMPDIR/$stdout">Standard output</a><br/>
  <a href="$wDIR/$wTMPDIR/$stderr">Error output</a><br/>
  </p>
ERROR;
  fwrite($fe,$error);
  fclose($fe);
  echo $err_file;
}
?>
