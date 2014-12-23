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

function saveLink($string)
{
  global $LINKDIR,$wLINKDIR,$wDIR,$Modes;
  $masterlink="?LOADCONFIG&Modes=$Modes&$string";
  $md5str=md5($masterlink);
  $sysid=$GLOBALS["binary_str_SysID"];
  $sysid=strtolower(preg_replace("/['\s-_,\.]/","",$sysid));
  $linkcontent=<<<LINK
<html>
<head>
<meta http-equiv="refresh" content="0;URL=$wDIR/$masterlink">
</head>
</html>
LINK;

  $linkfile=$LINKDIR."$sysid-$Modes-$md5str.html";
  $fl=fopen($linkfile,"w");
  fwrite($fl,$linkcontent);
  fclose($fl);
  $link=$wLINKDIR."$sysid-$Modes-$md5str.html";
  
  return $link;
}

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
  $link=saveLink($PARSE_STRING);
  echo<<<LINK
<a href="$link" target="_blank">Copy this link</a>
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
  $masterlink=saveLink($PARSE_STRING);
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

  $masterlink="<li id='$id'>$Modes: <a href=\"$masterlink\">$id</a></li>\n";

  if(!isBlank($out)){
    $out=shell_exec("cat $cfile");
    $master=preg_replace("/<li id='$id'>.+<\/li>\n/","$masterlink\n",$out);
    $fl=fopen($cfile,"w");
    fwrite($fl,$master);
    fclose($fl);
    $signal="<i style='color:red'>Configuration '$id' updated</i>";
  }else{
    $fl=fopen($cfile,"a");
    fwrite($fl,$masterlink);
    fclose($fl);
    $signal="<i style='color:blue'>New configuration '$id' saved</i>";
  }
  $content=shell_exec("cat $cfile");
  echo "$signal<ul>$content</ul>";
}
////////////////////////////////////////////////////
//CLEAN CONFIGURATION
////////////////////////////////////////////////////
else if($ACTION=="SaveObject"){
  $id=preg_replace("/'/","",$NewId);
  $cmd="$PYTHONCMD BHMsummary.py $SESSDIR $ObjType hash";
  if(isBlank($id) or 
     preg_match("/\.+/",$id) or
     preg_match("/\/+/",$id) or
     preg_match("/\s+/",$id)){
    echo "Invalid id '$id'";
    return;
  }
  $hash=rtrim(shell_exec($cmd));
  $parts=preg_split("/-/",$hash);
  $obj=$parts[0];
  $tgtdir="$OBJSDIR/$obj-$id";
  $lnkdir="<a href=\"$wOBJSDIR/$obj-$id/\" target='_blank'>$obj-$id</a>";
  if(!is_dir($tgtdir)){
    $cmd="cp -rf $OBJSDIR/$hash $tgtdir && echo '<li>$lnkdir</li>' >> $SESSDIR/objects.html";
  }else{
    $cmd="cp -rf $OBJSDIR/$hash/* $tgtdir/";
  }
  shell_exec("echo '$cmd' > /tmp/cmd");
  shell_exec("$cmd &> $TMPDIR/BHMsave-$SESSID");
  shell_exec("sed -e 's/$hash/$obj-$id/' $OBJSDIR/$hash/$obj.html > $tgtdir/$obj.html");
  //echo "sed -e 's/$hash/$obj-$id/' $tgtdir/$obj.html &> /tmp/sed";
  echo "Object $id saved.<br/>Use this link: $lnkdir.";
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
