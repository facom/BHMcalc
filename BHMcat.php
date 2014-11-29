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
# BHM Catalogue
###################################################
*/
include_once("web/BHM.php");
?>

<?PHP
shell_exec("echo 'Parameters: $qover $sortfield $sortorder $catfilter $catid' > /tmp/c");
$stdout="BHMcat-stdout-$SESSID";
$stderr="BHMcat-stderr-$SESSID";
$cmd="$PYTHONCMD BHMcat.py $SESSDIR $qover $sortfield $sortorder $displaylevel \"$catfilter\" $catid";
$out=shell_exec($cmd." 2> $TMPDIR/$stderr |tee $TMPDIR/$stdout");
echo "$wSESSDIR/BHMcat$catid.html";
?>
