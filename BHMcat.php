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
//////////////////////////////////////////////////////////////
//READ CATALOGUE
//////////////////////////////////////////////////////////////
$systems=loadSystems();
$content="";

//////////////////////////////////////////////////////////////
//HEADER
//////////////////////////////////////////////////////////////
$content.=<<<C
<html>
<head>
  <link rel="stylesheet" type="text/css" href="$RELATIVE/web/BHM.css">
</head>
<body>
C;

//////////////////////////////////////////////////////////////
//CREATE TABLE
//////////////////////////////////////////////////////////////
$content.=<<<C
  <table width="100%">
  <tr class="header">
    <td class="field_cat" width="10%">ID</td><!--BHMCat-->
    <td class="field_cat" width="10%">System</td><!--SysID-->
    <td class="field_cat" width="10%">Planet</td><!--(planet)PlanetID-->
    <td class="field_cat">M<sub>1</sub></td><!--M1-->
    <td class="field_cat">M<sub>2</sub></td><!--M2-->
    <td class="field_cat">a<sub>bin</sub></td><!--abin-->
    <td class="field_cat">P<sub>bin</sub></td><!--Pbin-->
    <td class="field_cat">e<sub>bin</sub></td><!--ebin-->
    <td class="field_cat">References</td><!--SysADS-->
  </tr>
C;

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//LOAD VARIABLES PER SYSTEM
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
$i=0;
foreach($systems as $system){
  //echo "System:<br/>";
  //print_r($system);echo "<br/>";
  //print_r(array_keys($system));echo "<br/>";
  foreach($system["PlanetsData"] as $planet){
    //echo "Planet:<br/>";
    //print_r($planet);echo "<br/>";
    //print_r(array_keys($planet));echo "<br/>";return;
    $qstring="";
    foreach($MODULES as $module){
      $module_str=$DATA_STRUCTURE[$module];
      foreach(array_keys($module_str) as $parameter){
	$field=$module_str["$parameter"][0];
	$default=$module_str["$parameter"][1];
	if($field==""){$value=$default;}
	else{
	  if($module!="planet"){$value=$system["$field"];}
	  else{$value=$planet["$field"];}
	}
	if($value==-1){$value=$default;}
	$qstring.="${module}_$parameter=$value&";
	//echo "${module}_$parameter=$value<br/>";
      }
    }
    //echo "$qstring<br/>";
    //==================================================
    //CREATE TABLE
    //==================================================
    if(($i%2)==0){$class="row_light";}
    else{$class="row_dark";}
    $link="$wDIR?LOADCONFIG&$qstring";
$content.=<<<C
<tr class="$class">
  <td class="field_cat">
    <a href="$link" target="_parent">
      $system[BHMCat]
    </a>
  </td>
  <td class="field_cat">$system[SysID]</td>
  <td class="field_cat">$planet[PlanetID]</td>
  <td class="field_cat">$system[M1]</td>
  <td class="field_cat">$system[M2]</td>
  <td class="field_cat">$system[abin]</td>
  <td class="field_cat">$system[Pbin]</td>
  <td class="field_cat">$system[ebin]</td>
  <td class="field_cat">$system[SysADS]</td>
</tr>
C;
     $i++;
  }
}

$content.=<<<C
  </table>
</body>
</html>
C;

//////////////////////////////////////////////////////////////
//SAVE CATALOGUE TABLE
//////////////////////////////////////////////////////////////
$fl=fopen("BHMcatalogue.html","w");
fwrite($fl,$content);
fclose($fl);
if(!isset($preview)){
  echo "BHMcatalogue.html";
}else{
  echo $content;
}
?>
