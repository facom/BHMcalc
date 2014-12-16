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
# UTILITARY FUNCTIONS
###################################################
*/
include_once("web/BHM.php");
?>

<?PHP
if(preg_match("/template/",$SESSDIR)){
  $SESSID=session_id();
  $wSESSDIR=$wSYSDIR."$SESSID/";
  $SESSDIR=$ROOTDIR.$wSESSDIR;
  shell_exec("mkdir -p $SESSDIR");
  shell_exec("cp -rf $SYSDIR/template/* $SESSDIR/");
}
$source_dir=$SESSDIR;
/*
if(!is_dir($SESSDIR)){$source_dir=$SYSDIR."template/";}
else{$source_dir=$SYSDIR."$SESSID/";}
shell_exec("echo '$SESSDIR $source_dir' > /tmp/m");
*/
if(false){}
////////////////////////////////////////////////////
//GENERATE MASTER LINK
////////////////////////////////////////////////////
else if($ACTION=="Metals"){
  $qstring=preg_replace("/ACTION=Metals&/","",$_SERVER["QUERY_STRING"]);
  $cmd=$PYTHONCMD." BHMmetals.py '$qstring' 2> $TMPDIR/BHMmetals.log";
  $out=shell_exec($cmd);
  $out=sprintf("%.4f",$out);
  echo "$out";
}
////////////////////////////////////////////////////
//GENERATE MASTER LINK
////////////////////////////////////////////////////
else if($ACTION=="MasterLink"){
  loadConfiguration("$source_dir/star1.conf","star1");
  loadConfiguration("$source_dir/star2.conf","star2");
  loadConfiguration("$source_dir/binary.conf","binary");
  loadConfiguration("$source_dir/hz.conf","hz");
  loadConfiguration("$source_dir/rotation.conf","rotation");
  loadConfiguration("$source_dir/planet.conf","planet");
  loadConfiguration("$source_dir/interaction.conf","interaction");
  $masterlink="?LOADCONFIG&Modes=$Modes&$PARSE_STRING";
  echo<<<LINK
<a href="$masterlink" target="_blank">Copy this link</a>
LINK;
}
////////////////////////////////////////////////////
//GENERATE MASTER LINK
////////////////////////////////////////////////////
else if($ACTION=="CommandLine"){
  loadConfiguration("$source_dir/star1.conf","star1");
  loadConfiguration("$source_dir/star2.conf","star2");
  loadConfiguration("$source_dir/binary.conf","binary");
  loadConfiguration("$source_dir/hz.conf","hz");
  loadConfiguration("$source_dir/rotation.conf","rotation");
  loadConfiguration("$source_dir/planet.conf","planet");
  loadConfiguration("$source_dir/interaction.conf","interaction");
  $id=md5($PARSE_STRING);
  $cmd="$PYTHONCMD BHMrun.py BHMinteraction.py $SESSDIR/sys_$id \"LOADCONFIG&Modes=$Modes&$PARSE_STRING\"";
  echo $cmd;
}
////////////////////////////////////////////////////
//SAVE CONFIGURATION
////////////////////////////////////////////////////
else if($ACTION=="SaveConfiguration"){
  loadConfiguration("$source_dir/star1.conf","star1");
  loadConfiguration("$source_dir/star2.conf","star2");
  loadConfiguration("$source_dir/binary.conf","binary");
  loadConfiguration("$source_dir/hz.conf","hz");
  loadConfiguration("$source_dir/rotation.conf","rotation");
  loadConfiguration("$source_dir/planet.conf","planet");
  loadConfiguration("$source_dir/interaction.conf","interaction");
  $id=md5($PARSE_STRING);
  $masterlink="?LOADCONFIG&Modes=$Modes&$PARSE_STRING";
  $cfile="$SESSDIR/configurations.html";
  if(!is_file($cfile)){$out=shell_exec("echo > $cfile");}

  if(false){
  }
  else if(preg_match("/Star1/",$Modes)){
      $id=$star1_str_StarID;
  }
  else if(preg_match("/Star2/",$Modes)){
    $id=$star2_str_StarID;
  }
  else if(preg_match("/Planet/",$Modes)){
    $id=$planet_str_PlanetID;
  }
  else{
    $id=$binary_str_SysID;
  }
  $id=preg_replace("/'/","",$id);
  $out=shell_exec("grep '>$id<' $cfile");
  if(!isBlank($out)){
$content=<<<C
<i>We have detected a configuration with the same name already. Try to change the ID of the system/planet/star and try again.</i>
C;
  }else{
  $masterlink=<<<LINK

    <li>$Modes: <a href="$masterlink" target="_blank">$id</a></li>

LINK;
  $fl=fopen($cfile,"a");
  fwrite($fl,$masterlink);
  fclose($fl);
  $content=shell_exec("cat $cfile");
  }
  echo "<ul>$content</ul>";
}
////////////////////////////////////////////////////
//CLEAN CONFIGURATION
////////////////////////////////////////////////////
else if($ACTION=="CleanConfiguration"){
  $cfile="$SESSDIR/configurations.html";
  shell_exec("echo > $cfile");
  $content=shell_exec("cat $cfile");
  echo "<ul>$content</ul>";
}
////////////////////////////////////////////////////
//DOWNLOAD CONFIGURATION
////////////////////////////////////////////////////
else if($ACTION=="DownloadConfig"){
  $outfile="sys-$SESSID.tgz";
  shell_exec("rm $TMPDIR/$outfile");
  shell_exec("cd $SYSDIR/;tar zcf $TMPDIR/$outfile $SESSID/*.conf");
  $link="<a href='$wTMPDIR/$outfile'>Configuration Tarball</a>";
  echo $link;
 }
