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
# Web Interface
###################################################
*/
include_once("web/BHM.php");
?>
<?PHP
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//ACTION PREVIOUS TO LOAD INDEX
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if(isset($LOADCONFIG)){
  //========================================
  //LOAD CONFIGURATION FROM QUERY STRING
  //========================================
  saveConfiguration($SESSDIR,$QUERY_STRING);
  $header=mainHeader("1","?LOAD");
  echo "$header<body>Loading configuration...</body>";
  return;
}

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//CATALOGUE KEYS
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
$keys=file($SESSDIR."BHMcat.keys");
$catfields="";
foreach($keys as $key){
   $key=rtrim($key);
   $catfields.="<option value='$key'>$key</option>";
}

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//HEADER
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
$header=mainHeader();
$CONTENT.="<html>$header<body>";
if($VERBOSE){
$CONTENT.=<<<C
Sessid:$SESSID<br/>
ROOTDIR: $ROOTDIR
GET: $GETSTR<br/>
POST: $POSTSTR<br/>
C;
}

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//HEADER AND FRONTMATTER
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
$CONTENT.=<<<C
<h1>
<a style='font-size:32' href="?TABID=0">Binary Habitability Calculator</a><sup> <b style='color:red'>2.0</b></sup>
</h1>
C;

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//AJAX FORM
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//CATALOGUE
$code=ajaxMultipleForm(array("cat"),"cat_form");
$ajaxform_cat_Update=ajaxFromCode($code,"'#cat_Update'","click");

//STAR1
$code=ajaxMultipleForm(array("star1"),"star1_form");
$ajaxform_star1_Update=ajaxFromCode($code,"'#star1_Update'","click");

//STAR2
$code=ajaxMultipleForm(array("star2"),"star2_form");
$ajaxform_star2_Update=ajaxFromCode($code,"'#star2_Update'","click");

//PLANET
$code=ajaxMultipleForm(array("planet"),"planet_form");
$ajaxform_planet_Update=ajaxFromCode($code,"'#planet_Update'","click");

//BINARY
$code=ajaxMultipleForm(array("binary"),"binary_form");
$ajaxform_binary_Update=ajaxFromCode($code,"'#binary_Update'","click");

//HABITABLE ZONE
$code=ajaxMultipleForm(array("hz"),"hz_form");
$ajaxform_hz_Update=ajaxFromCode($code,"'#hz_Update'","click");

//ROTATION
$code=ajaxMultipleForm(array("rotation"),"rotation_form");
$ajaxform_rotation_Update=ajaxFromCode($code,"'#rotation_Update'","click");

//INTERACTION
$code=ajaxMultipleForm(array("interaction"),"interaction_form");
$ajaxform_interaction_Update=ajaxFromCode($code,"'#interaction_Update'","click");

//INTERACTION
$code=ajaxMultipleForm(array("summary"),"summary_form");
$ajaxform_summary_Update=ajaxFromCode($code,"'#summary_Update'","click");

//echo "<pre>$ajaxform_summary_Update</pre>";

//LOAD ALL
if(isset($LOAD)){$slope=1.0;}
else{$slope=1.0;}
$code=ajaxMultipleForm(array("interaction","rotation","hz","binary","star1","star2","planet","cat"),"allforms",$slope);
//$code=ajaxMultipleForm(array("interaction","cat"),"allforms");
$ajax_all_Update=ajaxFromCode($code,"'#all_Update'","click");
$ajax_all_Load=ajaxFromCode($code,"document","ready");

//FORCE UPDATE
$force_update=<<<F
  <input class="qover" type="hidden" name="qover" value="0">
  <a href="JavaScript:void(0)" class="force" onclick="forceUpdate('.force','.qover')">Smart</a> 
F;

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//CHANGE OTHER THINGS IN DOCUMENT WHEN LOAD
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
$changeFeH=<<<C
  changeAjax('/BHMcalc/BHMutil.php?ACTION=Metals&ZtoFeH','.star_Z','.star_FeH');
