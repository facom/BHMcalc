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
accessLog("summary $Mode");
?>

<?PHP
//////////////////////////////////////////////////////////////
//READ ALL RESULTS
//////////////////////////////////////////////////////////////
//COMMAND
$cmd="$PYTHONCMD BHMsummary.py $SESSDIR $Mode";
shell_exec("echo '$cmd' > $TMPDIR/cmdsummary-$SESSID-${module}.txt");

//OUTPUT
$stdout="BHMsummary-output-$SESSID";
$stderr="BHMsummary-error-$SESSID";
$tgt_content="";

//EXCECUTE COMMAND
$out=shell_exec($cmd." 2> $TMPDIR/$stderr |tee $TMPDIR/$stdout");
$objects=preg_split("/\s+/",rtrim($out));

//READING HTML
foreach($objects as $object){
  $parts=preg_split("/:/",$object);
  $module=$parts[0];
  if(count($parts)>1){$hash=$parts[1];}
  else{$hash="";}

  //GET OBJECT HASH
  $src_file="objs/$module-$hash/$module.html";
  
  //READ OUTPUT CONTENT
  if(file_exists($src_file)){$src_content=shell_exec("cat $src_file");}
  else{$src_content="";}

  if(isBlank($src_content)){
    $src_content="<i>Results have not yet been calculated for this system.</i>";
  }
  //WRITE OUTPUT
$tgt_content.=<<<C
$src_content
<hr/>
C;
}

if(is_dir("sys/$SESSID")){
  //WRITE OUTPUT
  $tgt_file="sys/$SESSID/summary.html";
  $ft=fopen($tgt_file,"w");
  fwrite($ft,$tgt_content);
  fclose($ft);
  echo $tgt_file;
}else{
  echo "web/noresults.html";
}
?>
