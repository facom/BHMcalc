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
////////////////////////////////////////////////////
//GLOBAL
////////////////////////////////////////////////////
$parts=preg_split("/\./",$plot);
$fname=$parts[0];
$file="$ROOTDIR/$dir/$plot";
$image="$dir/$fname.png";
$stdout="plot-stdout-$SESSID";
$stderr="plot-stderr-$SESSID";
$file_stdout="$wTMPDIR/plot-stdout-$SESSID";
$file_stderr="$wTMPDIR/plot-stderr-$SESSID";

echo<<<C
<html>
<head>
  <link rel="stylesheet" type="text/css" href="$RELATIVE/web/BHM.css">
</head>
<body>
C;

////////////////////////////////////////////////////
//CHANGE SCRIPT
////////////////////////////////////////////////////
if(isset($action))
{
  $fs=fopen($file,"w");
  fwrite($fs,$script);
  fclose($fs);
  $rdir=preg_replace("/\/BHMcalc\//","",$dir);
  $cmd="$PYTHONCMD $rdir/$plot 2> $file_stderr |tee $file_stdout";
  shell_exec($cmd);
}

////////////////////////////////////////////////////
//DRAW FORM
////////////////////////////////////////////////////
$script=shell_exec("cat $file");
$script=preg_replace("/^\s*/","",$script);

echo<<<C
<form method="post">
<input type="hidden" name="dir" value="$dir">
<input type="hidden" name="plot" value="$plot">
<div class="wrapper">
  <div class="formarea">
    <h3>Script</h3>
    <b>Name:</b>$plot<br/>
    <!--<b>Command:</b>$cmd<br/>-->
    <b>Output:</b>
    <a href=$wDIR/$file_stdout target=_blank>Output</a> | 
    <a href=$wDIR/$file_stderr target=_blank>Error</a><br/>
    <br/>
    <textarea name="script" style="width:90%;height:100%">
$script
    </textarea>
    <br/>
    <div style="position:absolute;top:10%;right:55%">
      <input type="hidden" name="action" value="replot">
      <button>Replot</button>
    </div>
  </div>
  <div class="results">
    <img src="$image" width="100%">
  </div>
</div>
</form>
</body>
</html>
C;
?>