C;
$changeZ=<<<C
  changeAjax('/BHMcalc/BHMutil.php?ACTION=Metals&FeHtoZ','.star_FeH','.star_Z');
C;
$CONTENT.=<<<C
<script>
  $(document).ready(function(){
      $changeFeH
      changeValues(['.star_Z'],'input[name=star1_Z]');
      changeValues(['.star_FeH'],'input[name=star1_FeH]');
    });
</script>
<script>
function idSystem(){
  //IT SHOULD BE THE WHOLE FORM
  var forms=["star1_form","star2_form","planet_form"];
  var sysid="";
  for(i=0;i<3;i++){
    elements=document.forms[forms[i]].elements;
    for(j=0;j<elements.length;j++){
      clase=elements[j].getAttribute("class")+"";
      if(clase.search("sensitive")>=0){
	val=elements[j].value;
	sysid=sysid+val;
      }
    }
  }
  //alert(sysid);
  var sys=calcMD5(sysid);
  $('.sys_input').attr("value","\"\'"+sys+"\'\"");
  //alert($("input[name=binary_str_sys]").val());
}
</script>
C;

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//LOAD DATA
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if(!is_dir($SESSDIR)){
  $source_dir=$SYSDIR."template/";
  echoVerbose("No session directory.");
  $qdir="No session directory";
  if(!isset($TABID)){$TABID=0;}
}else{
  $source_dir=$SESSDIR;
  echoVerbose("Session directory already exist.");
  $qdir="Existing session directory.";
  if(!isset($TABID)){$TABID=2;}
}

//========================================
//LOADING RESULTS
//========================================
if(isset($LOAD) and False){
  $CONTENT.="$ajax_all_Load";
}
echoVerbose("<br/>");
echoVerbose("Source dir: $source_dir<br/>");

//========================================
//READING CONFIGURATION FILES
//========================================
loadConfiguration("$source_dir/star1.conf","star1");
loadConfiguration("$source_dir/star2.conf","star2");
loadConfiguration("$source_dir/binary.conf","binary");
loadConfiguration("$source_dir/hz.conf","hz");
loadConfiguration("$source_dir/rotation.conf","rotation");
loadConfiguration("$source_dir/planet.conf","planet");
loadConfiguration("$source_dir/interaction.conf","interaction");

//ADJUST VALUES
$planet_Morb=$star1_M+$star2_M;
$CONTENT.=<<<C
<script>
function changePlanetMorb(){
  Morb=parseFloat($("input[name=star1_M]").val())+parseFloat($("input[name=star2_M]").val());
  $("input[name=planet_Morb]").attr("value",Morb);
}
</script>
C;

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//TABBED FORM
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
$CONTENT.=<<<C
<div style="position:fixed;top:10px;right:10px">
<form id="allforms" action="JavaScript:void(0)">
  <button id="all_Update">Update All</button>
  $ajax_all_Update
