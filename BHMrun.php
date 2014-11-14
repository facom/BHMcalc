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
if(!is_dir($SESSDIR)){
  shell_exec("mkdir -p $SESSDIR");
  shell_exec("cp -rf $SYSDIR/template/*.conf $SESSDIR/");
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
  if(preg_match('/str_/',$key)){$val="\"$val\"";}
  fwrite($fc,"$var = $val\n");
}
fclose($fc);
//////////////////////////////////////////////////////////////
//SUBMIT EXECUTION
//////////////////////////////////////////////////////////////

//COMMAND
$cmd="$PYTHONCMD BHMrun.py BHM${module}.py $SESSDIR $object.conf 0";

//OUTPUT
$stdout="BHMrun-stdout-$SESSID";
$stderr="BHMrun-error-$SESSID";

//EXCECUTE COMMAND
$out=shell_exec($cmd." 2> $TMPDIR/$stderr |tee $TMPDIR/$stdout");
$parts=preg_split("/--sig--\s*/",$out);

//GET OBJECT HASH
$hash=rtrim(end($parts));
$src_file="objs/$module-$hash/$module.html";

//RETURN OUTPUT
echo $src_file;
?>
