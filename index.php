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
//////////////////////////////////////////////////////////////////////////////////
//HEADER
//////////////////////////////////////////////////////////////////////////////////
$header=mainHeader();
$CONTENT.="<html>$header<body>";
if($VERBOSE){
$CONTENT.=<<<C
Sessid:$SESSID<br/>
GET: $GETSTR<br/>
POST: $POSTSTR<br/>
C;
}

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//HEADER AND FRONTMATTER
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
$CONTENT.=<<<C
<h1>
<a style='font-size:32' href="?">Binary Habitability Calculator</a><sup> <b style='color:red'>2.0</b></sup>
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

//LOAD ALL
$code=ajaxMultipleForm(array("star1","star2","planet"),"allforms");
$ajax_all_Update=ajaxFromCode($code,"'#all_Update'","click");
$ajax_all_Load=ajaxFromCode($code,"document","ready");

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
  $TABID=3;
  //========================================
  //LOADING RESULTS
  //========================================
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
  <div class="tabbertab" id="Introduction" title="Introduction">
    <div class="tabcontent">
    </div>
  </div>

  <!-- //////////////////////////////////////////////////////////// -->
  <!-- STAR 1
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
		  <input type="text" class="star_Z" name="star1_Z" value="$star1_Z" onchange="changeAjax('/BHMcalc/BHMmetals.php?ZtoFeH',this,'.star_FeH');changeValues(['.star_Z'],this);">
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
		  <input type="text" class="star_FeH" name="star1_FeH" value="$star1_FeH" onchange="changeAjax('/BHMcalc/BHMmetals.php?FeHtoZ',this,'.star_Z');changeValues(['.star_FeH'],this);">
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
		  <button id="star1_Update">Update</button> 
		  $ajaxform_star1_Update
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	    </table>
	</div>
	<div id="star1_results_panel" class="results">
	  <div><center class="title">Results</center><hr width="90%"/></div>
	  <div id="star1_results_status_loader" style="background-color:white;">
	    <div id="star1_results_status" style="background-color:white;">
	      <iframe id="star1_results_frame" src="web/blank.html" 
		      scrolling="no" onload="adjustiFrame(this);">
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
		  <input type="text" class="star_Z" name="star2_Z" value="$star2_Z" onchange="changeAjax('/BHMcalc/BHMmetals.php?ZtoFeH',this,'.star_FeH');changeValues(['.star_Z'],this);">
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
		  <input type="text" class="star_FeH" name="star2_FeH" value="$star2_FeH" onchange="changeAjax('/BHMcalc/BHMmetals.php?FeHtoZ',this,'.star_Z');changeValues(['.star_FeH'],this);">
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
		  <button id="star2_Update">Update</button> 
		  $ajaxform_star2_Update
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	    </table>
	</div>
	<div id="star2_results_panel" class="results">
	  <div><center class="title">Results</center><hr width="90%"/></div>
	  <div id="star2_results_status_loader" style="background-color:white;">
	    <div id="star2_results_status" style="background-color:white;">
	      <iframe id="star2_results_frame" src="web/blank.html" 
		      scrolling="no" onload="adjustiFrame(this);">
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
	  <div id="planet_results_status_loader" style="background-color:white;">
	    <div id="planet_results_status" style="background-color:white;">
	      <iframe id="planet_results_frame" src="web/blank.html" 
		      scrolling="no" onload="adjustiFrame(this);">
	      </iframe>
	    </div>
	  </div>
	</div>
      </div>
    </div>
   </form>
  </div>

  <div class="tabbertab" id="plBas" title="Binary">
    <div class="tabcontent">
      Casa
    </div>
  </div>
  <div class="tabbertab" id="iHZ" title="Habitable Zone">
    <div class="tabcontent">
      Casa
    </div>
  </div>
  <div class="tabbertab" id="rotEvo" title="Rotational Evolution">
    <div class="tabcontent">
      Casa
    </div>
  </div>
  <div class="tabbertab" id="envEvo" title="Stars-Planet Interaction">
    <div class="tabcontent">
      Casa
    </div>
  </div>
</div>
C;

//////////////////////////////////////////////////////////////////////////////////
//CONTENT DISPLAY
//////////////////////////////////////////////////////////////////////////////////
$CONTENT.="</body></html>";
echo $CONTENT;
?>
