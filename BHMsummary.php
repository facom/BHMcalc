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
# Stellar evolution interface
###################################################
*/
include_once("web/BHM.php");
?>

<?PHP
//////////////////////////////////////////////////////////////
//READ ALL RESULTS
//////////////////////////////////////////////////////////////
//COMMAND
$cmd="$PYTHONCMD BHMsummary.py $SESSDIR";

//OUTPUT
$stdout="BHMsummary-output-$SESSID";
$stderr="BHMsummary-error-$SESSID";

//EXCECUTE COMMAND
$out=shell_exec($cmd." 2> $TMPDIR/$stderr |tee $TMPDIR/$stdout");
$objects=preg_split("/\s+/",rtrim($out));

//READING HTML
foreach($objects as $object){
  $parts=preg_split("/:/",$object);
  $module=$parts[0];
  $hash=$parts[1];

  //GET OBJECT HASH
  $src_file="objs/$module-$hash/$module.html";
  
  //READ OUTPUT CONTENT
  $src_content=shell_exec("cat $src_file");
  
  //WRITE OUTPUT
$tgt_content.=<<<C
$src_content
<hr/>
C;
}

//WRITE OUTPUT
$tgt_file="sys/$SESSID/summary.html";
$ft=fopen($tgt_file,"w");
fwrite($ft,$tgt_content);
fclose($ft);

//RETURN OUTPUT
echo $tgt_file;
?>