////////////////////////////////////////////////////
//DOWNLOAD All files
////////////////////////////////////////////////////
else if($ACTION=="DownloadAll"){
  $cmd="$PYTHONCMD BHMsummary.py $SESSDIR $Modes";
  $out=shell_exec($cmd);
  $objects=preg_split("/\s+/",$out);
  $outfile="results-$SESSID.tar";
  shell_exec("rm $TMPDIR/$outfile");
  foreach($objects as $object){
    if(isBlank($object)){continue;}
    $parts=preg_split("/:/",$object);
    $objdir="$parts[0]-$parts[1]";
    shell_exec("cd objs;tar -rf $TMPDIR/$outfile $objdir");
  }
  $link="<a href='$wTMPDIR/$outfile'>Results Tarball</a>";
  echo $link;
}
////////////////////////////////////////////////////
//DOWNLOAD DATA
////////////////////////////////////////////////////
else if($ACTION=="DownloadData"){
  $cmd="$PYTHONCMD BHMsummary.py $SESSDIR $Modes";
  $out=shell_exec($cmd);
  $objects=preg_split("/\s+/",$out);
  $outfile="data-$SESSID.tar";
  shell_exec("rm $TMPDIR/$outfile");
  shell_exec("cd $SYSDIR/$SESSID;tar -rf $TMPDIR/$outfile *.conf");
  shell_exec("rm $TMPDIR/objects.log");
  foreach($objects as $object){
    if(isBlank($object)){continue;}
    $parts=preg_split("/:/",$object);
    $objdir="$parts[0]-$parts[1]";
    shell_exec("echo $objdir >> $TMPDIR/objects.log");
    shell_exec("cd objs/$objdir;tar -rf $TMPDIR/$outfile --exclude 'star.data' *.data");
  }
  $link="<a href='$wTMPDIR/$outfile'>Data Tarball</a>";
  echo $link;
}
////////////////////////////////////////////////////
//DEFAULT BEHAVIOR
////////////////////////////////////////////////////
else{
  echo "<i>Unrecognized option</i>";
}
?>