</form>
</div>
<div class="tabber maintabber" id="$TABID">

  <!-- //////////////////////////////////////////////////////////// -->
  <!-- INTRODUCTION -->
  <!-- //////////////////////////////////////////////////////////// -->
  <div class="tabbertab" id="Introduction" title="Introduction">
    <div class="tabcontent">
    </div>
  </div>

  <!-- //////////////////////////////////////////////////////////// -->
  <!-- CATALOGUE -->
  <!-- //////////////////////////////////////////////////////////// -->
  <div class="tabbertab" id="Introduction" title="BHM Catalogue">
    <p><b>Binary Habitability Catalogue</b></p>
    <form id="cat_form" action="BHMcat.php">
      Sort field:
      <select name="sortfield">
	$catfields
      </select>
      Sort order:
      <select name="sortorder">
	<option value="0">Ascending</option>
	<option value="1">Descending</option>
      </select>
      Detail level:
      <select name="displaylevel">
	<option value="1">Basic Properties</option>
	<option value="2">Detailed</option>
	<option value="3">All Properties</option>
	<option value="4">Errors</option>
      </select>
      Filter : <input type="text" name="catfilter" value="binary_Pbin>0">
      <a href=JavaScript:$('.help').toggle('fast',null) style="font-size:10px">Show/Hide Help</a>
      <div class="help" style="display:none">
	<b>Filter examples</b>:<br/>
	Periods in a given range: binary_Pbin>10 and binary_Pbin<40<br/>
	Primary stars with measured rotational velocity: star1_Protv>0<br/>
	Both stars with measured rotational velocity: star1_Protv>0 and star2_Protv<br/>
	Kepler planets: 'Kepler' in PlanetID<br/>
	Systems in DEBCat: 'DEB' in SourceCat<br/>
	Systems in Ekar catalogue with measured distance: 'Ek' in SourceCat and binary_d>0<br/>
      </div>
      <p></p>
      <button class="update" id="cat_Update">Update</button> 
      $ajaxform_cat_Update
      $force_update
      <div id="cat_results_panel" class="catalogue">
	<div class="download" id="cat_download"></div>
	<div id="cat_results_status_loader" style="background-color:white;">
	  <div id="cat_results_status" style="background-color:white;">
	    <iframe class="iframe" id="cat_results_frame" src="web/blank.html" 
		    scrolling="yes" onload="adjustiFrame(this);">
	    </iframe>
	  </div>
	</div>
      </div>
    </form>
  </div>

  <!-- //////////////////////////////////////////////////////////// -->
  <!-- STAR 1 -->
  <!-- //////////////////////////////////////////////////////////// -->
  <div class="tabbertab" id="star1" title="Star 1">
    <form id="star1_form" action="BHMrun.php">
    <div class="tabcontent">
      <div class="wrapper">
	<div class="formarea">
	  <div><center class="title">Input Form</center><hr width="90%"/></div>
	    <input type="hidden" name="module" value="star">
	    <input type="hidden" name="object" value="star1">
	    <table border=0px>
	      <tr>
		<!-- ---------------------------------------- -->
		<td class="name">Mass:</td>
		<td class="field">
		  <input class="sensitive" type="text" name="star1_M" value="$star1_M" onchange="changePlanetMorb();idSystem();">
		  M<sub>Sun</sub>
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Stellar mass.  Minimum mass 0.1, maximum mass 1.5 M<sub>sun</sub>
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Metallicity, Z:</td>
		<td class="field">
		  <input type="text" class="star_Z sensitive" name="star1_Z" value="$star1_Z" 
			 onchange="$changeFeH;changeValues(['.star_Z'],this);idSystem();">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Stellar mass.  Minimum mass 0.1, maximum mass 1.5 M<sub>sun</sub>
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Metallicity, [Fe/H]:</td>
		<td class="field">
		  <input type="text" class="star_FeH sensitive" name="star1_FeH" value="$star1_FeH" 
			 onchange="$changeZ;changeValues(['.star_FeH'],this);idSystem();">
		  dex
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Stellar mass.  Minimum mass 0.1, maximum mass 1.5 M<sub>sun</sub>
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Age:</td>
		<td class="field">
		  <input id="ini" type="text" class="star_tau sensitive" name="star1_tau" value="$star1_tau" onchange="changeValues(['.star_tau'],this);idSystem();">
		  Gyr
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Stellar mass.  Minimum mass 0.1, maximum mass 1.5 M<sub>sun</sub>
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Main Sequence:</td>
		<td class="field">
		  <input class="sensistive" type="text" id="test" name="star1_taums" value="$star1_taums" onchange="idSystem();">
		  Gyr
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Main sequence time.  Leave zero if you expect that
		  the tool calculate it by itself.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="button" colspan=2>
		  <button class="update" id="star1_Update">Update</button>
		  $ajaxform_star1_Update
		  $force_update
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	    </table>
	</div>
	<div id="star1_results_panel" class="results">
	  <div><center class="title">Results</center><hr width="90%"/></div>
	  <div class="download" id="star1_download"></div>
	  <div id="star1_results_status_loader" style="background-color:white;">
	    <div id="star1_results_status" style="background-color:white;">
	      <iframe class="iframe" id="star1_results_frame" src="web/blank.html" 
		      scrolling="yes" onload="adjustiFrame(this);">
	      </iframe>
	    </div>
	  </div>
	</div>
      </div>
    </div>
   </form>
  </div>

  <!-- //////////////////////////////////////////////////////////// -->
  <!-- STAR 2
  <!-- //////////////////////////////////////////////////////////// -->
  <div class="tabbertab" id="star2" title="Star 2">
    <form id="star2_form" action="BHMrun.php">
    <div class="tabcontent">
      <div class="wrapper">
	<div class="formarea">
	  <div><center class="title">Input Form</center><hr width="90%"/></div>
	    <input type="hidden" name="module" value="star">
	    <input type="hidden" name="object" value="star2">
	    <table border=0px>
	      <tr>
		<!-- ---------------------------------------- -->
		<td class="name">Mass:</td>
		<td class="field">
		  <input class="sensitive" type="text" name="star2_M" value="$star2_M" onchange="changePlanetMorb();idSystem();">
		  M<sub>Sun</sub>
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Stellar mass.  Minimum mass 0.1, maximum mass 1.5 M<sub>sun</sub>
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Metallicity, Z:</td>
		<td class="field">
		  <input type="text" class="star_Z sensitive" name="star2_Z" value="$star2_Z" 
			 onchange="$changeFeH;changeValues(['.star_Z'],this);idSystem();">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Stellar mass.  Minimum mass 0.1, maximum mass 1.5 M<sub>sun</sub>
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Metallicity, [Fe/H]:</td>
		<td class="field">
		  <input type="text" class="star_FeH sensitive" name="star2_FeH" value="$star2_FeH" 
			 onchange="$changeZ;changeValues(['.star_FeH'],this);idSystem();">
		  dex
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Stellar mass.  Minimum mass 0.1, maximum mass 1.5 M<sub>sun</sub>
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Age:</td>
		<td class="field">
		  <input id="ini" type="text" class='star_tau sensitive' name="star2_tau" value="$star2_tau" onchange="changeValues(['.star_tau'],this);idSystem();">
		  Gyr
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Stellar mass.  Minimum mass 0.1, maximum mass 1.5 M<sub>sun</sub>
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Main Sequence:</td>
		<td class="field">
		  <input type="text" id="test" class="sensitive" name="star2_taums" value="$star2_taums" onchange="idSystem();">
		  Gyr
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Main sequence time.  Leave zero if you expect that
		  the tool calculate it by itself.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="button" colspan=2>
		  <button class="update" id="star2_Update">Update</button> 
		  $ajaxform_star2_Update
		  $force_update
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	    </table>
	</div>
	<div id="star2_results_panel" class="results">
	  <div><center class="title">Results</center><hr width="90%"/></div>
	  <div class="download" id="star2_download"></div>
	  <div id="star2_results_status_loader" style="background-color:white;">
	    <div id="star2_results_status" style="background-color:white;">
	      <iframe class="iframe" id="star2_results_frame" src="web/blank.html" 
		      scrolling="yes" onload="adjustiFrame(this);">
	      </iframe>
	    </div>
	  </div>
	</div>
      </div>
    </div>
   </form>
  </div>
  
  <!-- //////////////////////////////////////////////////////////// -->
  <!-- PLANET -->
  <!-- //////////////////////////////////////////////////////////// -->
  <div class="tabbertab" id="planet" title="Planet">
  <form id="planet_form" action="BHMrun.php">
    <div class="tabcontent">
      <div class="wrapper">
	<div id="planet_form" class="formarea">
	  <div><center class="title">Input Form</center><hr width="90%"/></div>
	    <input type="hidden" name="module" value="planet">
	    <input type="hidden" name="object" value="planet">
	    <table border=0px>
	      <tr>
		<!-- ---------------------------------------- -->
		<td class="name">Mass:</td>
		<td class="field">
		  <input type="text" class="sensitive" name="planet_M" value="$planet_M" onchange="idSystem();">
		  M<sub>Earth</sub>
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Minimum mass 1.0, maximum mass 320 M<sub>Earth</sub>
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">H/He Mass Fraction:</td>
		<td class="field">
		  <input type="text" class="sensitive" name="planet_fHHe" value="$planet_fHHe" onchange="idSystem();">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Smaller than 1.  Not important for Earth-like planets.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Core Mass Fraction:</td>
		<td class="field">
		  <input type="text" class="sensitive" name="planet_CMF" value="$planet_CMF" onchange="idSystem();">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Smaller than 1.  Earth is CMF=0.34
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Planetary Age:</td>
		<td class="field">
		  <input type="text" class="star_tau sensitive" name="planet_tau" value="$planet_tau" onchange="changeValues(['.star_tau'],this);idSystem();">
		  Gyr
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Planetary Age.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Orbiting Mass:</td>
		<td class="field">
		  <input type="text" id="planet_Morb" class="sensistive" name="planet_Morb" value="$planet_Morb" onchange="idSystem();">
		  M<sub>Sun</sub>
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  In case of a binary this should be the sum of M1 + M2.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Orbital semimajor axis:</td>
		<td class="field">
		  <input type="text" id="test" class="sensitive" name="planet_aorb" value="$planet_aorb" onchange="idSystem();">
		  AU
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Larger than stellar radius.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Orbital period:</td>
		<td class="field">
		  <input type="text" id="test" class="sensistive" name="planet_Porb" value="$planet_Porb" onchange="idSystem();">
		  days
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Leave blank for calculation
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Orbital eccentricity:</td>
		<td class="field">
		  <input type="text" id="test" class="sensitive" name="planet_eorb" value="$planet_eorb" onchange="idSystem();">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  0&lt;e&lt;1
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Argument of periapsis:</td>
		<td class="field">
		  <input type="text" id="test" class="sensitive" name="planet_worb" value="$planet_worb" onchange="idSystem();">
		  degrees
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  0<&omega;<360<sup>o</sup>
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Rotational Period:</td>
		<td class="field">
		  <input type="text" id="test" class="sensitive" name="planet_Prot" value="$planet_Prot" onchange="idSystem();">
		  days
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Not larger than orbital period
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="button" colspan=2>
		  <button class="update" id="planet_Update">Update</button> 
		  $ajaxform_planet_Update
		  $force_update
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	    </table>
	</div>
	<div id="planet_results_panel" class="results">
	  <div><center class="title">Results</center><hr width="90%"/></div>
	  <div class="download" id="planet_download"></div>
	  <div id="planet_results_status_loader" style="background-color:white;">
	    <div id="planet_results_status" style="background-color:white;">
	      <iframe class="iframe" id="planet_results_frame" src="web/blank.html" 
		      scrolling="yes" onload="adjustiFrame(this);">
	      </iframe>
	    </div>
	  </div>
	</div>
      </div>
    </div>
   </form>
  </div>

  <!-- //////////////////////////////////////////////////////////// -->
  <!-- BINARY -->
  <!-- //////////////////////////////////////////////////////////// -->
  <div class="tabbertab" id="binary" title="Binary">
  <form id="binary_form" action="BHMrun.php">
    <div class="tabcontent">
      <div class="wrapper">
	<div id="binary_form" class="formarea">
	  <div><center class="title">Input Form</center><hr width="90%"/></div>
	    <input type="hidden" name="module" value="binary">
	    <input type="hidden" name="object" value="binary">
	    <table border=0px>
	      <tr>
		<!-- ---------------------------------------- -->
		<td class="name">Binary period:</td>
		<td class="field">
		  <input type="text" name="binary_Pbin" value="$binary_Pbin">
		  days
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Longer than 0.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Binary semimajor axis:</td>
		<td class="field">
		  <input type="text" name="binary_abin" value="$binary_abin">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Larger than 0.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Binary Eccentricity:</td>
		<td class="field">
		  <input type="text" name="binary_ebin" value="$binary_ebin">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  0&lt;e&gt;1
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="button" colspan=2>
		  <button class="update" id="binary_Update">Update</button> 
		  $ajaxform_binary_Update
		  $force_update
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	    </table>
	</div>
	<div id="binary_results_panel" class="results">
	  <div><center class="title">Results</center><hr width="90%"/></div>
	  <div class="download" id="binary_download"></div>
	  <div id="binary_results_status_loader" style="background-color:white;">
	    <div id="binary_results_status" style="background-color:white;">
	      <iframe class="iframe" id="binary_results_frame" src="web/blank.html" 
		      scrolling="yes" onload="adjustiFrame(this);">
	      </iframe>
	    </div>
	  </div>
	</div>
      </div>
    </div>
   <input class="sys_input" type="hidden" name="binary_str_sys" value="$binary_str_sys">
   </form>
  </div>

  <!-- //////////////////////////////////////////////////////////// -->
  <!-- HABITABLE ZONE -->
  <!-- //////////////////////////////////////////////////////////// -->
  <div class="tabbertab" id="hz" title="Habitable Zone">
  <form id="hz_form" action="BHMrun.php">
    <div class="tabcontent">
      <div class="wrapper">
	<div id="hz_form" class="formarea">
	  <div><center class="title">Input Form</center><hr width="90%"/></div>
	    <input type="hidden" name="module" value="hz">
	    <input type="hidden" name="object" value="hz">
	    <table border=0px>
	      <tr>
		<!-- ---------------------------------------- -->
		<td class="name">Inner edge (wider HZ):</td>
		<td class="field">
		  <input type="text" name="hz_str_incrit_wd" value="$hz_str_incrit_wd">
		  days
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Available: 'recent venus', 'moist greenhouse',
		  'runaway greenhouse' (sustained lowercase)
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Outer edge (wider HZ):</td>
		<td class="field">
		  <input type="text" name="hz_str_outcrit_wd" value="$hz_str_outcrit_wd">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Available: 'maximum greenhouse', 'early mars' (sustained lowercase)
		</td>
	      </tr>
	      <tr>
		<!-- ---------------------------------------- -->
		<td class="name">Inner edge (conservative HZ):</td>
		<td class="field">
		  <input type="text" name="hz_str_incrit_nr" value="$hz_str_incrit_nr">
		  days
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Available: 'recent venus', 'moist greenhouse',
		  'runaway greenhouse' (sustained lowercase)
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Outer edge (conservative HZ):</td>
		<td class="field">
		  <input type="text" name="hz_str_outcrit_nr" value="$hz_str_outcrit_nr">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Available: 'maximum greenhouse', 'early mars' (sustained lowercase)
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="button" colspan=2>
		  <button class="update" id="hz_Update">Update</button> 
		  $ajaxform_hz_Update
		  $force_update
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	    </table>
	</div>
	<div id="hz_results_panel" class="results">
	  <div><center class="title">Results</center><hr width="90%"/></div>
	  <div class="download" id="hz_download"></div>
	  <div id="hz_results_status_loader" style="background-color:white;">
	    <div id="hz_results_status" style="background-color:white;">
	      <iframe class="iframe" id="hz_results_frame" src="web/blank.html" 
		      scrolling="yes" onload="adjustiFrame(this);">
	      </iframe>
	    </div>
	  </div>
	</div>
      </div>
    </div>
   <input class="sys_input" type="hidden" name="hz_str_sys" value="$hz_str_sys">
   </form>
  </div>

  <!-- //////////////////////////////////////////////////////////// -->
  <!-- EVOLUTION OF ROTATION -->
  <!-- //////////////////////////////////////////////////////////// -->
  <div class="tabbertab" id="rotation" title="Rotation and Activity">
  <form id="rotation_form" action="BHMrun.php">
    <div class="tabcontent">
      <div class="wrapper">
	<div id="rotation_form" class="formarea">
	  <div><center class="title">Input Form</center><hr width="90%"/></div>
	    <input type="hidden" name="module" value="rotation">
	    <input type="hidden" name="object" value="rotation">
	    <table border=0px>
	      <tr>
		<!-- ---------------------------------------- -->
		<td class="name">k:</td>
		<td class="field">
		  <input type="text" name="rotation_k" value="$rotation_k">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Exponent.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="button" colspan=2>
		  <button class="update" id="rotation_Update">Update</button> 
		  $ajaxform_rotation_Update
		  $force_update
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	    </table>
	</div>
	<div id="rotation_results_panel" class="results">
	  <div><center class="title">Results</center><hr width="90%"/></div>
	  <div class="download" id="rotation_download"></div>
	  <div id="rotation_results_status_loader" style="background-color:white;">
	    <div id="rotation_results_status" style="background-color:white;">
	      <iframe class="iframe" id="rotation_results_frame" src="web/blank.html" 
		      scrolling="yes" onload="adjustiFrame(this);">
	      </iframe>
	    </div>
	  </div>
	</div>
      </div>
    </div>
   <input class="sys_input" type="hidden" name="rotation_str_sys" value="$rotation_str_sys">
   </form>
  </div>

  <!-- //////////////////////////////////////////////////////////// -->
  <!-- BINARY-PLANET INTERACTION -->
  <!-- //////////////////////////////////////////////////////////// -->
  <div class="tabbertab" id="summary" title="Binary-Planet Interaction">
  <form id="interaction_form" action="BHMrun.php">
    <div class="tabcontent">
      <div class="wrapper">
	<div id="interaction_form" class="formarea">
	  <div><center class="title">Input Form</center><hr width="90%"/></div>
	    <input type="hidden" name="module" value="interaction">
	    <input type="hidden" name="object" value="interaction">
	    <table border=0px>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Initial time:</td>
		<td class="field">
		  <input type="text" name="interaction_tauini" value="$interaction_tauini">
		  Gyr
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Initial time for integration.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Reference time</td>
		<td class="field">
		  <input type="text" name="interaction_tauref" value="$interaction_tauref">
		  Gyr
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Reference time.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Early-wind assumption:</td>
		<td class="field">
		  <input type="text" name="interaction_str_earlywind" value="$interaction_str_earlywind">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Available: 'trend', 'constant'
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Magnetosphere Reference Object:</td>
		<td class="field">
		  <input type="text" name="interaction_str_refobj" value="$interaction_str_refobj">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Available: 'Earth', 'Saturn'
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Standoff distance, M-exponent:</td>
		<td class="field">
		  <input type="text" name="interaction_nM" value="$interaction_nM">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  For most magnetospheres n<sub>M</sub>=3.0.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Standoff distance, P-exponent:</td>
		<td class="field">
		  <input type="text" name="interaction_nP" value="$interaction_nP">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  For stiff magnetospheres (Earth-like to
		  Neptune-like) n<sub>P</sub>=6.0, for responsive
		  magnetospheres (gas giants) n<sub>P</sub>=4.5.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Entrapment factor</td>
		<td class="field">
		  <input type="text" name="interaction_alpha" value="$interaction_alpha">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  For Venus &alpha;=0.3 fits well early mass-loss.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Atmospheric mean molecular weight</td>
		<td class="field">
		  <input type="text" name="interaction_muatm" value="$interaction_muatm">
		  g/mol
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Earth's atmosphere, &mu;<sub>atm</sub>=44 g/mol
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Minimum planetary mass for Mass-loss scaling</td>
		<td class="field">
		  <input type="text" name="interaction_Mmin" value="$interaction_Mmin">
		  M<sub>Earth</sub>
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Earth's atmosphere, &mu;<sub>atm</sub>=44 g/mol
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Maximum planetary mass for Mass-loss scaling</td>
		<td class="field">
		  <input type="text" name="interaction_Mmax" value="$interaction_Mmax">
		  M<sub>Earth</sub>
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Earth atmosphere, &mu;<sub>atm</sub>=44 g/mol
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="button" colspan=2>
		  <button class="update" id="interaction_Update">Update</button> 
		  $ajaxform_interaction_Update
		  $force_update
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	    </table>
	</div>
	<div id="interaction_results_panel" class="results">
	  <div><center class="title">Results</center><hr width="90%"/></div>
	  <div class="download" id="interaction_download"></div>
	  <div id="interaction_results_status_loader" style="background-color:white;">
	    <div id="interaction_results_status" style="background-color:white;">
	      <iframe class="iframe" id="interaction_results_frame" src="web/blank.html" 
		      scrolling="yes" onload="adjustiFrame(this);">
	      </iframe>
	    </div>
	  </div>
	</div>
      </div>
    </div>
    <input class="sys_input" type="hidden" name="interaction_str_sys" value="$interaction_str_sys">
   </form>
   <input class="sys_input" type="hidden" name="interaction_str_sys" value="$interaction_str_sys">
  </div>

  <!-- //////////////////////////////////////////////////////////// -->
  <!-- SUMMARY -->
  <!-- //////////////////////////////////////////////////////////// -->
  <div class="tabbertab" id="summary" title="Summary">
    <form id="summary_form" action="BHMsummary.php">
    <div class="tabcontent">
      <div class="wrapper">
	<div id="summary_form" class="formarea">
	  <div><center class="title">Additional Information</center><hr width="90%"/></div>
	  <button class="update" id="summary_Update">Update</button> 
	  $ajaxform_summary_Update
	  <ul>
	    <li>
	      <a class="activelink" 
		 href="JavaScript:loadAjax('BHMutil.php?ACTION=DownloadConfig','#download_config');">
		Download configuration files.
	      </a>
	      <div class="target" id="download_config"></div>
	    </li>
	    <li>
	      <a class="activelink" 
		 href="JavaScript:loadAjax('BHMutil.php?ACTION=DownloadAll','#download_allfiles');">
		Download all files.
	      </a>
	      <div class="target" id="download_allfiles"></div>
	    </li>
	    <li>
	      <a class="activelink" 
		 href="JavaScript:loadAjax('BHMutil.php?ACTION=MasterLink','#systemlink');">
		Generate system link.</a>
	      <!--<a class="activelink" 
		 href="JavaScript:alert('hola');">
		Generate system link.</a>-->
	      <div class="target" id="systemlink"></div>
	    </li>
	    <li>
	      <a class="activelink" 
		 href="JavaScript:loadAjax('/$wDIR/BHMutil.php?ACTION=CommandLine','#commandline');">
		Generate command line.</a>
	      <div class="target" id="commandline"></div>
	    </li>
	  </ul>
	</div>
	<div id="summary_results_panel" class="results">
	  <div><center class="title">Summary of Results</center><hr width="90%"/></div>
	  <div class="download" id="summary_download"></div>
	  <div id="summary_results_status_loader" style="background-color:white;">
	    <div id="summary_results_status" style="background-color:white;">
	      <iframe id="summary_results_frame" src="web/blank.html" 
		      scrolling="yes" onload="adjustiFrame(this);">
	      </iframe>
	    </div>
	  </div>
	</div>
      </div>
    </div>
    </form>
  </div>

</div>
<center>
  <i style="font-size:10px">Session ID: $SESSID. $qdir |  
  <a href=tmp/BHMrun-stdout-$SESSID target=_blank>stdout</a> | <a href=tmp/BHMrun-stderr-$SESSID target=_blank>stderr</a>
  </i>

</center>
C;

//////////////////////////////////////////////////////////////////////////////////
//CONTENT DISPLAY
//////////////////////////////////////////////////////////////////////////////////
$CONTENT.="</body></html>";
echo $CONTENT;
?>
