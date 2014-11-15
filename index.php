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
  $header=mainHeader("1");
  echo "$header<body>Loading configuration...</body>";
  return;
}
if(isset($ADMINMODE)){
  //========================================
  //ENTERING ADMIN MODE
  //========================================
  saveConfiguration($SESSDIR,$QUERY_STRING);
  $header=mainHeader("1");
  echo "$header<body>Loading configuration...</body>";
  return;
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
$code=ajaxMultipleForm(array("interaction","rotation","hz","binary","star1","star2","planet"),"allforms");
$ajax_all_Update=ajaxFromCode($code,"'#all_Update'","click");
$ajax_all_Load=ajaxFromCode($code,"document","ready");

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//CHANGE OTHER THINGS IN DOCUMENT WHEN LOAD
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
$changeFeH=<<<C
  changeAjax('/BHMcalc/BHMmetals.php?ZtoFeH','.star_Z','.star_FeH');
C;
$changeZ=<<<C
  changeAjax('/BHMcalc/BHMmetals.php?FeHtoZ','.star_FeH','.star_Z');
C;
$CONTENT.=<<<C
<script>
  $(document).ready(function(){
      $changeFeH
      changeValues(['.star_Z'],'input[name=star1_Z]');
      changeValues(['.star_FeH'],'input[name=star1_FeH]');
    });
</script>
C;

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//LOAD DATA
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if(!is_dir($SESSDIR)){
  $source_dir=$SYSDIR."template/";
  echoVerbose("No session directory.");
  $TABID=0;
}else{
  $source_dir=$SYSDIR."$SESSID/";
  echoVerbose("Session directory already exist.");
  if(!isset($TABID)){$TABID=2;}
}

//========================================
//LOADING RESULTS
//========================================
//$CONTENT.="$ajax_all_Load";
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
    <div class="tabcontent">
    </div>
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
		  <input type="text" name="star1_M" value="$star1_M">
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
		  <input type="text" class="star_Z" name="star1_Z" value="$star1_Z" 
			 onchange="$changeFeH;changeValues(['.star_Z'],this);">
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
		  <input type="text" class="star_FeH" name="star1_FeH" value="$star1_FeH" 
			 onchange="$changeZ;changeValues(['.star_FeH'],this);">
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
		  <input id="ini" type="text" class="star_tau" name="star1_tau" value="$star1_tau" onchange="changeValues(['.star_tau'],this)">
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
		  <input type="text" id="test" name="star1_taums" value="$star1_taums">
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
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	    </table>
	</div>
	<div id="star1_results_panel" class="results">
	  <div><center class="title">Results</center><hr width="90%"/></div>
	  <div class="download" id="star1_download">Hola</div>
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
		  <input type="text" name="star2_M" value="$star2_M">
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
		  <input type="text" class="star_Z" name="star2_Z" value="$star2_Z" 
			 onchange="$changeFeH;changeValues(['.star_Z'],this);">
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
		  <input type="text" class="star_FeH" name="star2_FeH" value="$star2_FeH" 
			 onchange="$changeZ;changeValues(['.star_FeH'],this);">
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
		  <input id="ini" type="text" class='star_tau' name="star2_tau" value="$star2_tau" onchange="changeValues(['.star_tau'],this)">
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
		  <input type="text" id="test" name="star2_taums" value="$star2_taums">
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
		  <input type="text" name="planet_M" value="$planet_M">
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
		  <input type="text" name="planet_fHHe" value="$planet_fHHe">
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
		  <input type="text" name="planet_CMF" value="$planet_CMF">
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
		  <input type="text" class="star_tau" name="planet_tau" value="$planet_tau" onchange="changeValues(['.star_tau'],this)">
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
		  <input type="text" id="test" name="planet_Morb" value="$planet_Morb">
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
		  <input type="text" id="test" name="planet_aorb" value="$planet_aorb">
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
		  <input type="text" id="test" name="planet_Porb" value="$planet_Porb">
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
		  <input type="text" id="test" name="planet_eorb" value="$planet_eorb">
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
		  <input type="text" id="test" name="planet_worb" value="$planet_worb">
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
		  <input type="text" id="test" name="planet_Prot" value="$planet_Prot">
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
   </form>
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
	      <a class="activelink" href="">Download configuration files.</a>
	      <div class="target" id="downlad_config"></div>
	    </li>
	    <li>
	      <a class="activelink" href="">Download all files.</a>
	      <div class="target" id="downlad_allfiles"></div>
	    </li>
	    <li>
	      <a class="activelink" 
		 href="JavaScript:loadAjax('/$wDIR/BHMutil.php?ACTION=MasterLink','#download_systemlink');">
		Generate system link.</a>
	      <div class="target" id="download_systemlink"></div>
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
C;

//////////////////////////////////////////////////////////////////////////////////
//CONTENT DISPLAY
//////////////////////////////////////////////////////////////////////////////////
$CONTENT.="</body></html>";
echo $CONTENT;
?>
